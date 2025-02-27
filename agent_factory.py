from typing import Dict, Optional, Union
# Import typing hints to specify the expected types of variables and function parameters/returns
# Dict: A dictionary with keys and values of specific types
# Optional: Indicates that a value can be of a specific type or None
# Union: Indicates that a value can be one of several types

from base_agent import BaseAgent
# Import the BaseAgent abstract base class that defines the common interface for all agents

from openai_agent import OpenAIAgent
# Import the OpenAIAgent class that implements the BaseAgent interface for OpenAI models

from anthropic_agent import AnthropicAgent
# Import the AnthropicAgent class that implements the BaseAgent interface for Anthropic models

from deepseek_agent import DeepseekAgent
# Import the DeepseekAgent class that implements the BaseAgent interface for Deepseek models

class AgentFactory:
    """Factory class for creating LLM agent instances."""
    # This class implements the Factory design pattern to create different types of AI agents
    # The Factory pattern centralizes object creation and makes it easier to change implementations
    
    def __init__(self):
        """Initialize the agent factory."""
        # Constructor method that runs when a new AgentFactory is created
        
        self.agent_map = {
            "gpt-4": self.create_openai_agent,
            "claude": self.create_anthropic_agent,
            "deepseek": self.create_deepseek_agent
        }
        # Create a dictionary that maps agent type names to their creation methods
        # This allows us to easily look up the correct method to call based on the agent type
        # The keys are strings representing the agent types
        # The values are methods of this class that create the corresponding agent types
    
    def create_openai_agent(self, api_key: str, model_name: str = "gpt-4") -> OpenAIAgent:
        """Create an instance of the OpenAI agent.
        
        Args:
            api_key (str): OpenAI API key
            model_name (str, optional): Model to use. Defaults to "gpt-4".
            
        Returns:
            OpenAIAgent: An instance of the OpenAI agent
        """
        # Method to create an OpenAI agent
        # Takes an API key and an optional model name
        # Returns a new OpenAIAgent instance
        
        return OpenAIAgent(api_key=api_key, model_name=model_name)
        # Create and return a new OpenAIAgent with the provided API key and model name
    
    def create_anthropic_agent(self, api_key: str, model_name: str = "claude-3-5-sonnet-20240620") -> AnthropicAgent:
        """Create an instance of the Anthropic agent.
        
        Args:
            api_key (str): Anthropic API key
            model_name (str, optional): Model to use. Defaults to "claude-3-5-sonnet-20240620".
            
        Returns:
            AnthropicAgent: An instance of the Anthropic agent
        """
        # Method to create an Anthropic agent
        # Takes an API key and an optional model name
        # Returns a new AnthropicAgent instance
        
        return AnthropicAgent(api_key=api_key, model_name=model_name)
        # Create and return a new AnthropicAgent with the provided API key and model name
    
    def create_deepseek_agent(self, api_key: str, model_name: str = "deepseek-chat") -> DeepseekAgent:
        """Create an instance of the Deepseek agent.
        
        Args:
            api_key (str): Deepseek API key
            model_name (str, optional): Model to use. Defaults to "deepseek-chat".
            
        Returns:
            DeepseekAgent: An instance of the Deepseek agent
        """
        # Method to create a Deepseek agent
        # Takes an API key and an optional model name
        # Returns a new DeepseekAgent instance
        
        return DeepseekAgent(api_key=api_key, model_name=model_name)
        # Create and return a new DeepseekAgent with the provided API key and model name
    
    def get_agent(self, agent_type: str, api_key: str, model_name: Optional[str] = None) -> Optional[BaseAgent]:
        """Get an agent instance based on the specified type.
        
        Args:
            agent_type (str): Type of agent to create ("gpt-4", "claude", or "deepseek")
            api_key (str): API key for the agent
            model_name (str, optional): Specific model name to use. Defaults to None.
            
        Returns:
            Optional[BaseAgent]: An instance of the requested agent, or None if the type is invalid
        """
        # Method to get an agent of the specified type
        # This is the main method that clients will call to create agents
        # Takes an agent type, an API key, and an optional model name
        # Returns a BaseAgent instance (which will actually be one of the specific agent types)
        # Returns None if the agent type is invalid
        
        if agent_type not in self.agent_map:
            # Check if the requested agent type is in our map of supported types
            return None
            # If not, return None to indicate that the agent type is not supported
        
        create_func = self.agent_map[agent_type]
        # Get the creation function for the requested agent type from our map
        
        if model_name:
            # Check if a specific model name was provided
            return create_func(api_key=api_key, model_name=model_name)
            # If so, call the creation function with the API key and model name
        else:
            # If no model name was provided
            return create_func(api_key=api_key) 
            # Call the creation function with just the API key, using the default model name 