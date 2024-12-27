# Local LLM Chat with MongoDB History

A Streamlit-based chat application that integrates with Ollama for local LLM interactions and MongoDB for conversation history storage. The application supports persistent chat history, conversation embeddings, and real-time interactions with local language models.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Onanore/local-llm-chat
cd local-llm-chat
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up required services:
   - Install and start MongoDB locally or use a cloud instance
   - Install and configure Ollama with the required models:
     ```bash
     curl https://ollama.ai/install.sh | sh
     ollama pull qwen2.5
     ollama pull mxbai-embed-large
     ```

4. Configure environment variables:
```bash
export MONGO_URI="mongodb://localhost:27017/"  # Or your MongoDB connection string
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run src/main.py
```

2. Access the application through your web browser at `http://localhost:8501`

3. Begin chatting with the LLM. Your conversations will be automatically stored in MongoDB with embeddings for future reference.

## Project Structure

```
local-llm-chat/
├── README.md
├── LICENSE
├── requirements.txt
└── src/
    ├── __init__.py
    └── main.py
```

## Examples

1. Basic conversation:
```python
# In your web browser
User: "What is the capital of France?"
Assistant: "The capital of France is Paris."
```

2. Accessing conversation history:
```python
from src.database.mongodb import load_conversation_history
history = load_conversation_history()
for query, response in history:
    print(f"Q: {query}\nA: {response}\n")
```

3. Using custom embeddings:
```python
from src.utils.embeddings import get_embeddings
query = "Your text here"
embeddings = get_embeddings(query, model="mxbai-embed-large")
```
