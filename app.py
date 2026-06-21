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

# 🔬 Expanded individual paper schema to hold custom metadata per reference source


class IndividualPaper(BaseModel):
    title: str = Field(description="Paper title")
    journal: str = Field(description="Journal name")
    pubmed_link: str = Field(description="URL to PubMed or source study page")
    paper_reliability: int = Field(
        description="0-100 reliability score rating")
    study_type: str = Field(
        description="The specific methodology framework layout design (e.g., Randomized Controlled Trial, Case Report, Systematic Review).")
    publication_year: str = Field(
        description="The explicit year of publishing.")
    sample_size: str = Field(
        description="The numerical sample size integer value, e.g., '14' or '1'. Do not write N/A if extractable.")
    target_cohort: str = Field(
        description="Detailed baseline population cohort demographics or target sample metrics.")


class AuditResultSchema(BaseModel):
    audit_text: str = Field(
        description="Main response text containing a clean, direct, 2-3 sentence professional clinical assessment summary of the core consensus findings.")
    safety_score: int = Field(
        description="0-100 score evaluating protocol safety. Default to 100 if safe/unrelated.")
    performance_score: int = Field(
        description="0-100 score evaluating performance enhancement impact. Default to 0 if irrelevant.")
    reliability_score: int = Field(
        description="Overall evidence quality index rating.")
    matched_paper: str = Field(
        description="The primary reference study title matched from the database.")
    study_type: str = Field(
        description="Default primary reference methodology framework design.")
    journal_authority: str = Field(
        description="Primary publishing journal authority.")
    publication_year: str = Field(
        description="Default publication year metadata.")
    sample_size: str = Field(
        description="Primary dataset aggregate sample size count.")
    target_cohort: str = Field(
        description="Primary cohort overview demographic metadata.")
    translated_consensus: str = Field(
        description="Plain-English conversational clinical summary verdict.")
    alternative: Optional[str] = Field(
        default=None, description="Recommended safe alternatives if the query is risky/unproductive.")
    individual_papers: List[IndividualPaper] = Field(
        description="Array of supporting research papers with individual metadata matrices filled completely.")


@app.route('/api/audit', methods=['POST'])
def audit_reliability():
    try:
        user_data = request.json
        if not user_data:
            return jsonify({"error": "Invalid JSON payload provided."}), 400

        claim = user_data.get('claim', '').strip()
        if not claim:
            return jsonify({"error": "Message content is required."}), 400

        prompt = f"""You are CoachVerify, an advanced sports science verification engine engineered to match the data depth of Consensus AI.
Analyze the athlete's query objectively and exhaustively fill out the schema fields using data-grounded science from the provided database.

CRITICAL TONE & PLAIN-LANGUAGE STRUCTURAL DIRECTIVES:
- Speak normally, professionally, and objectively[cite: 35, 38]. Do not use generic filler words, dramatic jargon, or sports-coach clichés.
- MANDATE: The 'audit_text' field must be written in clear, plain language accessible to a high school student or parent under stress[cite: 8, 35, 91]. 
- Avoid dense academic or medical jargon. If a technical term is found in the database, translate it into everyday English:
  * Do NOT say 'acute myocardial infarction' -> Say 'a sudden, severe heart attack'.
  * Do NOT say 'esophageal damage or ulcerations' -> Say 'painful throat burns and sores'.
  * Do NOT say 'ingesting raw caustic compounds' -> Say 'swallowing highly concentrated dry powders'.
- Keep your explanation to 2-3 direct sentences that move the user from uncertainty to clear, immediate action[cite: 8, 19, 92].
- STIPULATION: Use standard alphanumeric text and punctuation only. Do not output any graphical emojis or pictorial symbols.

ATHLETE QUERY: {claim}

VERIFIED SPORTS SCIENCE GROUNDING DATABASE:
{json.dumps(SPORTS_SCIENCE_DB, indent=2)}

RETURN SCHEMA FIELD REQUIREMENT MATCHING:
1. audit_text: Provide a concise clinical overview paragraph summarizing the core consensus findings. Do not insert HTML tags or markdown formatting.
2. Fill all other schema parameter fields—including the complete metadata fields nested within the individual_papers array items—with clean text values matching the database context.
"""

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

    except Exception as e:
        print(f"Backend error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
