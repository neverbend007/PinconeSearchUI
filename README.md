# Pinecone Query Agent

A Streamlit application that allows you to ask questions and get comprehensive answers based on information stored in your Pinecone vector database. The application uses multiple AI models to generate answers, including OpenAI's GPT-4, Anthropic's Claude, and Deepseek.

## Table of Contents

1. [Features](#features)
2. [How It Works](#how-it-works)
3. [Project Structure](#project-structure)
4. [Setup Instructions](#setup-instructions)
5. [Running the Application](#running-the-application)
6. [Usage Guide](#usage-guide)
7. [Customization Options](#customization-options)
   - [UI Customization](#ui-customization)
   - [AI Model Selection](#ai-model-selection)
   - [Search Results Configuration](#search-results-configuration)
   - [Prompt Engineering](#prompt-engineering)
   - [Result Formatting](#result-formatting)
8. [Understanding the Code](#understanding-the-code)
9. [Troubleshooting](#troubleshooting)
10. [Requirements](#requirements)
11. [Development and Debugging](#development-and-debugging)

## Features

- Query your Pinecone vector database using natural language
- Get comprehensive answers generated by multiple AI models
- Choose between different AI models for different perspectives:
  - **GPT-4**: OpenAI's most advanced model, excellent for complex reasoning
  - **Claude**: Anthropic's Claude 3.5 Sonnet model, known for thoughtful and nuanced responses
  - **Deepseek**: Deepseek AI's powerful language model, offering another perspective

## How It Works

This application follows these steps to answer your questions:

1. **User Input**: You enter a question in natural language.
2. **Vector Embedding**: Your question is converted into a vector embedding using OpenAI's embedding model.
3. **Similarity Search**: The application searches your Pinecone vector database for the most similar content to your question.
4. **Context Building**: The most relevant information is extracted and formatted into a context.
5. **Answer Generation**: The selected AI model (GPT-4, Claude, or Deepseek) generates a comprehensive answer based on the context.
6. **Display**: The answer is displayed to you in the Streamlit interface.

## Project Structure

The project is organized into several Python files, each with a specific purpose:

- **app.py**: The main application file that sets up the Streamlit interface and orchestrates the entire process.
- **base_agent.py**: Defines the abstract base class that all AI agents must implement.
- **agent_factory.py**: Implements the Factory design pattern to create different types of AI agents.
- **openai_agent.py**: Implements the OpenAI agent for generating answers with GPT-4.
- **anthropic_agent.py**: Implements the Anthropic agent for generating answers with Claude.
- **deepseek_agent.py**: Implements the Deepseek agent for generating answers with Deepseek models.
- **pinecone_agent.py**: Processes and formats results from Pinecone, including metadata extraction and content summarization.
- **test_pinecone_api.py**: A utility script to test the connection to Pinecone.
- **.env.example**: A template for the environment variables file.
- **requirements.txt**: Lists all the Python packages required by the application.

## Setup Instructions

Follow these steps to set up the application:

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd PineconeQueryAgent
   ```

2. **Create a Virtual Environment** (optional but recommended):
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the Required Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   - Create a `.env` file based on the `.env.example` template:
     ```bash
     # On Windows
     copy .env.example .env

     # On macOS/Linux
     cp .env.example .env
     ```
   - Open the `.env` file in a text editor and fill in your API keys:
     ```
     # OpenAI API key
     OPENAI_API_KEY=your_openai_api_key_here

     # Anthropic API key
     ANTHROPIC_API_KEY=your_anthropic_api_key_here

     # Deepseek API key
     DEEPSEEK_API_KEY=your_deepseek_api_key_here

     # Pinecone configuration
     PINECONE_API_KEY=your_pinecone_api_key_here
     PINECONE_INDEX_NAME=your_pinecone_index_name_here
     ```

5. **Verify Pinecone Connection** (optional):
   ```bash
   python test_pinecone_api.py
   ```
   This will test your connection to Pinecone and list the available indexes.

## Running the Application

Run the application with:

```bash
streamlit run app.py
```

The application will be available at http://localhost:8501 (or another port if 8501 is already in use).

## Usage Guide

1. **Open the Application**: Navigate to http://localhost:8501 in your web browser.
2. **Choose an AI Model**: Select one of the available models (GPT-4, Claude, or Deepseek) using the radio buttons.
3. **Enter Your Question**: Type your question in the text input field.
4. **Get an Answer**: Click the "Get Answer" button to generate an answer.
5. **View the Answer**: The generated answer will be displayed below the button.

## Customization Options

### UI Customization

You can customize the user interface of the application, including the logo:

1. **Logo Placement**: The application displays a logo in the top-left corner of the sidebar:
   - Place your logo file in the `assets` directory (create it if it doesn't exist)
   - The default path is `assets/AIworkshopLogo.png`
   - To use a different logo file, update the path in `app.py`:
     ```python
     logo_path = os.path.join("assets", "your-logo-file.png")
     ```
   - You can adjust the logo size by changing the width parameter:
     ```python
     st.image(logo, width=100)  # Increase or decrease the width as needed
     ```

2. **Page Configuration**: You can modify the page title, icon, and layout in `app.py`:
   ```python
   st.set_page_config(
       page_title="Your Custom Title",  # Change the browser tab title
       page_icon="🔍",                  # Change the icon (emoji or path to image)
       layout="wide"                    # Options: "wide" or "centered"
   )
   ```

3. **Colors and Themes**: Streamlit supports themes that can be configured in a `.streamlit/config.toml` file:
   ```toml
   [theme]
   primaryColor = "#F63366"
   backgroundColor = "#FFFFFF"
   secondaryBackgroundColor = "#F0F2F6"
   textColor = "#262730"
   font = "sans serif"
   ```

### AI Model Selection

You can modify which AI models are available for users to choose from:

1. Open `app.py`
2. Locate the model selection code (around line 310):
   ```python
   # Model selection with radio buttons
   model_option = st.radio(
       "Choose the AI model to answer your question:",  # Label for the radio buttons
       ["GPT-4", "Claude", "Deepseek"],                # Options for the radio buttons
       horizontal=True                                 # Display the options horizontally
   )
   ```
3. To add or remove models:
   - Add a new model name to the list: `["GPT-4", "Claude", "Deepseek", "Your-New-Model"]`
   - Remove a model by deleting it from the list: `["GPT-4", "Deepseek"]`
   - Change the display name of a model: `["GPT-4 Turbo", "Claude", "Deepseek"]`

4. If you add a new model, you'll also need to update the `agent_type_map` (around line 350):
   ```python
   # Get the appropriate agent based on the selected model
   agent_type_map = {
       "GPT-4": "gpt-4",           # Map the display name to the internal name
       "Claude": "claude",          # Map the display name to the internal name
       "Deepseek": "deepseek",      # Map the display name to the internal name
       "Your-New-Model": "internal-name"  # Add your new model mapping here
   }
   ```

5. You'll also need to implement a new agent class and update the `AgentFactory` class:
   - Create a new file (e.g., `your_new_model_agent.py`) that implements the `BaseAgent` abstract class
   - Add a new method to `AgentFactory` to create your new agent type
   - Update the `agent_map` in the `AgentFactory` constructor to include your new agent type

6. **Important**: Add the API key for your new model to the `.env` file:
   ```
   # Existing API keys
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   DEEPSEEK_API_KEY=your_deepseek_api_key_here
   
   # New model API key
   YOUR_NEW_MODEL_API_KEY=your_new_model_api_key_here
   ```

7. Update the API key validation and mapping in `app.py`:
   - Add a check for the new API key in the environment variables section
   - Add the new API key to the `api_key_map` (around line 350):
     ```python
     # Map the agent type to the corresponding API key
     api_key_map = {
         "gpt-4": openai_api_key,           # Map the internal name to the API key
         "claude": anthropic_api_key,        # Map the internal name to the API key
         "deepseek": deepseek_api_key,       # Map the internal name to the API key
         "internal-name": your_new_model_api_key  # Add your new model's API key mapping
     }
     ```

### Search Results Configuration

By default, the application retrieves the top 5 most similar results from the Pinecone database for each query. This limit balances providing enough context for the AI while maintaining performance and keeping API costs reasonable.

If you want to adjust this limit:

1. Open `app.py`
2. Locate the similarity search code (around line 328):
   ```python
   search_results = vector_store.similarity_search_with_score(
       query=query,  # The user's question
       k=5            # Return the top 5 most similar results - adjust this value to retrieve more or fewer results
   )
   ```
3. Change the `k=5` parameter to your desired number of results:
   - Increasing this value will provide more context to the AI but may increase response time and API costs
   - Decreasing this value will reduce context but may improve performance

### Prompt Engineering

You can customize how the AI generates answers by modifying the system prompts:

1. Open the agent file for the model you want to customize:
   - `openai_agent.py` for GPT-4
   - `anthropic_agent.py` for Claude
   - `deepseek_agent.py` for Deepseek

2. Locate the system prompt in the `generate_answer` method:
   ```python
   # Example from openai_agent.py
   messages=[
       {
           "role": "system",
           "content": "You are a helpful assistant that provides comprehensive answers based on the retrieved information. Cite your sources when appropriate."
       },
       # ... other messages ...
   ]
   ```

3. Modify the "content" of the system message to change how the AI behaves:
   - To make answers more concise: "You are a concise assistant that provides brief, accurate answers..."
   - To make answers more detailed: "You are a detailed assistant that thoroughly explains concepts..."
   - To change the tone: "You are a friendly assistant that uses simple language..."

4. You can also modify the user message format to change how the question and context are presented to the AI.

### Result Formatting

You can change how search results are formatted before being sent to the AI model:

1. Open `base_agent.py`
2. Locate the `format_context` method:
   ```python
   def format_context(self, results: List[Dict[str, Any]]) -> str:
       context = ""
       for i, result in enumerate(results):
           context += f"Document {i + 1}:\n"
           if "title" in result:
               context += f"Title: {result.get('title', 'Untitled')}\n"
           if "description" in result:
               context += f"Description: {result.get('description', '')}\n"
           if "text" in result:
               context += f"Content: {result.get('text', '')}\n"
           context += f"Relevance Score: {result.get('score', 0):.4f}\n\n"
       return context
   ```

3. Modify this method to change how the results are formatted:
   - Change the labels: Replace "Document" with "Source" or another term
   - Add or remove fields: Include additional metadata fields if available
   - Change the formatting: Use markdown formatting for better readability
   - Reorder information: Put the most important information first

4. Example of a modified `format_context` method with markdown formatting:
   ```python
   def format_context(self, results: List[Dict[str, Any]]) -> str:
       context = "## Retrieved Information\n\n"
       for i, result in enumerate(results):
           context += f"### Source {i + 1} (Relevance: {result.get('score', 0):.2f})\n\n"
           if "title" in result:
               context += f"**Title:** {result.get('title', 'Untitled')}\n\n"
           if "description" in result:
               context += f"**Summary:** {result.get('description', '')}\n\n"
           if "text" in result:
               context += f"**Content:**\n{result.get('text', '')}\n\n"
           # Add a separator between results
           context += "---\n\n"
       return context
   ```

These customizations allow you to tailor the application to your specific needs, changing how it presents information to users and how it interacts with AI models.

## Understanding the Code

### How the Files Work Together

1. **Entry Point**: The application starts with `app.py`, which sets up the Streamlit interface and handles user input.

2. **Agent Creation Flow**:
   - `app.py` creates an instance of `AgentFactory`
   - When a user selects a model and submits a question, `app.py` calls `agent_factory.get_agent()`
   - `AgentFactory` creates the appropriate agent (OpenAI, Anthropic, or Deepseek)
   - Each agent implements the `BaseAgent` abstract class

3. **Query Processing Flow**:
   - User enters a question in the Streamlit interface
   - `app.py` converts the question to a vector embedding using OpenAI's embedding model
   - `app.py` searches the Pinecone vector database for similar content
   - The search results are passed to the selected agent
   - The agent formats the context and generates an answer
   - The answer is displayed to the user

### Key Components

#### 1. BaseAgent (base_agent.py)

This is an abstract base class that defines the interface for all AI agents. It includes:
- A constructor that takes an API key
- A method to validate the API key
- A method to format the context from search results
- An abstract method `generate_answer()` that must be implemented by subclasses

```python
class BaseAgent(ABC):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self._validate_api_key()

    def _validate_api_key(self):
        if not self.api_key:
            raise ValueError("API key is required.")

    def format_context(self, results: List[Dict[str, Any]]) -> str:
        # Format the search results into a context string
        ...

    @abstractmethod
    async def generate_answer(self, query: str, results: List[Dict[str, Any]]) -> str:
        # This method must be implemented by subclasses
        pass
```

#### 2. AgentFactory (agent_factory.py)

This class implements the Factory design pattern to create different types of AI agents. It includes:
- A constructor that sets up a mapping from agent types to creation methods
- Methods to create each type of agent
- A method to get an agent of the specified type

```python
class AgentFactory:
    def __init__(self):
        self.agent_map = {
            "gpt-4": self.create_openai_agent,
            "claude": self.create_anthropic_agent,
            "deepseek": self.create_deepseek_agent
        }

    def create_openai_agent(self, api_key: str, model_name: str = "gpt-4") -> OpenAIAgent:
        return OpenAIAgent(api_key=api_key, model_name=model_name)

    # Similar methods for other agent types

    def get_agent(self, agent_type: str, api_key: str, model_name: Optional[str] = None) -> Optional[BaseAgent]:
        if agent_type not in self.agent_map:
            return None
        
        create_func = self.agent_map[agent_type]
        
        if model_name:
            return create_func(api_key=api_key, model_name=model_name)
        else:
            return create_func(api_key=api_key)
```

#### 3. Specific Agents (openai_agent.py, anthropic_agent.py, deepseek_agent.py)

Each agent implements the `BaseAgent` abstract class and provides a specific implementation of the `generate_answer()` method for its respective AI model. For example:

```python
class OpenAIAgent(BaseAgent):
    def __init__(self, api_key: str, model_name: str = "gpt-4"):
        super().__init__(api_key)
        self.model_name = model_name
        self.client = AsyncOpenAI(api_key=api_key)

    async def generate_answer(self, query: str, results: List[Dict[str, Any]]) -> str:
        context = self.format_context(results)
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant..."},
                    {"role": "user", "content": f"Based on the following information..."}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating answer with OpenAI: {e}")
            return "I couldn't generate an answer based on the retrieved information."
```

#### 4. Main Application (app.py)

This file sets up the Streamlit interface and orchestrates the entire process. It:
- Loads environment variables
- Initializes connections to OpenAI, Anthropic, Deepseek, and Pinecone
- Creates the Streamlit interface
- Handles user input
- Searches the Pinecone vector database
- Calls the selected agent to generate an answer
- Displays the answer to the user

## Troubleshooting

### Common Issues

1. **API Key Issues**:
   - **Symptom**: Error messages about invalid or missing API keys
   - **Solution**: Double-check your API keys in the `.env` file and make sure they are correct
   - **Note**: The application checks for leading/trailing whitespace in API keys and attempts to clean them automatically

2. **Pinecone Connection Issues**:
   - **Symptom**: Errors connecting to Pinecone or finding your index
   - **Solution**: Run `python test_pinecone_api.py` to test your connection and verify your API key and index name
   - **Note**: The test script provides detailed error messages to help diagnose connection problems

3. **Missing Dependencies**:
   - **Symptom**: Import errors or missing module errors
   - **Solution**: Make sure you've installed all the required packages with `pip install -r requirements.txt`
   - **Note**: The requirements file includes comments explaining what each package is used for

4. **GRPC Dependencies**:
   - **Symptom**: Errors about missing GRPC dependencies
   - **Solution**: Install the GRPC dependencies with `pip install pinecone-client[grpc]`
   - **Note**: The application uses the GRPC client for better performance with Pinecone

5. **Logo Display Issues**:
   - **Symptom**: Logo not appearing in the sidebar
   - **Solution**: Ensure your logo file is in the correct location (`assets/AIworkshopLogo.png` by default)
   - **Note**: The code includes error handling to prevent crashes if the logo file is missing

### Getting Help

If you encounter issues not covered in this README, please:
1. Check the error messages for clues about what's wrong
2. Search for the error message online
3. Check the documentation for the specific package causing the error
4. Reach out to the community for help

## Requirements

- Python 3.8+
- Streamlit
- OpenAI API key
- Anthropic API key
- Deepseek API key
- Pinecone API key and index

See `requirements.txt` for a complete list of Python package dependencies.

## Development and Debugging

The application includes several debugging features to help with development and troubleshooting:

1. **Debug Print Statements**: The code includes debug print statements that output information to the terminal (not visible in the Streamlit UI):
   ```python
   print(f"DEBUG - Pinecone API key first 5 chars: {pinecone_api_key[:5] if pinecone_api_key else 'None'}")
   ```

2. **Error Handling**: Each major component includes try-except blocks with specific error messages:
   ```python
   try:
       # Code that might fail
   except Exception as e:
       print(f"Error message: {e}")
       st.error("User-friendly error message")
   ```

3. **Fallback Mechanisms**: If an API call fails, the agents return a fallback message:
   ```python
   return "I couldn't generate an answer based on the retrieved information."
   ```

4. **Testing Utilities**: The `test_pinecone_api.py` script can be used to verify your Pinecone connection independently of the main application.

5. **Manual API Key Input**: If environment variables are missing, the application provides text inputs for users to enter API keys directly.

When developing new features or debugging issues:

1. Check the terminal output for debug messages
2. Use `st.write()` or `st.json()` to display variables in the Streamlit UI
3. Add temporary `print()` statements to track execution flow
4. Use `st.exception(e)` to display full exception details in the UI 