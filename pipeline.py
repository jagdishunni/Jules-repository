import os
import anthropic
import google.generativeai as genai

# Models
# Ensure we use the correct model identifiers.
# Claude 3.5 Haiku: claude-3-5-haiku-20241022 (as of latest docs, verify if possible, but this is standard)
CLAUDE_MODEL = "claude-3-5-haiku-20241022"
GEMINI_MODEL = "gemini-1.5-flash"

def reflection_loop(data):
    """
    Orchestrates the analysis and reflection loop using Claude 3.5 Haiku and Gemini 1.5 Flash.

    Args:
        data (str): The input data to be analyzed (e.g., raw tweets, topic).

    Returns:
        dict: A dictionary containing the original draft, critique, and final content.
    """
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    google_key = os.environ.get("GOOGLE_API_KEY")

    if not anthropic_key or not google_key:
        return {"error": "API keys (ANTHROPIC_API_KEY, GOOGLE_API_KEY) not configured."}

    try:
        client_anthropic = anthropic.Anthropic(api_key=anthropic_key)
        genai.configure(api_key=google_key)
        model_gemini = genai.GenerativeModel(GEMINI_MODEL)

        # 1. Initial Analysis/Draft with Claude
        # We instruct Claude to be the analyst.
        analysis_prompt = f"You are an expert AI analyst. Analyze the following data and draft a professional newsletter section about it:\n\n{data}"

        response_claude = client_anthropic.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1000,
            messages=[
                {"role": "user", "content": analysis_prompt}
            ]
        )
        draft = response_claude.content[0].text

        # 2. Reflection/Critique with Gemini
        # We instruct Gemini to be the critic.
        critique_prompt = f"You are a senior editor. Critique the following newsletter draft for clarity, accuracy, tone, and engagement. Provide constructive feedback to improve it.\n\nDraft:\n{draft}"

        response_gemini = model_gemini.generate_content(critique_prompt)
        critique = response_gemini.text

        # 3. Final Polish with Claude (incorporating feedback)
        final_prompt = f"Here is the original draft you wrote:\n{draft}\n\nHere is feedback from the senior editor:\n{critique}\n\nPlease rewrite the draft to incorporate this feedback and make it production-ready."

        response_final = client_anthropic.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1000,
            messages=[
                {"role": "user", "content": final_prompt}
            ]
        )
        final_content = response_final.content[0].text

        return {
            "original_draft": draft,
            "critique": critique,
            "final_content": final_content
        }

    except Exception as e:
        return {"error": str(e)}
