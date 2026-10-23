"""TokenGuard: lightweight local request protection for Python AI apps."""

from collections import deque
from hashlib import sha256
from threading import Lock
import time


class TokenGuard:
    """Block oversized, repeated, and rapidly growing prompts."""

    def __init__(
        self,
        max_tokens=8000,
        max_repeats=3,
        window_seconds=60,
        growth_limit=3,
        growth_ratio=1.5,
    ):
        if max_tokens < 1:
            raise ValueError("max_tokens must be at least 1")
        if max_repeats < 1:
            raise ValueError("max_repeats must be at least 1")
        if window_seconds <= 0:
            raise ValueError("window_seconds must be positive")
        if growth_limit < 2:
            raise ValueError("growth_limit must be at least 2")
        if growth_ratio <= 1:
            raise ValueError("growth_ratio must be greater than 1")

        self.max_tokens = max_tokens
        self.max_repeats = max_repeats
        self.window_seconds = window_seconds
        self.growth_limit = growth_limit
        self.growth_ratio = growth_ratio

        self.history = deque()
        self.growth_history = {}
        self.lock = Lock()

    @staticmethod
    def estimate_tokens(text):
        """Estimate tokens using characters; not an exact tokenizer."""
        if not isinstance(text, str):
            raise TypeError("prompt must be a string")

        return max(1, (len(text) + 3) // 4)

    def check(self, prompt, context_id=None):
        """Return True if allowed, or False if blocked.

        Provide context_id to enable growth detection for a conversation.
        Repeated-prompt detection applies to the whole guard instance.
        """
        if not isinstance(prompt, str):
            raise TypeError("prompt must be a string")

        if context_id is not None and not isinstance(context_id, str):
            raise TypeError("context_id must be a string or None")

        estimated_tokens = self.estimate_tokens(prompt)

        if estimated_tokens > self.max_tokens:
            return False

        now = time.monotonic()
        fingerprint = sha256(prompt.encode("utf-8")).hexdigest()

        with self.lock:
            # Expire old repeated-request records.
            while (
                self.history
                and now - self.history[0][0] >= self.window_seconds
            ):
                self.history.popleft()

            repeats = sum(
                1
                for _, previous_hash in self.history
                if previous_hash == fingerprint
            )

            if repeats >= self.max_repeats:
                return False

            # Growth detection is scoped to a conversation.
            if context_id is not None:
                sizes = self.growth_history.get(context_id)

                if sizes is None:
                    sizes = deque()
                    self.growth_history[context_id] = sizes

                while (
                    sizes
                    and now - sizes[0][0] >= self.window_seconds
                ):
                    sizes.popleft()

                recent_sizes = [
                    size for _, size in sizes
                ]

                needed = self.growth_limit - 1

                if len(recent_sizes) >= needed:
                    recent_sizes = recent_sizes[-needed:]
                    sequence = recent_sizes + [estimated_tokens]

                    growing = all(
                        current > previous
                        and current >= previous * self.growth_ratio
                        for previous, current in zip(
                            sequence, sequence[1:]
                        )
                    )

                    if growing:
                        return False

                sizes.append((now, estimated_tokens))

            self.history.append((now, fingerprint))
            return True


# Ready-to-use default guard.
guard = TokenGuard()
