FLAG_WORDS = ["error", "failed", "unable", "exception", "traceback"]

REQUIRED_PHRASES = [
    # Example: add phrases a “good response” must include (optional)
    # "next steps",
]

MAX_CHARS = 1500  # simple guardrail for overly long output
PASS_THRESHOLD = 70  # score needed to "pass"
