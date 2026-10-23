
# TokenGuard 🛡️

**Lightweight local request protection for Python AI applications.**

TokenGuard helps developers limit oversized prompts and detect repeated requests within a configurable time window.

## Features

- **Prompt size limits** — Reject prompts that exceed the configured token estimate.
- **Repeated request detection** — Block identical prompts after a configurable number of previous requests.
- **Time-window tracking** — Expire old request records automatically.
- **Thread safety** — Protect shared request history with a lock.
- **Input validation** — Reject invalid prompt types and configuration values.
- **No external dependencies** — Uses Python's standard library.

## Requirements

- Python 3.9 or newer recommended.
- No third-party packages required.

## Installation

Clone the repository:

```bash
git clone https://github.com/mokhabelet habang4-cpu/token-guard.git
```

Enter the project directory:

```bash
cd token-guard
```

> If your GitHub username or repository URL differs, replace the URL with your repository's actual clone URL.

## Usage

```python
from token_guard import TokenGuard

guard = TokenGuard(
    max_tokens=8000,
    max_repeats=3,
    window_seconds=60,
)

prompt = "Explain how AI works."

if guard.check(prompt):
    print("Request allowed")
else:
    print("Request blocked")
```

## Configuration

| Parameter | Default | Description |
|---|---:|---|
| `max_tokens` | `8000` | Maximum estimated prompt tokens |
| `max_repeats` | `3` | Maximum number of previously accepted identical prompts |
| `window_seconds` | `60` | Time window used for request tracking |

The repeat limit counts previous matching requests. A prompt is blocked when the number of earlier matching requests in the active window reaches `max_repeats`.

## Token estimation

TokenGuard estimates token usage using prompt length:

```python
estimated_tokens = max(1, (len(text) + 3) // 4)
```

This is a rough estimate, not an exact model tokenizer. Actual token counts vary by AI model and text content.

## Run tests

Run the test suite with Python:

```bash
python -m unittest -v
```

## Limitations

- Request history is stored in memory and resets when the process restarts.
- Limits apply to a single `TokenGuard` instance, not automatically across multiple processes or servers.
- TokenGuard does not contact AI providers or validate their actual token usage.
- Applications must call `guard.check(prompt)` before sending a request to their AI provider.
- This package does not replace authentication, authorization, or provider-side rate limits.

## Project status

TokenGuard is an early-stage project focused on lightweight, local request protection for Python AI applications.

## License

See the repository's license file for usage and distribution terms.
