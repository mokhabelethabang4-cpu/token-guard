
# TokenGuard 🛡️

Lightweight, local request protection for Python AI applications.

TokenGuard helps developers limit oversized prompts and detect repeated request patterns before sending requests to an AI provider.

## Features

- Configurable prompt-size limit
- Repeated-prompt detection
- Local, in-memory request history
- No telemetry or cloud service required
- Automated tests with GitHub Actions

## Requirements

- Python 3.9 or newer

## Installation

TokenGuard is not published on PyPI yet.

To use it locally, place `token_guard.py` in your project and import it:

```python
from token_guard import TokenGuard

guard = TokenGuard(max_tokens=8000, max_repeats=3)

prompt = "Explain how Python works."

if guard.check(prompt):
    print("Request allowed")
else:
    print("Request blocked")
```

## Important limitations

TokenGuard uses an approximate character-based token estimate, not an exact model tokenizer.

It checks only prompts explicitly passed to `guard.check()`. It does not automatically intercept all network requests, enforce an API spending limit, or provide operating-system kernel protection.

## Development

Run the tests with:

```bash
python -m unittest -v
```

## License

MIT
