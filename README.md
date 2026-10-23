
````markdown
# TokenGuard 🛡️

Lightweight local request protection for Python AI applications.

TokenGuard helps developers check prompts before sending them to an AI provider. It can reject oversized prompts, detect repeated requests, and flag rapidly growing prompts within a conversation.

TokenGuard is a local checking utility, not an automatic network interceptor or a complete billing-protection system.

## Features

- **Estimated prompt-size limits:** Reject prompts that exceed a configured estimate.
- **Repeated-request detection:** Block identical prompts after a configured number of previous accepted requests.
- **Growth detection:** Detect rapid increases in estimated prompt size within a conversation.
- **Conversation isolation:** Track prompt growth separately using a conversation identifier.
- **Time-window tracking:** Expire old request records.
- **Thread safety:** Protect shared request history with a lock.
- **Input validation:** Reject invalid prompts and configuration values.
- **No third-party runtime dependencies:** Uses Python's standard library.

## Requirements

- Python 3.9 or newer.
- No third-party runtime dependencies.

## Installation

Install the published package from PyPI:

```bash
python -m pip install tokenguard-local
````

PyPI: [https://pypi.org/project/tokenguard-local/](https://pypi.org/project/tokenguard-local/?utm_source=chatgpt.com)

Note: The published PyPI release may not contain the latest unreleased repository changes. Check the release version before relying on newer features.

### Quick start

```python
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
```

Call `guard.check(prompt)` before sending the prompt to your provider. TokenGuard does not automatically intercept network requests.

### Configuration

| Parameter      | Default | Description                                                          |
| -------------- | ------- | -------------------------------------------------------------------- |
| max_tokens     | 8000    | Maximum estimated prompt size                                        |
| max_repeats    | 3       | Maximum previously accepted identical prompts within the time window |
| window_seconds | 60      | Time window for tracking request history                             |
| growth_limit   | 3       | Number of consecutive prompt sizes used to evaluate rapid growth     |
| growth_ratio   | 1.5     | Minimum growth ratio required between consecutive prompt sizes       |

Values must satisfy the constructor's validation rules. `max_tokens` and `max_repeats` must be at least 1, `window_seconds` must be positive, `growth_limit` must be at least 2, and `growth_ratio` must be greater than 1.

### Detecting rapid prompt growth

Growth detection requires a `context_id` so TokenGuard can associate prompts with a conversation.

```python
from token_guard import TokenGuard

guard = TokenGuard(
    max_tokens=8000,
    growth_limit=3,
    growth_ratio=1.5,
    window_seconds=60,
)

conversation_id = "conversation-123"

prompts = [
    "a" * 4,
    "b" * 8,
    "c" * 16,
]

for prompt in prompts:
    if guard.check(prompt, context_id=conversation_id):
        print("Request allowed")
    else:
        print("Request blocked")
```

This example illustrates the growth rule using artificial strings, not real AI prompts. Under the default settings shown, the first two prompts are accepted and the third is blocked because the estimated size has grown rapidly across the sequence.

Use a stable, unique conversation identifier for each conversation. Calls without a `context_id` still receive size and repeated-request checks, but growth detection is not applied.

Growth detection is a heuristic. It does not understand the meaning of a prompt or prove that a request is unsafe.

### Repeated-request behavior

The repeat limit counts earlier accepted matching requests. With `max_repeats=3`, the first three identical requests can be accepted, while the fourth is blocked if it occurs within the active time window.

Repeated-request tracking applies to the whole `TokenGuard` instance, even when different conversation IDs are supplied.

### Token estimation

TokenGuard estimates token counts using character length:

```python
estimated_tokens = max(1, (len(text) + 3) // 4)
```

This is an approximation. Actual token counts depend on the model, tokenizer, and content. TokenGuard does not calculate exact provider token usage.

### Run tests

Clone the repository:

```bash
git clone https://github.com/mokhabelethabang4-cpu/token-guard.git
cd token-guard
```

Run the tests:

```bash
python test_token_guard.py
```

### Limitations

TokenGuard is an early-stage local request-checking utility, not a complete API security or billing enforcement system.

* Your application must explicitly call `guard.check(prompt)` before sending a request.

* It does not automatically intercept AI API calls or network traffic.

* Token estimates are approximate.

* Growth detection relies on prompt-size patterns, not semantic analysis.

* Request history is stored in memory and resets when the process restarts.

* Limits are local to each `TokenGuard` instance; they are not shared automatically across processes or servers.

* It does not enforce provider-side spending limits, authentication, authorization, or provider rate limits.

* It cannot guarantee that runaway loops or excessive API costs will be prevented.

Use provider-side usage limits, monitoring, and appropriate application-level controls alongside TokenGuard.

### Project status

TokenGuard is an early-stage project focused on lightweight, local request protection for Python AI applications.

Contributions, bug reports, and suggestions are welcome through the GitHub repository.

### License

This project is licensed under the MIT License. See `LICENSE` for details.

### Links

* PyPI: [https://pypi.org/project/tokenguard-local/](https://pypi.org/project/tokenguard-local/?utm_source=chatgpt.com)

* GitHub: [https://github.com/mokhabelethabang4-cpu/token-guard](https://github.com/mokhabelethabang4-cpu/token-guard?utm_source=chatgpt.com)

```
