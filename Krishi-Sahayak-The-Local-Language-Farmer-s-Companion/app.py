import os
import io
import json
import time
from pathlib import Path

import streamlit as st
from PIL import Image
from google import genai
from google.genai import types
from google.genai import errors as genai_errors

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Krishi Sahayak | Farmer's Companion",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

MODEL_NAME   = "gemini-2.5-flash"
DEFAULT_API_KEY = "AQ.Ab8RN6LS4kNBLEQeaJrjPYvQ7JWV7kdljACIKXenuHcTPkdRSg"
LANGUAGES    = ["Kannada", "Hindi", "Telugu", "Tamil", "English"]
SCHEMES_DIR  = Path(__file__).parent / "schemes_data"

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
h1,h2,h3,h4 { font-family: 'Outfit', sans-serif !important; font-weight: 700 !important; }

.stApp { background: linear-gradient(150deg,#f0faf3 0%,#e8f5ec 50%,#f8fdf9 100%); }

/* ── Hero ── */
.ks-hero {
    background: linear-gradient(120deg,#14532d 0%,#16a34a 60%,#4ade80 100%);
    padding: 2rem 2.2rem; border-radius: 20px; color: white;
    box-shadow: 0 12px 40px rgba(22,163,74,0.30); margin-bottom: 1.5rem;
}
.ks-hero h1 { color:white !important; font-size:2rem !important; margin-bottom:.2rem; }
.ks-hero p  { color:#dcfce7; font-size:1rem; margin:0; }

/* ── Generic card ── */
.ks-card {
    background: white; border-radius: 16px;
    padding: 1.4rem 1.6rem;
    box-shadow: 0 4px 18px rgba(20,83,45,.07);
    border: 1px solid #d1fae5; margin-bottom: 1.2rem;
}
.ks-card h3 { color:#14532d !important; margin-bottom:.25rem; }
.ks-card p  { color:#374151; font-size:.97rem; }

/* ── Buttons ── */
.stButton>button {
    background: linear-gradient(120deg,#15803d,#22c55e);
    color: white !important; border: none; border-radius: 12px;
    padding: .65rem 1.5rem; font-weight: 700;
    font-family: 'Outfit', sans-serif; font-size: 1rem;
    width: 100%; box-shadow: 0 4px 14px rgba(21,128,61,.35);
    transition: transform .15s, box-shadow .15s;
}
.stButton>button:hover { transform:translateY(-2px); box-shadow:0 8px 22px rgba(21,128,61,.45); }
.stButton>button p { color:white !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { gap: 10px; }
.stTabs [data-baseweb="tab"] {
    background: white; border-radius: 12px 12px 0 0;
    padding: 10px 20px; font-family:'Outfit',sans-serif; font-weight:600;
}
.stTabs [data-baseweb="tab"] p { color:#14532d; }
.stTabs [aria-selected="true"] { background:linear-gradient(120deg,#15803d,#22c55e) !important; }
.stTabs [aria-selected="true"] p { color:white !important; }

/* ── Agent pipeline bar ── */
.agent-pipeline {
    display: flex; align-items: center; gap: 0; margin: 1.2rem 0 1.4rem;
    background: #f0fdf4; border-radius: 14px; padding: .8rem 1rem;
    border: 1px solid #bbf7d0; flex-wrap: wrap;
}
.agent-step {
    display: flex; align-items: center; gap: 8px;
    padding: .4rem .8rem; border-radius: 10px;
    font-family: 'Outfit', sans-serif; font-weight: 600; font-size: .85rem;
    color: #6b7280; background: #f9fafb; border: 1.5px solid #e5e7eb;
    transition: all .3s;
}
.agent-step.active {
    background: linear-gradient(120deg,#15803d,#22c55e);
    color: white; border-color: #15803d;
    box-shadow: 0 4px 12px rgba(21,128,61,.35);
}
.agent-step.done { background:#dcfce7; color:#15803d; border-color:#86efac; }
.agent-step.skipped { background:#fef9c3; color:#854d0e; border-color:#fde047; }
.step-arrow { color:#d1d5db; font-size:1.1rem; margin:0 4px; }

/* ── Step detail cards ── */
.step-card {
    border-radius: 14px; padding: 1.1rem 1.3rem; margin-bottom: .9rem;
    border-left: 5px solid; font-size: .97rem; line-height: 1.6;
}
.step-card.think  { background:#f0fdf4; border-color:#22c55e; }
.step-card.search { background:#eff6ff; border-color:#3b82f6; }
.step-card.skip   { background:#fefce8; border-color:#eab308; }
.step-card.final  { background:#faf5ff; border-color:#a855f7; }

.step-card h4 {
    font-family:'Outfit',sans-serif; font-weight:700; margin:0 0 .5rem;
    font-size:1rem;
}
.step-card.think  h4 { color:#15803d; }
.step-card.search h4 { color:#1d4ed8; }
.step-card.skip   h4 { color:#a16207; }
.step-card.final  h4 { color:#7e22ce; }

.step-card p, .step-card li { color:#1f2937 !important; }
.step-card strong { color:#111827; }

.badge {
    display:inline-block; padding:.15rem .55rem; border-radius:6px;
    font-size:.78rem; font-weight:700; font-family:'Outfit',sans-serif;
    margin-right:.4rem;
}
.badge-green  { background:#dcfce7; color:#15803d; }
.badge-blue   { background:#dbeafe; color:#1d4ed8; }
.badge-yellow { background:#fef9c3; color:#a16207; }
.badge-purple { background:#f3e8ff; color:#7e22ce; }

/* ── Final output box ── */
.ks-output {
    background: #ffffff; border-radius: 16px;
    border: 2px solid #22c55e;
    padding: 1.8rem 2rem; margin-top: 1rem;
    box-shadow: 0 8px 28px rgba(21,128,61,.12);
    color: #111827 !important; font-size: 1.05rem; line-height: 1.75;
}
.ks-output h1,.ks-output h2,.ks-output h3,.ks-output h4 {
    color: #14532d !important; font-family:'Outfit',sans-serif !important;
    margin-top:1.1rem; margin-bottom:.4rem;
}
.ks-output p    { color:#111827 !important; }
.ks-output li   { color:#1f2937 !important; margin-bottom:.25rem; }
.ks-output strong { color:#14532d; }
.ks-output-header {
    background: linear-gradient(120deg,#14532d,#16a34a);
    color: white; padding: .7rem 1.2rem; border-radius: 10px;
    font-family:'Outfit',sans-serif; font-weight:700; font-size:1.05rem;
    margin-bottom: 1rem;
}

/* ── Placeholder ── */
.ks-placeholder {
    text-align:center; color:#6b7280; padding:3rem 1.5rem;
    background:#f9fafb; border:1.5px dashed #d1d5db; border-radius:14px;
    font-size:.97rem;
}

/* ── Widget labels (selectbox / text_input / text_area titles) ── */
.stSelectbox label, .stTextInput label, .stTextArea label,
div[data-testid="stWidgetLabel"] label,
div[data-testid="stWidgetLabel"] p,
div[data-testid="stWidgetLabel"] span {
    color: #14532d !important;
    font-weight: 700 !important;
    font-size: .95rem !important;
    opacity: 1 !important;
    -webkit-text-fill-color: #14532d !important;
}

/* ── Force widgets themselves to a consistent light look
     (fixes dark-theme browsers making boxes dark + labels invisible) ── */
div[data-baseweb="select"] > div,
div[data-baseweb="base-input"],
.stTextInput input,
.stTextArea textarea {
    background-color: #ffffff !important;
    color: #111827 !important;
    border: 1.5px solid #bbf7d0 !important;
    border-radius: 10px !important;
}
div[data-baseweb="select"] * { color: #111827 !important; }
.stTextInput input::placeholder,
.stTextArea textarea::placeholder { color: #9ca3af !important; }

/* Dropdown popover menu (the list that opens on click) */
ul[data-testid="stSelectboxVirtualDropdown"],
div[data-baseweb="popover"] li {
    background-color: #ffffff !important;
    color: #111827 !important;
}
ul[data-testid="stSelectboxVirtualDropdown"] li:hover { background-color: #dcfce7 !important; }

/* Section sub-headings written with st.markdown("##### ...") */
.stApp h5, .stApp h6 { color: #14532d !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] { background:#052e16; }
section[data-testid="stSidebar"] * { color:#f0fdf4 !important; }
section[data-testid="stSidebar"] .stSelectbox label { color:#bbf7d0 !important; }

/* ── Info chips ── */
.chip {
    display:inline-block; padding:.25rem .75rem; border-radius:999px;
    font-size:.8rem; font-weight:600; font-family:'Outfit',sans-serif;
    margin:.2rem;
}
.chip-green  { background:#dcfce7; color:#15803d; border:1px solid #86efac; }
.chip-red    { background:#fee2e2; color:#b91c1c; border:1px solid #fca5a5; }
.chip-yellow { background:#fef9c3; color:#a16207; border:1px solid #fde047; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# API KEY
# ─────────────────────────────────────────────────────────────────────────────
def get_api_key():
    return (os.environ.get("GEMINI_API_KEY")
            or st.session_state.get("manual_api_key")
            or DEFAULT_API_KEY
            or None)


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌾 Krishi Sahayak")
    st.caption("Agentic AI · Farmer's Companion")
    st.markdown("---")
    api_key = get_api_key()
    if not api_key:
        st.markdown("### 🔑 Gemini API Key")
        st.warning("`GEMINI_API_KEY` not found. Enter below as fallback.")
        mk = st.text_input("Gemini API Key", type="password", key="manual_api_key_input")
        if mk:
            st.session_state["manual_api_key"] = mk
            st.rerun()
    else:
        st.success("✅ Gemini API Key active")

    st.markdown("---")
    st.markdown("""
**How the agent works:**

Each time you run a feature, the AI goes through multiple steps — it thinks, decides, searches the web if needed, and then gives you a personalised answer.

This is **agentic AI** — not just one prompt, but a chain of decisions.
""")

# ─────────────────────────────────────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ks-hero">
    <h1>🌾 Krishi Sahayak</h1>
    <p>Agentic AI that thinks step-by-step, searches live data, and gives farmers personalised answers in their language.</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# GUARD
# ─────────────────────────────────────────────────────────────────────────────
api_key = get_api_key()
if not api_key:
    st.error("⚠️ No Gemini API Key found. Please enter it in the sidebar.")
    st.stop()

try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Failed to initialise Gemini client: {e}")
    st.stop()


# ─────────────────────────────────────────────────────────────────────────────
# RETRY WRAPPER — handles Google's temporary 503 (server overload) and
# 429 (rate limit) errors automatically instead of crashing the app.
# ─────────────────────────────────────────────────────────────────────────────
def generate_with_retry(status_slot=None, max_retries=4, base_delay=6, **kwargs):
    """
    Calls client.models.generate_content(**kwargs) with automatic retry on
    503 UNAVAILABLE (server overloaded) and 429 RESOURCE_EXHAUSTED (rate limit).
    status_slot: an st.empty() placeholder to show live retry status (optional).
    """
    last_err = None
    for attempt in range(1, max_retries + 1):
        try:
            return client.models.generate_content(**kwargs)
        except genai_errors.ServerError as e:
            last_err = e
            wait = base_delay * attempt  # 6s, 12s, 18s, 24s
            if status_slot is not None:
                status_slot.markdown(step_card("skip", "⏳",
                    f"Gemini servers are busy — retrying in {wait}s… (attempt {attempt}/{max_retries})",
                    "<p style='color:#6b7280'>This is a temporary Google-side overload, not an app error. Sit tight.</p>"
                ), unsafe_allow_html=True)
            time.sleep(wait)
        except genai_errors.ClientError as e:
            msg = str(e)
            if "RESOURCE_EXHAUSTED" in msg or "429" in msg:
                last_err = e
                wait = base_delay * attempt
                if status_slot is not None:
                    status_slot.markdown(step_card("skip", "⏳",
                        f"Rate limit hit — retrying in {wait}s… (attempt {attempt}/{max_retries})",
                        "<p style='color:#6b7280'>Free-tier quota briefly exceeded. Waiting for it to reset.</p>"
                    ), unsafe_allow_html=True)
                time.sleep(wait)
            else:
                raise
    # All retries exhausted — surface a clean message instead of a raw traceback
    if status_slot is not None:
        status_slot.markdown(step_card("skip", "⚠️",
            "Gemini is still unavailable after several retries",
            "<p style='color:#6b7280'>Please wait a minute and click the button again.</p>"
        ), unsafe_allow_html=True)
    raise last_err


# ─────────────────────────────────────────────────────────────────────────────
# AGENT PIPELINE RENDERER  — shows live step-by-step cards as each step runs
# ─────────────────────────────────────────────────────────────────────────────
def render_pipeline_bar(labels, current_idx, skipped_idxs=None):
    skipped_idxs = skipped_idxs or []
    html = '<div class="agent-pipeline">'
    for i, label in enumerate(labels):
        if i < current_idx:
            cls = "done"
        elif i == current_idx:
            cls = "active"
        elif i in skipped_idxs:
            cls = "skipped"
        else:
            cls = ""
        html += f'<div class="agent-step {cls}">{label}</div>'
        if i < len(labels) - 1:
            html += '<span class="step-arrow">→</span>'
    html += '</div>'
    return html


def step_card(kind, icon, title, body_html):
    return f"""
<div class="step-card {kind}">
  <h4>{icon} {title}</h4>
  {body_html}
</div>"""


def json_to_html(obj):
    if isinstance(obj, dict):
        rows = "".join(
            f"<tr><td style='padding:.2rem .6rem;font-weight:600;color:#374151;white-space:nowrap'>{k}</td>"
            f"<td style='padding:.2rem .6rem;color:#111827'>{json_to_html(v)}</td></tr>"
            for k, v in obj.items()
        )
        return f"<table style='border-collapse:collapse;width:100%'>{rows}</table>"
    elif isinstance(obj, list):
        items = "".join(f"<li style='color:#1f2937'>{json_to_html(i)}</li>" for i in obj)
        return f"<ul style='margin:.3rem 0;padding-left:1.2rem'>{items}</ul>"
    else:
        val = str(obj)
        if val.lower() in ("true", "yes", "high", "eligible"):
            return f'<span class="chip chip-green">{val}</span>'
        elif val.lower() in ("false", "no", "severe", "not eligible"):
            return f'<span class="chip chip-red">{val}</span>'
        elif val.lower() in ("uncertain", "moderate", "medium"):
            return f'<span class="chip chip-yellow">{val}</span>'
        return f"<span style='color:#111827'>{val}</span>"


# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tab_a, tab_b = st.tabs(["📸 Crop Disease Diagnosis", "📄 Scheme Simplifier"])


# ══════════════════════════════════════════════════════════════════════════════
# TAB A
# ══════════════════════════════════════════════════════════════════════════════
with tab_a:
    st.markdown("""
<div class="ks-card">
  <h3>📸 Crop Disease Diagnosis</h3>
  <p>Upload a photo of the infected crop. The agent will <strong>think → decide → search live web if needed → give you a full answer</strong> in your language.</p>
</div>""", unsafe_allow_html=True)

    left, right = st.columns([1, 1.1], gap="large")

    with left:
        uploaded_image = st.file_uploader("Upload crop photo (PNG / JPG / JPEG)",
                                          type=["png","jpg","jpeg"],
                                          key="crop_img")
        lang_a = st.selectbox("Your language", LANGUAGES, key="lang_a")
        if uploaded_image:
            st.image(Image.open(uploaded_image), caption="Uploaded photo",
                     use_container_width=True)
        diagnose_btn = st.button("🔍 Diagnose Crop", key="diagnose_btn")

    with right:
        if not diagnose_btn:
            st.markdown("""
<div class="ks-placeholder">
  <div style="font-size:3rem">🤖</div>
  <p style="font-size:1.05rem;font-weight:600;color:#374151;margin:.5rem 0">
    Agent will work here</p>
  <p>Upload a photo and click <b>Diagnose Crop</b>.<br>
  You'll see every reasoning step as it happens.</p>
</div>""", unsafe_allow_html=True)

        elif uploaded_image is None:
            st.warning("Please upload a crop photo first.")

        else:
            image = Image.open(uploaded_image).convert("RGB")
            buf = io.BytesIO(); image.save(buf, format="JPEG")
            image_bytes = buf.getvalue()

            PIPELINE_A = ["🧠 Assess", "🔎 Web Search", "✅ Synthesise"]

            bar_slot    = st.empty()
            steps_slot  = st.container()
            output_slot = st.empty()

            # ── STEP 1 ──────────────────────────────────────────────────────
            bar_slot.markdown(render_pipeline_bar(PIPELINE_A, 0), unsafe_allow_html=True)

            with steps_slot:
                s1_slot = st.empty()
                s1_slot.markdown(step_card("think","🧠","Step 1 — Agent is reading the image and thinking…",
                    "<p style='color:#6b7280'>Identifying crop, disease, severity and deciding if live search is needed…</p>"),
                    unsafe_allow_html=True)

            try:
                assess_resp = generate_with_retry(
                    status_slot=s1_slot,
                    model=MODEL_NAME,
                    contents=[
                        types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                        """Return ONLY a JSON object with keys:
crop, diagnosis, confidence (low|medium|high), severity (none|mild|moderate|severe),
needs_live_lookup (true/false), search_query (string, or empty).
Set needs_live_lookup=true only when severity is moderate or severe."""
                    ],
                    config=types.GenerateContentConfig(response_mime_type="application/json"),
                )
                assessment = json.loads(assess_resp.text)
            except Exception:
                assessment = {"crop":"unclear","diagnosis":"unclear",
                              "confidence":"low","severity":"mild",
                              "needs_live_lookup":False,"search_query":""}

            s1_slot.markdown(step_card("think","🧠",
                "Step 1 — Initial Assessment Complete",
                json_to_html(assessment)
            ), unsafe_allow_html=True)

            # ── STEP 2 ──────────────────────────────────────────────────────
            needs_search = assessment.get("needs_live_lookup", False)
            grounded_info = None

            if needs_search:
                bar_slot.markdown(render_pipeline_bar(PIPELINE_A, 1), unsafe_allow_html=True)
                with steps_slot:
                    s2_slot = st.empty()
                    query = assessment.get("search_query") or assessment.get("diagnosis","crop disease")
                    s2_slot.markdown(step_card("search","🔎",
                        "Step 2 — Agent triggered Live Web Search",
                        f"<p><span class='badge badge-blue'>AUTO-DECIDED</span> Severity is <strong>{assessment.get('severity','moderate')}</strong> — agent is searching the web for current treatment info.</p>"
                        f"<p style='color:#374151'>🔍 Query: <em>{query}</em></p>"
                        f"<p style='color:#6b7280'>Fetching live results…</p>"
                    ), unsafe_allow_html=True)

                try:
                    search_resp = generate_with_retry(
                        status_slot=s2_slot,
                        model=MODEL_NAME,
                        contents=(
                            f"Search for up-to-date practical treatment information for "
                            f"'{assessment.get('diagnosis')}' in {assessment.get('crop')} crops in India. "
                            f"{query}. Give 3-4 sentences of the most useful current facts."
                        ),
                        config=types.GenerateContentConfig(
                            tools=[types.Tool(google_search=types.GoogleSearch())]
                        ),
                    )
                    grounded_info = search_resp.text
                except Exception as e:
                    grounded_info = f"Web search failed: {e}"

                s2_slot.markdown(step_card("search","🔎",
                    "Step 2 — Live Web Search Results",
                    f"<span class='badge badge-blue'>LIVE DATA</span>"
                    f"<p style='color:#1f2937;margin-top:.5rem'>{grounded_info}</p>"
                ), unsafe_allow_html=True)

            else:
                bar_slot.markdown(render_pipeline_bar(PIPELINE_A, 1, skipped_idxs=[1]), unsafe_allow_html=True)
                with steps_slot:
                    st.markdown(step_card("skip","⏭️",
                        "Step 2 — Web Search Skipped",
                        f"<span class='badge badge-yellow'>AGENT DECISION</span>"
                        f"<p>Severity is <strong>{assessment.get('severity','mild')}</strong> — agent decided live search is not needed. Using internal knowledge.</p>"
                    ), unsafe_allow_html=True)

            # ── STEP 3 ──────────────────────────────────────────────────────
            bar_slot.markdown(render_pipeline_bar(PIPELINE_A, 2), unsafe_allow_html=True)
            with steps_slot:
                s3_slot = st.empty()
                s3_slot.markdown(step_card("final","✅",
                    "Step 3 — Synthesising final answer…",
                    "<p style='color:#6b7280'>Combining assessment + live data → writing farmer-friendly answer in your language…</p>"
                ), unsafe_allow_html=True)

            live_block = (f"\nAdditional live information from the web: {grounded_info}" if grounded_info else "")
            final_resp = generate_with_retry(
                status_slot=s3_slot,
                model=MODEL_NAME,
                contents=f"""
You are a friendly agricultural advisor. Respond ENTIRELY in {lang_a}
(use {lang_a} script, not transliteration, unless {lang_a} is English).

Internal assessment JSON: {json.dumps(assessment)}
{live_block}

Write a clear Markdown answer with these exact sections:
1. **Crop Identified**
2. **Disease / Issue Diagnosis** (include confidence level)
3. **Symptoms Observed**
4. **Recommended Remedy** (include live info if present; give organic and chemical options)
5. **Prevention Tips**
6. **When to Consult an Expert**

Short sentences. Simple words. If unclear, ask for a better photo.
""",
            )

            s3_slot.markdown(step_card("final","✅",
                "Step 3 — Answer Ready",
                "<span class='badge badge-purple'>DONE</span> All steps complete. See full answer below."
            ), unsafe_allow_html=True)

            bar_slot.markdown(render_pipeline_bar(PIPELINE_A, 3), unsafe_allow_html=True)

            output_slot.markdown(
                f'<div class="ks-output">'
                f'<div class="ks-output-header">🌾 Diagnosis Report — {lang_a}</div>'
                f'{final_resp.text}'
                f'</div>',
                unsafe_allow_html=True,
            )


# ══════════════════════════════════════════════════════════════════════════════
# TAB B
# ══════════════════════════════════════════════════════════════════════════════
with tab_b:
    st.markdown("""
<div class="ks-card">
  <h3>📄 Government Scheme Simplifier</h3>
  <p>Paste or choose a scheme document and fill your details. The agent will <strong>extract rules → check YOUR eligibility → search for latest updates → give you a personalised answer</strong>.</p>
</div>""", unsafe_allow_html=True)

    left, right = st.columns([1, 1.1], gap="large")

    with left:
        sample_files = sorted(SCHEMES_DIR.glob("*.txt")) if SCHEMES_DIR.exists() else []
        sample_names = ["✍️ Paste my own text"] + [
            f.stem.replace("_"," ").title() for f in sample_files]

        selected = st.selectbox("Choose a sample scheme or paste your own",
                                sample_names, key="sample_sel")
        default_text = ""
        if selected != "✍️ Paste my own text":
            idx = sample_names.index(selected) - 1
            default_text = sample_files[idx].read_text(encoding="utf-8")

        policy_text = st.text_area("Scheme / policy text", value=default_text,
                                   height=260, key="policy_text")
        lang_b = st.selectbox("Your language", LANGUAGES, key="lang_b")

        st.markdown("##### 👤 Your Details — Agent will check if YOU qualify")
        c1, c2 = st.columns(2)
        with c1:
            land_size  = st.text_input("Land owned (e.g. 2 acres)", key="land_size")
            govt_job   = st.selectbox("Govt job / pension?", ["No","Yes"], key="govt_job")
        with c2:
            pays_tax   = st.selectbox("Paid income tax last year?", ["No","Yes"], key="pays_tax")
            farmer_type= st.selectbox("Farmer type",
                                      ["Owner farmer","Tenant farmer","Sharecropper"],
                                      key="farmer_type")

        simplify_btn = st.button("✨ Simplify Scheme", key="simplify_btn")

    with right:
        if not simplify_btn:
            st.markdown("""
<div class="ks-placeholder">
  <div style="font-size:3rem">🤖</div>
  <p style="font-size:1.05rem;font-weight:600;color:#374151;margin:.5rem 0">
    Agent will work here</p>
  <p>Select a scheme, fill your details and click <b>Simplify Scheme</b>.<br>
  Watch the agent reason through every step live.</p>
</div>""", unsafe_allow_html=True)

        elif not policy_text.strip():
            st.warning("Please paste or select some policy text first.")

        else:
            profile = {
                "land_size": land_size or "not specified",
                "has_govt_job_or_pension": govt_job,
                "paid_income_tax_last_year": pays_tax,
                "farmer_type": farmer_type,
            }

            PIPELINE_B = ["🧠 Extract Rules","🧮 Check Eligibility","🔎 Live Updates","✅ Synthesise"]
            bar_slot    = st.empty()
            steps_slot  = st.container()
            output_slot = st.empty()

            # ── STEP 1 ──────────────────────────────────────────────────────
            bar_slot.markdown(render_pipeline_bar(PIPELINE_B, 0), unsafe_allow_html=True)
            with steps_slot:
                s1_slot = st.empty()
                s1_slot.markdown(step_card("think","🧠",
                    "Step 1 — Agent is reading the scheme document…",
                    "<p style='color:#6b7280'>Extracting eligibility rules, benefits, exclusions and required documents…</p>"
                ), unsafe_allow_html=True)

            try:
                ext_resp = generate_with_retry(
                    status_slot=s1_slot,
                    model=MODEL_NAME,
                    contents=f"""Read this scheme text and return ONLY a JSON object with keys:
scheme_name, eligibility_rules (list), exclusions (list), benefits (list), documents_needed (list).
TEXT: \"\"\"{policy_text}\"\"\"""",
                    config=types.GenerateContentConfig(response_mime_type="application/json"),
                )
                extracted = json.loads(ext_resp.text)
            except Exception:
                extracted = {"scheme_name":"Unknown","eligibility_rules":[],
                             "exclusions":[],"benefits":[],"documents_needed":[]}

            s1_slot.markdown(step_card("think","🧠",
                "Step 1 — Scheme Rules Extracted",
                json_to_html(extracted)
            ), unsafe_allow_html=True)

            # ── STEP 2 ──────────────────────────────────────────────────────
            bar_slot.markdown(render_pipeline_bar(PIPELINE_B, 1), unsafe_allow_html=True)
            with steps_slot:
                s2_slot = st.empty()
                s2_slot.markdown(step_card("think","🧮",
                    "Step 2 — Agent is reasoning about YOUR profile…",
                    f"<p style='color:#6b7280'>Comparing your details against the extracted rules…</p>"
                    f"{json_to_html(profile)}"
                ), unsafe_allow_html=True)

            try:
                elig_resp = generate_with_retry(
                    status_slot=s2_slot,
                    model=MODEL_NAME,
                    contents=f"""Scheme rules JSON: {json.dumps(extracted)}
Farmer profile JSON: {json.dumps(profile)}
Return ONLY JSON with: likely_eligible (true|false|"uncertain"), reasoning (1-2 sentences).""",
                    config=types.GenerateContentConfig(response_mime_type="application/json"),
                )
                verdict = json.loads(elig_resp.text)
            except Exception:
                verdict = {"likely_eligible":"uncertain","reasoning":"Could not determine."}

            elig_val = verdict.get("likely_eligible", "uncertain")
            elig_chip = (
                "<span class='chip chip-green'>✅ LIKELY ELIGIBLE</span>" if elig_val is True or str(elig_val).lower()=="true"
                else "<span class='chip chip-red'>❌ LIKELY NOT ELIGIBLE</span>" if elig_val is False or str(elig_val).lower()=="false"
                else "<span class='chip chip-yellow'>⚠️ UNCERTAIN</span>"
            )
            s2_slot.markdown(step_card("think","🧮",
                "Step 2 — Personalized Eligibility Verdict",
                f"{elig_chip}<p style='margin-top:.6rem;color:#1f2937'>{verdict.get('reasoning','')}</p>"
            ), unsafe_allow_html=True)

            # ── STEP 3 ──────────────────────────────────────────────────────
            bar_slot.markdown(render_pipeline_bar(PIPELINE_B, 2), unsafe_allow_html=True)
            scheme_name = extracted.get("scheme_name","this scheme")
            with steps_slot:
                s3_slot = st.empty()
                s3_slot.markdown(step_card("search","🔎",
                    "Step 3 — Agent searching live web for 2026 updates…",
                    f"<span class='badge badge-blue'>AUTO-TRIGGERED</span>"
                    f"<p>Searching for latest news, deadlines, and changes to <strong>{scheme_name}</strong>…</p>"
                ), unsafe_allow_html=True)

            try:
                upd_resp = generate_with_retry(
                    status_slot=s3_slot,
                    model=MODEL_NAME,
                    contents=(
                        f"Search the web for the latest 2026 updates, deadlines, or changes "
                        f"to the Indian government scheme '{scheme_name}'. "
                        f"Summarise in 2-3 sentences what a farmer must know right now."
                    ),
                    config=types.GenerateContentConfig(
                        tools=[types.Tool(google_search=types.GoogleSearch())]
                    ),
                )
                live_updates = upd_resp.text
            except Exception as e:
                live_updates = f"Could not fetch live updates: {e}"

            s3_slot.markdown(step_card("search","🔎",
                "Step 3 — Live 2026 Updates Found",
                f"<span class='badge badge-blue'>LIVE DATA</span>"
                f"<p style='color:#1f2937;margin-top:.5rem'>{live_updates}</p>"
            ), unsafe_allow_html=True)

            # ── STEP 4 ──────────────────────────────────────────────────────
            bar_slot.markdown(render_pipeline_bar(PIPELINE_B, 3), unsafe_allow_html=True)
            with steps_slot:
                s4_slot = st.empty()
                s4_slot.markdown(step_card("final","✅",
                    "Step 4 — Synthesising your personalised answer…",
                    "<p style='color:#6b7280'>Combining scheme rules + your eligibility verdict + live updates → writing in your language…</p>"
                ), unsafe_allow_html=True)

            final_resp = generate_with_retry(
                status_slot=s4_slot,
                model=MODEL_NAME,
                contents=f"""
You are a helpful government scheme advisor. Respond ENTIRELY in {lang_b}
(use {lang_b} script, not transliteration, unless {lang_b} is English).

Scheme rules JSON: {json.dumps(extracted)}
Farmer profile JSON: {json.dumps(profile)}
Eligibility verdict JSON: {json.dumps(verdict)}
Latest live updates: {live_updates}

Write a clear Markdown answer with these exact sections:
1. **Scheme Name**
2. **In Simple Words** — 2-3 sentence plain summary
3. **Are You Eligible?** — personalised answer using the verdict above, explained simply
4. **Benefits** — bullet points
5. **Next Steps** — numbered, step by step
6. **Documents Needed** — bullet points
7. **Latest 2026 Updates** — from the live search above

No legal jargon. Short sentences.
""",
            )

            s4_slot.markdown(step_card("final","✅",
                "Step 4 — Personalised Answer Ready",
                "<span class='badge badge-purple'>DONE</span> All 4 steps complete. Full answer below."
            ), unsafe_allow_html=True)

            bar_slot.markdown(render_pipeline_bar(PIPELINE_B, 4), unsafe_allow_html=True)

            output_slot.markdown(
                f'<div class="ks-output">'
                f'<div class="ks-output-header">📄 Scheme Summary — {lang_b}</div>'
                f'{final_resp.text}'
                f'</div>',
                unsafe_allow_html=True,
            )

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;color:#6b7280;margin-top:2.5rem;padding-bottom:1rem;font-size:.9rem">
    Built with ❤️ for the <strong>Agents for Good</strong> track · Krishi Sahayak
</div>
""", unsafe_allow_html=True)
