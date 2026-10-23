# token-guard
A lightweight local request guard for Python AI applications

"""TokenGuard: lightweight local AI request protection."""

from collections import deque
from threading import Lock
import time


class TokenGuard:
    """Block oversized requests and repeated request loops."""

    def __init__(
        self,
        max_tokens=8000,
        max_repeats=3,
        window_seconds=60,
    ):
        self.max_tokens = max_tokens
        self.max_repeats = max_repeats
        self.window_seconds = window_seconds
        self.history = deque()
        self.lock = Lock()

    @staticmethod
    def estimate_tokens(text):
        """Fast rough estimate; not an exact tokenizer."""
        return max(1, (len(text) + 3) // 4)

    def check(self, prompt):
        """Return True if allowed, otherwise False."""
        now = time.monotonic()
        fingerprint = hash(prompt)
        estimated = self.estimate_tokens(prompt)

        with self.lock:
            while (
                self.history
                and now - self.history[0][0] > self.window_seconds
            ):
                self.history.popleft()

            if estimated > self.max_tokens:
                return False

            repeats = sum(
                1 for _, previous in self.history
                if previous == fingerprint
            )

            if repeats >= self.max_repeats:
                return False

            self.history.append((now, fingerprint))
            return True


guard = TokenGuard()
