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

        results = [guard.check(prompt) for _ in range(4)]

        self.assertEqual(results, [True, True, True, False])

    def test_allows_different_prompts(self):
        guard = TokenGuard(max_repeats=3)

        self.assertTrue(guard.check("Explain Python"))
        self.assertTrue(guard.check("Explain Java"))
        self.assertTrue(guard.check("Explain JavaScript"))

    def test_rejects_non_string_prompt(self):
        guard = TokenGuard()

        with self.assertRaises(TypeError):
            guard.check(123)

    def test_rejects_invalid_max_tokens(self):
        with self.assertRaises(ValueError):
            TokenGuard(max_tokens=0)

    def test_rejects_invalid_max_repeats(self):
        with self.assertRaises(ValueError):
            TokenGuard(max_repeats=0)

    def test_rejects_invalid_window(self):
        with self.assertRaises(ValueError):
            TokenGuard(window_seconds=0)

    def test_blocks_growing_prompts(self):
        guard = TokenGuard(growth_limit=3, growth_ratio=1.5)

        self.assertTrue(guard.check("a" * 4, context_id="chat-a"))
        self.assertTrue(guard.check("b" * 8, context_id="chat-a"))
        self.assertFalse(guard.check("c" * 16, context_id="chat-a"))

    def test_allows_prompts_without_rapid_growth(self):
        guard = TokenGuard(growth_limit=3, growth_ratio=1.5)

        self.assertTrue(guard.check("a" * 4, context_id="chat-a"))
        self.assertTrue(guard.check("b" * 8, context_id="chat-a"))
        self.assertTrue(guard.check("c" * 8, context_id="chat-a"))

    def test_growth_is_separate_per_context(self):
        guard = TokenGuard(growth_limit=3, growth_ratio=1.5)

        self.assertTrue(guard.check("a" * 4, context_id="chat-a"))
        self.assertTrue(guard.check("b" * 8, context_id="chat-a"))
        self.assertTrue(guard.check("x" * 4, context_id="chat-b"))
        self.assertTrue(guard.check("y" * 4, context_id="chat-b"))
        self.assertFalse(guard.check("c" * 16, context_id="chat-a"))

    def test_rejects_invalid_context_id(self):
        guard = TokenGuard()

        with self.assertRaises(TypeError):
            guard.check("Hello", context_id=123)

    def test_rejects_invalid_growth_limit(self):
        with self.assertRaises(ValueError):
            TokenGuard(growth_limit=1)

    def test_rejects_invalid_growth_ratio(self):
        with self.assertRaises(ValueError):
            TokenGuard(growth_ratio=1)


if __name__ == "__main__":
    unittest.main()
