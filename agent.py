from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def summarize_content(text: str) -> str:
    """
    Summarizes the provided text using the OpenAI language model.

    Args:
        text (str): The text to be summarized.

    Returns:
        str: The summary of the text.
    """
    if not text:
        return "No content available to summarize."
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text concisely."},
                {"role": "user", "content": f"Please summarize the following content in 2-3 sentences:\n{text}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error summarizing content: {e}")
        return "Error generating summary."

def extract_metadata(result: dict) -> dict:
    """
    Extracts relevant metadata from a Pinecone result.

    Args:
        result (dict): A raw result from Pinecone.

    Returns:
        dict: Extracted metadata.
    """
    return {
        "title": result.get("title", "Untitled"),
        "source": result.get("source", "Unknown source"),
        "url": result.get("url", ""),
        "description": result.get("description", ""),
        "blob_type": result.get("blobType", ""),
        "score": result.get("score", 0),
    }

async def process_pinecone_results(results):
    """
    Process raw Pinecone results into a user-friendly format.
    
    Args:
        results (list): A list of raw results from Pinecone.

    Returns:
        list: A structured summary of the results.
    """
    structured_results = []
    for result in results:
        metadata = extract_metadata(result)
        summary = await summarize_content(result.get("text", ""))
        
        structured_result = {
            "title": metadata["title"],
            "summary": summary,
            "source": metadata["source"],
            "url": metadata["url"],
            "description": metadata["description"],
            "blob_type": metadata["blob_type"],
            "score": metadata["score"],
        }
        structured_results.append(structured_result)
    
    return structured_results 