import hashlib
from groq import Groq
from time import sleep
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize Groq client with your API key
client = Groq(api_key="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")

# Function to hash sensitive data
def hash_data(data):
    """Generates a SHA-256 hash for anonymizing sensitive data."""
    return hashlib.sha256(data.encode()).hexdigest()

# Function to query Groq Llama model with fallback mechanism
def query_llama(messages, tech_stack=None, model="llama-3.3-70b-versatile", temperature=1, max_tokens=1024, top_p=1):
    """
    Send a query to the Groq Llama model with fallback support.
    """
    try:
        # Apply prompt engineering for generating technical questions
        if tech_stack:
            structured_prompt = (
                f"You are an expert technical interviewer specializing in {tech_stack}. "
                "Your task is to generate 3-5 challenging and relevant technical interview questions "
                "that evaluate both foundational knowledge and advanced concepts. "
                "Ensure the questions are clear, concise, and focus on practical problem-solving skills."
            )
            messages.append({"role": "user", "content": structured_prompt})

        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=False,
        )
        return completion.choices[0].message.content

    except AttributeError as e:
        logging.error(f"AttributeError: {e}")
        return [
            "Describe the differences between synchronous and asynchronous programming.",
            "Explain the concept of polymorphism in object-oriented programming.",
            "What are the primary benefits of using Docker containers?",
        ]
    except Exception as e:
        logging.error(f"Unexpected Error: {e}")
        return [
            "What are the advantages of RESTful APIs over SOAP?",
            "Explain the CAP theorem in distributed systems.",
            "How does garbage collection work in Java?",
        ]

# Asynchronous query function (optional for scalability)
async def query_llama_async(messages, tech_stack=None, model="llama-3.3-70b-versatile", temperature=1, max_tokens=1024, top_p=1):
    """
    Async version of querying the Groq Llama model with fallback support.
    """
    try:
        if tech_stack:
            structured_prompt = (
                f"You are an expert technical interviewer specializing in {tech_stack}. "
                "Your task is to generate 3-5 challenging and relevant technical interview questions "
                "that evaluate both foundational knowledge and advanced concepts. "
                "Ensure the questions are clear, concise, and focus on practical problem-solving skills."
            )
            messages.append({"role": "user", "content": structured_prompt})

        completion = await client.chat.completions.create_async(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=False,
        )
        return completion.choices[0].message.content

    except AttributeError as e:
        logging.error(f"AttributeError: {e}")
        return [
            "Describe the differences between synchronous and asynchronous programming.",
            "Explain the concept of polymorphism in object-oriented programming.",
            "What are the primary benefits of using Docker containers?",
        ]
    except Exception as e:
        logging.error(f"Unexpected Error: {e}")
        return [
            "What are the advantages of RESTful APIs over SOAP?",
            "Explain the CAP theorem in distributed systems.",
            "How does garbage collection work in Java?",
        ]

# Progress simulation for better UX
def simulate_progress(duration=0.5):
    """Simulates delay to improve user experience."""
    sleep(duration)
