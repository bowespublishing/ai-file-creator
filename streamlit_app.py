# app.py
import os
import streamlit as st

# ——— Settings you can tweak ———
BRAND_NAME = "AI Story Press"
TAGLINE = "We’re polishing things behind the scenes."
ETA = None  # e.g., "Today, 6 PM (UK)" — or pass ?eta=Today%206%20PM in the URL
CONTACT_EMAIL = "bowespublishing@gmail.com"  # change to your real inbox
TWITTER_URL = None  # e.g., "https://x.com/yourhandle"
STATUS_URL = None   # e.g., "https://status.yourdomain.com"
LOGO_PATH = "logo.png"  # optional local file; PNG/SVG recommended

# Allow quick ETA override via URL query param (Streamlit 1.39+)
eta_from_qs = st.query_params.get("eta")
if eta_from_qs:
    ETA = eta_from_qs

st.set_page_config(
    page_title=f"{BRAND_NAME} — Maintenance",
    page_icon="🛠️",
    layout="wide",
)

# ——— Global CSS (animated gradient + glass card) ———
st.markdown(
    """
    <style>
      /* Remove default chrome */
      #MainMenu, header, footer {visibility: hidden;}
      .block-container {padding-top: 2rem; padding-bottom: 2rem; max-width: 1100px;}

      /* Animated gradient background */
      body, .stApp {
        background: linear-gradient(120deg, #0d1117, #0b1a3a, #0b2e5b, #0d1117);
        background-size: 300% 300%;
        animation: bgShift 18s ease infinite;
      }
      @keyframes bgShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
      }

      /* Center wrapper */
      .maint-wrap {
        min-height: 80vh;
        display: grid;
        place-items: center;
      }

      /* Glass card */
      .maint-card {
        width: min(900px, 92vw);
        background: rgba(255,255,255,0.06);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 22px;
        padding: clamp(24px, 4vw, 44px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.45);
        color: #ECF2FF;
      }

      /* Layout: logo + text */
      .maint-row {
        display: grid;
        grid-template-columns: 110px 1fr;
        gap: 28px;
        align-items: center;
      }
      @media (max-width: 640px) {
        .maint-row { grid-template-columns: 1fr; text-align: center; }
      }

      /* Logo circle */
      .logo-wrap {
        width: 110px; height: 110px; display: grid; place-items: center;
        border-radius: 20px;
        background: radial-gradient(120px 120px at 30% 20%, #2aa6ff33, transparent),
                    radial-gradient(140px 140px at 70% 80%, #ffd12a33, transparent),
                    rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
      }

      .brand {
        font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Apple Color Emoji","Segoe UI Emoji";
      }
      .brand h1 {
        margin: 0 0 6px 0;
        font-weight: 800;
        letter-spacing: 0.2px;
        font-size: clamp(28px, 4vw, 44px);
      }
      .brand p {
        margin: 0;
        opacity: 0.92;
        font-size: clamp(15px, 1.6vw, 18px);
      }

      /* Status chip */
      .chip {
        display: inline-flex; gap: 10px; align-items: center;
        padding: 8px 14px; border-radius: 999px;
        border: 1px solid rgba(255,255,255,0.18);
        background: rgba(255,209,42,0.12);
        color: #FFD12A;
        font-weight: 700; letter-spacing: 0.3px;
        margin-top: 14px;
      }

      /* CTA row */
      .cta {
        margin-top: 22px; display: flex; gap: 10px; flex-wrap: wrap;
      }
      .cta a, .cta button {
        text-decoration: none; color: #0d1117;
        background: #ECF2FF;
        border: 0; border-radius: 12px; padding: 10px 14px; font-weight: 700;
      }
      .cta a.secondary {
        background: transparent; color: #ECF2FF; border: 1px solid rgba(255,255,255,0.3);
      }

      /* Fine print */
      .fine {
        margin-top: 18px; opacity: 0.7; font-size: 14px;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# ——— Content ———
st.markdown('<div class="maint-wrap"><div class="maint-card">', unsafe_allow_html=True)

# Logo: use local file if present; else show emoji fallback
col_logo, col_text = st.columns([0.17, 0.83])
with col_logo:
    st.markdown('<div class="logo-wrap">', unsafe_allow_html=True)
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, use_container_width=True)
    else:
        st.markdown(
            '<div style="font-size:56px; line-height:1;">✨</div>',
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

with col_text:
    st.markdown(
        f"""
        <div class="brand">
          <h1>{BRAND_NAME}</h1>
          <p>{TAGLINE}</p>
          <div class="chip">🛠️ Temporarily down for updates</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)  # close maint-row container column layout

# Details block
eta_line = f"Estimated back online: <b>{ETA}</b>" if ETA else "We’ll be back shortly."
contact_line = f"Questions? Email <b>{CONTACT_EMAIL}</b>." if CONTACT_EMAIL else ""
st.markdown(
    f"""
    <div class="brand" style="margin-top:18px;">
      <p>{eta_line}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# CTAs
cta_cols = st.columns(3)
with cta_cols[0]:
    if st.button("🔁 Try again"):
        st.rerun()
with cta_cols[1]:
    if STATUS_URL:
        st.link_button("📈 Status page", STATUS_URL)
    else:
        st.markdown('<div class="cta"><a class="secondary" href="#" onclick="return false;">📈 Status page</a></div>', unsafe_allow_html=True)
with cta_cols[2]:
    if TWITTER_URL:
        st.link_button("📣 Follow updates", TWITTER_URL)
    else:
        st.markdown('<div class="cta"><a class="secondary" href="#" onclick="return false;">📣 Follow updates</a></div>', unsafe_allow_html=True)

# Fine print
st.markdown(
    f"""
    <div class="fine brand">{contact_line}</div>
    """,
    unsafe_allow_html=True,
)

st.markdown("</div></div>", unsafe_allow_html=True)  # close .maint-card & .maint-wrap

# Optional: discourage indexing
st.markdown(
    '<meta name="robots" content="noindex,nofollow">',
    unsafe_allow_html=True
)
