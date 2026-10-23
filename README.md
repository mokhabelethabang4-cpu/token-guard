TokenGuard 🛡️

Lightweight local request protection for Python AI applications.

TokenGuard helps Python developers limit oversized prompts and detect repeated requests before sending them to an AI provider.

It is a small, dependency-free utility designed to help applications reduce accidental repeated requests and catch prompts that exceed a configured estimated token limit.

Features

- Prompt size limits: Reject prompts that exceed a configurable estimated token limit.
- Repeated request detection: Block identical prompts after a configurable number of previous accepted requests.
- Time-window tracking: Automatically expire old request records.
- Thread safety: Protect shared request history with a lock.
- Input validation: Reject invalid prompt types and configuration values.
- No third-party dependencies: Uses Python's standard library.

Requirements

- Python 3.9 or newer.
- No third-party runtime dependencies.

Installation

Install TokenGuard from PyPI:

python -m pip install tokenguard-local

PyPI project page: https://pypi.org/project/tokenguard-local/

Quick start

from token_guard import TokenGuard

guard = TokenGuard(
    max_tokens=8000,
    max_repeats=3,
    window_seconds=60,
)

prompt = "Explain how artificial intelligence works."

if guard.check(prompt):
    # Send the prompt to your AI provider here.
    print("Request allowed")
else:
    print("Request blocked")

Important: Call "guard.check(prompt)" before sending the prompt to your AI provider. TokenGuard does not automatically intercept network requests.

Configuration

Parameter| Default| Description
"max_tokens"| "8000"| Maximum estimated prompt tokens allowed
"max_repeats"| "3"| Maximum previous accepted identical prompts within the time window
"window_seconds"| "60"| Time window used to track repeated prompts

Example with stricter limits:

from token_guard import TokenGuard

guard = TokenGuard(
    max_tokens=2000,
    max_repeats=2,
    window_seconds=30,
)

prompt = "Summarize this document."

if not guard.check(prompt):
    print("Prompt blocked by TokenGuard")

The repeat limit counts earlier accepted matching requests. With "max_repeats=3", the first three matching requests can be accepted, while the fourth is blocked if it occurs within the active time window.

Token estimation

TokenGuard uses a quick character-based estimate:

estimated_tokens = max(1, (len(text) + 3) // 4)

This is only an approximation. Actual token counts depend on the model, tokenizer, and content. TokenGuard does not use a model-specific tokenizer or verify actual provider token usage.

Run tests

To obtain the source code:

git clone https://github.com/mokhabelethabang4-cpu/token-guard.git
cd token-guard

Run the test suite from the repository directory:

python -m unittest -v

Limitations

TokenGuard is a local request-checking utility, not a complete API security or billing enforcement system.

- Your application must explicitly call "guard.check(prompt)" before sending a request.
- It does not automatically intercept all AI API calls or network traffic.
- Token estimates are approximate, not exact provider token counts.
- Request history is stored in memory and resets when the process restarts.
- Limits apply to each "TokenGuard" instance; they are not shared automatically across multiple processes or servers.
- It does not enforce provider-side spending limits, authentication, authorization, or rate limits.
- It does not guarantee that every runaway loop or excessive API cost will be prevented.

Use provider-side usage limits and monitoring alongside TokenGuard when controlling AI API costs.

Project status

TokenGuard is an early-stage project focused on lightweight, local request protection for Python AI applications.

Contributions, bug reports, and suggestions are welcome through the GitHub repository.

License

This project is licensed under the MIT License. See the "LICENSE" file in the repository for details.

Links

- PyPI: https://pypi.org/project/tokenguard-local/
- GitHub: https://github.com/mokhabelethabang4-cpu/token-guard
