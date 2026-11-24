import os
import sys
import unittest
from unittest.mock import MagicMock

# Mock google and google.genai if not installed locally
if "google" not in sys.modules:
    mock_google = MagicMock()
    mock_genai = MagicMock()
    mock_google.genai = mock_genai
    sys.modules["google"] = mock_google
    sys.modules["google.genai"] = mock_genai

from agents.agent_runner import get_default_model, DEFAULT_MODEL, DEPRECATED_MODELS, run_scenario_text

class TestAgentRunner(unittest.TestCase):
    def test_default_model(self):
        os.environ.pop("SYNAPSE_MODEL", None)
        self.assertEqual(get_default_model(), DEFAULT_MODEL)

        os.environ["SYNAPSE_MODEL"] = "gemini-2.0-flash"
        self.assertEqual(get_default_model(), DEFAULT_MODEL)

        os.environ["SYNAPSE_MODEL"] = "gemini-2.5-pro"
        self.assertEqual(get_default_model(), "gemini-2.5-pro")
        os.environ.pop("SYNAPSE_MODEL", None)

    def test_deprecated_models_set(self):
        self.assertIn("gemini-2.0-flash", DEPRECATED_MODELS)
        self.assertIn("gemini-1.5-flash", DEPRECATED_MODELS)

    def test_run_scenario_text_with_mock_client(self):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "THOUGHT: test reasoning\nFINAL_PLAN: resolved successfully"
        mock_client.models.generate_content.return_value = mock_response

        result = run_scenario_text("Test scenario", client=mock_client)
        self.assertEqual(result["final_plan"], "resolved successfully")
        self.assertIn("THOUGHT: test reasoning", result["trace"])

    def test_run_scenario_text_fallback_on_404(self):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "FINAL_PLAN: resolved via fallback"
        
        call_count = 0
        def side_effect(model, contents, config):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise Exception("404 Not Found: models/old-model is not supported")
            return mock_response

        mock_client.models.generate_content.side_effect = side_effect

        result = run_scenario_text("Test scenario", model="old-model", client=mock_client)
        self.assertEqual(result["final_plan"], "resolved via fallback")
        self.assertEqual(call_count, 2)

if __name__ == "__main__":
    unittest.main()
