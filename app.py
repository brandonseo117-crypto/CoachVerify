import os
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from google import genai
from database import SPORTS_SCIENCE_DB
from google.genai import types
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


API_key = os.getenv("gemini_key")
client = genai.Client(api_key=API_key)

# Pydantic Schema with all required telemetry fields for frontend


class IndividualPaper(BaseModel):
    title: str = Field(description="Paper title")
    journal: str = Field(description="Journal name")
    pubmed_link: str = Field(description="URL to PubMed or source")
    paper_reliability: int = Field(description="0-100 reliability score")


class AuditResultSchema(BaseModel):
    audit_text: str = Field(
        description="Main response text containing the fully constructed HTML layout matching the template directive exactly.")
    safety_score: int = Field(
        description="0-100 score evaluating protocol safety. If a generic greeting or non-supplement question, return 100.")
    performance_score: int = Field(
        description="0-100 score evaluating performance enhancement impact. Default to 0 if irrelevant.")
    reliability_score: int = Field(
        description="0-100 score for evidence quality. Gold standard = 80+, Limited = 50-79, Low = <50.")
    matched_paper: str = Field(
        description="The citation title/journal source matched from the DB or external medical consensus.")
    translated_consensus: str = Field(
        description="The primary conversational response from CoachVerify. Keep it punchy, athletic, direct, and professional.")
    alternative: Optional[str] = Field(
        default=None,
        description="Recommended clinical alternatives or pivots if the queried protocol is unsafe or ineffective.")
    individual_papers: List[IndividualPaper] = Field(
        description="Array of supporting research papers with reliability scoring.")


@app.route('/api/audit', methods=['POST'])
def audit_reliability():
    try:
        user_data = request.json
        if not user_data:
            return jsonify({"error": "Invalid JSON payload provided."}), 400

        # Extract user input
        claim = user_data.get('claim', '').strip()

        if not claim:
            return jsonify({"error": "Message content is required."}), 400

        # Build the structured HTML layout engine prompt
        prompt = f"""You are CoachVerify, an advanced sports science verification engine engineered to match the structural depth and objective visual layout of Consensus AI. 
Your primary goal is to dissect athlete queries using data-grounded science and output beautifully structured, highly visual HTML inside the 'audit_text' variable.

CRITICAL TONE DIRECTIVES:
1. Speak normally, professionally, and clinically. Never use generic filler words, dramatic jargon, or high-energy sports-coach clichés.
2. Talk like a premier sports scientist or elite clinical researcher: calm, authoritative, precise, and objective.
3. Be direct and concise. State the medical facts clearly without unnecessary conversational filler text.

FORMATTING & RESPONSE ARCHITECTURE (YOU MUST USE THIS EXACT HTML LAYOUT FOR THE 'audit_text' FIELD):
You must structure the text assigned to 'audit_text' using the exact HTML template provided below. Do not use any emojis, and fill in the brackets with the relevant information based on the matching database keys or general medical consensus. Do not use markdown syntax inside the HTML.

<div class="scientific-response-block">
    <div class="consensus-summary-card">
        <span class="summary-header">SYSTEM SYNTHESIS CONSENSUS</span>
        <p>[Provide a calm, direct, and highly concise synthesis of the medical/scientific consensus here. If the practice is unsafe or ineffective, explain why clearly.]</p>
    </div>

    <div class="study-badge-row">
        <span class="study-pill">DESIGN: [Insert Study Type from database, e.g., Randomized Controlled Trial]</span>
        <span class="study-pill">JOURNAL: [Insert Journal Authority from database, e.g., Biology of Sport]</span>
        <span class="study-pill">YEAR: [Insert Publication Year]</span>
    </div>

    <div class="clinical-data-grid">
        <div class="data-metric-tile">
            <span class="tile-label">Sample Size</span>
            <span class="tile-value">N = [Insert Sample Size number]</span>
        </div>
        <div class="data-metric-tile">
            <span class="tile-label">Target Cohort</span>
            <span class="tile-value">[Insert brief Population Demographics summary from database]</span>
        </div>
    </div>
</div>

ATHLETE QUERY: {claim}

VERIFIED SPORTS SCIENCE GROUNDING DATABASE:
{json.dumps(SPORTS_SCIENCE_DB, indent=2)}

RETURN SCHEMA FIELD REQUIREMENT MATCHING:
1. audit_text: Wrap the complete HTML block designed above exactly into this string field.
2. safety_score: 0-100 evaluation integer matching your database find.
3. performance_score: 0-100 evaluation integer matching your database find.
4. reliability_score: 0-100 evidence quality rating integer.
5. matched_paper: Title string of primary reference matched.
6. translated_consensus: Plain-English conversational summary string.
7. alternative: Safe alternative recommendation string (or null if practice is perfectly safe).
8. individual_papers: List of individual source paper objects extracted from the database matching the criteria.

Return ONLY valid JSON matching the schema parameters perfectly. No markdown formatting around the outer JSON object, no code blocks."""

        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=AuditResultSchema,
            temperature=0.2
        )

        try:
            ai_response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=config
            )
        except Exception as api_error:
            print(f"Gemini API Error: {str(api_error)}")
            return jsonify({
                "error": "AI service unavailable",
                "details": f"Gemini API error: {str(api_error)}"
            }), 503

        raw_text = ai_response.text.strip()

        # Strip code fences if model wraps them mistakenly
        if raw_text.startswith("```"):
            lines = raw_text.splitlines()
            if lines[0].startswith("```json") or lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            raw_text = "\n".join(lines).strip()

        try:
            processed_result = json.loads(raw_text)
        except json.JSONDecodeError as je:
            print(f"JSON Parse Error: {str(je)}")
            print(f"Raw response text: {raw_text[:500]}")
            return jsonify({
                "error": "Response parsing failed",
                "details": f"AI returned invalid JSON: {str(je)}"
            }), 500

        return jsonify(processed_result), 200

    except json.JSONDecodeError as je:
        print(f"Payload JSON Parse Error: {str(je)}")
        return jsonify({"error": "Invalid request", "details": "Could not parse request body"}), 400
    except Exception as e:
        print(f"Backend error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
