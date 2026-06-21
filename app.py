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

# in-memory chat history store for the judging window
CHAT_MEMORIES = {}


@app.route('/')
def index():
    return render_template('index.html')


API_key = os.getenv("gemini_key")
client = genai.Client(api_key=API_key)

# intent routing schema


class IntentSchema(BaseModel):
    route: str = Field(
        description="Must be exactly 'RESEARCH_DEEP_DIVE' if they ask about a compound/claim/trend, or 'CASUAL_CONVERSATION' if it is a generic chat, greeting, or follow-up question."
    )

# individual paper schema


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
        description="Main response text containing a clean, direct, professional clinical assessment summary, or a direct conversational reply.")
    safety_score: int = Field(
        default=100, description="0-100 score evaluating protocol safety. Default to 100 if safe/unrelated.")
    performance_score: int = Field(
        default=0, description="0-100 score evaluating performance enhancement impact. Default to 0 if irrelevant.")
    reliability_score: int = Field(
        default=100, description="Overall evidence quality index rating.")
    matched_paper: str = Field(
        default="N/A", description="The primary reference study title matched from the database.")
    study_type: str = Field(
        default="N/A", description="Default primary reference methodology framework design.")
    journal_authority: str = Field(
        default="N/A", description="Primary publishing journal authority.")
    publication_year: str = Field(
        default="N/A", description="Default publication year metadata.")
    sample_size: str = Field(
        default="N/A", description="Primary dataset aggregate sample size count.")
    target_cohort: str = Field(
        default="N/A", description="Primary cohort overview demographic metadata.")
    translated_consensus: str = Field(
        default="Conversational response mode active.", description="Plain-English conversational clinical summary verdict.")
    alternative: Optional[str] = Field(
        default=None, description="Recommended safe alternatives if the query is risky/unproductive.")
    individual_papers: List[IndividualPaper] = Field(
        default=[], description="Array of supporting research papers with individual metadata matrices filled completely.")


@app.route('/api/audit', methods=['POST'])
def audit_reliability():
    try:
        user_data = request.json
        if not user_data:
            return jsonify({"error": "Invalid JSON payload provided."}), 400

        claim = user_data.get('claim', '').strip()
        if not claim:
            return jsonify({"error": "Message content is required."}), 400

        # unique user session
        session_id = user_data.get('session_id', 'anonymous_session')
        if session_id not in CHAT_MEMORIES:
            CHAT_MEMORIES[session_id] = []

        session_history = CHAT_MEMORIES[session_id]

        history_context = ""
        if session_history:
            history_context = "PAST CONVERSATION HISTORY:\n"
            for msg in session_history[-6:]:
                history_context += f"{msg['role']}: {msg['content']}\n"
            history_context += "\n--- END OF HISTORY ---\n"

        # check to determine if this is a research deep dive or a casual conversation
        router_prompt = f"""
        Analyze the user's message and determine if they are initiating a science-backed trend analysis 
        on a specific compound, supplement, or recovery strategy, or if they are just chatting naturally or asking a casual follow-up.
        
        Take into consideration the conversation history context to track pronouns like 'it', 'this', or 'that'.
        
        {history_context}
        
        Athlete says: "{claim}"
        
        Select exactly one route options:
        - "RESEARCH_DEEP_DIVE" (If they explicitly name a supplement, wellness trend, require database records, or ask contextual follow-ups about them)
        - "CASUAL_CONVERSATION" (If they say hello, thank you, or ask an open-ended conversational greeting)
        """

        try:
            intent_response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=router_prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=IntentSchema,
                    temperature=0.1
                )
            )
            intent_json = json.loads(intent_response.text.strip())
            chosen_route = intent_json.get("route", "RESEARCH_DEEP_DIVE")
        except Exception as route_err:
            print(
                f"Routing check failed, defaulting to deep dive: {route_err}")
            chosen_route = "RESEARCH_DEEP_DIVE"

        if chosen_route == "CASUAL_CONVERSATION":
            chat_prompt = f"""
            You are CoachVerify. Answer this athlete's casual message or follow-up question in a friendly, 
            professional, and completely clear manner. Use plain English without jargon or data parameters.
            
            {history_context}
            
            Athlete says: "{claim}"
            """

            ai_response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=chat_prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=AuditResultSchema,
                    temperature=0.5
                )
            )
        else:
            prompt = f"""You are CoachVerify, an advanced sports science research auditor engineered to synthesize analytical insights.
Analyze the athlete's query objectively and exhaustively fill out the schema fields using data-grounded science from the provided database.
Take into consideration the past conversation history context to resolve any contextual references or follow-up syntax.

CRITICAL TONE & PLAIN-LANGUAGE STRUCTURAL DIRECTIVES:
- Speak normally, professionally, and objectively. Do not use generic filler words, dramatic jargon, or sports-coach clichés.
- MANDATE: The 'audit_text' field must be written in clear, plain language accessible to a high school student or parent under stress. 
- Avoid dense academic or medical jargon. If a technical term is found in the database, translate it into everyday English:
  * Do NOT say 'acute myocardial infarction' -> Say 'a sudden, severe heart attack'.
  * Do NOT say 'esophageal damage or ulcerations' -> Say 'painful throat burns and sores'.
  * Do NOT say 'ingesting raw caustic compounds' -> Say 'swallowing highly concentrated dry powders'.
- Keep your explanation to 2-3 direct sentences that move the user from uncertainty to clear, immediate action.
- STIPULATION: Use standard alphanumeric text and punctuation only. Do not output any graphical emojis or pictorial symbols.

{history_context}

ATHLETE QUERY: {claim}

VERIFIED SPORTS SCIENCE GROUNDING DATABASE:
{json.dumps(SPORTS_SCIENCE_DB, indent=2)}

RETURN SCHEMA FIELD REQUIREMENT MATCHING:
1. audit_text: Provide a concise clinical overview paragraph summarizing the core consensus findings. Do not insert HTML tags or markdown formatting.
2. Fill all other schema parameter fields—including the complete metadata fields nested within the individual_papers array items—with clean text values matching the database context.
"""
            ai_response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=AuditResultSchema,
                    temperature=0.2
                )
            )

        # clean up code blocks if present
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
            return jsonify({
                "error": "Response parsing failed",
                "details": f"AI returned invalid JSON: {str(je)}"
            }), 500

        session_history.append({"role": "Athlete", "content": claim})
        session_history.append(
            {"role": "CoachVerify", "content": processed_result.get("audit_text", "")})

        CHAT_MEMORIES[session_id] = session_history

        return jsonify(processed_result), 200

    except Exception as e:
        print(f"Backend error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
