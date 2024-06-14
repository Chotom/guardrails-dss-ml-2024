"""An example of LLM without guardrails."""

from nemoguardrails.logging.explain import ExplainInfo


def estimate_used_tokens(info: ExplainInfo) -> float:
    """Estimate the number of tokens used by the LLM based on the prompt and completion lengths."""
    sum_chars = 0
    for llm_call in info.llm_calls:
        sum_chars += len(llm_call.prompt)
        sum_chars += len(llm_call.completion)

    chars_per_token = 4
    """Assume that the average token length is 4 characters. This is only an estimate."""

    return sum_chars / chars_per_token
