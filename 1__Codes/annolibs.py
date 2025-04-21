## This library module is mainly for teammates to use
## It contain functions that help to retrieve top 5 chunks from the given paper from each question
import os
import pandas as pd  # type: ignore
from typing import List, Dict
import numpy as np  # type: ignore
import ast
from libs import embed_entity


# Function to get all chunks per paper
def get_all_chunks_per_paper(
    graph,
    paperNames: List[str],  # Changed parameter name for clarity
) -> Dict[str, pd.DataFrame]:
    """
    Get all chunks for each paper and save them as separate CSV files.

    Args:
        graph: Neo4j graph connection
        paperNames: List of paper names without .pdf extension

    Returns:
        Dictionary of DataFrames, one for each paper
    """
    paper_dataframes = {}  # Store DataFrames for each paper

    for idx, paper in enumerate(paperNames):
        results = []  # Reset results for each paper

        query = """
            MATCH (c:Chunk)
            WHERE c.fileName = $paperName + ".pdf"
            ORDER BY c.position 
            RETURN c.fileName AS paper_name, 
                   c.position AS position,
                   c.text AS chunk_text, 
                   c.embedding AS chunk_embedding
        """

        params = {"paperName": paper}
        result = graph.query(query, params=params)
        print(f"Found {len(result)} chunks in paper {paper}")

        # Process results for this paper
        for record in result:
            results.append(
                {
                    "paper_num": idx + 1,
                    "paper_name": record["paper_name"],
                    "position": record["position"],
                    "chunk_text": record["chunk_text"],
                    "chunk_embedding": record["chunk_embedding"],
                }
            )

        # Create DataFrame for this paper
        df_paper = pd.DataFrame(results)

        # Save to CSV if we have results
        if not df_paper.empty:
            output_dir = "./chunks_of_paper"
            os.makedirs(output_dir, exist_ok=True)
            csv_path = f"{output_dir}/chunks_of_{paper}.csv"
            df_paper.to_csv(csv_path, index=False)
            # print(f"Saved {csv_path}")

        # Store DataFrame in dictionary
        paper_dataframes[paper] = df_paper

    return paper_dataframes


def compare_embeddings(question: str, paper: str, top_k: int = 5) -> pd.DataFrame:
    """
    Compare question embedding with chunk embeddings from CSV files.

    Args:
        question: Question text to compare against
        paper: Paper name without .pdf extension
        top_k: Number of top matches to return

    Returns:
        DataFrame with top matching chunks and similarity scores
    """
    # Create empty DataFrame with expected columns
    empty_df = pd.DataFrame(
        columns=["paper_name", "position", "chunk_text", "similarity_score"]
    )

    # Load chunk embeddings from CSV
    csv_path = f"./chunks_of_paper/chunks_of_{paper}.csv"
    if not os.path.exists(csv_path):
        print(f"No chunk data found for paper: {paper}")
        return empty_df

    try:
        # Load chunks DataFrame
        chunks_df = pd.read_csv(csv_path)

        # Get question embedding
        question_embedding = embed_entity(question)

        # Convert string embeddings back to lists with error handling
        def safe_convert_embedding(emb_str):
            try:
                return ast.literal_eval(emb_str)
            except (ValueError, SyntaxError):
                return None

        chunks_df["chunk_embedding"] = chunks_df["chunk_embedding"].apply(
            safe_convert_embedding
        )

        # Remove invalid embeddings
        chunks_df = chunks_df[chunks_df["chunk_embedding"].notna()]

        if chunks_df.empty:
            print(f"No valid embeddings found in {paper}")
            return empty_df

        # Calculate cosine similarities with error handling
        similarities = []
        for _, row in chunks_df.iterrows():
            try:
                chunk_emb = np.array(row["chunk_embedding"])
                q_emb = np.array(question_embedding)
                similarity = np.dot(chunk_emb, q_emb) / (
                    np.linalg.norm(chunk_emb) * np.linalg.norm(q_emb)
                )
                similarities.append(similarity)
            except:
                similarities.append(0.0)

        # Add similarities to DataFrame
        chunks_df["similarity_score"] = similarities

        # Sort and get top k results
        results = chunks_df.nlargest(top_k, "similarity_score")[
            ["paper_name", "position", "chunk_text", "similarity_score"]
        ].round({"similarity_score": 4})

        # Set display options for full text visibility
        pd.set_option("display.max_colwidth", None)

        return results

    except Exception as e:
        print(f"Error processing paper {paper}: {str(e)}")
        return empty_df
