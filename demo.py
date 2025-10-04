import requests
import json
import time
from datetime import datetime


class DemoRunner:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url

    def test_safety_scenarios(self):
        """Test various safety scenarios"""
        scenarios = [
            {
                "name": "Normal Conversation",
                "user_id": "user123",
                "message": "Hello, how are you doing today?",
                "user_age": 25,
                "guardian_mode": False
            },
            {
                "name": "Abusive Language",
                "user_id": "user456",
                "message": "I hate you! You're stupid and worthless!",
                "user_age": 25,
                "guardian_mode": False
            },
            {
                "name": "Crisis Situation",
                "user_id": "user789",
                "message": "I can't take it anymore. I want to end it all.",
                "user_age": 25,
                "guardian_mode": False
            },
            {
                "name": "Age-Inappropriate Content",
                "user_id": "child_user",
                "message": "I saw some violent content with drugs and alcohol",
                "user_age": 10,
                "guardian_mode": True
            },
            {
                "name": "Escalating Conversation",
                "user_id": "escalating_user",
                "messages": [
                    "I'm getting really frustrated",
                    "This is making me angry",
                    "I hate this so much!",
                    "I can't stand it anymore!"
                ],
                "user_age": 25,
                "guardian_mode": False
            }
        ]

        for scenario in scenarios:
            print(f"\n{'=' * 50}")
            print(f"Testing: {scenario['name']}")
            print(f"{'=' * 50}")

            if 'messages' in scenario:
                # Test conversation flow
                for i, message in enumerate(scenario['messages']):
                    print(f"Message {i + 1}: {message}")
                    response = self._send_message(
                        scenario['user_id'],
                        message,
                        scenario['user_age'],
                        scenario['guardian_mode']
                    )
                    self._print_results(response)
                    time.sleep(1)  # Simulate real conversation timing
            else:
                # Single message test
                response = self._send_message(
                    scenario['user_id'],
                    scenario['message'],
                    scenario['user_age'],
                    scenario['guardian_mode']
                )
                self._print_results(response)

    def _send_message(self, user_id, message, user_age, guardian_mode):
        """Send message to safety API"""
        payload = {
            "user_id": user_id,
            "message": message,
            "user_age": user_age,
            "guardian_mode": guardian_mode
        }

        try:
            response = requests.post(
                f"{self.base_url}/api/safety/analyze",
                json=payload,
                headers={'Content-Type': 'application/json'}
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def _print_results(self, result):
        """Print analysis results in readable format"""
        if 'error' in result:
            print(f"Error: {result['error']}")
            return

        safety_status = result.get('safety_status', {})
        model_results = result.get('model_results', {})

        print(f"Safety Level: {safety_status.get('concern_level', 'unknown').upper()}")
        print(f"Actions Required: {', '.join(safety_status.get('actions_required', []))}")

        # Abuse detection results
        abuse = model_results.get('abuse_detection', {})
        if abuse.get('is_abusive', False):
            print(f"🚨 ABUSE DETECTED: {abuse.get('abuse_type')} "
                  f"(confidence: {abuse.get('confidence'):.2f})")

        # Crisis detection
        crisis = model_results.get('crisis_intervention', {})
        if crisis.get('crisis_detected', False):
            print(f"🚨 CRISIS DETECTED: Level {crisis.get('intervention_level')} "
                  f"(score: {crisis.get('risk_score'):.2f})")

        # Escalation detection
        escalation = model_results.get('escalation_detection', {})
        if escalation.get('is_escalating', False):
            print(f"⚠️ CONVERSATION ESCALATING: {escalation.get('confidence'):.2f}")

        # Content filtering
        content = model_results.get('content_filtering', {})
        if not content.get('is_appropriate', True):
            print(f"🛡️ CONTENT FILTERED: {content.get('blocked_categories', [])}")


if __name__ == "__main__":
    demo = DemoRunner()
    print("Starting AI Safety System Demo...")
    demo.test_safety_scenarios()