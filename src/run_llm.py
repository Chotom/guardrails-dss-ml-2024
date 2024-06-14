"""Module with generation methods for the Garak benchmark.

Methods to use in the garak benchmark must be in foo(input_prompt: str, generations: int) -> list[str] format.

Available generators:
- gpt2: Generate text using the GPT2 model.
- llama3: Generate text using the Llama3 model.
- nemo_llama3: Generate text using the Llama3 model with nemo guardrails.
- guardrailsai_llama3: Generate text using the Llama3 model with guardrails-ai.
- repeat: Repeat the input prompt for debugging purposes.
"""

from langchain_community.llms.ollama import Ollama
from nemoguardrails import LLMRails, RailsConfig
from transformers import pipeline

from src.guardrailsai.guardrails_config import guard
from src.utils.logger import create_logger

# INIT GENERATORS ##############################################################
log = create_logger(__name__)
log.debug("Initializing instances.")
huggingface_gpt2_generator = pipeline("text-generation", model="gpt2", do_sample=True)
"""Huggingface pipeline for GPT2 model."""

langchain_ollama_llama3 = Ollama(model="llama3")
"""Langchain Ollama instance for the Llama3 model."""

nemo_config = RailsConfig.from_path("./src/nemo_guardrails/config")
nemo_langchain_llama3 = LLMRails(nemo_config, llm=langchain_ollama_llama3)
"""Nemo Guardrails instance for the Llama3 model with usage of langchain model."""

log.debug("Instances initialized.")


# INIT GENERATORS ##############################################################
def guardrailsai_llama3(input_prompt: str, generations: int) -> list[str]:
    """Generate text using the Llama3 model with guardrails-ai.

    Args:
        input_prompt (str): The initial text to start the generation from.
        generations (int): The number of text sequences to generate.

    Returns:
        list[str]: A list of generated text sequences.
    """
    if generations > 1:
        log.warning("Llama3 in Ollama supports 1 generation at a time. Using more will increase the response time.")

    responses = [_generate_response_for_guardrailsai_llama3(input_prompt) for _ in range(generations)]

    return responses


def _generate_response_for_guardrailsai_llama3(input_prompt: str) -> str:
    try:
        validated_input = guard.validate(input_prompt)
    except Exception:
        return "Sorry, I cannot help with that. The input prompt violates our policy."

    response = langchain_ollama_llama3.invoke(validated_input.validated_output)

    try:
        validated_output = guard.validate(response)
    except Exception:
        return "Sorry, I cannot help with that. Can I help you with something else?"

    return validated_output.validated_output


def nemo_llama3(input_prompt: str, generations: int) -> list[str]:
    """Generate text using the Llama3 model with nemo guardrails.

    Args:
        input_prompt (str): The initial text to start the generation from.
        generations (int): The number of text sequences to generate.

    Returns:
        list[str]: A list of generated text sequences.
    """
    if generations > 1:
        log.warning("Llama3 in Ollama supports 1 generation at a time. Using more will increase the response time.")

    responses = [_generate_response_for_nemo_llama3(input_prompt) for _ in range(generations)]

    return responses


def _generate_response_for_nemo_llama3(input_prompt: str) -> str:
    response = nemo_langchain_llama3.generate(messages=[{"role": "user", "content": input_prompt}])

    return response["content"]


def llama3(input_prompt: str, generations: int) -> list[str]:
    """Generate text using the Llama3 model.

    Args:
        input_prompt (str): The initial text to start the generation from.
        generations (int): The number of text sequences to generate.

    Returns:
        list[str]: A list of generated text sequences.
    """
    if generations > 1:
        log.warning("Llama3 in Ollama supports 1 generation at a time. Using more will increase the response time.")
    responses = [langchain_ollama_llama3.invoke(input_prompt) for _ in range(generations)]

    return responses


def gpt2(input_prompt: str, generations: int) -> list[str]:
    """Generate text using the GPT2 model.

    Args:
        input_prompt (str): The initial text to start the generation from.
        generations (int): The number of text sequences to generate.

    Returns:
        list[str]: A list of generated text sequences.
    """
    encoded_prompt = huggingface_gpt2_generator.tokenizer(input_prompt, truncation=True)
    truncated_prompt = huggingface_gpt2_generator.tokenizer.decode(
        encoded_prompt["input_ids"], skip_special_tokens=True
    )

    outputs = huggingface_gpt2_generator(
        truncated_prompt,
        pad_token_id=huggingface_gpt2_generator.tokenizer.eos_token_id,
        max_new_tokens=150,
        num_return_sequences=generations,
    )

    responses = [response["generated_text"] for response in outputs]

    return responses


def repeat(input_prompt: str, generations: int) -> list[str]:
    """Repeat the input prompt for debugging purposes.

    Args:
        input_prompt (str): The initial text to start the generation from.
        generations (int): The number of text sequences to generate.

    Returns:
        list[str]: A list of repeated input prompts.
    """
    return [f"Hello {input_prompt}"] * generations
