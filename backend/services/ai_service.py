import logging
import os
from typing import Optional, Dict, List
import google.generativeai as genai

logger = logging.getLogger(__name__)


class AIService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not configured")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-pro")
        self.sessions = {}  # {session_id: {"chat": chat_obj, "history": []}}
    
    def _get_or_create_session(self, session_id: str):
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "chat": self.model.start_chat(history=[]),
                "history": []
            }
        return self.sessions[session_id]
    
    async def chat(self, message: str, session_id: str) -> str:
        try:
            logger.info(f"💬 Chat from {session_id[:8]}...")
            
            session = self._get_or_create_session(session_id)
            chat_obj = session["chat"]
            history = session["history"]
            
            system_context = """You are SPARK, AI assistant for MHCV (Medium & Heavy Commercial Vehicles) industry.

Expertise:
- European MHCV regulations (Euro 6, Euro 7, emissions)
- Alternative fuels (electric, hydrogen, biofuels)
- Supply chain & manufacturing
- Global automotive trends
- Environmental regulations

Provide accurate, detailed responses. Reference specific details from articles.
Be professional but conversational.
            """
            
            full_message = f"{system_context}\n\nUser: {message}"
            
            response = chat_obj.send_message(full_message)
            response_text = response.text
            
            # Store in history
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": response_text})
            
            logger.info("✅ Response generated")
            return response_text
        
        except Exception as e:
            logger.error(f"❌ Chat error: {str(e)}")
            raise
    
    def get_session_history(self, session_id: str) -> List[Dict]:
        session = self._get_or_create_session(session_id)
        return session["history"]
