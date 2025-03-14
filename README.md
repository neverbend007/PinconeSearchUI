# Pinecone Query Agent 🔍

A Streamlit application that allows you to ask questions and get comprehensive answers based on information stored in your Pinecone vector database. The application uses multiple AI models to generate answers, including OpenAI's GPT-4, Anthropic's Claude, and Deepseek.

![image](https://github.com/user-attachments/assets/2fd514d3-aeb3-4d5d-9e7e-dfd348131e7b)


## Table of Contents

1. [✨ Features](#features)
2. [🔄 How It Works](#how-it-works)
3. [📁 Project Structure](#project-structure)
4. [🚀 Setup Instructions](#setup-instructions)
5. [▶️ Running the Application](#running-the-application)
6. [📝 Usage Guide](#usage-guide)
7. [⚙️ Customization Options](#customization-options)
   - [🎨 UI Customization](#ui-customization)
   - [🤖 AI Model Selection](#ai-model-selection)
   - [🔎 Search Results Configuration](#search-results-configuration)
   - [💬 Prompt Engineering](#prompt-engineering)
   - [📊 Result Formatting](#result-formatting)
8. [🧩 Understanding the Code](#understanding-the-code)
9. [🛠️ Troubleshooting](#troubleshooting)
10. [📋 Requirements](#requirements)
11. [🔧 Development and Debugging](#development-and-debugging)

---

## ✨ Features

- Query your Pinecone vector database using natural language
- Get comprehensive answers generated by multiple AI models
- Choose between different AI models for different perspectives:
  - **GPT-4**: OpenAI's most advanced model, excellent for complex reasoning
  - **Claude**: Anthropic's Claude 3.5 Sonnet model, known for thoughtful and nuanced responses
  - **Deepseek**: Deepseek AI's powerful language model, offering another perspective

---

## 🔄 How It Works

This application follows these steps to answer your questions:

1. **User Input**: You enter a question in natural language.
2. **Vector Embedding**: Your question is converted into a vector embedding using OpenAI's embedding model.
3. **Similarity Search**: The application searches your Pinecone vector database for the most similar content to your question.
4. **Context Building**: The most relevant information is extracted and formatted into a context.
5. **Answer Generation**: The selected AI model (GPT-4, Claude, or Deepseek) generates a comprehensive answer based on the context.
6. **Display**: The answer is displayed to you in the Streamlit interface.

---

## 📁 Project Structure

The project is organized into several Python files, each with a specific purpose:

| File | Purpose |
|------|---------|
| **app.py** | The main application file that sets up the Streamlit interface and orchestrates the entire process. |
| **base_agent.py** | Defines the abstract base class that all AI agents must implement. |
| **agent_factory.py** | Implements the Factory design pattern to create different types of AI agents. |
| **openai_agent.py** | Implements the OpenAI agent for generating answers with GPT-4. |
| **anthropic_agent.py** | Implements the Anthropic agent for generating answers with Claude. |
| **deepseek_agent.py** | Implements the Deepseek agent for generating answers with Deepseek models. |
| **pinecone_agent.py** | Processes and formats results from Pinecone, including metadata extraction and content summarization. |
| **test_pinecone_api.py** | A utility script to test the connection to Pinecone. |
| **.env.example** | A template for the environment variables file. |
| **requirements.txt** | Lists all the Python packages required by the application. |

---

## 🚀 Setup Instructions

Follow these steps to set up the application:

### 1. Clone the Repository

```bash
git clone <repository-url>
cd PineconeQueryAgent
```

### 2. Create a Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install the Required Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

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

### 5. Verify Pinecone Connection (optional)

```bash
python test_pinecone_api.py
```

This will test your connection to Pinecone and list the available indexes.

---

## ▶️ Running the Application

Run the application with:

```bash
streamlit run app.py
```

The application will be available at http://localhost:8501 (or another port if 8501 is already in use).

---

## 📝 Usage Guide

1. **Open the Application**: Navigate to http://localhost:8501 in your web browser.
2. **Choose an AI Model**: Select one of the available models (GPT-4, Claude, or Deepseek) using the radio buttons.
3. **Enter Your Question**: Type your question in the text input field.
4. **Get an Answer**: Click the "Get Answer" button to generate an answer.
5. **View the Answer**: The generated answer will be displayed below the button.

---

## ⚙️ Customization Options

### 🎨 UI Customization

You can customize the user interface of the application, including the logo:

#### Logo Placement

The application displays a logo in the top-left corner of the sidebar:

```python
# Place your logo file in the assets directory
logo_path = os.path.join("assets", "AIworkshopLogo.png")
st.image(logo, width=100)  # Adjust width as needed
```

> 💡 **Tip:** Create the `assets` directory if it doesn't exist and place your logo file there.

#### Page Configuration

Modify the page title, icon, and layout in `app.py`:

```python
st.set_page_config(
    page_title="Your Custom Title",  # Change the browser tab title
    page_icon="🔍",                  # Change the icon (emoji or path to image)
    layout="wide"                    # Options: "wide" or "centered"
)
```

#### Colors and Themes

Streamlit supports themes that can be configured in a `.streamlit/config.toml` file:

```toml
[theme]
primaryColor = "#F63366"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

### 🤖 AI Model Selection

You can modify which AI models are available for users to choose from:

#### Step 1: Update the Model Selection UI

Open `app.py` and locate the model selection code:

```python
# Model selection with radio buttons
model_option = st.radio(
    "Choose the AI model to answer your question:",
    ["GPT-4", "Claude", "Deepseek"],
    horizontal=True
)
```

To add or remove models:
- Add a new model: `["GPT-4", "Claude", "Deepseek", "Your-New-Model"]`
- Remove a model: `["GPT-4", "Deepseek"]`
- Change display name: `["GPT-4 Turbo", "Claude", "Deepseek"]`

#### Step 2: Update the Agent Type Mapping

If you add a new model, update the `agent_type_map`:

```python
agent_type_map = {
    "GPT-4": "gpt-4",
    "Claude": "claude",
    "Deepseek": "deepseek",
    "Your-New-Model": "internal-name"  # Add your new model mapping here
}
```

#### Step 3: Implement a New Agent Class

Create a new file (e.g., `your_new_model_agent.py`) that implements the `BaseAgent` abstract class.

#### Step 4: Update the Environment Variables

Add the API key for your new model to the `.env` file:

```
# Existing API keys
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# New model API key
YOUR_NEW_MODEL_API_KEY=your_new_model_api_key_here
```

#### Step 5: Update the API Key Mapping

Add the new API key to the `api_key_map`:

```python
api_key_map = {
    "gpt-4": openai_api_key,
    "claude": anthropic_api_key,
    "deepseek": deepseek_api_key,
    "internal-name": your_new_model_api_key
}
```

### 🔎 Search Results Configuration

By default, the application retrieves the top 5 most similar results from the Pinecone database for each query.

To adjust this limit:

1. Open `app.py`
2. Locate the similarity search code:
   ```python
   search_results = vector_store.similarity_search_with_score(
       query=query,  # The user's question
       k=5            # Return the top 5 most similar results
   )
   ```
3. Change the `k=5` parameter to your desired number of results.

> ⚠️ **Note:** Increasing this value provides more context but may increase response time and API costs.

### 💬 Prompt Engineering

You can customize how the AI generates answers by modifying the system prompts:

#### Step 1: Open the Agent File

Open the agent file for the model you want to customize:
- `openai_agent.py` for GPT-4
- `anthropic_agent.py` for Claude
- `deepseek_agent.py` for Deepseek

#### Step 2: Locate the System Prompt

Find the system prompt in the `generate_answer` method:

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

#### Step 3: Modify the Prompt

Change the "content" of the system message to adjust the AI's behavior:

| Behavior | Example Prompt |
|----------|----------------|
| **More concise** | "You are a concise assistant that provides brief, accurate answers..." |
| **More detailed** | "You are a detailed assistant that thoroughly explains concepts..." |
| **Friendlier tone** | "You are a friendly assistant that uses simple language..." |

### 📊 Result Formatting

You can change how search results are formatted before being sent to the AI model:

#### Step 1: Open the Base Agent File

Open `base_agent.py` and locate the `format_context` method:

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

#### Step 2: Modify the Formatting

Example with markdown formatting:

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

> 💡 **Tip:** Using markdown formatting can significantly improve readability for both the AI model and humans reviewing the code.

---

## 🧩 Understanding the Code

### How the Files Work Together

1. **Entry Point**: The application starts with `app.py`, which sets up the Streamlit interface and handles user input.

2. **Agent Creation Flow**:
   ```
   app.py → AgentFactory → Specific Agent (OpenAI, Anthropic, or Deepseek)
   ```

3. **Query Processing Flow**:
   ```
   User Input → Vector Embedding → Pinecone Search → Context Formatting → Answer Generation → Display
   ```

### Key Components

#### 1. BaseAgent (base_agent.py)

This is an abstract base class that defines the interface for all AI agents:

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

This class implements the Factory design pattern to create different types of AI agents:

```python
class AgentFactory:
    def __init__(self):
        self.agent_map = {
            "gpt-4": self.create_openai_agent,
            "claude": self.create_anthropic_agent,
            "deepseek": self.create_deepseek_agent
        }

    def get_agent(self, agent_type: str, api_key: str, model_name: Optional[str] = None) -> Optional[BaseAgent]:
        if agent_type not in self.agent_map:
            return None
        
        create_func = self.agent_map[agent_type]
        
        if model_name:
            return create_func(api_key=api_key, model_name=model_name)
        else:
            return create_func(api_key=api_key)
```

#### 3. Specific Agents

Each agent implements the `BaseAgent` abstract class with a specific implementation for its AI model.

---

## 🛠️ Troubleshooting

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| **API Key Issues** | Error messages about invalid or missing API keys | Double-check your API keys in the `.env` file |
| **Pinecone Connection** | Errors connecting to Pinecone | Run `python test_pinecone_api.py` to test your connection |
| **Missing Dependencies** | Import errors or missing module errors | Run `pip install -r requirements.txt` |
| **GRPC Dependencies** | Errors about missing GRPC dependencies | Install with `pip install pinecone-client[grpc]` |
| **Logo Display Issues** | Logo not appearing in the sidebar | Ensure your logo file is in the correct location |

> 🔍 **Tip:** The application includes error handling to provide helpful error messages when things go wrong.

---

## 📋 Requirements

- Python 3.8+
- Streamlit
- OpenAI API key
- Anthropic API key
- Deepseek API key
- Pinecone API key and index

See `requirements.txt` for a complete list of Python package dependencies.

---

## 🔧 Development and Debugging

The application includes several debugging features to help with development and troubleshooting:

### Debug Print Statements

```python
print(f"DEBUG - Pinecone API key first 5 chars: {pinecone_api_key[:5] if pinecone_api_key else 'None'}")
```

### Error Handling

```python
try:
    # Code that might fail
except Exception as e:
    print(f"Error message: {e}")
    st.error("User-friendly error message")
```

### Debugging Tips

1. Check the terminal output for debug messages
2. Use `st.write()` or `st.json()` to display variables in the Streamlit UI
3. Add temporary `print()` statements to track execution flow
4. Use `st.exception(e)` to display full exception details in the UI 
