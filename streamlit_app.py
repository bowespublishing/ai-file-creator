# app.py
import os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import streamlit as st

# ——— Brand & content ———
BRAND_NAME   = "AI File Creator (Bonus)"
TAGLINE      = "We’re carrying out scheduled improvements."
ETA          = None  # Free text, e.g. "Today, 6 PM (UK)" (also override with ?eta=...)
ETA_ISO      = "2025-08-22T18:00"  # ISO 8601 for countdown, e.g. "2025-08-21T18:00" (or ?eta_iso=...)
CONTACT_EMAIL = "bowespublishing@gmail.com"
TWITTER_URL   = None  # e.g., "https://x.com/yourhandle"
STATUS_URL    = None  # e.g., "https://status.yourdomain.com"
LOGO_PATH     = "logo.png"  # local PNG/SVG recommended

# ——— Visuals ———
ACCENT_A = "#60A5FA"   # light blue
ACCENT_B = "#A78BFA"   # purple
CARD_BG  = "rgba(255,255,255,0.06)"

# ——— Query-string overrides (Streamlit 1.39+) ———
qs = st.query_params
if qs.get("eta"):      ETA = qs.get("eta")
if qs.get("eta_iso"):  ETA_ISO = qs.get("eta_iso")

# ——— Helpers ———
TZ = ZoneInfo("Europe/London")

def parse_eta_iso(value: str):
    """Parse ISO datetime safely; return aware datetime in Europe/London or None."""
    try:
        dt = datetime.fromisoformat(value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=TZ)
        else:
            dt = dt.astimezone(TZ)
        return dt
    except Exception:
        return None

def human_delta(to_dt: datetime):
    """Return a concise 'in 2h 15m' style delta (or 'now')."""
    now = datetime.now(TZ)
    diff = (to_dt - now).total_seconds()
    if diff <= 0:
        return "now"
    mins = int(diff // 60)
    hours, minutes = divmod(mins, 60)
    parts = []
    if hours: parts.append(f"{hours}h")
    if minutes or not parts: parts.append(f"{minutes}m")
    return "in " + " ".join(parts)

def email_link(addr: str) -> str:
    return f"mailto:{addr}" if addr else "#"

# ——— Page config ———
st.set_page_config(
    page_title=f"{BRAND_NAME} — Maintenance",
    page_icon="🛠️",
    layout="wide",
)

# ——— Global CSS ———
st.markdown(
    f"""
    <style>
      /* Reset chrome */
      #MainMenu, header, footer {{visibility: hidden;}}
      .block-container {{padding-top: 2rem; padding-bottom: 2rem; max-width: 1100px;}}

      :root {{
        --accent-a: {ACCENT_A};
        --accent-b: {ACCENT_B};
      }}

      /* Animated gradient background with motion preference */
      body, .stApp {{
        background: linear-gradient(120deg, #0b1020, #0b1c3a, #0b2e5b, #0b1020);
        background-size: 300% 300%;
        animation: bgShift 22s ease infinite;
      }}
      @media (prefers-reduced-motion: reduce) {{
        body, .stApp {{ animation: none; }}
      }}
      @keyframes bgShift {{
        0%   {{ background-position: 0% 50%; }}
        50%  {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
      }}

      /* Decorative grid glow */
      .bg-overlay:before {{
        content: "";
        position: fixed; inset: 0;
        background:
          radial-gradient(600px 300px at 10% 10%, color-mix(in oklab, var(--accent-a) 30%, transparent), transparent 60%),
          radial-gradient(600px 300px at 90% 90%, color-mix(in oklab, var(--accent-b) 30%, transparent), transparent 60%);
        pointer-events: none; opacity: .35;
      }}

      .maint-wrap {{
        min-height: 82vh; display: grid; place-items: center; position: relative;
      }}

      .maint-card {{
        width: min(900px, 92vw);
        background: {CARD_BG};
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 22px;
        padding: clamp(26px, 4vw, 46px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.45);
        color: #ECF2FF;
      }}

      .maint-row {{
        display: grid;
        grid-template-columns: 120px 1fr;
        gap: 28px; align-items: center;
      }}
      @media (max-width: 680px) {{
        .maint-row {{ grid-template-columns: 1fr; text-align: center; gap: 18px; }}
      }}

      .logo-wrap {{
        width: 120px; height: 120px; display: grid; place-items: center;
        border-radius: 24px;
        background:
          radial-gradient(140px 140px at 30% 20%, color-mix(in oklab, var(--accent-a) 24%, transparent), transparent),
          radial-gradient(160px 160px at 70% 80%, color-mix(in oklab, var(--accent-b) 24%, transparent), transparent),
          rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
      }}
      .logo-fallback {{
        font-size: 42px; line-height: 1; font-weight: 800;
        background: linear-gradient(45deg, var(--accent-a), var(--accent-b));
        -webkit-background-clip: text; background-clip: text; color: transparent;
      }}

      .brand {{
        font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Apple Color Emoji","Segoe UI Emoji";
      }}
      .brand h1 {{
        margin: 0 0 6px 0;
        font-weight: 800; letter-spacing: 0.2px;
        font-size: clamp(28px, 4vw, 44px);
      }}
      .brand p {{
        margin: 0; opacity: 0.92; font-size: clamp(15px, 1.6vw, 18px);
      }}

      .chip {{
        display: inline-flex; gap: 10px; align-items: center;
        padding: 8px 14px; border-radius: 999px;
        border: 1px solid rgba(255,255,255,0.18);
        background: rgba(255,209,42,0.12);
        color: #FFD12A; font-weight: 700; letter-spacing: 0.3px;
        margin-top: 14px;
      }}

      .cta {{ margin-top: 22px; display: flex; gap: 10px; flex-wrap: wrap; }}
      .btn {{
        text-decoration: none; color: #0d1117; background: #ECF2FF;
        border: 0; border-radius: 12px; padding: 10px 14px; font-weight: 700; display: inline-block;
      }}
      .btn.secondary {{
        background: transparent; color: #ECF2FF; border: 1px solid rgba(255,255,255,0.3);
      }}
      .btn[aria-disabled="true"] {{
        opacity: .55; cursor: not-allowed;
      }}

      .fine {{ margin-top: 18px; opacity: 0.7; font-size: 14px; }}

      /* Hide red "running" indicator for a cleaner look */
      .stStatusWidget, [data-testid="stStatusWidget"] {{ display: none; }}
    </style>
    <div class="bg-overlay"></div>
    """,
    unsafe_allow_html=True,
)

# ——— Content ———
st.markdown('<div class="maint-wrap"><div class="maint-card">', unsafe_allow_html=True)

# Header row (logo + text)
col_logo, col_text = st.columns([0.17, 0.83], vertical_alignment="center")
with col_logo:
    st.markdown('<div class="logo-wrap">', unsafe_allow_html=True)
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, use_container_width=True)
    else:
        # Fallback: gradient initials from brand name
        initials = "".join([w[0] for w in BRAND_NAME.split() if w[:1].isalnum()])[:3].upper() or "✨"
        st.markdown(f'<div class="logo-fallback" aria-label="Logo">{initials}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_text:
    st.markdown(
        f"""
        <div class="brand">
          <h1>{BRAND_NAME}</h1>
          <p>{TAGLINE}</p>
          <div class="chip">🛠️ Under maintenance</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Details / ETA block
eta_text_line = "We’ll be back shortly."
if ETA:
    eta_text_line = f"Estimated back online: <b>{ETA}</b>"

# ISO countdown (optional)
countdown_line = ""
eta_dt = parse_eta_iso(ETA_ISO) if ETA_ISO else None
if eta_dt:
    countdown_line = f" <span style='opacity:.85'>(~{human_delta(eta_dt)})</span>"

st.markdown(
    f"""
    <div class="brand" style="margin-top:18px;">
      <p>{eta_text_line}{countdown_line}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# CTAs (buttons adapt if missing URLs)
cta_cols = st.columns(3)
with cta_cols[0]:
    if st.button("🔁 Try again", type="primary"):
        st.rerun()

with cta_cols[1]:
    if STATUS_URL:
        st.link_button("📈 Status page", STATUS_URL, use_container_width=True)
    else:
        st.markdown('<a class="btn secondary" aria-disabled="true">📈 Status page</a>', unsafe_allow_html=True)

with cta_cols[2]:
    if TWITTER_URL:
        st.link_button("📣 Follow updates", TWITTER_URL, use_container_width=True)
    else:
        st.markdown('<a class="btn secondary" aria-disabled="true">📣 Follow updates</a>', unsafe_allow_html=True)

# Fine print & contact
contact_line = f'Questions? Email <a href="{email_link(CONTACT_EMAIL)}"><b>{CONTACT_EMAIL}</b></a>.' if CONTACT_EMAIL else ""
last_updated = datetime.now(TZ).strftime("%d %b %Y, %H:%M %Z")

st.markdown(
    f"""
    <div class="fine brand">
      {contact_line} <span style="margin-left:.5rem; opacity:.6">Last updated: {last_updated}</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# Close wrappers
st.markdown("</div></div>", unsafe_allow_html=True)

# SEO/Robots
st.markdown('<meta name="robots" content="noindex,nofollow">', unsafe_allow_html=True)
