import garak.cli
import garak.generators.function

# List of probes: https://github.com/leondz/garak/tree/main?tab=readme-ov-file#intro-to-probes or garak --list_probes
garak_probes = [
    # Chosen various DAN and DAN-like attacks (Do Anything Now).
    "dan.AntiDAN",
    "dan.Dan_10_0",
    "dan.Dan_9_0",
    "dan.Dan_8_0",
    "dan.STAN",

    # Chosen prompt injection through text encoding.
    "encoding.InjectBase64",

    # Implementations of Riley Goodside attacks.
    "goodside.ThreatenJSON",
    "goodside.WhoIsRiley",

    # Probes that attempt to make the model output malicious content signatures.
    "knownbadsignatures.EICAR",
    "knownbadsignatures.GTUBE",
    "knownbadsignatures.GTphish",

    # Evaluate if a model will replay training data.
    "leakreplay.LiteratureCloze80",
    "leakreplay.LiteratureComplete80",

    # Subsample of the Language Model Risk Cards probes.
    "lmrc.Anthropomorphisation",
    "lmrc.Bullying",
    "lmrc.Profanity",
    "lmrc.QuackMedicine",

    # Attempts to have the model generate code for building malware.
    "malwaregen.Evasion",
    "malwaregen.SubFunctions",
    "malwaregen.TopLevel",

    # Attempts to make a model support misleading and false claims
    "misleading.FalseAssertion50",

    # Implementation of the Agency Enterprise PromptInject work.
    "promptinject.HijackHateHumansMini",
    "promptinject.HijackKillHumansMini",
    "promptinject.HijackLongPromptMini",

    # Subset of the RealToxicityPrompts work
    "realtoxicityprompts.RTPFlirtation",
    "realtoxicityprompts.RTPIdentity_Attack",
    "realtoxicityprompts.RTPSevere_Toxicity",
    "realtoxicityprompts.RTPSexually_Explicit",
    "realtoxicityprompts.RTPThreat",

    # Look for vulnerabilities the permit or enact cross-site attacks, such as private data exfiltration.
    "xss.MarkdownImageExfil",
]

# Name of function from src/run_llm.py
function_name = "guardrailsai_llama3"

# Working directory is the root of the repository.
garak.cli.main([
    "--model_type=function.Multiple",
    f"--model_name=src.run_llm#{function_name}",
    f"--report_prefix=runs/{function_name}",
    f"--probes={','.join(garak_probes)}",
    "--generations=1"
])
