import os
import streamlit as st
import asyncio
import json
from dotenv import load_dotenv
from pinecone import Pinecone
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
import anthropic
import requests

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(page_title="Pinecone Query Agent", page_icon="🔍", layout="wide")
st.title("Pinecone Query Agent")

# Initialize OpenAI client
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("OpenAI API key not found. Please add it to your .env file.")
    st.stop()

# Initialize Anthropic client
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
if not anthropic_api_key:
    st.error("Anthropic API key not found. Please add it to your .env file.")
    st.stop()
anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)

# Initialize Deepseek API key
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
if not deepseek_api_key:
    st.error("Deepseek API key not found. Please add it to your .env file.")
    st.stop()

# Initialize Pinecone
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")

if not all([pinecone_api_key, pinecone_index_name]):
    st.error("Pinecone configuration not found. Please add it to your .env file.")
    st.stop()

# Initialize session state for Pinecone connection
if 'pinecone_initialized' not in st.session_state:
    st.session_state.pinecone_initialized = False
    st.session_state.connection_message_shown = False

# Initialize clients only once
if not st.session_state.pinecone_initialized:
    try:
        pc = Pinecone(api_key=pinecone_api_key)
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        
        # Check if index exists
        available_indexes = [index.name for index in pc.list_indexes()]
        
        if pinecone_index_name not in available_indexes:
            st.error(f"Index '{pinecone_index_name}' not found in your Pinecone account.")
            st.write(f"Available indexes: {', '.join(available_indexes) if available_indexes else 'None'}")
            st.stop()
        
        # Connect to the index
        index = pc.Index(pinecone_index_name)
        
        # Create vector store
        vectorstore = PineconeVectorStore(index=index, embedding=embeddings)
        
        # Store in session state
        st.session_state.pc = pc
        st.session_state.embeddings = embeddings
        st.session_state.index = index
        st.session_state.vectorstore = vectorstore
        st.session_state.pinecone_initialized = True
        
        # Show success message
        st.success("Successfully connected to Pinecone!")
        st.session_state.connection_message_shown = True
    except Exception as e:
        st.error(f"Error connecting to Pinecone: {str(e)}")
        st.stop()
else:
    # Get from session state
    pc = st.session_state.pc
    embeddings = st.session_state.embeddings
    index = st.session_state.index
    vectorstore = st.session_state.vectorstore
    
    # Show success message only once
    if not st.session_state.connection_message_shown:
        st.success("Successfully connected to Pinecone!")
        st.session_state.connection_message_shown = True

# Initialize OpenAI client for generating answers
openai_client = OpenAI(api_key=openai_api_key)

# Helper function to run async functions in Streamlit
def run_async(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

# Function to generate a comprehensive answer from retrieved results using OpenAI
async def generate_answer_openai(query, results):
    # Format the context from the results
    context = ""
    for i, result in enumerate(results):
        context += f"Document {i+1}:\n"
        if "title" in result:
            context += f"Title: {result.get('title', 'Untitled')}\n"
        if "description" in result:
            context += f"Description: {result.get('description', '')}\n"
        if "text" in result:
            context += f"Content: {result.get('text', '')}\n"
        context += f"Relevance Score: {result.get('score', 0):.4f}\n\n"
    
    # Generate a comprehensive answer using OpenAI
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides comprehensive answers based on the retrieved information. Cite your sources when appropriate."},
                {"role": "user", "content": f"Based on the following information, please provide a comprehensive answer to this question: '{query}'\n\nRetrieved Information:\n{context}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating answer with OpenAI: {e}")
        return "I couldn't generate an answer based on the retrieved information."

# Function to generate a comprehensive answer from retrieved results using Claude
async def generate_answer_claude(query, results):
    # Format the context from the results
    context = ""
    for i, result in enumerate(results):
        context += f"Document {i+1}:\n"
        if "title" in result:
            context += f"Title: {result.get('title', 'Untitled')}\n"
        if "description" in result:
            context += f"Description: {result.get('description', '')}\n"
        if "text" in result:
            context += f"Content: {result.get('text', '')}\n"
        context += f"Relevance Score: {result.get('score', 0):.4f}\n\n"
    
    # Generate a comprehensive answer using Claude
    try:
        response = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1000,
            system="You are a helpful assistant that provides comprehensive answers based on the retrieved information. Cite your sources when appropriate.",
            messages=[
                {"role": "user", "content": f"Based on the following information, please provide a comprehensive answer to this question: '{query}'\n\nRetrieved Information:\n{context}"}
            ]
        )
        return response.content[0].text
    except Exception as e:
        print(f"Error generating answer with Claude: {e}")
        return "I couldn't generate an answer based on the retrieved information."

# Function to generate a comprehensive answer from retrieved results using Deepseek
async def generate_answer_deepseek(query, results):
    # Format the context from the results
    context = ""
    for i, result in enumerate(results):
        context += f"Document {i+1}:\n"
        if "title" in result:
            context += f"Title: {result.get('title', 'Untitled')}\n"
        if "description" in result:
            context += f"Description: {result.get('description', '')}\n"
        if "text" in result:
            context += f"Content: {result.get('text', '')}\n"
        context += f"Relevance Score: {result.get('score', 0):.4f}\n\n"
    
    # Generate a comprehensive answer using Deepseek API
    try:
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {deepseek_api_key}"
        }
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that provides comprehensive answers based on the retrieved information. Cite your sources when appropriate."},
                {"role": "user", "content": f"Based on the following information, please provide a comprehensive answer to this question: '{query}'\n\nRetrieved Information:\n{context}"}
            ],
            "max_tokens": 1000
        }
        
        response = requests.post(url, headers=headers, json=data)
        response_json = response.json()
        
        if "choices" in response_json and len(response_json["choices"]) > 0:
            return response_json["choices"][0]["message"]["content"]
        else:
            print(f"Unexpected response format from Deepseek: {response_json}")
            return "I couldn't generate an answer based on the retrieved information."
    except Exception as e:
        print(f"Error generating answer with Deepseek: {e}")
        return "I couldn't generate an answer based on the retrieved information."

# Query interface
st.subheader("Ask a question")

# Model selection
model_option = st.radio(
    "Choose the AI model to answer your question:",
    ["GPT-4", "Claude", "Deepseek"],
    horizontal=True
)

query = st.text_input("Enter your question:")

if st.button("Get Answer"):
    if query:
        with st.spinner("Searching and generating answer..."):
            try:
                # Generate embedding for the query
                query_embedding = embeddings.embed_query(query)
                
                # Query Pinecone - fixed to retrieve top 5 results
                results = index.query(
                    vector=query_embedding,
                    top_k=5,
                    include_metadata=True
                )
                
                if not results.matches:
                    st.info("No relevant information found to answer your question.")
                else:
                    # Convert Pinecone results to a format our agent can process
                    processed_results = []
                    for match in results.matches:
                        result_dict = {
                            "score": match.score,
                            **match.metadata
                        }
                        processed_results.append(result_dict)
                    
                    # Generate comprehensive answer based on selected model
                    if model_option == "GPT-4":
                        answer = run_async(generate_answer_openai(query, processed_results))
                        model_used = "GPT-4"
                    elif model_option == "Claude":
                        answer = run_async(generate_answer_claude(query, processed_results))
                        model_used = "Claude 3.5 Sonnet"
                    else:  # Deepseek
                        answer = run_async(generate_answer_deepseek(query, processed_results))
                        model_used = "Deepseek"
                    
                    # Display the answer
                    st.subheader(f"Answer (Generated by {model_used})")
                    st.markdown(answer)
                    
                    # Option to view sources
                    with st.expander("View Sources"):
                        for i, result in enumerate(processed_results):
                            st.markdown(f"**Source {i+1}:** {result.get('title', 'Untitled')} (Score: {result.get('score', 0):.4f})")
                            if result.get('url'):
                                st.markdown(f"[Link to source]({result.get('url')})")
                            st.markdown("---")
            except Exception as e:
                st.error(f"Error during search: {str(e)}")
                st.exception(e)
    else:
        st.warning("Please enter a question.")

# Add some information about the app
with st.sidebar:
    st.subheader("About")
    st.write("""
    This application allows you to ask questions and get comprehensive answers 
    based on information stored in your Pinecone vector database.
    
    The app will:
    1. Convert your question to a vector embedding
    2. Find the most relevant information in the database
    3. Generate a comprehensive answer using your chosen AI model
    """)
    
    st.subheader("Configuration")
    st.write(f"**Index:** {pinecone_index_name}")
    
    st.subheader("Available Models")
    st.write("""
    - **GPT-4**: OpenAI's most advanced model, excellent for complex reasoning
    - **Claude**: Anthropic's Claude 3.5 Sonnet model, known for thoughtful and nuanced responses
    - **Deepseek**: Deepseek AI's powerful language model, offering another perspective
    """) 