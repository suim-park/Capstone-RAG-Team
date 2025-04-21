from openai import OpenAI
import os
from dotenv import load_dotenv
import ast
from typing import Tuple, List, Optional

# Load environment variables from .env file
load_dotenv()


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
            model="gpt-4",
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


# Example usage
if __name__ == "__main__":
    # Make sure you have a .env file in your working directory with:
    # OPENAI_API_KEY=your-api-key-here

    test_prompt = "The patient was prescribed Metformin 500mg for type 2 diabetes by Dr. Smith at Mayo Clinic on January 15, 2024."
    try:
        entities, context = get_entities(test_prompt)
        print("Extracted entities:", entities)
    except ValueError as e:
        print(f"Error: {e}")
