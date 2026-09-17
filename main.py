from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict, Any
from reasoning.conversation import ConversationManager
from reasoning.recommender import generate_recommendations
from rag.retriever import retrieve

app = FastAPI(title="Darukaa Earth AI")

# In-memory conversation store for handling multi-turn memory
conversations: Dict[str, ConversationManager] = {}

class QueryRequest(BaseModel):
    user_id: str
    message: str
    structured_data: Optional[Dict[str, Any]] = None

@app.post("/chat")
async def chat(request: QueryRequest):
    # 1. Initialize or retrieve conversation memory for this user
    if request.user_id not in conversations:
        conversations[request.user_id] = ConversationManager()
    
    cm = conversations[request.user_id]
    cm.add_message("user", request.message)
    
    # 2. Update conversation slots with any structured data provided
    if request.structured_data:
        cm.update_slots(request.structured_data)
    
    # 3. Check for missing data and ask clarifying questions
    missing = cm.get_missing_slots()
    if missing:
        question = f"I can help with that. To give you a scientific recommendation, I need a bit more data. Can you provide: {', '.join(missing)}?"
        cm.add_message("assistant", question)
        return {"response": question, "type": "clarification", "missing_slots": missing}
    
    # 4. Generate multi-metric recommendations based on the filled slots
    recs = generate_recommendations(cm.slots)
    
    # 5. RETRIEVAL TWEAK: Combine user prompt + recommendation names for a better RAG query
    rec_names = " ".join([r['recommendation'] for r in recs]) if recs else ""
    search_query = f"{request.message} {rec_names}".strip()
    docs = retrieve(search_query)
    
    # 6. Format the response with evidence and RAG sources
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
    
    # 7. Show exactly what was retrieved from the RAG vector database
    if docs:
        response_text += "---\n**📚 Knowledge Retrieved from Vector DB (RAG):**\n"
        for i, d in enumerate(docs[:1]): # Show top 1 retrieved chunk for cleanliness
            # Clean up newlines for better display in the chat UI
            snippet = d['content'][:250].replace('\n', ' ') 
            response_text += f"{i+1}. *{snippet}...*\n"
    
    # 8. Save the assistant's response to memory and return
    cm.add_message("assistant", response_text)
    return {"response": response_text, "recommendations": recs, "retrieved_docs_count": len(docs)}