from typing import List, Dict, Any
# Import typing hints to specify the expected types of variables and function parameters/returns
# List: A list of items of a specific type
# Dict: A dictionary with keys and values of specific types
# Any: Can be any type

import requests
# Import the requests package for making HTTP requests to the Deepseek API

import asyncio
# Import asyncio for asynchronous programming, allowing non-blocking operations

from base_agent import BaseAgent
# Import the BaseAgent abstract base class that defines the common interface for all agents

class DeepseekAgent(BaseAgent):
    """Agent for generating answers using Deepseek models."""
    # This class implements the BaseAgent interface for Deepseek models
    # It handles the specifics of communicating with the Deepseek API
    
    def __init__(self, api_key: str, model_name: str = "deepseek-chat"):
        """Initialize Deepseek agent with an API key and model name.
        
        Args:
            api_key (str): Deepseek API key
            model_name (str, optional): Model to use. Defaults to "deepseek-chat".
        """
        # Constructor method that runs when a new DeepseekAgent is created
        # Takes an API key and an optional model name
        
        super().__init__(api_key)
        # Call the parent class (BaseAgent) constructor with the API key
        # This will store the API key and validate it
        
        self.model_name = model_name
        # Store the model name as an instance variable
        
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        # Store the API endpoint URL as an instance variable
        # This is the URL that we'll send requests to

    async def generate_answer(self, query: str, results: List[Dict[str, Any]]) -> str:
        """Generate a comprehensive answer from retrieved results using Deepseek.
        
        Args:
            query (str): The user's question
            results (List[Dict[str, Any]]): Retrieved results from Pinecone
            
        Returns:
            str: The generated answer
        """
        # Implementation of the abstract method from BaseAgent
        # This method generates an answer to the user's question based on the retrieved results
        # It's marked as async, which means it's an asynchronous method that can be awaited
        
        context = self.format_context(results)
        # Format the retrieved results into a context string using the method from BaseAgent
        
        try:
            # Try to generate an answer using the Deepseek API
            
            headers = {
                "Content-Type": "application/json",
                # Specify that we're sending JSON data
                "Authorization": f"Bearer {self.api_key}"
                # Include the API key in the Authorization header using Bearer token authentication
            }
            
            data = {
                "model": self.model_name,
                # Specify which model to use (e.g., "deepseek-chat")
                "messages": [
                    # Provide a list of messages that define the conversation
                    {"role": "system", "content": "You are a helpful assistant that provides comprehensive answers based on the retrieved information. Cite your sources when appropriate."},
                    # The system message sets the behavior of the assistant
                    # This content tells the model to act as a helpful assistant and cite sources
                    {"role": "user", "content": f"Based on the following information, please provide a comprehensive answer to this question: '{query}'\n\nRetrieved Information:\n{context}"}
                    # The user message contains the user's question and the context
                    # This content includes the user's question and the formatted context
                ],
                "max_tokens": 1000
                # Set the maximum number of tokens (words/parts of words) in the response
            }
            
            # Since requests doesn't have async methods, we'll use it in a thread pool
            # This is a way to run a synchronous function asynchronously without blocking the event loop
            loop = asyncio.get_event_loop()
            # Get the current event loop
            
            response = await loop.run_in_executor(
                # Run the synchronous requests.post function in a thread pool
                None,  # Use the default executor (ThreadPoolExecutor)
                lambda: requests.post(self.api_url, headers=headers, json=data)
                # This lambda function makes a POST request to the Deepseek API
                # It sends the headers and data as JSON
            )
            # The response contains the HTTP response from the API
            
            response_json = response.json()
            # Parse the JSON response into a Python dictionary
            
            if "choices" in response_json and len(response_json["choices"]) > 0:
                # Check if the response contains choices and at least one choice
                return response_json["choices"][0]["message"]["content"]
                # Extract the content of the first choice's message and return it
                # This is the actual answer generated by the model
            else:
                # If the response doesn't contain choices or is empty
                print(f"Unexpected response format from Deepseek: {response_json}")
                # Print the unexpected response format for debugging
                
                return "I couldn't generate an answer based on the retrieved information."
                # Return a fallback message to the user
                
        except Exception as e:
            # If there's an error during the API call or processing
            print(f"Error generating answer with Deepseek: {e}")
            # Print the error message for debugging
            
            return "I couldn't generate an answer based on the retrieved information."
            # Return a fallback message to the user 