import os
import google.generativeai as genai
from memory_store import MemoryManager

# Configure Gemini
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

class IntelligencePipeline:
    def __init__(self, memory_manager=None):
        self.memory_manager = memory_manager or MemoryManager()
        if api_key:
            self.gemini_model = genai.GenerativeModel("gemini-1.5-flash")
        else:
            print("Warning: No GEMINI_API_KEY found. Using mock model.")
            self.gemini_model = None

    def reflection_loop(self, draft_content):
        """
        Reflects on the draft content using historical context and Gemini 1.5 Flash.
        """
        print("Starting reflection loop...")

        # 1. Retrieve historical context
        active_concepts = self.memory_manager.get_active_concepts()
        print(f"Retrieved {len(active_concepts)} active concepts from memory.")

        # 2. Evaluate using Gemini 1.5 Flash with Binary Gate Checks
        prompt = f"""
        You are an expert editor for an AI intelligence newsletter.

        Review the following draft content:
        ---
        {draft_content}
        ---

        Historical Context (Active Concepts):
        {active_concepts}

        Perform the following Binary Gate Checks:
        1. Does the content reference historical continuity from the prior 7-30 days based on the provided context? (Pass/Fail)
        2. Are the claims supported by evidence? (Pass/Fail)
        3. Is the tone appropriate for a professional audience? (Pass/Fail)

        If any check fails, provide specific feedback for improvement.
        If all checks pass, output "PASS".

        Also, identify any new concepts, claims, or narrative shifts that should be stored in memory.
        Format your response as JSON with keys: "status", "feedback", "new_insights".
        "new_insights" should have keys: "concepts", "claims", "shifts".
        """

        try:
            if self.gemini_model:
                response = self.gemini_model.generate_content(prompt)
                reflection_result = response.text
            else:
                # Mock response
                import json
                reflection_result = json.dumps({
                    "status": "PASS",
                    "feedback": "Mocked successful check.",
                    "new_insights": {
                        "concepts": [{"name": "Mock Concept", "status": "Accelerating"}],
                        "claims": ["Mock Claim"],
                        "shifts": ["Mock Shift"]
                    }
                })

            print("Gemini Reflection Result:", reflection_result)

            # Simulated parsing logic for demonstration purposes
            # We assume Gemini returns a JSON string if instructed well, but here we'll mock the extraction
            # if we can't parse it.
            import json
            try:
                # specific clean up for potential markdown code blocks
                clean_response = reflection_result.replace("```json", "").replace("```", "").strip()
                result_data = json.loads(clean_response)
            except json.JSONDecodeError:
                print("Failed to parse Gemini response as JSON. using fallback.")
                result_data = {
                    "status": "FAIL",
                    "feedback": "Could not parse AI response.",
                    "new_insights": {}
                }

            if result_data.get("status") == "PASS":
                # 3. Store final pass results back into Memory Layer
                if "new_insights" in result_data:
                    self.memory_manager.update_memory(result_data["new_insights"])
                return draft_content  # Return the approved draft
            else:
                print("Draft failed checks. Feedback:", result_data.get("feedback"))
                # In a real loop, we would loop back to the writer agent.
                # For this task, we return the feedback.
                return f"Draft rejected. Feedback: {result_data.get('feedback')}"

        except Exception as e:
            print(f"Error in reflection loop: {e}")
            return draft_content # Fallback to original draft on error

# Example usage (for testing)
if __name__ == "__main__":
    pipeline = IntelligencePipeline()
    # Mock draft
    draft = "AI agents are accelerating. The new model X shows 20% improvement."
    result = pipeline.reflection_loop(draft)
    print("Final Result:", result)
