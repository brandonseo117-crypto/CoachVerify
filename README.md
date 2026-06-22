# CoachVerify

### USAII Global AI Hackathon 2026 — High School Track (Grades 9-12)
**Challenge 1:** Help is Hard to Find  
**Direction B:** Rumor vs. Reality Tracker

---

## Project Overview
**CoachVerify** is a production-grade, AI-powered sports science research auditor designed to ground online health claims in peer-reviewed clinical reality. Built specifically to support the **Plainview community**, CoachVerify empowers parents, caregivers, and student-athletes under immense stress to separate dangerous, viral social media fitness trends (e.g., "dry-scooping") from verified scientific facts. 

Instead of relying on generic public LLMs that are prone to hallucinating or delivering unsafe medical diagnoses, CoachVerify leverages a strict, deterministic **Retrieval-Augmented Generation (RAG)** pipeline backed by automated **Pydantic/JSON validation** to deliver plain-language, structured, and non-diagnostic safety audits.

---

## The Problem & Human Impact
* **The Algorithmic Threat:** Up to 95% of teenagers use social media daily, where 6 in 10 fitness and nutrition posts contain scientifically inaccurate or unverified advice. 
* **High-Stakes Pressures:** High school student-athletes face unique, high-stress competitive environments where college scholarships, physical safety, and athletic careers are on the line. They are highly vulnerable to viral "shortcuts."
* **The Context Dilemma:** Stressed parents trying to protect their children are met with dense academic papers filled with clinical jargon or conflicting blog posts. They need quick, clear, and trustworthy guidance.

---

## Key Features & Capabilities
* **Grounded RAG Pipeline:** Circumvents the open web and restricts the LLM's context window entirely to an immutable local database of peer-reviewed sports science and medical literature.
* **Plain-Language Translation Layer:** Translates complex clinical terminology (e.g., *"esophageal ulcerations"*) into clear, digestible, and understandable terms (e.g., *"painful throat burns and sores"*).
* **Deterministic Guardrails:** Implements strict system boundaries that prohibit the tool from making medical diagnoses or clinical decisions, keeping it firmly as an educational tracker.
* **Structured Payload Interface:** Utilizes a Pydantic interceptor to enforce a strict JSON output schema, ensuring the user interface always cleanly displays three blocks: **Reality Consensus**, **Verified Source**, and **Safe Performance Alternatives**.

---

## Technical Stack
* **Backend:** Python, Flask Framework
* **Frontend:** Responsive HTML5, CSS3, JavaScript (Designed to reduce cognitive load)
* **AI Engine:** Google Gemini 2.5 Flash API
* **Data Validation & Structuring:** Pydantic (In-built schema modeling)
* **Data Core:** Curated Local Sports Science DB (Representing a production-scale pilot)

---

## AI Architecture & Data Flow
```
[ User Input / Claim ] 
         │
         ▼
[ RAG Engine Intercept ] ──> Queries ──> [ Curated Sports Science DB ]
         │                                         │
         ▼                                         ▼
[ Gemini 2.5 Flash API ] <── Context Injection ────┘
         │ (System Prompt Rules: Non-Diagnostic + Plain Language)
         ▼
[ Pydantic Validation Layer ] (Strict JSON Schema Enforcement)
         │
         ▼
[ UI Render ] ──> 1. Reality Consensus Summary
              ──> 2. Direct PubMed Reference Link (Human-in-the-Loop)
              ──> 3. Safe Alternative Checklist
```

---

## Responsible AI Requirements Fullfilled

### 1. Realistic Risk Identification
**Risk:** Generative models outputting accidental diagnostic or medical advice, causing users to over-rely on the system for clinical decisions rather than seeking human medical aid.

### 2. Concrete Mitigation Strategy
**Mitigation:** Hardcoded structural prompt limitations combined with a strict **Pydantic schema model**. If the model attempts to generate conversational filler, diagnostic summaries, or unexpected parameters, the payload is automatically rejected and dropped at the validation layer before hitting the UI.

### 3. Human-in-the-Loop Design
**The Boundary:** CoachVerify **does not** authorize supplement usage or pass medical judgments. 
**The Execution:** The system explicitly extracts and surfaces an unaltered, verified hyperlink to the original **PubMed** research. This gives the parent, athlete, and local school coaching staff full ownership and ultimate authority over final health and training decisions.

---

## 📈 What's Next for CoachVerify
* **Live API Ecosystems:** Scale the static pilot DB by migrating to active endpoints with open-access public research repositories (e.g., Consensus, Semantic Scholar APIs).
* **Automated Video Parsing:** Allow users to paste a direct TikTok or Instagram Reel URL, leverage Whisper/OCR text extraction, and automatically audit the spoken words or caption claims against medical reality.
