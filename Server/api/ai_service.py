import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_KEY")

# Initialize OpenAI client
client = AsyncOpenAI(api_key=OPENAI_KEY) if OPENAI_KEY else None


async def chat_completion(messages: list, model: str = "gpt-4o-mini", temperature: float = 0.7):
    """
    Send a chat completion request to OpenAI.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content'
        model: Model to use (default: gpt-4o-mini)
        temperature: Sampling temperature (default: 0.7)
    
    Returns:
        Response from OpenAI API
    """
    if not client:
        raise ValueError("OPENAI_KEY not found in environment variables")
    
    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    
    return response


async def simple_chat(user_message: str, system_prompt: str = None, model: str = "gpt-4o-mini") -> str:
    """
    Simple chat function that takes a user message and optional system prompt.
    
    Args:
        user_message: The user's message
        system_prompt: Optional system prompt to set context
        model: Model to use (default: gpt-4o-mini)
    
    Returns:
        The assistant's response text
    """
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_message})
    
    response = await chat_completion(messages, model=model)
    return response.choices[0].message.content


async def generate_text(prompt: str, model: str = "gpt-4o-mini", temperature: float = 0.7) -> str:
    """
    Generate text from a prompt.
    
    Args:
        prompt: The text prompt
        model: Model to use (default: gpt-4o-mini)
        temperature: Sampling temperature (default: 0.7)
    
    Returns:
        Generated text
    """
    messages = [{"role": "user", "content": prompt}]
    response = await chat_completion(messages, model=model, temperature=temperature)
    return response.choices[0].message.content

