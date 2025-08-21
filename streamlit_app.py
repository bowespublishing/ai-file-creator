# app.py
import os
import base64
import textwrap
from datetime import datetime
from zoneinfo import ZoneInfo
import streamlit as st

# ——— Brand & content ———
BRAND_NAME    = "AI File Creator (Bonus)"
TAGLINE       = "We’re carrying out scheduled improvements."
ETA           = None                     # free text, also override with ?eta=...
ETA_ISO       = "2025-08-21T18:00"       # ISO 8601, override with ?eta_iso=...
CONTACT_EMAIL = "bowespublishing@gmail.com"
TWITTER_URL   = None                     # e.g., "https://x.com/yourhandle"
STATUS_URL    = None                     # e.g., "https://status.yourdomain.com"
LOGO_PATH     = "logo.png"               # local PNG/SVG recommended

# ——— Visuals ———
ACCENT_A = "#60A5FA"   # light blue
ACCENT_B = "#A78BFA"   # purple
CARD_BG  = "rgba(255,255,255,0.06)"

# ——— Query-string overrides (Streamlit 1.39+) ———
qs = st.query_params
if qs.get("eta"):
    ETA = qs.get("eta")
if qs.get("eta_iso"):
    ETA_ISO = qs.get("eta_iso")

# ——— Helpers ———
TZ = ZoneInfo("Europe/London")

def parse_eta_iso(value: str):
    try:
        dt = datetime.fromisoformat(value)
        dt = dt.replace(tzinfo=TZ) if dt.tzinfo is None else dt.astimezone(TZ)
        return dt
    except Exception:
        return None

def human_delta(to_dt: datetime):
    now = datetime.now(TZ)
    diff = (to_dt - now).total_seconds()
    if diff <= 0:
        return "now"
    mins = int(diff // 60)
    h, m = divmod(mins, 60)
    return "in " + (f"{h}h {m}m" if h else f"{m}m")

def email_link(addr: str) -> str:
    return f"mailto:{addr}" if addr else "#"

def logo_data_uri(path: str):
    if not path or not os.path.exists(path):
        return None
    ext = os.path.splitext(path)[1].lower()
    mime = "image/png" if ext == ".png" else ("image/svg+xml" if ext == ".svg" else "image/jpeg")
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{b64}"

# ——— Computed text ———
eta_text = "We’ll be back shortly."
if ETA:
    eta_text = f"Estimated back online: <b>{ETA}</b>"

countdown_line = ""
eta_dt = parse_eta_iso(ETA_ISO) if ETA_ISO else None
if eta_dt:
    countdown_line = f" <span style='opacity:.85'>(~{human_delta(eta_dt)})</span>"

contact_html = (
    f'Questions? Email <a href="{email_link(CONTACT_EMAIL)}"><b>{CONTACT_EMAIL}</b></a>.'
    if CONTACT_EMAIL else ""
)
last_updated = datetime.now(TZ).strftime("%d %b %Y, %H:%M %Z")
logo_uri = logo_data_uri(LOGO_PATH)
initials = ("".join([w[0] for w in BRAND_NAME.split() if w[:1].isalnum()])[:3] or "✨").upper()

# ——— Page config ———
st.set_page_config(
    page_title=f"{BRAND_NAME} — Maintenance",
    page_icon="🛠️",
    layout="wide",
)

# ——— HTML (dedented so Markdown won’t treat it as a code block) ———
html = textwrap.dedent(f"""\
<style>
  /* Remove Streamlit chrome */
  #MainMenu, header, footer {{ display: none !important; }}
  .block-container {{ padding-top: 2rem; padding-bottom: 2rem; max-width: 1100px; }}

  :root {{
    --accent-a: {ACCENT_A};
    --accent-b: {ACCENT_B};
  }}

  /* Animated gradient background */
  body, .stApp {{
    background: linear-gradient(120deg, #0b1020, #0b1c3a, #0b2e5b, #0b1020);
    background-size: 300% 300%;
    animation: bgShift 22s ease infinite;
  }}
  @keyframes bgShift {{
    0%   {{ background-position: 0% 50%; }}
    50%  {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
  }}

  /* Decorative glow */
  .bg-overlay:before {{
    content: "";
    position: fixed; inset: 0;
    background:
      radial-gradient(600px 300px at 10% 10%, color-mix(in oklab, var(--accent-a) 30%, transparent), transparent 60%),
      radial-gradient(600px 300px at 90% 90%, color-mix(in oklab, var(--accent-b) 30%, transparent), transparent 60%);
    pointer-events: none; opacity: .35;
  }}

  /* Hide run-status pill */
  .stStatusWidget, [data-testid="stStatusWidget"] {{ display: none !important; }}

  /* Card layout */
  .maint-wrap {{
    min-height: 82vh;
    display: grid; place-items: center; position: relative;
  }}

  .maint-card {{
    width: min(980px, 94vw);
    background: {CARD_BG};
    backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 22px;
    padding: clamp(26px, 4vw, 46px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.45);
    color: #ECF2FF;
  }}

  .maint-row {{
    display: grid; grid-template-columns: 120px 1fr;
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
    overflow: hidden;
  }}
  .logo-fallback {{
    font-size: 42px; line-height: 1; font-weight: 800;
    background: linear-gradient(45deg, var(--accent-a), var(--accent-b));
    -webkit-background-clip: text; background-clip: text; color: transparent;
  }}
  .logo-img {{ width: 100%; height: 100%; object-fit: contain; padding: 10px; }}

  .brand {{
    font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Apple Color Emoji","Segoe UI Emoji";
  }}
  .brand h1 {{
    margin: 0 0 6px 0; font-weight: 800; letter-spacing: .2px;
    font-size: clamp(28px, 4vw, 44px);
  }}
  .brand p {{ margin: 0; opacity: .92; font-size: clamp(15px, 1.6vw, 18px); }}

  .chip {{
    display: inline-flex; gap: 10px; align-items: center;
    padding: 8px 14px; border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.18);
    background: rgba(255,209,42,0.12); color: #FFD12A;
    font-weight: 700; letter-spacing: .3px; margin-top: 14px;
  }}

  .sections {{
    display: grid; gap: 16px; margin-top: 24px;
  }}
  .panel {{
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 16px; padding: 16px 18px;
    background: rgba(255,255,255,0.04);
  }}
  .panel h3 {{ margin: 0 0 10px 0; font-size: 18px; }}
  .panel ul {{ margin: 0; padding-left: 18px; opacity: .92; }}
  .panel li {{ margin: 6px 0; }}

  .cta {{ margin-top: 22px; display: flex; gap: 10px; flex-wrap: wrap; }}
  .btn {{
    text-decoration: none; color: #0d1117; background: #ECF2FF;
    border: 0; border-radius: 12px; padding: 10px 14px; font-weight: 700; display: inline-block;
  }}
  .btn.secondary {{ background: transparent; color: #ECF2FF; border: 1px solid rgba(255,255,255,0.3); }}
  .btn[aria-disabled="true"] {{ opacity: .55; cursor: not-allowed; }}

  .fine {{ margin-top: 18px; opacity: .7; font-size: 14px; }}
</style>
<div class="bg-overlay"></div>

<div class="maint-wrap">
  <div class="maint-card">
    <div class="maint-row">
      <div class="logo-wrap">
        {"<img class='logo-img' src='" + logo_uri + "' alt='Logo'/>" if logo_uri else f"<div class='logo-fallback' aria-label='Logo'>{initials}</div>"}
      </div>
      <div class="brand">
        <h1>{BRAND_NAME}</h1>
        <p>{TAGLINE}</p>
        <div class="chip">🛠️ Under maintenance</div>
      </div>
    </div>

    <div class="brand" style="margin-top:18px;">
      <p>{eta_text}{countdown_line}</p>
    </div>

    <div class="sections">
      <div class="panel">
        <h3>What’s happening</h3>
        <ul>
          <li>Speed & reliability improvements across key flows</li>
          <li>UI polish for a cleaner, more consistent experience</li>
          <li>A few frequently requested features from recent feedback</li>
        </ul>
      </div>
      <div class="panel">
        <h3>Stay in the loop</h3>
        <div class="cta">
          <a class="btn" href="#" onclick="parent.location.reload(); return false;">🔁 Try again</a>
          {"<a class='btn' target='_blank' rel='noopener' href='" + STATUS_URL + "'>📈 Status page</a>" if STATUS_URL else "<a class='btn secondary' aria-disabled='true'>📈 Status page</a>"}
          {"<a class='btn' target='_blank' rel='noopener' href='" + TWITTER_URL + "'>📣 Follow updates</a>" if TWITTER_URL else "<a class='btn secondary' aria-disabled='true'>📣 Follow updates</a>"}
        </div>
      </div>
    </div>

    <div class="fine brand">
      {contact_html} <span style="margin-left:.5rem; opacity:.6">Last updated: {last_updated}</span>
    </div>
  </div>
</div>

<meta name="robots" content="noindex,nofollow">
""")

st.markdown(html, unsafe_allow_html=True)
