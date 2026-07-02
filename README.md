# 🌾 Krishi Sahayak (ಕೃಷಿ ಸಹಾಯಕ) — Local Language Farmer's Companion
**Agentic AI Capstone Project** | *Track: Agents for Good*

---

## 👥 Project Team
* **Srusti M**
* **Sneha Nayak**
* **Sandhya H M**
* **Yashaswini K M**

---

## 1. Project Overview & Problem Statement
In India, small-scale and marginal farmers face two critical, day-to-day challenges that directly impact their livelihoods:

* **Delayed Crop Disease Diagnosis:** When crops are affected by pests or diseases, obtaining quick, localized, and expert advisory is highly difficult. Delayed actions lead to devastating yield losses.
* **Complex Government Schemes:** High-impact welfare programs like **PM-KISAN** are documented in convoluted, official language and dense legal text. Consequently, millions of eligible farmers miss out on financial benefits they rightfully deserve due to information barriers.

**Krishi Sahayak** addresses both challenges by leveraging multi-modal **Agentic AI**. It acts not merely as a regular conversational chatbot, but as an autonomous, intelligent agent that thinks step-by-step, performs live web queries when required, matches farmer profiles against policy criteria, and translates complex insights into the farmer’s regional language (e.g., Kannada, Hindi, Telugu, Tamil).

---


## 3. Detailed System Execution Walkthrough

### Module A: Crop Disease Diagnosis

#### 1. Initial State (Empty Upload Dashboard)
* **Visual Reference:** <img width="1600" height="693" alt="image" src="https://github.com/user-attachments/assets/80294078-86a8-43e8-853a-9ca362b99400" />

* **Details:** Clear upload interface supporting multiple Indian languages (defaulted to Kannada). Displays a prompt area on the right informing the user that the AI agent's live reasoning path will render dynamically upon file ingestion.

#### 2. Live Agent Logic & In-Execution Reasoning
* **Visual Reference:** <img width="1600" height="739" alt="image" src="https://github.com/user-attachments/assets/a3fea840-5efe-4a97-a7f0-e341648b46b4" />

* **Details:** This displays the agentic pipeline processing a sample image of a potato leaf infected with **Early Blight**. The dashboard records the internal logic blocks: pulling attributes, flagging severity as moderate, generating the explicit web query string `potato early blight treatment`, executing real-time web scans, and verifying complete synthesis execution.

#### 3. Structured Regional Diagnosis Report
* **Visual Reference:** <img width="1851" height="870" alt="Screenshot 2026-07-02 110929" src="https://github.com/user-attachments/assets/f108b694-ef0f-450d-8a2a-628f07ff7ffa" />

* **Details:** Showcases the final synthesized response box in Kannada text (**Diagnosis Report – Kannada**). The output neatly outlines identified symptoms, chemical countermeasures (e.g., Chlorothalonil application thresholds), bio-agents (*Trichoderma viride* recommendations), cultural prevention methodologies, and guidelines on when to escalate issues to local agricultural extension offices.

---

### Module B: Scheme Simplifier

#### 1. Input Panel & Language Selection Matrix
* **Visual Reference:** <img width="1168" height="807" alt="Screenshot 2026-07-02 111101" src="https://github.com/user-attachments/assets/a5cc0486-92c0-4e56-956d-f57a370bcf9a" />
<img width="1121" height="867" alt="Screenshot 2026-07-02 112055" src="https://github.com/user-attachments/assets/90f9e3fe-07e4-4d0d-a057-bf1ce4cee018" />

* **Details:** Provides flexible parameters allowing users to paste custom policies or use presets like PM-KISAN. The multi-lingual selection matrix facilitates simple switching among Kannada, Hindi, Telugu, Tamil, and English. The form captures farmer specifics dynamically (e.g., 3-acre asset ownership profile, tax exemption status, and employment categories).

#### 2. Document Parsing & Structure Mapping
* **Visual Reference:** <img width="1276" height="737" alt="image" src="https://github.com/user-attachments/assets/e8ff6fb0-f80f-44c3-bb49-4d752bfb1f36" />

* **Details:** Illustrates **Step 1 (Scheme Rules Extracted)**. The agent parses legal parameters, itemizing institutional exclusions, income-tax constraints, and base financial benefits (Rs. 6,000 disbursed annually) into clean, separate attributes.

#### 3. Eligibility Verdict & Real-Time Search Ingestion
* **Visual Reference:** <img width="1567" height="597" alt="image" src="https://github.com/user-attachments/assets/a2c5b365-70c6-4b21-876b-f4cd5d0fa1bc" />

* **Details:** Displays the matching logs (**Step 2 to Step 4**). Shows an *UNCERTAIN* verification status warning the farmer that land-title records must align with specific chronological baseline criteria. Concurrently, it flags real-time 2026 updates fetched from the web (e.g., e-KYC compliance deadline and recent installment disbursements).

#### 4. Final Regional Summary Card
* **Visual Reference:** <img width="1027" height="852" alt="image" src="https://github.com/user-attachments/assets/cfe301ed-b9a0-422a-965f-7c30ad3386c0" />

* **Details:** A completely localized dashboard readout (**Scheme Summary – Kannada**) converting dense legal policy guidelines into a highly actionable, user-centric checklist explaining exactly how, when, and where the farmer must apply to lock in welfare resources.

---

## 4. Technical Stack Architecture

* **Frontend UI Framework:** Streamlit (Python-based interactive web interface)
* **Core LLM & Vision Engine:** Google Gemini API (for image understanding, policy semantic mapping, and multi-lingual text synthesis)
* **Agent Framework Logic:** Python backend incorporating conditional branching, tool-use selection for live search orchestration, and stateful prompt engineering.

---

## 5. Local Setup & Installation

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/Yashaswinikm29/Krishi-Sahayak-The-Local-Language-Farmer-s-Companion.git]
   cd Krishi-Sahayak-The-Local-Language-Farmer-s-Companion

2. **Install Dependecies**
    ```bash
    pip install -r requirements.txt

3. **Configure Environment Variables:**
Create a .env file in the root directory and add your API key:
Code snippet
GEMINI_API_KEY=your_actual_api_key_here

5. **Run the Application:**
 ```bash
streamlit run app.py
