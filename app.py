from flask import Flask, request, jsonify
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnableLambda
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

try:
    loader = PyPDFLoader("C:/Users/Santhuru/OneDrive/Desktop/chatbot/Technology_Trends_Outlook_2024_1721230978 (2).pdf")
 
    docs = loader.load()
    vectorstore = Chroma.from_documents(docs, OllamaEmbeddings())
except Exception as e:
    print("Error loading PDF or initializing vector store:", e)
    exit(1)  
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

@app.route('/chat/', methods=['POST'])
def chat():
    question = request.json.get('question')

    retriever = RunnableLambda(vectorstore.similarity_search).bind(k=7)
    llm = ChatOllama(model="llama 3.2:3b")

    context = retriever.invoke(question)
    message = f"""
    Answer this question using the provided context only.

    {question}

    Context:
    {context}
    """

    prompt = ChatPromptTemplate.from_messages([{"role": "user", "content": message}])
    response = llm.invoke(prompt)

    return jsonify({'answer': response.content})

if __name__ == '__main__':
    app.run(port=5000, debug=True)  # Enable debug mode for detailed error output
