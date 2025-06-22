import os
import pkg_resources
import json
from openai import OpenAI
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
api_key = os.getenv("OPENROUTER_API_KEY")
def generate_metadata(text, api_key, model="x-ai/grok-3-mini-beta"):
    """Generate metadata using Grok-3-mini-beta via OpenRouter"""
    if not text.strip():
        return {"error": "No text extracted from document"}
    
    
    truncated_text = text[:5000] + "..." if len(text) > 5000 else text
    
    prompt = f"""
    You are a metadata generator. Given the following document content, generate:
    - Title
    - 3-sentence summary
    - 5 keywords
    - Topic category
    
    Return JSON format with these keys:
    {{
        "title": "...",
        "summary": "...",
        "keywords": ["...", "...", "..."],
        "topics": "...",
        "category": "...",
        "document_type": "report"  # optional
    }}
    
    Document Content:
    {truncated_text}
    """
    
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            timeout=30
        )
        
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct:free",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.2,
            max_tokens=500,
            extra_headers={
                "HTTP-Referer": "https://metadata-generator-app.com",
                "X-Title": "Automated Metadata Generator"
            }
        )
        
        content = response.choices[0].message.content
        metadata = json.loads(content)
        
        
        required_keys = ["title", "summary", "keywords", "topics", "category"]
        if not all(key in metadata for key in required_keys):
            missing = [k for k in required_keys if k not in metadata]
            return {"error": f"Missing keys: {', '.join(missing)}"}
            
        return metadata
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON error: {e}\nResponse: {content}")
        return {"error": "Invalid JSON response from API"}
    except Exception as e:
        logger.exception("API request failed")
        return {"error": f"API request failed: {str(e)}"}
