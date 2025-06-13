# src/generator.py

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from langchain.schema import HumanMessage, SystemMessage
from .retriever import Retriever

# 🔐 Load environment variables from .env file
load_dotenv()

class Generator:
    def __init__(self, model_name: str = "llama-3.1-8b-instant"):
        """
        Initializes the Groq-based LLM and the retriever.
        """
        # 🧠 Load your Retriever
        BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        self.retriever = Retriever(
            index_path=os.path.join(BASE_DIR, "data", "processed", "faiss_cosine_index.idx"),
            chunk_json_path=os.path.join(BASE_DIR, "data", "processed", "TN_traffic_rules_chunks.json")
        )


        # 🤖 Initialize Groq LLM via LangChain
        self.llm = ChatGroq(
            model_name=model_name,
            temperature=0.3,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

    def ask(self, query: str, top_k: int = 10) -> str:
        """
        Uses retriever to find context and Groq to generate an answer.
        """
        # 📄 Step 1: Retrieve top-k relevant chunks
        relevant_chunks = self.retriever.query(query, top_k)

        # print("Relevant Chunks: ")
        # print("\nTop Matching Chunks:\n")
        # for i, chunk in enumerate(relevant_chunks, 1):
        #     print(f"[Chunk {chunk['chunk_id']}]\n{chunk['text']}\n{'-'*60}")
        # print("\n \n")
        
        context = "\n\n".join([chunk["text"] for chunk in relevant_chunks])

        # 🧾 Step 2: Create prompt using System + Human messages
        messages = [
            SystemMessage(
                content=(
                    # 🛠️ Instruction
                    "You are a traffic law assistant trained on Tamil Nadu traffic rules and regulations. "
                    "Your task is to answer user questions by using only the information provided in the context. "
                    "Do not generate answers based on external knowledge or assumptions.\n\n"

                    # ❌ Out-of-Context Control
                    "If the context does not contain enough information to answer the question accurately, "
                    "politely inform the user that the answer is not available and suggest they rephrase or ask something else. "
                    "Do not mention 'context provided' or similar phrases in the answer. Do not speculate.\n\n"

                    # ✍️ Output Constraints
                    "Give clear, factual, and concise answers. If applicable, include:\n"
                    "- Specific penalties, fines (₹), or legal terms\n"
                    "- Rule numbers or sections (if present)\n"
                    "- Safety instructions or procedures\n\n"

                    # 🎭 Role/Persona
                    "You are a helpful, neutral, and official-sounding assistant for citizens, law enforcers, and learners.\n\n"

                    # 🎨 Style & Tone
                    "Use professional, polite, and understandable language. Avoid unnecessary repetition or disclaimers.\n\n"

                    # 🎯 Goal
                    "Help users understand their rights, duties, and consequences as per Tamil Nadu road traffic laws, using only the source material."
                )
            ),
            HumanMessage(
                content=f"Context:\n{context}\n\nQuestion: {query}"
            )
        ]

        # 🧠 Step 3: Generate and return answer from Groq LLM
        response = self.llm(messages)
        return response.content

# 🧪 Test runner
if __name__ == "__main__":
    generator = Generator()
    query = "What are the rules for overtaking?"
    answer = generator.ask(query)
    print("\nAnswer:\n")
    print(answer)
