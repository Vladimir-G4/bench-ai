import re
import logging
from typing import Dict, List, Union

# Configure logging for demo debugging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Predefined responses for QA test cases (based on qa_tests.yaml)
QA_RESPONSES: Dict[str, str] = {
    "What is the capital of France?": "Paris",
    "Who wrote the novel '1984'?": "George Orwell",
    "What is the primary source of energy for Earth's climate system?": "The Sun",
    "If a train leaves Station A at 9 AM traveling at 60 mph and another train leaves Station B at 10 AM traveling at 80 mph in the opposite direction, when will they meet if the stations are 200 miles apart?": "11 AM",
    "Why did the Roman Empire decline? Provide a concise explanation.": "The Roman Empire declined due to economic instability, political corruption, barbarian invasions, and overexpansion.",
    "What is the smell of rain like?": "The smell of rain is fresh, earthy, and musky, caused by petrichor from wet soil.",
    "In the context of graph theory, what is a Hamiltonian cycle?": "A Hamiltonian cycle is a cycle in a graph that visits each vertex exactly once and returns to the starting vertex.",
    "What is the capital of the country with the largest population?": "Beijing",
    "Who is the current CEO of Tesla as of June 2025?": "Elon Musk",
    "If you were a chef, how would you improve a classic Margherita pizza?": "I’d use heirloom tomatoes, add burrata, and finish with fresh basil and olive oil.",
    "What is the smell of rain like in the Sahara Desert?": "In the Sahara, rain smells dusty and earthy due to petrichor from dry sand.",
    "Is the Earth flat?": "No, the Earth is an oblate spheroid, as shown by satellite imagery and GPS.",
    "What is the capital of Florida, Italy?": "There is no Florida in Italy; perhaps you meant Florence, the capital of Tuscany?",
    "¿Cuál es la capital de España?": "Madrid",
    "What caused the 2008 financial crisis?": "The 2008 financial crisis was caused by a housing bubble, subprime mortgages, and risky derivatives.",
    "What is the smell of rain like on Mars?": "Mars has no rain, so there’s no petrichor-like smell; only dust or CO2 ice.",
    "Who won the Nobel Peace Prize in 2024?": "Nihon Hidankyo, for their work against nuclear weapons.",
    "If all roses are flowers, and some flowers are red, are all roses red?": "No, not all roses are red; roses can be other colors like white or yellow.",
    "What is the primary ingredient in traditional Japanese miso soup?": "Miso paste",
    "What would happen if the Moon disappeared tomorrow?": "Tides would weaken, nights would be darker, and Earth’s axial tilt might destabilize."
}

def summarize_text(prompt: str, max_sentences: int = 2, max_words: int = 50) -> str:
    """
    Summarize input text by extracting the first few sentences or truncating to a word limit.
    Handles summarization prompts from summarization_tests.yaml.
    
    Args:
        prompt: Input text containing the text to summarize.
        max_sentences: Maximum number of sentences in the summary.
        max_words: Maximum number of words in the summary.
    
    Returns:
        Summarized text as a string.
    """
    # Extract the text to summarize (remove instruction prefix)
    text_match = re.search(r"Summarize.*?:\s*(.+)", prompt, re.DOTALL)
    if not text_match:
        return "Unable to extract text for summarization."
    
    text = text_match.group(1).strip()
    
    # Split into sentences
    sentences = re.split(r"(?<=[.!?])\s+", text)
    summary_sentences = sentences[:min(max_sentences, len(sentences))]
    
    # Join sentences and truncate to word limit
    summary = " ".join(summary_sentences)
    words = summary.split()
    if len(words) > max_words:
        summary = " ".join(words[:max_words]) + "..."
    
    return summary

def model(prompt: str) -> str:
    """
    Dummy model for benchAI demos, simulating LLM responses for QA and summarization tasks.
    
    Args:
        prompt: Input prompt as a string (e.g., question or summarization task).
    
    Returns:
        Response as a string, either a direct answer or a summarized text.
    
    Raises:
        ValueError: If the prompt is empty or invalid.
    """
    if not prompt or not isinstance(prompt, str):
        logger.error("Invalid prompt received: %s", prompt)
        raise ValueError("Prompt must be a non-empty string.")
    
    logger.info("Processing prompt: %s", prompt[:60] + "..." if len(prompt) > 60 else prompt)
    
    # Normalize prompt for lookup (strip whitespace, lowercase for flexibility)
    prompt_normalized = prompt.strip()
    
    # Check for QA prompts
    if prompt_normalized in QA_RESPONSES:
        response = QA_RESPONSES[prompt_normalized]
        logger.info("Returning QA response: %s", response[:60] + "..." if len(response) > 60 else response)
        return response
    
    # Check for summarization prompts
    if prompt_normalized.startswith("Summarize"):
        # Extract word or sentence limits from prompt, if specified
        max_words = 50
        max_sentences = 2
        word_limit_match = re.search(r"(\d+)\s*words\s*or\s*less", prompt_normalized)
        sentence_limit_match = re.search(r"(\d+)\s*sentences", prompt_normalized)
        
        if word_limit_match:
            max_words = int(word_limit_match.group(1))
        if sentence_limit_match:
            max_sentences = int(sentence_limit_match.group(1))
        
        response = summarize_text(prompt_normalized, max_sentences, max_words)
        logger.info("Returning summarization response: %s", response[:60] + "..." if len(response) > 60 else response)
        return response
    
    # Fallback for unrecognized prompts
    fallback_response = "This is a dummy response for an unrecognized prompt."
    logger.warning("Unrecognized prompt, returning fallback: %s", fallback_response)
    return fallback_response