import streamlit as st
import ollama
from langchain.llms import Ollama
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from pymongo import MongoClient
import os
import datetime

# Configuration constants
MONGO_URI = os.environ.get("MONGO_URI") or "mongodb://localhost:27017/"
DATABASE_NAME = "chat_history"
COLLECTION_NAME = "conversations"
OLLAMA_MODEL = "qwen2.5"  # Fixed model name format

def get_database():
    client = MongoClient(MONGO_URI)
    return client[DATABASE_NAME]

def get_collection():
    db = get_database()
    return db[COLLECTION_NAME]

def store_conversation(query, response):
    collection = get_collection()
    try:
        # Generate embeddings
        query_embedding = ollama.embeddings(
            model="mxbai-embed-large", 
            prompt=query
        )["embedding"]
        
        response_embedding = ollama.embeddings(
            model="mxbai-embed-large", 
            prompt=response
        )["embedding"]

        conversation_data = {
            "query": query,
            "response": response,
            "query_embedding": query_embedding,
            "response_embedding": response_embedding,
            "timestamp": st.session_state.conversation_start_time
        }
        collection.insert_one(conversation_data)
    except Exception as e:
        st.error(f"Error storing conversation: {str(e)}")

def load_conversation_history():
    collection = get_collection()
    history = []
    try:
        cursor = collection.find()
        for doc in cursor:
            history.append((doc["query"], doc["response"]))
    except Exception as e:
        st.error(f"Error loading conversation history: {str(e)}")
    return history

def initialize_session_state():
    if "conversation_start_time" not in st.session_state:
        st.session_state.conversation_start_time = datetime.datetime.now()
    
    if "conversation" not in st.session_state:
        llm = Ollama(base_url="http://localhost:11434", model=OLLAMA_MODEL)
        st.session_state.conversation = ConversationChain(
            llm=llm,
            memory=ConversationBufferMemory()
        )
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

def main():
    st.title("Local LLM Chat with MongoDB History")
    
    # Initialize session state
    initialize_session_state()
    
    # Load conversation history only once when messages are empty
    if not st.session_state.messages:
        history = load_conversation_history()
        for query, response in history:
            st.session_state.messages.extend([
                {"role": "user", "content": query},
                {"role": "assistant", "content": response}
            ])
    
    # Display message history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Handle new user input
    if prompt := st.chat_input("Your message"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.conversation.predict(input=prompt)
                    st.markdown(response)
                    store_conversation(prompt, response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Error generating response: {str(e)}")

if __name__ == "__main__":
    main()