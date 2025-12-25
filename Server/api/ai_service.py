import os
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
from openai import AsyncOpenAI

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_KEY")

# Initialize OpenAI client
client = None
if OPENAI_API_KEY:
    client = AsyncOpenAI(api_key=OPENAI_API_KEY)


async def chat_completion(
    messages: List[Dict[str, str]],
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.7,
    max_tokens: Optional[int] = None
) -> Optional[str]:
    """
    Send a chat completion request to OpenAI.
    
    Args:
        messages: List of message dictionaries with "role" and "content" keys
                 Example: [{"role": "user", "content": "Hello!"}]
        model: OpenAI model to use (default: "gpt-3.5-turbo")
        temperature: Sampling temperature (0.0 to 2.0, default: 0.7)
        max_tokens: Maximum tokens in response (optional)
    
    Returns:
        Response content string or None if error
    """
    if not client:
        raise ValueError("OPENAI_KEY not found in environment variables")
    
    try:
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        if response.choices and len(response.choices) > 0:
            return response.choices[0].message.content
        return None
        
    except Exception as e:
        raise ValueError(f"OpenAI API error: {str(e)}")


async def simple_chat(
    user_message: str,
    system_message: Optional[str] = None,
    model: str = "gpt-3.5-turbo"
) -> str:
    """
    Simple chat function for single user messages.
    
    Args:
        user_message: The user's message
        system_message: Optional system message to set context
        model: OpenAI model to use
    
    Returns:
        AI response string
    """
    messages = []
    
    if system_message:
        messages.append({
            "role": "system",
            "content": system_message
        })
    
    messages.append({
        "role": "user",
        "content": user_message
    })
    
    response = await chat_completion(messages, model=model)
    
    if not response:
        raise ValueError("No response from OpenAI")
    
    return response


async def generate_text(
    prompt: str,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.7
) -> str:
    """
    Generate text from a simple prompt.
    
    Args:
        prompt: The text prompt
        model: OpenAI model to use
        temperature: Sampling temperature
    
    Returns:
        Generated text
    """
    return await simple_chat(prompt, model=model, temperature=temperature)

