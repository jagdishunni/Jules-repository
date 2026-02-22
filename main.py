import os
from flask import Flask, request, jsonify
from pipeline import IntelligencePipeline
from format_engine import FormatEngine
from data_fetcher import DataFetcher
from email_sender import EmailSender

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello World! AI Influencer Intelligence Platform"

@app.route("/trigger", methods=["POST"])
def trigger_pipeline():
    try:
        # 1. Fetch Data
        fetcher = DataFetcher()
        handles = fetcher.get_influencers()
        if not handles:
            # Mock handles if none found for testing
            handles = ['jules_ai', 'sama']
            print("No handles found in Firestore. Using mock handles.")

        all_tweets = []
        for handle in handles:
            tweets = fetcher.fetch_tweets(handle)
            all_tweets.extend(tweets)

        if not all_tweets:
            return jsonify({"status": "error", "message": "No tweets fetched."}), 500

        # 2. Run Analysis
        draft_content = "Latest Tweets:\n"
        for t in all_tweets:
            draft_content += f"- {t.get('text', 'No text')}\n"

        pipeline = IntelligencePipeline()
        final_content = pipeline.reflection_loop(draft_content)

        # 3. Format Output
        formatter = FormatEngine()
        # In a real scenario, we would get trends from the pipeline result or memory
        # Here we mock them for demonstration since pipeline output is just text for now
        narrative_trends = [
            {'name': 'Agentic Workflows', 'status': 'Accelerating'},
            {'name': 'Prompt Engineering', 'status': 'Decaying'}
        ]
        html_report = formatter.generate_html(final_content, narrative_trends)

        # 4. Send Email
        # Handle cases where request.json is None or empty
        json_data = request.get_json(silent=True) or {}
        recipient = json_data.get("recipient", "subscriber@example.com")

        sender = EmailSender()
        success = sender.send_email(html_report, recipient)

        if success:
            return jsonify({"status": "success", "message": "Pipeline triggered and email sent."}), 200
        else:
            return jsonify({"status": "error", "message": "Pipeline ran but email failed."}), 500

    except Exception as e:
        print(f"Error in pipeline: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    app.run(debug=debug_mode, host="0.0.0.0", port=port)
