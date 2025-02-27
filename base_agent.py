from abc import ABC, abstractmethod
# Import ABC (Abstract Base Class) and abstractmethod from the abc module
# ABC is used to create abstract classes that can't be instantiated directly
# abstractmethod is a decorator that defines abstract methods that must be implemented by subclasses

from typing import Any, List, Dict
# Import typing hints to specify the expected types of variables and function parameters/returns
# Any: Can be any type
# List: A list of items of a specific type
# Dict: A dictionary with keys and values of specific types

class BaseAgent(ABC):
    """Base class for different LLM agents."""
    # This is an abstract base class that defines the common interface for all AI agents
    # LLM stands for Large Language Model (like GPT-4, Claude, etc.)

    def __init__(self, api_key: str):
        """Initialize the agent with the provided API key."""
        # Constructor method that runs when a new agent is created
        # Takes an API key as a parameter, which is required to authenticate with the AI service
        
        self.api_key = api_key
        # Store the API key as an instance variable so it can be used in other methods
        
        self._validate_api_key()
        # Call the validation method to ensure the API key is not empty

    def _validate_api_key(self):
        """Validate that the API key is not empty."""
        # Private method to validate the API key
        # The underscore prefix indicates this is an internal method not meant to be called directly
        
        if not self.api_key:
            # Check if the API key is empty or None
            raise ValueError("API key is required.")
            # If the API key is empty, raise a ValueError with an error message
            # This will stop the program and show the error message

    def format_context(self, results: List[Dict[str, Any]]) -> str:
        """Format the context string from retrieved results.
        
        Args:
            results (List[Dict[str, Any]]): A list of result dictionaries.

        Returns:
            str: Formatted context string.
        """
        # Method to format the search results into a string that can be used as context for the AI
        # Takes a list of dictionaries containing the search results
        # Returns a formatted string with all the relevant information
        
        context = ""
        # Initialize an empty string to store the formatted context
        
        for i, result in enumerate(results):
            # Loop through each result in the results list
            # enumerate gives us both the index (i) and the value (result)
            
            context += f"Document {i + 1}:\n"
            # Add a header for each document with its number (starting from 1)
            
            if "title" in result:
                # Check if the result has a title field
                context += f"Title: {result.get('title', 'Untitled')}\n"
                # Add the title to the context, or 'Untitled' if the title is None
            
            if "description" in result:
                # Check if the result has a description field
                context += f"Description: {result.get('description', '')}\n"
                # Add the description to the context, or an empty string if the description is None
            
            if "text" in result:
                # Check if the result has a text field
                context += f"Content: {result.get('text', '')}\n"
                # Add the content to the context, or an empty string if the text is None
            
            context += f"Relevance Score: {result.get('score', 0):.4f}\n\n"
            # Add the relevance score to the context, formatted to 4 decimal places
            # If there's no score, use 0 as the default
            # Add two newlines to separate this result from the next one
        
        return context
        # Return the complete formatted context string

    @abstractmethod
    # This decorator marks the method as abstract, meaning it must be implemented by any subclass
    async def generate_answer(self, query: str, results: List[Dict[str, Any]]) -> str:
        """Abstract method for generating an answer.
        
        Each child class must implement this method.
        
        Args:
            query (str): The query for which to generate an answer.
            results (List[Dict[str, Any]]): The results to base the answer on.

        Returns:
            str: The generated answer.
        """
        # This is an abstract method that defines the interface for generating answers
        # It's marked as async, which means it's an asynchronous method that can be awaited
        # Each specific agent class (OpenAI, Claude, etc.) must implement this method
        # The method takes a query string and a list of search results
        # It should return a string containing the generated answer
        
        pass 
        # The pass statement is a placeholder that does nothing
        # In an abstract method, the implementation is provided by the subclasses 