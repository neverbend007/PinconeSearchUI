import os
# Import the os module to interact with the operating system, including environment variables

from dotenv import load_dotenv
# Import load_dotenv to load environment variables from a .env file

from pinecone.grpc import PineconeGRPC as Pinecone  # Changed to explicitly use GRPC client
# Import the Pinecone GRPC client for vector database operations
# GRPC is a high-performance remote procedure call framework

# Load environment variables from .env file
load_dotenv()
# This loads API keys and other configuration from a .env file in the project directory

# Get Pinecone API key from environment variables
pinecone_api_key = os.getenv("PINECONE_API_KEY")
# Retrieve the Pinecone API key from the environment variables

# Print debug information about the API key
print(f"API Key first 5 chars: {pinecone_api_key[:5] if pinecone_api_key else 'None'}")
# Print the first 5 characters of the API key for verification without exposing the full key

print(f"API Key length: {len(pinecone_api_key) if pinecone_api_key else 'None'}")
# Print the length of the API key to verify it's not empty or truncated

# Test with direct initialization
print("\nTesting with GRPC client and direct API key initialization...")
# Print a message indicating the start of the first test method
try:
    # Try to initialize Pinecone with direct API key
    
    # Make sure we have the GRPC dependencies
    import grpc
    # Import the grpc package, which is required for the GRPC client
    
    import googleapis_common_protos
    # Import the googleapis_common_protos package, which is required for the GRPC client
    
    pc = Pinecone(api_key=pinecone_api_key)
    # Create a Pinecone client instance with the API key directly
    
    indexes = pc.list_indexes()
    # Get a list of all indexes in the Pinecone account
    
    print(f"Success! Found {len(indexes)} indexes:")
    # Print a success message with the number of indexes found
    
    for idx in indexes:
        # Loop through each index
        print(f"- {idx.name}")
        # Print the name of each index
        
except ImportError as e:
    # If there's an error importing the required packages
    print(f"Missing GRPC dependencies: {str(e)}")
    # Print an error message with the specific import error
    
    print("Please install with 'pip install pinecone-client[grpc]'")
    # Print a suggestion for how to install the missing dependencies
    
except Exception as e:
    # If there's any other error
    print(f"Error with direct initialization: {str(e)}")
    # Print an error message with the specific error

# Test with environment variable
print("\nTesting with GRPC client and environment variable...")
# Print a message indicating the start of the second test method
try:
    # Try to initialize Pinecone with environment variable
    
    os.environ["PINECONE_API_KEY"] = pinecone_api_key
    # Set the PINECONE_API_KEY environment variable directly
    
    pc = Pinecone()
    # Create a Pinecone client instance without explicitly providing the API key
    # The client will automatically use the environment variable
    
    indexes = pc.list_indexes()
    # Get a list of all indexes in the Pinecone account
    
    print(f"Success! Found {len(indexes)} indexes:")
    # Print a success message with the number of indexes found
    
    for idx in indexes:
        # Loop through each index
        print(f"- {idx.name}")
        # Print the name of each index
        
except Exception as e:
    # If there's any error
    print(f"Error with environment variable: {str(e)}")
    # Print an error message with the specific error

# Test with a hardcoded API key
print("\nTesting with GRPC client and hardcoded API key...")
# Print a message indicating the start of the third test method
try:
    # Try to initialize Pinecone with hardcoded API key
    
    # Replace 'your-api-key-here' with your actual API key for testing
    # Be sure to remove it afterward for security
    pc = Pinecone(api_key=pinecone_api_key)
    # Create a Pinecone client instance with the API key directly
    # Note: In this example, we're using the same API key as before, but in a real test
    # you might want to use a different key to verify that it works
    
    indexes = pc.list_indexes()
    # Get a list of all indexes in the Pinecone account
    
    print(f"Success! Found {len(indexes)} indexes:")
    # Print a success message with the number of indexes found
    
    for idx in indexes:
        # Loop through each index
        print(f"- {idx.name}")
        # Print the name of each index
        
except Exception as e:
    # If there's any error
    print(f"Error with hardcoded key: {str(e)}")
    # Print an error message with the specific error 