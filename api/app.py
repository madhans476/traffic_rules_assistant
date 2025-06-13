from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Query
from pydantic import BaseModel
from src.generator import Generator

app = FastAPI(
    title="Traffic Rules RAG API",
    description="A RAG-based assistant for Tamil Nadu traffic rules using Groq + FAISS",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

generator = Generator()

class QueryRequest(BaseModel):
    query: str
    top_k: int = 10

class QueryResponse(BaseModel):
    answer: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Tamil Nadu Traffic Rules RAG API!"}

@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    try:
        answer = generator.ask(request.query, top_k=request.top_k)
        return {"answer": answer}
    except Exception as e:
        return {"answer": f"Error: {str(e)}"}
