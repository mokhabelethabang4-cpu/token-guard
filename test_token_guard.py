
import unittest

from token_guard import TokenGuard


class TestTokenGuard(unittest.TestCase):

    def test_allows_normal_prompt(self):
        guard = TokenGuard()
        self.assertTrue(guard.check("Explain how Python works."))

    def test_blocks_oversized_prompt(self):
        guard = TokenGuard(max_tokens=10)
        self.assertFalse(guard.check("A" * 100))

    def test_blocks_repeated_prompt(self):
        guard = TokenGuard(max_repeats=3)
        prompt = "Repeat this request"

        for _ in range(4):
            allowed = guard.check(prompt)

        self.assertFalse(allowed)


if __name__ == "__main__":
    unittest.main()
