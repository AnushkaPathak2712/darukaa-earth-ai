from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
from reasoning.conversation import ConversationManager
from reasoning.recommender import generate_recommendations
import os

# --- Configuration ---
# Set this to True only if you upgrade your Render plan to a higher memory tier
ENABLE_RAG = False 

app = FastAPI(title="Darukaa Earth AI")

# --- CORS Middleware ---
# This is crucial for allowing your Streamlit frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for this demo; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conversations: Dict[str, ConversationManager] = {}

class QueryRequest(BaseModel):
    user_id: str
    message: str
    structured_data: Optional[Dict[str, Any]] = None

@app.post("/chat")
async def chat(request: QueryRequest):
    if request.user_id not in conversations:
        conversations[request.user_id] = ConversationManager()
    
    cm = conversations[request.user_id]
    cm.add_message("user", request.message)
    
    if request.structured_data:
        cm.update_slots(request.structured_data)
    
    missing = cm.get_missing_slots()
    if missing:
        question = f"I can help with that. To give you a scientific recommendation, I need a bit more data. Can you provide: {', '.join(missing)}?"
        cm.add_message("assistant", question)
        return {"response": question, "type": "clarification", "missing_slots": missing}
    
    recs = generate_recommendations(cm.slots)
    
    # --- Lazy RAG Retrieval ---
    docs = []
    if ENABLE_RAG:
        try:
            from rag.retriever import retrieve  # Lazy import to save memory
            rec_names = " ".join([r['recommendation'] for r in recs]) if recs else ""
            search_query = f"{request.message} {rec_names}".strip()
            docs = retrieve(search_query)
        except Exception as e:
            print(f"RAG retrieval skipped: {e}")
    
    response_text = "Based on your environmental data, here are my recommendations:\n\n"
    if not recs:
        response_text += "No specific recommendations triggered based on the current data. Try adjusting the values in the sidebar."
    
    for rec in recs:
        response_text += f"**{rec['recommendation']}**\n"
        response_text += f"- *Why:* {rec['why']}\n"
        response_text += f"- *Metrics improved:* {', '.join(rec['metrics_improved'])}\n"
        response_text += f"- *Time horizon:* {rec['time_horizon']}\n"
        response_text += f"- *Confidence:* {rec['confidence']}\n"
        if rec.get('evidence'):
            response_text += "- *Evidence:*\n"
            for ev in rec['evidence']:
                response_text += f"  - {ev['source']} ({ev['year']}) - [Link]({ev['url']})\n"
        response_text += "\n"
    
    if docs:
        response_text += "---\n**📚 Knowledge Retrieved from Vector DB (RAG):**\n"
        for i, d in enumerate(docs[:1]):
            snippet = d['content'][:250].replace('\n', ' ') 
            response_text += f"{i+1}. *{snippet}...*\n"
    
    cm.add_message("assistant", response_text)
    return {"response": response_text, "recommendations": recs, "retrieved_docs_count": len(docs)}