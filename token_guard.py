
"""TokenGuard: lightweight local request protection for Python AI apps."""

from collections import deque
from hashlib import sha256
from threading import Lock
import time


class TokenGuard:
    """Block oversized prompts and repeated requests within a time window."""

    def __init__(
        self,
        max_tokens=8000,
        max_repeats=3,
        window_seconds=60,
    ):
        if max_tokens < 1:
            raise ValueError("max_tokens must be at least 1")
        if max_repeats < 1:
            raise ValueError("max_repeats must be at least 1")
        if window_seconds <= 0:
            raise ValueError("window_seconds must be positive")

        self.max_tokens = max_tokens
        self.max_repeats = max_repeats
        self.window_seconds = window_seconds
        self.history = deque()
        self.lock = Lock()

    @staticmethod
    def estimate_tokens(text):
        """Estimate tokens quickly; this is not an exact tokenizer."""
        if not isinstance(text, str):
            raise TypeError("prompt must be a string")

        return max(1, (len(text) + 3) // 4)

    def check(self, prompt):
        """Return True if allowed, or False if blocked."""
        if not isinstance(prompt, str):
            raise TypeError("prompt must be a string")

        if self.estimate_tokens(prompt) > self.max_tokens:
            return False

        now = time.monotonic()
        fingerprint = sha256(prompt.encode("utf-8")).hexdigest()

        with self.lock:
            # Remove requests outside the active time window.
            while (
                self.history
                and now - self.history[0][0] >= self.window_seconds
            ):
                self.history.popleft()

            # Count earlier matching requests in this window.
            repeats = sum(
                1
                for _, previous in self.history
                if previous == fingerprint
            )

            if repeats >= self.max_repeats:
                return False

            self.history.append((now, fingerprint))
            return True


# Ready-to-use default guard.
guard = TokenGuard()
