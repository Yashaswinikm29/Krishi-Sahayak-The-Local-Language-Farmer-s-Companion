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

## 2. Presentation & Video Visuals

### Visual 0: Team & Project Introduction
This clean, text-focused cover page features a simple agricultural backdrop to introduce the project identity and the development team clearly without visual clutter.
* **Asset Name Reference:** `watermarked_img_2341123774389601600.png`

### Visual 1: The Core Challenges Facing Indian Farmers
This graphic illustrates the dual challenges the project addresses. On the left, a farmer in his field stands looking at a diseased leaf, symbolizing the struggle for quick crop advice. On the right, he is shown confused while looking at complex official paperwork, representing the accessibility barrier to government schemes.
* **Asset Name Reference:** `watermarked_img_8962192025486232687.png`

### Visual 2: How It Works (The Agentic Process)
This image visualizes the "agentic" workflow. It follows the farmer through the step-by-step thinking process of the AI, moving from image capture to the autonomous "check" and "search" functions, showing how the agent makes decisions before delivering a simplified diagnosis or eligibility result.
* **Asset Name Reference:** `watermarked_img_10884419478287486524.png`

### Visual 3: Tech Stack & Social Impact
This visual showcases the ultimate positive outcome. The farmer stands confidently in a healthy field holding his phone, which displays both a *disease diagnosis* and *scheme eligibility* update. The visual flow incorporates small icons for Google Gemini and Streamlit, connecting the technical architecture to the real-world impact.
* **Asset Name Reference:** `watermarked_img_11276199123581827667.png`

---

## 3. Detailed System Execution Walkthrough

### Module A: Crop Disease Diagnosis

#### 1. Initial State (Empty Upload Dashboard)
* **Visual Reference:** `WhatsApp Image 2026-07-02 at 11.26.14 AM.jpeg`
* **Details:** Clear upload interface supporting multiple Indian languages (defaulted to Kannada). Displays a prompt area on the right informing the user that the AI agent's live reasoning path will render dynamically upon file ingestion.

#### 2. Live Agent Logic & In-Execution Reasoning
* **Visual Reference:** `WhatsApp Image 2026-07-02 at 11.26.17 AM.jpeg`
* **Details:** This displays the agentic pipeline processing a sample image of a potato leaf infected with **Early Blight**. The dashboard records the internal logic blocks: pulling attributes, flagging severity as moderate, generating the explicit web query string `potato early blight treatment`, executing real-time web scans, and verifying complete synthesis execution.

#### 3. Structured Regional Diagnosis Report
* **Visual Reference:** `WhatsApp Image 2026-07-02 at 11.26.18 AM.jpeg`
* **Details:** Showcases the final synthesized response box in Kannada text (**Diagnosis Report – Kannada**). The output neatly outlines identified symptoms, chemical countermeasures (e.g., Chlorothalonil application thresholds), bio-agents (*Trichoderma viride* recommendations), cultural prevention methodologies, and guidelines on when to escalate issues to local agricultural extension offices.

---

### Module B: Scheme Simplifier

#### 1. Input Panel & Language Selection Matrix
* **Visual Reference:** `WhatsApp Image 2026-07-02 at 11.26.19 AM.jpeg`, `WhatsApp Image 2026-07-02 at 11.26.20 AM.jpeg`, `WhatsApp Image 2026-07-02 at 11.26.18 AM (1).jpeg`
* **Details:** Provides flexible parameters allowing users to paste custom policies or use presets like PM-KISAN. The multi-lingual selection matrix facilitates simple switching among Kannada, Hindi, Telugu, Tamil, and English. The form captures farmer specifics dynamically (e.g., 3-acre asset ownership profile, tax exemption status, and employment categories).

#### 2. Document Parsing & Structure Mapping
* **Visual Reference:** `WhatsApp Image 2026-07-02 at 11.26.20 AM (1).jpeg`
* **Details:** Illustrates **Step 1 (Scheme Rules Extracted)**. The agent parses legal parameters, itemizing institutional exclusions, income-tax constraints, and base financial benefits (Rs. 6,000 disbursed annually) into clean, separate attributes.

#### 3. Eligibility Verdict & Real-Time Search Ingestion
* **Visual Reference:** `WhatsApp Image 2026-07-02 at 11.26.20 AM (2).jpeg`
* **Details:** Displays the matching logs (**Step 2 to Step 4**). Shows an *UNCERTAIN* verification status warning the farmer that land-title records must align with specific chronological baseline criteria. Concurrently, it flags real-time 2026 updates fetched from the web (e.g., e-KYC compliance deadline and recent installment disbursements).

#### 4. Final Regional Summary Card
* **Visual Reference:** `WhatsApp Image 2026-07-02 at 11.26.20 AM (3).jpeg`
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
   git clone [https://github.com/your-username/krishi-sahayak.git](https://github.com/your-username/krishi-sahayak.git)
   cd krishi-sahayak
