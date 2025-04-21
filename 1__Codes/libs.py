"""This is a library module for graph RAG which will contain helper
functions for the graph RAG module."""

from sentence_transformers import SentenceTransformer  # type: ignore
from openai import OpenAI  # type: ignore
import os
import ast
import pandas as pd  # type: ignore
from typing import List, Tuple, Dict, Optional
import logging


def embed_entity(entity):
    """
    This function utilizes sentence transformers (default for Neo4j builder)
    to embed a string and return a list of floats

    Args:
        entity: str, entity to embed

    Returns:
        embeddings: list, list of floats
    """
    embeddings = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return embeddings.encode(entity).tolist()


def create_vector_index(graph, name):
    """
    This function creates a vector index in our Neo4j graph Database so that
    we can perform a similarity search on the embeddings of the nodes.

    Args:
      graph: Neo4jGraph object
      name: str, name of the index

    Returns:
      None
    """
    # Check if the index exists and retrieve dimensions
    existing_indexes = graph.query(
        f"SHOW INDEXES YIELD name, type, options WHERE name = '{name}' AND type = 'VECTOR'"
    )

    if existing_indexes:
        current_options = existing_indexes[0]["options"]
        indexConfig = current_options.get("indexConfig", None)
        current_dimensions = indexConfig.get("vector.dimensions", None)

        if current_dimensions == 384:
            print(
                f"✅ Index '{name}' already exists with correct dimensions: {current_dimensions}"
            )
            return  # No need to drop and recreate

        print(
            f"Index '{name}' exists but has incorrect dimensions: {current_dimensions}. Recreating..."
        )
        graph.query(f"DROP INDEX `{name}` IF EXISTS")

    graph.query(f"DROP INDEX `{name}` IF EXISTS")
    graph.query(
        f"""
        CREATE VECTOR INDEX `{name}` IF NOT EXISTS  
        FOR (a:__Entity__) ON (a.embedding)
        OPTIONS {{
        indexConfig: {{
            `vector.dimensions`: 384,
            `vector.similarity_function`: 'cosine'
      }}
    }}
    """
    )


def vector_search(graph, query_embedding, index_name="entities", k=50):
    """
    This function performs a similarity search in our Neo4j graph database

    Args:
      graph: Neo4jGraph object
      query_embedding: list, embedding of the query
      index_name: str, name of the index
      k: int, number of results to return

    Returns:
      result: list, list of tuples containing the node id and the similarity score
    """
    similarity_query = f"""
    MATCH (n:__Entity__)
    CALL db.index.vector.queryNodes('{index_name}', {k}, {query_embedding})
    YIELD node, score
    RETURN DISTINCT node.id, score
    ORDER BY score DESC
    LIMIT {k}

    """
    result = graph.query(similarity_query)
    return result


def chunk_finder(graph, query):

    # get the id of the query associated node
    query_embedding = embed_entity(query)
    response = vector_search(graph, query_embedding)
    id = response[0]["node.id"]

    chunk_find_query = f"""
    MATCH (n:Chunk)-[r]->(m:`__Entity__` {{id: "{id}"}}) RETURN n.text,n.fileName LIMIT 80
    """
    result = graph.query(chunk_find_query)
    output = []
    for record in result:
        output.append((record["n.fileName"], record["n.text"]))
    return output, response


def get_entities(prompt: str, correction_context: str = " ") -> Tuple[List[str], str]:
    """
    Extract medical entities from text using OpenAI's models.
    API key is loaded from .env file.

    Args:
        prompt: Input text to extract entities from
        correction_context: Additional context for correction if needed

    Returns:
        Tuple containing list of extracted entities and correction context
    """
    # Check if API key is loaded
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env file")

    client = OpenAI(api_key=api_key)

    system_prompt = """
    You are a highly capable natural language processing assistant with extensive medical knowledge. 
    Your task is to extract medical entities from a given prompt. 
    Entities are specific names, places, dates, times, objects, organizations, or other identifiable items explicitly mentioned in the text.
    Please output the entities as a list of strings in the format ["string 1", "string 2"]. Do not include duplicates. 
    Do not include any other text. Always include at least one entity.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": correction_context},
                {
                    "role": "user",
                    "content": f"Here is the input prompt:\n{prompt}\n\nExtracted entities:",
                },
            ],
            temperature=0.1,
        )

        output = response.choices[0].message.content.strip()

        try:
            entities = ast.literal_eval(output)
            if not isinstance(entities, list):
                correction_string = f"The previous output threw this error: Expected a list of strings, but got {type(entities)} with value {entities}"
                return get_entities(prompt, correction_context=correction_string)

            if not all(isinstance(item, str) for item in entities):
                correction_string = (
                    f"The previous output contained non-string elements: {entities}"
                )
                return get_entities(prompt, correction_context=correction_string)

            return entities, correction_context

        except (ValueError, SyntaxError) as e:
            print(f"Error parsing response: {e}")
            print(f"Raw response was: {output}")
            return get_entities(
                prompt, correction_context=f"Previous response was invalid: {e}"
            )

    except Exception as e:
        print(f"API Error: {e}")
        return ["error occurred"], correction_context


def graph_retriever(graph, query):
    entities, _ = get_entities(query)
    ids = []
    for entity in entities:
        embedding = embed_entity(entity)
        closest_node = vector_search(
            graph, embedding, k=1
        )  # considering only the closest node
        id = closest_node[0]["node.id"]
        ids.append(id)
    context = ""
    for id in ids:
        neighbors_query = f"""
        MATCH path = (n:`__Entity__` {{id:"{id}"}})-[r*..2]-(m:`__Entity__`)
        WHERE ALL(rel IN relationships(path) WHERE NOT type(rel) IN ['HAS_ENTITY', 'MENTIONS'])
        RETURN 
        n.id AS startNode,
        [rel IN relationships(path) | 
            {{
            type: type(rel),
            direction: CASE 
                WHEN startNode(rel) = n THEN "outgoing" 
                WHEN endNode(rel) = n THEN "incoming" 
                ELSE "undirected"
            END
            }}] AS relationshipDetails,
        [node IN nodes(path) | node.id] AS pathNodes
        """
        result = graph.query(neighbors_query)
        for record in result:
            rel = record["relationshipDetails"]
            pathNodes = record["pathNodes"]
            formatted_path = ""
            for i in range(len(rel)):
                if rel[i]["direction"] == "outgoing":
                    formatted_path += (
                        f" {pathNodes[i]} {rel[i]['type']} {pathNodes[i+1]},"
                    )
                elif rel[i]["direction"] == "incoming":
                    formatted_path += (
                        f" {pathNodes[i+1]} {rel[i]['type']} {pathNodes[i]},"
                    )
                else:
                    formatted_path += (
                        f" {pathNodes[i]} {rel[i]['type']} {pathNodes[i+1]},"
                    )
            context += formatted_path + "\n"

    return context


def context_builder(graph, query, method="hybrid"):
    """
    This function performs vector search, graph search, or both to build a context string for
    an LLM

    Args:
    graph: Neo4jGraph object
    query: string

    Returns:
    context: string
    """
    context = ""
    if method == "vector":
        output = chunk_finder(graph, query)
        # context = "Given the following context in the format [(File Name, Text),...] \n"
        context += str(output)

    elif method == "graph":
        context = graph_retriever(graph, query)
    elif method == "hybrid":

        context = (
            graph_retriever(graph, query)
            + "\n And Given the following context in the format [(File Name, Text),...] \n"
            + str(chunk_finder(graph, query))
        )
    else:
        pass  # no context
    return context


def generate_response(graph, query, method="hybrid", model="gpt-4o-mini"):
    """
    This function will utilizze ollama to generate a response while providing context

    Args:
    graph: Neo4jGraph object
    query: string
    method: string, "vector", "graph", or "hybrid"
    model: string, model name

    Returns:
    response: string, generated response
    prompt: string, generated prompt (with context)

    """
    context = context_builder(graph, query, method)

    prompt = f""" 
    You are an intelligent document retrieval assistant. Your task is to retrieve relevant document names from a structured knowledge base based on the given User Query and Context.

    ### Instructions:
    - Search the knowledge base and return **only the names of the most relevant documents**.
    - The output must be in one of the following structured formats:
    - **Format**: "ARDS", "ACURASYS"
    - **Do not provide any explanations or additional text.** Output only the document names.
    - If no document is relevant, return an **empty list**: `[]`.
    
    User Query: {query}
    Context: {context}
    """

    # response = ollama.generate(model="llama3.1:latest", prompt=prompt)
    # Initialize the client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Assuming 'prompt' is defined elsewhere in your code
    # If not, you'll need to define it
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},  # Make sure 'prompt' is defined
                {"role": "user", "content": query},
            ],
        )
        return response, context  # Make sure 'context' is defined

    except Exception as e:
        print(f"Error during API call: {e}")
        return None, None

    # def run_trial(graph, question_list, num_trials=1):
    """
    This function will run a trial of questions and return the results

    Args:
    graph: Neo4jGraph object
    question_list: list, list of questions

    Returns:
    results: a dataframe where each row is a question and each column is a model mode combination.
    The value will be a list of response strings.
    """
    models = ["llama3.1:latest", "granite3-dense:2b"]
    methods = ["None", "vector", "graph", "hybrid"]

    # we will iterate for each model and method we will generate num_trial answers to each
    # question and store the resulting list of strings in a dataframe

    data = {f"{model}-{method}": [] for model in models for method in methods}

    # Iterate through questions
    for question in question_list:
        for model in models:
            for method in methods:
                responses = []
                for _ in range(num_trials):
                    # Generate a response for the current model, method, and question
                    response, _ = generate_response(
                        graph, question, method=method, model=model
                    )
                    responses.append(response.response)
                # Add the responses to the correct column
                data[f"{model}-{method}"].append(responses)

    # Create a DataFrame where rows are questions
    results = pd.DataFrame(
        data, index=[f"Question {i+1}" for i in range(len(question_list))]
    )
    return results

    # def create_md(csv_path, output_path, questions):
    """
    This function will convert a trial csv into md for evaluation

    Args:
    csv_path: string, path to the csv file
    output_path: string, path to the output file
    qusetions: list, list of questions

    Returns:
    None
    """
    # Load the CSV file
    df = pd.read_csv(csv_path)

    # Initialize a list to store the markdown content
    markdown_content = []

    # Iterate through each question
    for i in range(len(df)):
        question_number = f"Question {i + 1}"
        markdown_content.append(f"## {question_number} {questions[i]}\n")

        # Iterate through each column (model-method pair)
        for column in df.columns:
            response = df.iloc[i][column]
            markdown_content.append(f"**{column}**:\n\n{response}\n\n")

    # Write the markdown content to a file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(markdown_content))


############################################################################################################
# NEW CHUNCK FINDER FUNCTIONS
############################################################################################################


def enhanced_chunk_finder(
    graph,
    query: str,
    limit: int = 20,
    similarity_threshold: float = 0.8,
    max_hops: int = 1,
) -> List[Tuple[str, str, int, int, float]]:
    try:
        # Get query embedding and perform vector search
        query_embedding = embed_entity(query)
        vector_results = vector_search(graph, query_embedding)

        if not vector_results:
            logging.warning("No vector search results found for query")
            return [], []

        # Create a dictionary to store entity IDs and their similarity scores
        similarity_scores = dict(
            sorted(
                {
                    result["node.id"]: result["score"]
                    for result in vector_results
                    if result.get("score", 0) >= similarity_threshold
                }.items(),
                key=lambda x: x[1],
                reverse=True,
            )
        )

        if not similarity_scores:
            logging.info("No results met the similarity threshold")
            return [], []

        # Construct graph query to find connected chunks
        # ids_clause = ", ".join([f'"{id}"' for id in similarity_scores.keys()])

        # Create parameters dictionary for the query
        params = {
            "similarity_scores": similarity_scores,
            "ids": list(similarity_scores.keys()),
            "limit": limit,
        }

        # Use f-string for max_hops since it can't be parameterized in relationship patterns
        chunk_find_query = f"""
        MATCH path = (n:Chunk)-[*1..{max_hops}]->(m:`__Entity__`)
        WHERE m.id IN $ids
        WITH n, path, m
        WITH n, min(length(path)) as distance, m
        WITH n, distance, m.id as entity_id
        WITH n, distance, entity_id, 
             CASE 
                WHEN entity_id IN $ids 
                THEN $similarity_scores[entity_id]
             END as similarity
        ORDER BY similarity DESC, distance
        RETURN n.text, n.fileName, n.page_number, n.position, entity_id, similarity
        LIMIT $limit
        """

        # Execute graph query with parameters
        result = graph.query(chunk_find_query, params=params)

        output = []
        seen_chunks = set()
        filenames = set()

        for record in result:
            chunk_text = record["n.text"]
            filenames.add(record["n.fileName"])
            if chunk_text not in seen_chunks:
                output.append(
                    (
                        record["n.fileName"],
                        chunk_text,
                        record["n.page_number"],
                        record["n.position"],
                        record["similarity"],
                    )
                )
                seen_chunks.add(chunk_text)

        return list(filenames), output

    except Exception as e:
        logging.error(f"Error in enhanced_chunk_finder: {str(e)}")
        raise
