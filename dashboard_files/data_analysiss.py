# Indian Restaurant Analytics Dashboard
# Stack: Streamlit · Plotly · Folium
# Dataset columns: Name, City, Region, Cuisines, Rating, Votes,
#                  Cost for Two, Online Delivery, Table Booking,
#                  Food Items, Google Maps URL

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
from collections import Counter

st.set_page_config(page_title="Indian Restaurant Analytics",
                   page_icon="🍽️", layout="wide",
                   initial_sidebar_state="expanded")

# ── Helper: set page background color ─────────────────────────
def set_bg(color):
    st.markdown(f"<style>.stApp, html, body {{ background-color: {color} !important; background-image: none !important; }}</style>",
                unsafe_allow_html=True)

# ── CSS: appearance only, all in one block ────────────────────
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=DM+Sans:wght@400;500;600;700&display=swap');
:root { --bg:#fdf6ee; --card:#ffffff; --border:#f0e6d6; --accent:#c0392b; --orange:#e67e22; --green:#27ae60; --gold:#f39c12; --text:#2c1810; --muted:#8d6e63; }
html,body,[class*="css"] { font-family:'DM Sans',sans-serif !important; background:var(--bg) !important; color:var(--text) !important; }
.main .block-container { padding:0 2rem 3rem; max-width:1400px; }
@keyframes fadeUp { from{opacity:0;transform:translateY(18px)} to{opacity:1;transform:translateY(0)} }
@keyframes glow   { 0%,100%{box-shadow:0 0 10px rgba(192,57,43,.25)} 50%{box-shadow:0 0 24px rgba(192,57,43,.55)} }
@keyframes slide  { from{opacity:0;transform:scaleY(.94) translateY(-6px)} to{opacity:1;transform:scaleY(1) translateY(0)} }
.header-bar { background:linear-gradient(135deg,#2c1810,#6d2b1a,#922b21); border-bottom:3px solid var(--accent); padding:16px 32px; margin:0 -2rem 28px; display:flex; align-items:center; justify-content:space-between; position:sticky; top:0; z-index:100; box-shadow:0 4px 20px rgba(44,24,16,.3); }
.header-logo { width:44px; height:44px; border-radius:12px; background:linear-gradient(135deg,#f39c12,#e67e22); display:flex; align-items:center; justify-content:center; font-size:1.3rem; animation:glow 3s ease-in-out infinite; }
.live-badge { background:rgba(243,156,18,.2); border:1px solid rgba(243,156,18,.5); color:#f39c12; font-size:.7rem; font-weight:700; padding:4px 12px; border-radius:20px; }
.kpi-card { background:var(--card); border:1.5px solid var(--border); border-radius:16px; padding:18px 16px; position:relative; overflow:hidden; animation:fadeUp .5s ease both; transition:transform .22s,box-shadow .22s; box-shadow:0 2px 12px rgba(44,24,16,.07); }
.kpi-card:hover { transform:translateY(-4px); box-shadow:0 10px 30px rgba(192,57,43,.1); border-color:var(--accent); }
.kpi-card::before { content:''; position:absolute; top:0; left:0; right:0; height:4px; border-radius:16px 16px 0 0; }
.purple::before{background:linear-gradient(90deg,#8e44ad,#3498db)} .gold::before{background:linear-gradient(90deg,#f39c12,#e67e22)}
.green::before{background:linear-gradient(90deg,#27ae60,#16a085)}  .orange::before{background:linear-gradient(90deg,#e67e22,#e91e8c)}
.pink::before{background:linear-gradient(90deg,#e91e8c,#8e44ad)}   .teal::before{background:linear-gradient(90deg,#16a085,#27ae60)}
.kpi-value { font-family:'Cormorant Garamond',serif; font-size:1.75rem; font-weight:700; line-height:1; }
.kpi-label { font-size:.68rem; color:var(--muted); text-transform:uppercase; letter-spacing:1px; margin-top:5px; font-weight:600; }
.section-card { background:var(--card); border:1.5px solid var(--border); border-radius:18px; padding:22px; margin-bottom:18px; animation:fadeUp .55s ease both; box-shadow:0 2px 12px rgba(44,24,16,.07); }
.section-title { font-size:1rem; font-weight:700; display:flex; align-items:center; gap:9px; margin-bottom:16px; }
.dot { width:9px; height:9px; border-radius:50%; display:inline-block; flex-shrink:0; }
.restaurant-card { background:linear-gradient(135deg,#fffaf7,#fff8f3); border:1.5px solid var(--border); border-radius:14px; padding:16px 20px; margin-bottom:10px; display:flex; align-items:center; gap:15px; animation:fadeUp .4s ease both; transition:border-color .22s,box-shadow .22s,transform .22s; box-shadow:0 2px 8px rgba(44,24,16,.07); }
.restaurant-card:hover { border-color:var(--accent); box-shadow:0 8px 28px rgba(192,57,43,.15); transform:translateY(-2px); }
.rank-badge { width:40px; height:40px; border-radius:12px; background:linear-gradient(135deg,#c0392b,#e67e22); display:flex; align-items:center; justify-content:center; font-weight:800; font-size:1rem; color:white; flex-shrink:0; box-shadow:0 4px 12px rgba(192,57,43,.35); }
.restaurant-name { font-weight:700; font-size:.97rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.restaurant-meta { font-size:.76rem; color:var(--muted); margin-top:3px; }
.tag { display:inline-block; font-size:.64rem; font-weight:600; padding:3px 9px; border-radius:20px; margin-right:5px; margin-top:5px; }
.tag-cuisine{background:#f3e5f5;color:#7b1fa2} .tag-region{background:#fce4ec;color:#c2185b} .tag-delivery{background:#e8f5e9;color:#2e7d32} .tag-booking{background:#e0f2f1;color:#00695c}
.rating-box { background:linear-gradient(135deg,#fff8e1,#fff3cd); border:1.5px solid #f9a825; border-radius:12px; padding:8px 13px; text-align:center; flex-shrink:0; box-shadow:0 2px 8px rgba(249,168,37,.2); }
.rating-number { font-family:'Cormorant Garamond',serif; font-size:1.4rem; font-weight:700; color:#e65100; line-height:1; }
.rating-stars { font-size:.58rem; color:#f9a825; margin-top:2px; }
.maps-button { display:inline-flex; align-items:center; gap:5px; background:linear-gradient(135deg,#27ae60,#2ecc71); color:white !important; text-decoration:none !important; font-size:.72rem; font-weight:700; padding:8px 14px; border-radius:9px; flex-shrink:0; white-space:nowrap; transition:opacity .18s,transform .18s; box-shadow:0 3px 10px rgba(39,174,96,.35); }
.maps-button:hover { opacity:.9; transform:scale(1.05); }
.menu-panel { background:linear-gradient(135deg,#fff8f3,#fff3e8); border:2px solid #e67e22; border-radius:16px; padding:22px 24px; margin-bottom:12px; animation:slide .35s ease both; box-shadow:0 8px 32px rgba(230,126,34,.15); }
.dish-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(142px,1fr)); gap:12px; }
.dish-card { background:white; border:1.5px solid var(--border); border-radius:13px; overflow:hidden; animation:fadeUp .35s ease both; transition:transform .22s,border-color .22s,box-shadow .22s; box-shadow:0 2px 8px rgba(44,24,16,.07); }
.dish-card:hover { transform:translateY(-5px); border-color:var(--orange); box-shadow:0 10px 24px rgba(230,126,34,.18); }
.dish-image { width:100%; height:92px; object-fit:cover; display:block; }
.dish-image-fallback { width:100%; height:92px; background:linear-gradient(135deg,#fff3e0,#ffe0b2); display:flex; align-items:center; justify-content:center; font-size:1.8rem; }
.dish-body{padding:9px 11px} .dish-name{font-size:.78rem;font-weight:600;color:var(--text)}
.dish-dot{display:inline-block;width:7px;height:7px;border-radius:50%;margin-right:4px} .dot-veg{background:#27ae60} .dot-nonveg{background:#c0392b}
.dish-type{font-size:.62rem;color:var(--muted);margin-top:3px}
.dish-cloud{display:flex;flex-wrap:wrap;gap:9px}
.dish-bubble { background:linear-gradient(135deg,#fff3e0,#ffe0b2); border:1.5px solid #ffcc80; color:#e65100; border-radius:22px; padding:5px 14px; font-size:.78rem; font-weight:600; }
.dish-bubble.large{font-size:.9rem;padding:7px 17px} .dish-bubble.small{font-size:.68rem;padding:4px 11px}
.map-container { border-radius:16px; overflow:hidden; border:2px solid var(--border); box-shadow:0 6px 28px rgba(44,24,16,.07); }
.map-legend{display:flex;gap:16px;flex-wrap:wrap;font-size:.76rem;color:var(--muted);margin-top:10px;font-weight:500}
.legend-dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px}
.no-results{text-align:center;padding:48px 20px;border-radius:16px;border:2px dashed var(--border);background:#fffaf7}
[data-testid="stSidebar"] { background:#a33c08 !important; border-right:3px solid #7a2b06 !important; }
[data-testid="stSidebar"] * { color:#fdeee6 !important; }
[data-testid="stSidebar"] label { color:#f5c9ad !important; font-size:.72rem !important; text-transform:uppercase; letter-spacing:.8px; }
[data-testid="stSidebar"] .stSelectbox>div>div, [data-testid="stSidebar"] .stTextInput input { background:rgba(255,255,255,.12) !important; border:1px solid rgba(255,255,255,.22) !important; color:#fdeee6 !important; border-radius:8px !important; }
::-webkit-scrollbar{width:6px} ::-webkit-scrollbar-track{background:#fdf6ee} ::-webkit-scrollbar-thumb{background:#d4a08a;border-radius:4px} ::-webkit-scrollbar-thumb:hover{background:#c0392b}
hr{border-color:var(--border) !important;margin:22px 0 !important}
</style>""", unsafe_allow_html=True)

# Dish image filenames — keys match EXACTLY the dish names in the dataset.
# Images are loaded from the local "images/" folder (downloaded by download_images.py).
# Fallback emoji shown if image file is not found.
DISH_IMAGE_FILES = {
    "Biryani":              "images/Biryani.jpg",
    "Naan":                 "images/Naan.jpg",
    "Paneer Butter Masala": "images/Paneer Butter Masala.jpg",
    "Chicken Curry":        "images/Chicken Curry.jpg",
    "Dosa":                 "images/Dosa.jpg",
    "Idli":                 "images/Idli.jpg",
    "Vada":                 "images/Vada.jpg",
    "Sambar":               "images/Sambar.jpg",
    "Thali Meals":          "images/Thali Meals.jpg",
    "Roti":                 "images/Roti.jpg",
    "Pizza":                "images/Pizza.jpg",
    "Pasta":                "images/Pasta.jpg",
    "Fried Rice":           "images/Fried Rice.jpg",
    "Noodles":              "images/Noodles.jpg",
    "Veg Meals":            "images/Veg Meals.jpg",
}

# Fallback emoji if image file missing (shown until download_images.py is run)
DISH_EMOJI = {
    "Biryani":"🍛","Naan":"🫓","Paneer Butter Masala":"🧀",
    "Chicken Curry":"🍗","Dosa":"🥞","Idli":"🍚","Vada":"🍩",
    "Sambar":"🥣","Thali Meals":"🍱","Roti":"🫓","Pizza":"🍕",
    "Pasta":"🍝","Fried Rice":"🍚","Noodles":"🍜","Veg Meals":"🥗",
    "default":"🍽️",
}

import base64, os

@st.cache_data
def load_dish_image_b64(dish_name):
    """Load a dish image from local folder and encode as base64 for inline HTML.
    Returns a data URI string ready to use in <img src=...>."""
    path = DISH_IMAGE_FILES.get(dish_name.strip())
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return f"data:image/jpeg;base64,{data}"
    return None  # will use emoji fallback

def get_dish_display(name):
    """Return base64 image URI or None. Also returns fallback emoji."""
    img_b64 = load_dish_image_b64(name)
    emoji   = DISH_EMOJI.get(name.strip(), DISH_EMOJI["default"])
    return img_b64, emoji

# ── City coordinates for the Folium map ───────────────────────
CITY_COORDS = {
    "Bangalore":(12.97,77.59), "Chennai":(13.08,80.27), "Delhi":(28.70,77.10),
    "Hyderabad":(17.38,78.48), "Kolkata":(22.57,88.36), "Mumbai":(19.07,72.87),
    "Pune":(18.52,73.85),      "Tirupati":(13.62,79.41),"Vijayawada":(16.50,80.64),
    "Visakhapatnam":(17.68,83.21),
}

NON_VEG    = ["chicken","mutton","fish","prawn","egg","meat","lamb","beef","pork","keema","biryani"]
CHART_COLS = ["#c0392b","#e67e22","#27ae60","#f39c12","#8e44ad","#16a085","#2980b9","#e91e8c"]
PLOT_STYLE = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                  font=dict(color="#8d6e63", family="DM Sans"), margin=dict(l=8,r=8,t=28,b=8),
                  xaxis=dict(gridcolor="#f0e6d6", linecolor="#d4a08a"),
                  yaxis=dict(gridcolor="#f0e6d6", linecolor="#d4a08a"))

# ── Helper functions ───────────────────────────────────────────
def make_dish_card_html(dish_name, veg_dot, veg_label):
    """Build a beautiful dish card using emoji + color gradient.
    No external images needed — works completely offline."""
    emoji, bg_color, text_color = get_dish_display(dish_name)
    return (
        f"<div class=\'dish-card\'>"
        f"<div style=\'width:100%;height:92px;background:linear-gradient(135deg,{bg_color},{bg_color}cc);"
        f"display:flex;align-items:center;justify-content:center;font-size:3rem;\'>"
        f"{emoji}</div>"
        f"<div class=\'dish-body\'>"
        f"<div class=\'dish-name\'>{dish_name}</div>"
        f"<div class=\'dish-type\'><span class=\'dish-dot {veg_dot}\'></span>{veg_label}</div>"
        f"</div></div>"
    )

def is_vegetarian(name):
    return not any(kw in name.lower() for kw in NON_VEG)

def make_stars(rating):
    filled = min(int(rating), 5)
    return "★" * filled + "☆" * (5 - filled)

def get_maps_url(name, city, raw_url):
    # Use the restaurant's own Google Maps URL from the dataset (correct per-restaurant link)
    if str(raw_url).startswith("http"):
        return raw_url
    # Fallback: search by restaurant name + city
    return f"https://www.google.com/maps/search/?api=1&query={name.replace(' ', '+')}+{city}"

def get_city_maps_url(city):
    # For map markers: open Google Maps at the city's exact coordinates
    # This ensures clicking a city marker goes to the correct city location
    coords = CITY_COORDS.get(city)
    if coords:
        lat, lon = coords
        return f"https://www.google.com/maps/search/restaurants/@{lat},{lon},13z"
    return f"https://www.google.com/maps/search/?api=1&query=restaurants+in+{city.replace(' ', '+')}"

@st.cache_data(show_spinner="Loading dataset…")
def load_dataset(file):
    df = pd.read_excel(file, engine="openpyxl") if file.name.endswith(("xlsx","xls")) else pd.read_csv(file)
    df.columns = [c.strip() for c in df.columns]
    for col in ["Rating", "Votes", "Cost for Two"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col].fillna(df[col].median(), inplace=True)
    text_cols = ["Name","City","Region","Cuisines","Online Delivery","Table Booking","Food Items","Google Maps URL"]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    return df

# ── Session state ──────────────────────────────────────────────
if "df"   not in st.session_state: st.session_state.df   = None
if "menu" not in st.session_state: st.session_state.menu = None

# ── Work with loaded data or an empty placeholder ─────────────
df = st.session_state.df if st.session_state.df is not None else pd.DataFrame(
    columns=["Name","City","Cuisines","Rating","Votes","Cost for Two"])

all_dishes = Counter(d.strip() for v in df["Food Items"].dropna()
                     for d in str(v).split(",") if d.strip()) if not df.empty else []

# ── Sidebar: upload + filters ─────────────────────────────────
with st.sidebar:
    st.markdown("<div style='padding:10px 0 10px;text-align:center;'><div style='font-size:1.8rem'>📂</div><div style='font-weight:700;font-size:1rem;margin-top:4px;'>Data Source</div></div>",
                unsafe_allow_html=True)
    file = st.file_uploader("Upload Excel/CSV", type=["xlsx","xls","csv"], label_visibility="collapsed")

    if file:
        file_id = file.name + str(file.size)
        if st.session_state.get("current_file_id") != file_id:
            st.session_state.df = load_dataset(file)
            st.session_state.current_file_id = file_id
            st.rerun()

    st.markdown("---")
    st.markdown("<div style='text-align:center;font-weight:700;font-size:1rem;margin-bottom:12px;'>🔍 Filters</div>",
                unsafe_allow_html=True)

    if not df.empty:
        st.markdown("<span style='font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#f39c12;'>🏙️ Filter by City</span>", unsafe_allow_html=True)
        sel_city = st.selectbox("", ["All"] + sorted(df["City"].unique()), key="city", label_visibility="collapsed")

        st.markdown("<span style='font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#2ecc71;'>🍜 Filter by Cuisine</span>", unsafe_allow_html=True)
        sel_cuisine = st.selectbox("", ["All"] + sorted(df["Cuisines"].unique()), key="cuisine", label_visibility="collapsed")

        st.markdown("<span style='font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#f9ca24;'>🍛 Filter by Food Item</span>", unsafe_allow_html=True)
        sel_dish = st.selectbox("", ["All"] + sorted(all_dishes.keys()), key="dish", label_visibility="collapsed")

        st.markdown("---")
        all_regions  = ["All"] + sorted(df["Region"].unique()) if "Region" in df.columns else ["All"]
        sel_region   = st.selectbox(" Region", all_regions)
        search_name  = st.text_input("Search by Name", placeholder="Type restaurant name…")
        min_rating   = st.slider(" Min Rating", float(df["Rating"].min()), float(df["Rating"].max()), float(df["Rating"].min()), step=0.1)
        max_cost     = st.slider(" Max Cost (₹)", 0, int(df["Cost for Two"].max()), int(df["Cost for Two"].max()), step=100)
        min_votes    = st.number_input("🗳️ Min Votes", min_value=0, value=0, step=50)
        top_n        = st.slider("🏆 Top N", 5, 30, 10)
        st.markdown("---")
        delivery_only = st.checkbox("🛵 Online Delivery Only")
        booking_only  = st.checkbox("📅 Table Booking Only")
    else:
        sel_city = sel_cuisine = sel_dish = sel_region = "All"
        search_name, min_rating, max_cost, min_votes, top_n = "", 0.0, 0, 0, 10
        delivery_only = booking_only = False
        st.info("Upload data to enable filters.")

# ── Apply filters ──────────────────────────────────────────────
fdf = df.copy()
if not df.empty:
    if sel_city    != "All": fdf = fdf[fdf["City"] == sel_city]
    if sel_cuisine != "All": fdf = fdf[fdf["Cuisines"].str.contains(sel_cuisine, case=False, na=False)]
    if sel_dish    != "All": fdf = fdf[fdf["Food Items"].str.contains(sel_dish, case=False, na=False)]
    if sel_region  != "All" and "Region" in fdf.columns: fdf = fdf[fdf["Region"] == sel_region]
    if search_name: fdf = fdf[fdf["Name"].str.contains(search_name, case=False, na=False)]
    fdf = fdf[(fdf["Rating"] >= min_rating) & (fdf["Cost for Two"] <= max_cost) & (fdf["Votes"] >= min_votes)]
    if delivery_only: fdf = fdf[fdf["Online Delivery"].str.lower() == "yes"]
    if booking_only:  fdf = fdf[fdf["Table Booking"].str.lower()  == "yes"]

# ── Welcome screen shown when no data is loaded ───────────────
if df.empty:
    set_bg("#fdf6ee")
    st.markdown("""
    <div style="min-height:80vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;">
        <div style="font-size:5rem;margin-bottom:20px;">🍽️</div>
        <h1 style="font-family:'Cormorant Garamond',serif;font-size:3rem;background:linear-gradient(135deg,#c0392b,#e67e22);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:10px;">
            Indian Restaurant Analytics
        </h1>
        <p style="font-size:1.1rem;color:#8d6e63;margin-bottom:30px;max-width:560px;line-height:1.7;">
            Discover insights, visualize cuisines, and explore restaurant data like never before.
        </p>
        <div style="background:linear-gradient(135deg,#fff8f3,#fff3e8);border:2px solid #f0c080;padding:18px 36px;border-radius:16px;">
            <p style="color:#6d2b1a;font-size:1rem;margin:0;font-weight:500;">
                👈 Please upload your <b>Excel</b> or <b>CSV</b> file using the <b>Sidebar</b> to begin.
            </p>
        </div>
    </div>""", unsafe_allow_html=True)
    st.stop()

# ── Dashboard starts here ──────────────────────────────────────
set_bg("#fdf6ee")

st.markdown("""
<div class='header-bar'>
    <div style='display:flex;align-items:center;gap:14px;'>
        <div class='header-logo'>🍽️</div>
        <div>
            <div style='font-weight:800;font-size:1.1rem;color:#f5e6dc;'>🇮🇳 Indian Restaurant Analytics</div>
            <div style='font-size:.72rem;color:#d4a08a;margin-top:2px;'>Final Year Project Dashboard</div>
        </div>
    </div>
    <span class='live-badge'>✦ Live Dashboard</span>
</div>""", unsafe_allow_html=True)

st.markdown(f"<p style='text-align:center;color:#8d6e63;font-size:.85rem;margin-top:-10px;margin-bottom:28px;'>Dataset Loaded: {len(df)} restaurants · Use the sidebar filters to explore</p>",
            unsafe_allow_html=True)

# ── KPI cards ──────────────────────────────────────────────────
avg_r    = fdf["Rating"].mean()       if not fdf.empty else 0
avg_c    = fdf["Cost for Two"].mean() if not fdf.empty else 0
top_cui  = fdf["Cuisines"].mode()[0]  if not fdf.empty else "—"
u_dishes = set(d.strip() for v in fdf["Food Items"].dropna() for d in str(v).split(","))

kpis = [("purple","🍽️",f"{len(fdf):,}","Total Restaurants"), ("gold","⭐",f"{avg_r:.2f}","Avg Rating"),
        ("green","🥇",top_cui[:14],"Top Cuisine"),           ("orange","💰",f"₹{avg_c:.0f}","Avg Cost (2)"),
        ("pink","🏙️",str(fdf["City"].nunique()),"Cities"),   ("teal","🍛",str(len(u_dishes)),"Unique Dishes")]

for col, (color, icon, val, lbl) in zip(st.columns(6), kpis):
    col.markdown(f"<div class='kpi-card {color}'><div style='font-size:1.5rem;margin-bottom:6px;'>{icon}</div>"
                 f"<div class='kpi-value'>{val}</div><div class='kpi-label'>{lbl}</div></div>",
                 unsafe_allow_html=True)

# ── Top N restaurants ──────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
active = " · ".join(x for x in [f"🏙️ {sel_city}" if sel_city!="All" else "",
                                  f"🍜 {sel_cuisine}" if sel_cuisine!="All" else "",
                                  f"🍛 {sel_dish}" if sel_dish!="All" else ""] if x) or "No active filters"
st.markdown(f"<div class='section-card'><div class='section-title'><span class='dot' style='background:#c0392b'></span>"
            f"🏆 Top {top_n} Restaurants <span style='font-size:.72rem;font-weight:400;color:#8d6e63;margin-left:6px;'>{active}</span></div></div>",
            unsafe_allow_html=True)

if fdf.empty:
    st.markdown("<div class='no-results'><div style='font-size:2.5rem'>🔍</div>"
                "<div style='font-size:1rem;color:#8d6e63;font-weight:600;margin-top:8px;'>No restaurants match your filters.</div></div>",
                unsafe_allow_html=True)
else:
    top_df = fdf.sort_values(["Rating","Votes"], ascending=[False,False]).drop_duplicates("Name").head(top_n).reset_index(drop=True)

    for idx, row in top_df.iterrows():
        name    = str(row.get("Name",          f"Restaurant {idx+1}"))
        city    = str(row.get("City",          ""))
        region  = str(row.get("Region",        ""))
        cuisine = str(row.get("Cuisines",      ""))
        rating  = float(row.get("Rating",      0))
        votes   = int(row.get("Votes",         0))
        cost    = int(row.get("Cost for Two",  0))
        food    = str(row.get("Food Items",    ""))

        # Build Google Maps URL:
        # If dataset has a valid URL, use it directly.
        # Otherwise search by "Restaurant Name City" for accurate location.
        raw_url  = str(row.get("Google Maps URL", ""))
        if raw_url.startswith("http"):
            maps_url = raw_url
        else:
            maps_url = f"https://www.google.com/maps/search/?api=1&query={name.replace(' ', '+')}+{city}"

        tags  = (f"<span class='tag tag-cuisine'>🍜 {cuisine}</span>" if cuisine not in ["","nan"] else "")
        tags += (f"<span class='tag tag-region'>📌 {region}</span>"   if region  not in ["","nan"] else "")
        tags += ("<span class='tag tag-delivery'>🛵 Delivery</span>"   if str(row.get("Online Delivery","No")).lower()=="yes" else "")
        tags += ("<span class='tag tag-booking'>📅 Booking</span>"     if str(row.get("Table Booking","No")).lower()=="yes"   else "")

        st.markdown(f"""
        <div class='restaurant-card'>
            <div class='rank-badge'>{idx + 1}</div>
            <div style='flex:1;min-width:0;'>
                <div class='restaurant-name'>{name}</div>
                <div class='restaurant-meta'>📍 {city} &nbsp;·&nbsp; 💰 ₹{cost} for two &nbsp;·&nbsp; 🗳️ {votes:,} votes</div>
                <div style='margin-top:3px;'>{tags}</div>
            </div>
            <div style='display:flex;align-items:center;gap:10px;flex-shrink:0;'>
                <div class='rating-box'>
                    <div class='rating-number'>{rating:.1f}</div>
                    <div class='rating-stars'>{make_stars(rating)}</div>
                </div>
                <a href='{maps_url}' target='_blank' class='maps-button'>🗺️ Maps</a>
            </div>
        </div>""", unsafe_allow_html=True)

        is_open = (st.session_state.menu == idx)
        if st.button("▼ Hide Menu" if is_open else "▶ View Menu", key=f"btn_{idx}"):
            st.session_state.menu = None if is_open else idx
            st.rerun()

        if is_open:
            dishes   = [d.strip() for d in food.split(",") if d.strip() and d.strip().lower() not in ["nan","none",""]]
            map_link = f"<a href='{maps_url}' target='_blank' style='color:#27ae60;font-weight:700;'>Open in Google Maps 🗺️</a>"

            if not dishes:
                st.markdown(
                    f"<div class='menu-panel'>"
                    f"<div style='font-size:1rem;font-weight:700;color:#e67e22;'>🍽️ {name}</div>"
                    f"<div style='font-size:.75rem;color:#8d6e63;margin-top:4px;'>{map_link}</div>"
                    f"<p style='color:#8d6e63;font-size:.84rem;margin-top:8px;'>Menu details not available in dataset.</p>"
                    f"</div>",
                    unsafe_allow_html=True)
            else:
                # Build dish name pills — veg (green dot) or non-veg (red dot)
                dish_pills = ""
                for d in dishes:
                    dot = "dot-veg"    if is_vegetarian(d) else "dot-nonveg"
                    lbl = "Veg"        if is_vegetarian(d) else "Non-Veg"
                    dot_color = "#27ae60" if is_vegetarian(d) else "#c0392b"
                    dish_pills += (
                        f"<div style='display:flex;align-items:center;gap:10px;"
                        f"background:white;border:1.5px solid #f0e6d6;"
                        f"border-radius:10px;padding:10px 16px;'>"
                        f"<span style='width:10px;height:10px;border-radius:50%;"
                        f"background:{dot_color};flex-shrink:0;display:inline-block;'></span>"
                        f"<span style='font-size:.88rem;font-weight:600;color:#2c1810;'>{d}</span>"
                        f"<span style='margin-left:auto;font-size:.7rem;font-weight:500;"
                        f"color:{dot_color};background:{'#e8f5e9' if is_vegetarian(d) else '#fce4ec'};"
                        f"padding:2px 8px;border-radius:20px;'>{lbl}</span>"
                        f"</div>"
                    )

                st.markdown(
                    f"<div class='menu-panel'>"
                    f"<div style='font-size:1rem;font-weight:700;color:#e67e22;margin-bottom:3px;'>"
                    f"🍽️ {name} — Menu Items</div>"
                    f"<div style='font-size:.75rem;color:#8d6e63;margin-bottom:16px;'>"
                    f"📍 {city} · {cuisine} · ⭐ {rating:.1f} · {map_link}</div>"
                    f"<div style='display:flex;flex-direction:column;gap:8px;'>{dish_pills}</div>"
                    f"</div>",
                    unsafe_allow_html=True)

# ── Popular dishes cloud ───────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
dish_freq = Counter(d.strip() for v in fdf["Food Items"].dropna() for d in str(v).split(",") if d.strip())
if dish_freq:
    mx   = max(dish_freq.values())
    bubs = "".join(f"<span class='dish-bubble {'large' if c/mx>.75 else ('small' if c/mx<.35 else '')}'>"
                   f"{d} <span style='opacity:.5;font-size:.7em;'>×{c}</span></span>"
                   for d, c in dish_freq.most_common(20))
    st.markdown(f"<div class='section-card'><div class='section-title'>"
                f"<span class='dot' style='background:#f39c12'></span>🍛 Popular Dishes</div>"
                f"<div class='dish-cloud'>{bubs}</div></div>", unsafe_allow_html=True)

# ── Charts ─────────────────────────────────────────────────────
st.markdown("<div class='section-title' style='margin-left:4px;'><span class='dot' style='background:#16a085'></span>📊 Analytics Charts</div>",
            unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("<div class='section-card'><div class='section-title'><span class='dot' style='background:#e67e22'></span>Restaurants by City</div>", unsafe_allow_html=True)
    if not fdf.empty:
        d = fdf["City"].value_counts().reset_index(); d.columns = ["City","Count"]
        fig = px.bar(d, x="City", y="Count", color="Count", color_continuous_scale=[[0,"#fff3e0"],[1,"#c0392b"]])
        fig.update_layout(**PLOT_STYLE, coloraxis_showscale=False); fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='section-card'><div class='section-title'><span class='dot' style='background:#27ae60'></span>Cuisine Distribution</div>", unsafe_allow_html=True)
    if not fdf.empty:
        d = fdf["Cuisines"].value_counts().reset_index(); d.columns = ["Cuisine","Count"]
        fig = px.pie(d, values="Count", names="Cuisine", hole=0.45, color_discrete_sequence=CHART_COLS)
        fig.update_layout(**PLOT_STYLE, showlegend=True, legend=dict(font=dict(color="#8d6e63",size=11)))
        fig.update_traces(textfont_color="#2c1810", pull=[0.02]*len(d)); st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    st.markdown("<div class='section-card'><div class='section-title'><span class='dot' style='background:#f39c12'></span>Rating Distribution</div>", unsafe_allow_html=True)
    if not fdf.empty:
        fig = px.histogram(fdf, x="Rating", nbins=15, color_discrete_sequence=["#f39c12"])
        fig.update_layout(**PLOT_STYLE); fig.update_traces(marker_line_width=0); st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col4:
    st.markdown("<div class='section-card'><div class='section-title'><span class='dot' style='background:#e91e8c'></span>Price Distribution (₹ for two)</div>", unsafe_allow_html=True)
    if not fdf.empty:
        fig = px.histogram(fdf, x="Cost for Two", nbins=20, color_discrete_sequence=["#e91e8c"])
        fig.update_layout(**PLOT_STYLE); fig.update_traces(marker_line_width=0); st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

col5, col6 = st.columns(2)
with col5:
    st.markdown("<div class='section-card'><div class='section-title'><span class='dot' style='background:#e91e8c'></span>Regional Distribution</div>", unsafe_allow_html=True)
    if not fdf.empty and "Region" in fdf.columns:
        d = fdf["Region"].value_counts().reset_index(); d.columns = ["Region","Count"]
        fig = px.bar(d, x="Region", y="Count", color="Region", color_discrete_sequence=CHART_COLS)
        fig.update_layout(**PLOT_STYLE, showlegend=False); fig.update_traces(marker_line_width=0); st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col6:
    st.markdown("<div class='section-card'><div class='section-title'><span class='dot' style='background:#16a085'></span>Delivery vs Table Booking</div>", unsafe_allow_html=True)
    if not fdf.empty:
        dy = int((fdf["Online Delivery"].str.lower()=="yes").sum()); dn = len(fdf) - dy
        by = int((fdf["Table Booking"].str.lower()=="yes").sum());   bn = len(fdf) - by
        fig = go.Figure([go.Bar(name="Online Delivery", x=["Yes","No"], y=[dy,dn], marker_color=["#27ae60","#f0e6d6"]),
                         go.Bar(name="Table Booking",   x=["Yes","No"], y=[by,bn], marker_color=["#16a085","#f0e6d6"])])
        fig.update_layout(**PLOT_STYLE, barmode="group", showlegend=True, legend=dict(font=dict(color="#8d6e63",size=11)))
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── Folium map ─────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div class='section-title' style='margin-left:4px;'><span class='dot' style='background:#27ae60'></span>🗺️ Restaurant Location Map</div>",
            unsafe_allow_html=True)
st.caption("Click any marker to see city stats and open Google Maps.")

if not fdf.empty:
    city_agg = fdf.groupby("City").agg(count=("Name","count"), avg_r=("Rating","mean"),
                                        top=("Name","first"), murl=("Google Maps URL","first")).reset_index()
    m = folium.Map(location=[20.59, 78.96], zoom_start=5, tiles="CartoDB Positron")

    for _, r in city_agg.iterrows():
        lat, lon = CITY_COORDS.get(r["City"], (20.5, 79.0))
        avg_r    = float(r["avg_r"])
        # Use city coordinates URL — NOT the restaurant's individual URL
        city_url = get_city_maps_url(r["City"])
        color    = "#27ae60" if avg_r >= 4.3 else ("#f39c12" if avg_r >= 4.0 else "#c0392b")
        popup    = (f"<div style='font-family:DM Sans,sans-serif;background:#fff8f3;color:#2c1810;"
                    f"padding:12px 16px;border-radius:12px;min-width:190px;border:1.5px solid #f0c080;'>"
                    f"<b style='color:#c0392b;'>{r['City']}</b><br>"
                    f"<span style='color:#8d6e63;font-size:.75rem;'>🍽️ {int(r['count'])} restaurants</span><br>"
                    f"<span style='color:#e67e22;font-size:.75rem;'>⭐ Avg {avg_r:.2f}</span><br>"
                    f"<span style='color:#8d6e63;font-size:.72rem;'>Top: {str(r['top'])[:28]}</span><br><br>"
                    f"<a href='{city_url}' target='_blank' style='background:linear-gradient(135deg,#27ae60,#2ecc71);"
                    f"color:white;text-decoration:none;padding:5px 12px;border-radius:8px;font-size:.72rem;font-weight:700;'>"
                    f"🗺️ Open Google Maps</a></div>")
        folium.CircleMarker(location=[lat,lon], radius=8+min(int(r["count"])//10,12),
                            color=color, fill=True, fill_color=color, fill_opacity=0.82,
                            popup=folium.Popup(popup, max_width=240),
                            tooltip=f"📍 {r['City']} · {int(r['count'])} restaurants · ⭐{avg_r:.1f}").add_to(m)

    st.markdown("<div class='map-container'>", unsafe_allow_html=True)
    st_folium(m, width="100%", height=480)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='map-legend'>"
                "<span><span class='legend-dot' style='background:#27ae60'></span>≥ 4.3 Excellent</span>"
                "<span><span class='legend-dot' style='background:#f39c12'></span>4.0–4.3 Good</span>"
                "<span><span class='legend-dot' style='background:#c0392b'></span>&lt;4.0 Average</span>"
                "<span style='color:#d4a08a;'>· Marker size = restaurant count</span></div>",
                unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────
st.markdown("<div style='text-align:center;color:#d4a08a;font-size:.75rem;padding:22px 0 8px;font-weight:500;'>"
            "🇮🇳 Indian Restaurant Analytics Dashboard · Built with Streamlit &amp; Plotly · Final Year Project"
            "</div>", unsafe_allow_html=True)
