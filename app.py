import os
# Import the os module to interact with the operating system, including environment variables

import streamlit as st
# Import Streamlit library which is used to create web applications with Python

import asyncio
# Import asyncio for asynchronous programming, allowing non-blocking operations

import json
# Import json module for handling JSON data

from dotenv import load_dotenv
# Import load_dotenv to load environment variables from a .env file

from pinecone.grpc import PineconeGRPC as Pinecone
# Import the Pinecone GRPC client for vector database operations
# GRPC is a high-performance remote procedure call framework

from openai import OpenAI
# Import OpenAI client for accessing OpenAI's API services

from langchain_openai import OpenAIEmbeddings
# Import OpenAIEmbeddings from langchain to create vector embeddings of text

from langchain_pinecone import PineconeVectorStore
# Import PineconeVectorStore from langchain to interact with Pinecone vector database

import anthropic
# Import anthropic for accessing Anthropic's Claude AI models

import requests
# Import requests for making HTTP requests

from PIL import Image
# Import Image from PIL (Pillow) for handling image files

# Import our agent factory
from agent_factory import AgentFactory
# Import the AgentFactory class which creates different AI agents (OpenAI, Anthropic, Deepseek)

# Load environment variables from .env file
load_dotenv()
# This loads API keys and other configuration from a .env file in the project directory

# Configure Streamlit page
st.set_page_config(page_title="Pinecone Query Agent", page_icon="🔍", layout="wide")
# Set up the Streamlit page with a title, icon, and wide layout

# Display the title in the main area
st.title("Pinecone Query Agent")
# Display the main title of the application

# Initialize OpenAI client by getting the API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
# Get the OpenAI API key from environment variables

if not openai_api_key:
    # Check if the OpenAI API key exists
    st.error("OpenAI API key not found. Please add it to your .env file.")
    # Display an error message if the API key is missing
    st.stop()
    # Stop the application execution

# Initialize Anthropic client by getting the API key from environment variables
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
# Get the Anthropic API key from environment variables

if not anthropic_api_key:
    # Check if the Anthropic API key exists
    st.error("Anthropic API key not found. Please add it to your .env file.")
    # Display an error message if the API key is missing
    st.stop()
    # Stop the application execution

# Initialize Deepseek API key from environment variables
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
# Get the Deepseek API key from environment variables

if not deepseek_api_key:
    # Check if the Deepseek API key exists
    st.error("Deepseek API key not found. Please add it to your .env file.")
    # Display an error message if the API key is missing
    st.stop()
    # Stop the application execution

# Initialize Pinecone by getting the API key and index name from environment variables
pinecone_api_key = os.getenv("PINECONE_API_KEY")
# Get the Pinecone API key from environment variables

pinecone_index_name = os.getenv("PINECONE_INDEX_NAME", "pydanticai")
# Get the Pinecone index name from environment variables, defaulting to "pydanticai" if not specified

# Debug print statements - these will only show in the terminal, not in the Streamlit UI
print(f"DEBUG - Pinecone API key first 5 chars: {pinecone_api_key[:5] if pinecone_api_key else 'None'}")
# Print the first 5 characters of the Pinecone API key for debugging

print(f"DEBUG - Pinecone API key length: {len(pinecone_api_key) if pinecone_api_key else 'None'}")
# Print the length of the Pinecone API key for debugging

print(f"DEBUG - Pinecone index name: {pinecone_index_name}")
# Print the Pinecone index name for debugging

# Check for special characters or whitespace in the API key
if pinecone_api_key:
    # If the Pinecone API key exists
    if pinecone_api_key.strip() != pinecone_api_key:
        # Check if the API key has leading or trailing whitespace
        print("WARNING: Pinecone API key contains leading or trailing whitespace!")
        # Print a warning if whitespace is detected
        
        # Try to clean the API key by removing whitespace
        pinecone_api_key = pinecone_api_key.strip()
        # Remove leading and trailing whitespace from the API key
        
        print(f"DEBUG - Cleaned API key first 5 chars: {pinecone_api_key[:5]}")
        # Print the first 5 characters of the cleaned API key for debugging

# Allow manual input of API key if needed
if not pinecone_api_key:
    # If the Pinecone API key is not found in environment variables
    st.warning("Pinecone API key not found in environment variables.")
    # Display a warning message
    
    pinecone_api_key = st.text_input("Enter your Pinecone API key:", type="password")
    # Create a text input field for the user to enter their Pinecone API key
    
    if not pinecone_api_key:
        # If the user doesn't enter an API key
        st.stop()
        # Stop the application execution

if not pinecone_index_name:
    # If the Pinecone index name is not found in environment variables
    st.warning("Pinecone index name not found in environment variables.")
    # Display a warning message
    
    pinecone_index_name = st.text_input("Enter your Pinecone index name:", value="pydanticai")
    # Create a text input field for the user to enter their Pinecone index name, with a default value
    
    if not pinecone_index_name:
        # If the user doesn't enter an index name
        st.stop()
        # Stop the application execution

# SIMPLIFIED PINECONE INITIALIZATION
try:
    # Try to initialize Pinecone and connect to the index
    
    # Initialize Pinecone client using the GRPC client
    print("DEBUG - Creating Pinecone connection via LangChain...")
    # Print a debug message
    
    try:
        # Try to initialize the Pinecone client
        
        # Initialize Pinecone with the GRPC client
        pc = Pinecone(api_key=pinecone_api_key)
        # Create a Pinecone client instance with the API key
        
        print("DEBUG - Pinecone initialized successfully")
        # Print a debug message if initialization is successful
        
        # Verify connection by listing indexes
        try:
            # Try to list the available indexes
            indexes = pc.list_indexes()
            # Get a list of all indexes in the Pinecone account
            
            print(f"DEBUG - Successfully listed indexes: {indexes}")
            # Print a debug message with the list of indexes
            
            # Check if our index exists
            index_names = [idx.name for idx in indexes]
            # Create a list of index names
            
            if pinecone_index_name not in index_names:
                # If the specified index name is not found
                st.error(f"Index '{pinecone_index_name}' not found in your Pinecone account. Available indexes: {index_names}")
                # Display an error message with the available indexes
                
                st.stop()
                # Stop the application execution
                
        except Exception as e:
            # If there's an error listing indexes
            print(f"DEBUG - Error listing indexes: {str(e)}")
            # Print a debug message with the error
            
            st.error(f"Error connecting to Pinecone: {str(e)}")
            # Display an error message
            
            st.error("Your API key may be invalid or expired. Please check your Pinecone console.")
            # Display a more specific error message about the API key
            
            # Option to enter a new API key
            new_api_key = st.text_input("Enter a new Pinecone API key:", type="password", key="new_api_key")
            # Create a text input field for the user to enter a new API key
            
            if new_api_key and st.button("Try with new API key"):
                # If the user enters a new API key and clicks the button
                pinecone_api_key = new_api_key
                # Update the API key
                
                st.experimental_rerun()
                # Rerun the application with the new API key
            
            st.stop()
            # Stop the application execution
        
        # Initialize OpenAI embeddings for converting text to vectors
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",  # Use OpenAI's text-embedding-3-small model
            openai_api_key=openai_api_key    # Pass the OpenAI API key
        )
        
        # Create the vector store directly - using the correct method for the GRPC client
        vector_store = PineconeVectorStore.from_existing_index(
            index_name=pinecone_index_name,  # The name of the Pinecone index
            embedding=embeddings,            # The embedding model to use
            text_key="text"                  # The key in the metadata that contains the text
        )
        print("DEBUG - PineconeVectorStore created successfully")
        # Print a debug message if the vector store is created successfully
        
        # Get the underlying index
        index = vector_store._index
        # Access the underlying Pinecone index object
        
        print("DEBUG - Successfully connected to index")
        # Print a debug message if the connection is successful
        
    except Exception as e:
        # If there's an error creating the Pinecone connection
        print(f"DEBUG - Error creating Pinecone connection: {str(e)}")
        # Print a debug message with the error
        
        st.error(f"Error connecting to Pinecone: {str(e)}")
        # Display an error message
        
        # Provide more helpful error messages based on common issues
        if "401" in str(e) or "unauthorized" in str(e).lower() or "invalid api key" in str(e).lower():
            # If the error is related to authentication
            st.error("Authentication failed. Your Pinecone API key appears to be invalid or expired.")
            # Display a more specific error message about authentication
            
            st.info("Please check your Pinecone console and generate a new API key if needed.")
            # Display information about how to fix the issue
            
            # Option to enter a new API key
            new_api_key = st.text_input("Enter a new Pinecone API key:", type="password", key="new_api_key_inner")
            # Create a text input field for the user to enter a new API key
            
            if new_api_key and st.button("Try with new API key", key="try_new_key_inner"):
                # If the user enters a new API key and clicks the button
                pinecone_api_key = new_api_key
                # Update the API key
                
                st.experimental_rerun()
                # Rerun the application with the new API key
        
        st.stop()
        # Stop the application execution
    
except Exception as e:
    # If there's an error in the outer try block
    print(f"DEBUG - Outer exception: {str(e)}")
    # Print a debug message with the error
    
    st.error(f"Error connecting to Pinecone: {str(e)}")
    # Display an error message
    
    st.exception(e)
    # Display the full exception details
    
    st.stop()
    # Stop the application execution

# Initialize agent factory for creating AI agents
agent_factory = AgentFactory()
# Create an instance of the AgentFactory class

# Helper function to run async functions in Streamlit
def run_async(coro):
    """
    Run an asynchronous coroutine in a synchronous context.
    
    Args:
        coro: The coroutine (async function) to run
        
    Returns:
        The result of the coroutine
    """
    loop = asyncio.new_event_loop()
    # Create a new event loop
    
    asyncio.set_event_loop(loop)
    # Set the event loop
    
    try:
        return loop.run_until_complete(coro)
        # Run the coroutine until it completes and return the result
    finally:
        loop.close()
        # Close the event loop

# Query interface section
st.subheader("Ask a question")
# Display a subheading for the query section

# Model selection with radio buttons
model_option = st.radio(
    "Choose the AI model to answer your question:",  # Label for the radio buttons
    ["GPT-4", "Claude", "Deepseek"],                # Options for the radio buttons
    horizontal=True                                 # Display the options horizontally
)

# Text input for the user's question
query = st.text_input("Enter your question:")
# Create a text input field for the user to enter their question

# Button to trigger the answer generation
if st.button("Get Answer"):
    # If the user clicks the "Get Answer" button
    if query:
        # If the user has entered a question
        with st.spinner("Searching and generating answer..."):
            # Display a spinner while processing
            try:
                # Try to search and generate an answer
                
                # Query Pinecone using the vector store's similarity search
                search_results = vector_store.similarity_search_with_score(
                    query=query,  # The user's question
                    k=5            # Return the top 5 most similar results - adjust this value to retrieve more or fewer results
                )
                
                # Check if we got any results
                if not search_results:
                    # If no results were found
                    st.info("No relevant information found to answer your question.")
                    # Display an information message
                    
                    st.stop()
                    # Stop the application execution
                
                # Process results without displaying them
                processed_results = []
                # Create an empty list to store the processed results
                
                for doc, score in search_results:
                    # For each document and its similarity score
                    
                    # Create a result dictionary for the agent
                    result_dict = {
                        "score": float(score),           # The similarity score as a float
                        "text": doc.page_content,        # The content of the document
                        **doc.metadata                   # Include all metadata from the document
                    }
                    processed_results.append(result_dict)
                    # Add the result dictionary to the processed results list
                
                # Get the appropriate agent based on the selected model
                agent_type_map = {
                    "GPT-4": "gpt-4",           # Map the display name to the internal name
                    "Claude": "claude",          # Map the display name to the internal name
                    "Deepseek": "deepseek"       # Map the display name to the internal name
                }
                
                # Map the agent type to the corresponding API key
                api_key_map = {
                    "gpt-4": openai_api_key,           # Map the internal name to the API key
                    "claude": anthropic_api_key,        # Map the internal name to the API key
                    "deepseek": deepseek_api_key        # Map the internal name to the API key
                }
                
                # Get the agent type and API key
                agent_type = agent_type_map.get(model_option)
                # Get the internal agent type name based on the selected model
                
                api_key = api_key_map.get(agent_type)
                # Get the API key for the selected agent type
                
                # Create and use the agent
                agent = agent_factory.get_agent(agent_type, api_key)
                # Create an agent of the selected type with the appropriate API key
                
                if not agent:
                    # If the agent couldn't be created
                    st.error(f"Could not create agent for {model_option}")
                    # Display an error message
                    
                    st.stop()
                    # Stop the application execution
                
                # Generate the answer using the agent
                answer = run_async(agent.generate_answer(query, processed_results))
                # Run the agent's generate_answer method asynchronously
                
                # Display the answer
                st.subheader(f"Answer (Generated by {model_option})")
                # Display a subheading with the model name
                
                st.markdown(answer)
                # Display the generated answer with Markdown formatting
                
            except Exception as e:
                # If there's an error during search or answer generation
                st.error(f"Error during search or answer generation: {str(e)}")
                # Display an error message
                
                st.exception(e)
                # Display the full exception details
    else:
        # If the user hasn't entered a question
        st.warning("Please enter a question.")
        # Display a warning message

# Add information about the app in the sidebar
with st.sidebar:
    # Create a sidebar section
    
    # Display logo at the top of the sidebar if it exists
    logo_path = os.path.join("assets", "AIworkshopLogo.png")
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)
        st.image(logo, width=100)  # Adjust width as needed for proper display in the sidebar
        # The logo is placed at the top of the sidebar for better visibility and branding
    
    st.subheader("About")
    # Display a subheading
    
    st.write("""
    This application allows you to ask questions and get comprehensive answers 
    based on information stored in your Pinecone vector database.
    
    The app will:
    1. Convert your question to a vector embedding
    2. Find the most relevant information in the database
    3. Generate a comprehensive answer using your chosen AI model
    """)
    # Display information about the application
    
    st.subheader("Configuration")
    # Display a subheading
    
    st.write(f"**Index:** {pinecone_index_name}")
    # Display the Pinecone index name
    
    st.subheader("Available Models")
    # Display a subheading
    
    st.write("""
    - **GPT-4**: OpenAI's most advanced model, excellent for complex reasoning
    - **Claude**: Anthropic's Claude 3.5 Sonnet model, known for thoughtful and nuanced responses
    - **Deepseek**: Deepseek AI's powerful language model, offering another perspective
    """) 
    # Display information about the available models 