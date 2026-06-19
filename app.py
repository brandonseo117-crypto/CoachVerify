import os
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from google import genai
from google.genai import types  # 👈 Added to utilize the native SDK types layer
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

# 📊 Grounding database containing research parameters
SPORTS_SCIENCE_DB = {
    "dry_scooping": {
        "title": "Cardiovascular Strain of Concentrated Caffeine Ingestion in Adolescents",
        "consensus": "Highly Unsafe. Ingesting undiluted pre-workout powder causes rapid caffeine absorption into the bloodstream, triggering acute transient arterial hypertension (severe blood pressure spikes) and high risks of ventricular arrhythmia in developing adolescent cardiovascular systems.",
        "base_safety": 15,
        "base_performance": 45,
        "methodology": {
            "study_type": "Case-Control Retrospective Analysis & Observational Cohort",
            "sample_size": 42,
            "journal_authority": "Journal of Adolescent Health",
            "year": 2022,
            "population_demographics": "Adolescents aged 14-18 presenting with acute caffeine toxicity symptoms"
        }
    },
    "prime_energy": {
        "title": "Pediatric Risks of High-Caffeine Energy Drinks on Adolescent Metabolic Pathways",
        "consensus": "Unsafe for youth recovery. High stimulant loads (200mg+ caffeine) inhibit natural glycogen synthesis post-exercise, induce renal-level dehydration, and severely disrupt adolescent sleep architecture, which halts natural human growth hormone (HGH) release and muscle repair.",
        "base_safety": 30,
        "base_performance": 20,
        "methodology": {
            "study_type": "Randomized Double-Blind Placebo-Controlled Trial",
            "sample_size": 85,
            "journal_authority": "Pediatric Exercise Science",
            "year": 2023,
            "population_demographics": "Healthy active scholastic athletes (ages 13-17)"
        }
    },
    "creatine_monohydrate": {
        "title": "International Society of Sports Nutrition Position Stand: Creatine in Adolescent Athletes",
        "consensus": "Safe and clinically effective under proper guidance. Standard dosing (3-5g/day) safely accelerates ATP-PC energy system recovery and muscle protein synthesis without renal (kidney) impairment, provided the adolescent athlete is past puberty, well-hydrated, and consuming competitive-grade certified supplements.",
        "base_safety": 85,
        "base_performance": 90,
        "methodology": {
            "study_type": "Systematic Literature Review and Clinical Position Stand",
            "sample_size": 1200,
            "journal_authority": "Journal of the International Society of Sports Nutrition",
            "year": 2024,
            "population_demographics": "Developing human male and female competitive athletes, post-pubescent (ages 15-19)"
        }
    },
    "extreme_dehydration_weight_cuts": {
        "title": "Dehydration Strategies and Acute Kidney Injury in Scholastic Wrestling",
        "consensus": "Critically Dangerous. Utilizing plastic suits, saunas, or intentional severe fluid restriction to make a weight class causes severe hypovolemia (low blood volume), reducing cardiac output, disrupting electrolyte balances, and increasing the risk of acute kidney injury or heat stroke in adolescent bodies.",
        "base_safety": 5,
        "base_performance": 10,
        "methodology": {
            "study_type": "Multi-Center Retrospective Epidemiological Analysis",
            "sample_size": 310,
            "journal_authority": "American Journal of Sports Medicine",
            "year": 2021,
            "population_demographics": "Scholastic high school wrestlers (ages 14-18) actively competing"
        }
    }
}

# 🔐 NEW: Pydantic Schema mapping guarantees keys and type matching perfectly


class IndividualPaper(BaseModel):
    title: str
    journal: str
    pubmed_link: str
    paper_reliability: int


class AuditResultSchema(BaseModel):
    safety_score: int
    performance_score: int
    reliability_score: int
    matched_paper: str
    translated_consensus: str
    alternative_steps: List[str]
    individual_papers: List[IndividualPaper]


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
        3. **Rigorous Scientific Reliability Index**: Calculate an overall system `reliability_score` (0 to 100) and evaluate individual papers using the `methodology` data:
           - **Study Design (Max 40 pts)**: Meta-analyses, Systematic Reviews, and Randomized Controlled Trials (RCTs) score maximum points. Award fewer points for case reports or observational studies.
           - **Demographics Alignment (Max 40 pts)**: Check `population_demographics`. Does it match human adolescent athletes? If a study uses middle-aged adults or animal models, cap this subsection score below 15 points.
           - **Recency (Max 20 pts)**: Check `year`. Studies published within the last decade get full marks.
        4. **The Translation Layer**: Translate the complex medical findings of the study into clear, direct, and understandable English. Avoid intense academic jargon (e.g., instead of 'acute transient arterial hypertension', write 'a sudden, dangerous spike in blood pressure'). Keep it objective and authoritative.
        5. **Actionable Alternative Checklist**: Provide 2-3 safe, scientifically verified alternative steps the athlete can take instead to achieve their fitness goals safely.
        """

        # 🚀 UPGRADED: Explicitly pass Pydantic rules inside the generate engine configuration
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=AuditResultSchema,
            temperature=0.2  # Lowered temperature to minimize structural hallucinations
        )

        ai_response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=config
        )

        # 🛡️ BULLETPROOF: Safely clean out any edge-case string markdown closures before rendering
        raw_text = ai_response.text.strip()
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
