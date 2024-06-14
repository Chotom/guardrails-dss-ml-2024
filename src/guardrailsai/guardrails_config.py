"""Module for defining Guardrails ai configuration.

To use this module the additional dependencies must be installed:
    guardrails hub install hub://guardrails/detect_pii;
    guardrails hub install hub://guardrails/gibberish_text;
    guardrails hub install hub://cartesia/mentions_drugs;
    guardrails hub install hub://guardrails/nsfw_text;
    guardrails hub install hub://guardrails/profanity_free;
    guardrails hub install hub://guardrails/secrets_present;
    guardrails hub install hub://guardrails/toxic_language;
"""

import guardrails.hub
from guardrails import Guard, OnFailAction

detect_pii_entities = ["LOCATION", "EMAIL_ADDRESS", "PERSON", "PHONE", "PL_PESEL"]

guard = Guard().use_many(
    guardrails.hub.DetectPII(pii_entities=detect_pii_entities, on_fail=OnFailAction.FIX),
    guardrails.hub.GibberishText(on_fail=OnFailAction.EXCEPTION),
    guardrails.hub.MentionsDrugs(on_fail=OnFailAction.EXCEPTION),
    guardrails.hub.NSFWText(on_fail=OnFailAction.EXCEPTION),
    guardrails.hub.ProfanityFree(on_fail=OnFailAction.EXCEPTION),
    guardrails.hub.SecretsPresent(on_fail=OnFailAction.FIX),
    guardrails.hub.ToxicLanguage(on_fail=OnFailAction.EXCEPTION),
)
