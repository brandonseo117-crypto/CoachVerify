import os
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from google import genai          # Updated to the new SDK
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


API_key = os.getenv("gemini_key")
client = genai.Client(api_key=API_key)

SPORTS_SCIENCE_DB = {
    "dry_scooping": {
        "title": "Cardiovascular Strain of Concentrated Caffeine Ingestion in Adolescents",
        "consensus": "Highly Unsafe. Ingesting undiluted pre-workout powder causes rapid caffeine absorption into the bloodstream, triggering acute transient arterial hypertension (severe blood pressure spikes) and high risks of ventricular arrhythmia in developing adolescent cardiovascular systems.",
        "base_safety": 15,
        "base_performance": 45
    },
    "prime_energy": {
        "title": "Pediatric Risks of High-Caffeine Energy Drinks on Adolescent Metabolic Pathways",
        "consensus": "Unsafe for youth recovery. High stimulant loads (200mg+ caffeine) inhibit natural glycogen synthesis post-exercise, induce renal-level dehydration, and severely disrupt adolescent sleep architecture, which halts natural human growth hormone (HGH) release and muscle repair.",
        "base_safety": 30,
        "base_performance": 20
    },
    "creatine_monohydrate": {
        "title": "International Society of Sports Nutrition Position Stand: Creatine in Adolescent Athletes",
        "consensus": "Safe and clinically effective under proper guidance. Standard dosing (3-5g/day) safely accelerates ATP-PC energy system recovery and muscle protein synthesis without renal (kidney) impairment, provided the adolescent athlete is past puberty, well-hydrated, and consuming competitive-grade certified supplements.",
        "base_safety": 85,
        "base_performance": 90
    },
    "extreme_dehydration_weight_cuts": {
        "title": "Dehydration Strategies and Acute Kidney Injury in Scholastic Wrestling",
        "consensus": "Critically Dangerous. Utilizing plastic suits, saunas, or intentional severe fluid restriction to make a weight class causes severe hypovolemia (low blood volume), reducing cardiac output, disrupting electrolyte balances, and increasing the risk of acute kidney injury or heat stroke in adolescent bodies.",
        "base_safety": 5,
        "base_performance": 10
    }
}


@app.route('/api/audit', methods=['POST'])
def audit_reliability():
    try:

        user_data = request.json
        if not user_data:
            return jsonify({"error": "Invalid JSON payload provided."}), 400

        claim = user_data.get('claim', '').lower()
        routine = user_data.get('routine', '').lower()
        profile = user_data.get('profile', '')

        if not claim or not routine:
            return jsonify({"error": "Claim and routine are required fields."}), 400

        prompt = f"""You are CoachVerify, an automated expert sports medicine system calibrated for adolescent and pediatric exercise physiology. Your function is to act as an objective, clinical translation layer.

        ATHLETE PROFILE UNDER AUDIT:
        - Competitive/Age Level: {profile}
        - Proposed Trend/Product: {claim}
        - User's Proposed Routine: {routine}

        VERIFIED SPORTS SCIENCE GROUNDING DATABASE:
        {json.dumps(SPORTS_SCIENCE_DB, indent=2)}

        EXECUTION INSTRUCTIONS:
        1. **NLP Semantic Evaluation**: Analyze the user's input. Match it semantically against the concepts in our database. If it matches a concept (e.g., matching 'dry scoop' or 'powder before gym' to 'dry_scooping'), extract those values. If it does not match anything in our database, evaluate it using general adolescent sports science rules and flag it as 'External Medical Fact-Check'.
        2. **Context Gating**: Adjust the safety parameters based on the Athlete Profile. If the profile is 'Youth Sports' or 'Junior Varsity', lower safety thresholds aggressively if any stimulant or extreme method is mentioned.
        3. **The Translation Layer**: Translate the complex medical findings of the study into clear, direct, and understandable English. Avoid intense academic jargon (e.g., instead of 'acute transient arterial hypertension', write 'a sudden, dangerous spike in blood pressure'). Keep it objective and authoritative.
        4. **Actionable Alternative Checklist**: Provide 2-3 safe, scientifically verified alternative steps the athlete can take instead to achieve their fitness goals safely.

        OUTPUT FORMAT REQUIREMENTS:
        You must return your analysis as a raw, valid JSON object. Do not wrap it in markdown code blocks. Use this exact key structure:
        {{
            "safety_score": <integer from 0 to 100>,
            "performance_score": <integer from 0 to 100>,
            "matched_paper": "<Title of the study used>",
            "translated_consensus": "<Your plain-English translation text>",
            "alternative_steps": ["<Step 1>", "<Step 2>", "<Step 3>"]
        }}
        """

        # Updated syntax for the new google-genai library
        ai_response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config={'response_mime_type': 'application/json'}
        )

        processed_result = json.loads(ai_response.text)
        return jsonify(processed_result), 200

    except Exception as e:
        print(f"Backend processing error: {str(e)}")
        return jsonify({"error": "Internal engine parsing failure", "details": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
