import html
import random
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hello World Motion Lab", page_icon="✨", layout="wide")

st.title("✨ Hello World Motion Lab")
st.caption("Make your name move, change its style, and experiment with animated effects.")

with st.sidebar:
    st.header("Controls")
    name = st.text_input("Enter your name", value="Hello World", max_chars=80)
    font_family = st.selectbox(
        "Font type",
        ["Arial", "Courier New", "Georgia", "Times New Roman", "Verdana", "Trebuchet MS", "Impact"],
    )
    font_size = st.slider("Font size (px)", min_value=20, max_value=90, value=48)
    background = st.selectbox("Background", ["Light", "Dark", "Sunset", "Ocean", "Lavender"])
    name_mode = st.selectbox("Name display mode", ["Centered", "Ticker Tape", "Repeated"])
    effect = st.selectbox(
        "Dynamic action",
        ["None", "Rain", "Snow", "Hail", "Wind", "Confetti", "Tornado"],
    )
    speed = st.slider(
        "Animation speed",
        min_value=0.5,
        max_value=3.0,
        value=1.5,
        step=0.25,
        help="Higher values make the animation move faster.",
    )
    st.caption("Animations run inside the preview, so they loop continuously without repeatedly refreshing the app.")

backgrounds = {
    "Light": ("#f8fafc", "#172033"),
    "Dark": ("#10131c", "#f8fafc"),
    "Sunset": ("linear-gradient(135deg, #ffedd5, #fbcfe8, #ddd6fe)", "#4c1d3d"),
    "Ocean": ("linear-gradient(135deg, #cffafe, #93c5fd, #c7d2fe)", "#082f49"),
    "Lavender": ("linear-gradient(135deg, #f5f3ff, #e9d5ff, #fce7f3)", "#3b0764"),
}
bg, text_color = backgrounds[background]
safe_name = html.escape(name or "Your name", quote=True)
safe_font = font_family.replace("'", "").replace('"', "")

# Create particles for the selected effect. Their positions and delays are randomized
# once per preview; CSS animations then loop continuously in the embedded browser.
particles = []
symbols = {
    "Rain": ["💧", "💦"],
    "Snow": ["❄", "❅", "❆"],
    "Hail": ["🧊", "●"],
    "Wind": ["〰", "﹏", "➜", "💨"],
    "Confetti": ["🎉", "✨", "🎊", "●", "■", "▲"],
    "Tornado": ["🌪", "〰", "·"],
}
if effect != "None":
    count = 42 if effect in ("Rain", "Snow", "Hail", "Confetti") else 24
    for _ in range(count):
        symbol = random.choice(symbols[effect])
        left = random.randint(0, 100)
        delay = random.uniform(-8, 0)
        duration = random.uniform(2.0, 6.0) / speed
        size = random.randint(12, 28) if effect != "Tornado" else random.randint(16, 30)
        drift = random.randint(-90, 90) if effect in ("Snow", "Wind", "Confetti") else random.randint(-20, 20)
        particles.append(
            f'<span class="particle p-{effect.lower()}" '
            f'style="left:{left}%;--delay:{delay:.2f}s;--duration:{duration:.2f}s;'
            f'--size:{size}px;--drift:{drift}px">{html.escape(symbol)}</span>'
        )
particles_html = "".join(particles)

if name_mode == "Repeated":
    name_content = '<div class="repeated">' + "".join(
        f'<div>{safe_name}</div>' for _ in range(6)
    ) + "</div>"
elif name_mode == "Ticker Tape":
    name_content = f'<div class="ticker"><span>{safe_name}&nbsp;&nbsp; ✨ &nbsp;&nbsp;{safe_name}&nbsp;&nbsp; ✨ &nbsp;&nbsp;</span></div>'
else:
    name_content = f'<div class="centered">{safe_name}</div>'

html_doc = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; width: 100%; height: 100%; }}
.stage {{
  position: relative; width: 100%; height: 610px; overflow: hidden;
  border-radius: 18px; background: {bg}; color: {text_color};
  font-family: '{safe_font}', sans-serif;
}}
.particle-layer {{ position:absolute; inset:0; overflow:hidden; pointer-events:none; }}
.particle {{
  position:absolute; top:-12%; font-size:var(--size); opacity:.82;
  animation: fall var(--duration) linear var(--delay) infinite;
  will-change: transform;
}}
@keyframes fall {{
  0% {{ transform: translate3d(0,-5vh,0) rotate(0deg); opacity:0; }}
  10% {{ opacity:.9; }}
  100% {{ transform: translate3d(var(--drift), 125vh,0) rotate(540deg); opacity:.75; }}
}}
.p-rain, .p-hail {{ filter: saturate(1.15); }}
.p-wind {{ animation-name: gust; }}
@keyframes gust {{
  0% {{ transform:translate3d(-18vw, 0, 0) rotate(-12deg); opacity:0; }}
  15% {{ opacity:.9; }}
  100% {{ transform:translate3d(120vw, 32vh, 0) rotate(25deg); opacity:0; }}
}}
.p-tornado {{ animation-name: spiral; }}
@keyframes spiral {{
  0% {{ transform:translate3d(0,-10vh,0) rotate(0deg) scale(.65); opacity:0; }}
  15% {{ opacity:.85; }}
  100% {{ transform:translate3d(calc(var(--drift) * 2), 120vh,0) rotate(900deg) scale(1.25); opacity:0; }}
}}
.name-layer {{
  position:absolute; z-index:2; inset:0; display:flex; align-items:center;
  justify-content:center; padding:24px; font-size:{font_size}px;
  font-weight:800; line-height:1.2; text-align:center;
  overflow:hidden; overflow-wrap:anywhere;
  text-shadow: 0 2px 14px rgba(127,127,127,.18);
}}
.centered {{ max-width:100%; }}
.repeated {{ width:100%; display:flex; flex-direction:column; gap:12px; }}
.repeated div {{ white-space:nowrap; }}
.ticker {{ width:100%; overflow:hidden; white-space:nowrap; }}
.ticker span {{ display:inline-block; padding-left:100%; animation: marquee {max(5, 18 / speed):.2f}s linear infinite; }}
@keyframes marquee {{ from {{ transform:translateX(0); }} to {{ transform:translateX(-100%); }} }}
.hint {{ position:absolute; bottom:14px; right:18px; z-index:3; font-size:12px; opacity:.58; }}
</style>
</head>
<body>
  <div class="stage">
    <div class="particle-layer">{particles_html}</div>
    <div class="name-layer">{name_content}</div>
    <div class="hint">Hello World Motion Lab</div>
  </div>
</body>
</html>"""

components.html(html_doc, height=630, scrolling=False)

st.markdown(
    "Try changing the name, font, background, display mode, or dynamic action in the sidebar. "
    "The preview is a small browser-based animation playground."
)
