import os
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from google import genai
from database import SPORTS_SCIENCE_DB
from google.genai import types
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


API_key = os.getenv("gemini_key")
client = genai.Client(api_key=API_key)

# 🔐 Pydantic Schema customized perfectly for script.js telemetry fields


class AuditResultSchema(BaseModel):
    safety_score: int = Field(
        description="0-100 score evaluating protocol safety. If a generic greeting or non-supplement question, return 100.")
    performance_score: int = Field(
        description="0-100 score evaluating performance enhancement impact. Default to 0 if irrelevant.")
    matched_paper: str = Field(
        description="The citation title/journal source matched from the DB or external medical consensus.")
    translated_consensus: str = Field(
        description="The primary conversational response from CoachVerify. Keep it punchy, athletic, direct, and elite.")


@app.route('/api/audit', methods=['POST'])
def audit_reliability():
    try:
        user_data = request.json
        if not user_data:
            return jsonify({"error": "Invalid JSON payload provided."}), 400

        # script.js maps user input to 'claim' field directly
        claim = user_data.get('claim', '').strip()
        profile = "Varsity Athlete"

        if not claim:
            return jsonify({"error": "Message content is required."}), 400

        # Adjusted system prompt to deliver answers like a premium chatbot coach
        prompt = f"""You are CoachVerify, an elite AI sports medicine coach counseling a {profile}. 
        Respond to the user's message in a direct, motivational, authoritative coaching style. Speak directly to them.

        USER MESSAGE / INQUIRY:
        "{claim}"

        VERIFIED SPORTS SCIENCE GROUNDING DATABASE:
        {json.dumps(SPORTS_SCIENCE_DB, indent=2)}

        EXECUTION PIPELINE:
        1. **Semantic Grounding Mapping**: Evaluate the user's input against the database. If they are talking about dry scooping, creatine, or weight cuts, align your telemetry scores directly with our database.
        2. **External Fact-Checking**: If their message contains a training method or supplement not in our local database, use general adolescent sports science rules to determine a realistic safety/performance layout. If it's a generic greeting, keep safety at 100 and performance at 0.
        3. **The Voice of CoachVerify**: Place your full direct response into the `translated_consensus` variable. Do not wrap it in clinical textbook jargon—break it down into explicit, actionable athletic instructions.
        """

        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=AuditResultSchema,
            temperature=0.3
        )

        ai_response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=config
        )

        raw_text = ai_response.text.strip()

        # Strip code fences if the model wraps them mistakenly
        if raw_text.startswith("```"):
            lines = raw_text.splitlines()
            if lines[0].startswith("```json") or lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            raw_text = "\n".join(lines).strip()

        processed_result = json.loads(raw_text)
        return jsonify(processed_result), 200

    except json.JSONDecodeError as je:
        print(f"JSON Structure Extraction Failure: {str(je)}")
        return jsonify({"error": "Data generation error", "details": "The engine returned an improperly enclosed payload."}), 500
    except Exception as e:
        print(f"Backend processing error: {str(e)}")
        return jsonify({"error": "Internal engine parsing failure", "details": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
