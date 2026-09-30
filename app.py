"""app.py: FIXED LAYOUT. Do not put company-specific content here; edit config.py."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from config import (COMPANY, LABELS, SIDEBAR_NAV, KPIS, UNITS, HOURLY,
                    THRESHOLDS as T, CONTEXT, CONTEXT_TAKEAWAY)

ACC = COMPANY["accent"]
st.set_page_config(page_title=COMPANY["title"], page_icon="⚡", layout="wide")

# ---------- styling ----------
st.markdown(f"""
<style>

/* Force a light color scheme regardless of device preference */
:root {{
    color-scheme: light;
}}

.stApp {{
    background: #F4F6FB !important;
    color: #12172E !important;
}}

/* Main dashboard headings */
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4 {{
    color: #12172E !important;
    opacity: 1 !important;
}}

/* Normal body text */
.stApp [data-testid="stMarkdownContainer"] {{
    color: #252B45;
}}

/* Captions */
.stApp [data-testid="stCaptionContainer"],
.stApp [data-testid="stCaptionContainer"] p {{
    color: #59627A !important;
    opacity: 1 !important;
}}

/* Info message */
.stApp [data-testid="stAlert"] {{
    color: #252B45 !important;
    background: #EEF2FF !important;
    border: 1px solid #C7D2FE !important;
}}

/* KPI cards */
.stApp .card {{
    background: #FFFFFF !important;
    color: #12172E !important;
    border-color: #E7EAF3 !important;
    opacity: 1 !important;
}}

.stApp .card .lb {{
    color: #5B6280 !important;
}}

.stApp .card .v {{
    color: #12172E !important;
}}

.stApp .card .d {{
    color: #59627A !important;
}}

/* Tables */
.stApp [data-testid="stDataFrame"] {{
    background: #FFFFFF !important;
    color: #12172E !important;
}}

/* Inputs */
.stApp [data-testid="stMultiSelect"],
.stApp [data-testid="stSelectbox"] {{
    color: #12172E !important;
}}
/* Keep the app in light mode */
:root {{
    color-scheme: light;
}}

.stApp,
[data-testid="stAppViewContainer"] {{
    background-color: #F4F6FB !important;
    color: #12172E !important;
}}

/* Main content */
[data-testid="stMain"] {{
    background-color: #F4F6FB !important;
    color: #12172E !important;
}}

.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.stApp p,
.stApp label {{
    opacity: 1 !important;
}}

/* Sidebar */
[data-testid="stSidebar"] {{
    background-color: #FFFFFF !important;
    color: #252B45 !important;
}}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {{
    color: #252B45 !important;
    opacity: 1 !important;
}}

/* Cards */
.stApp .card {{
    background-color: #FFFFFF !important;
    color: #12172E !important;
    border-color: #E7EAF3 !important;
    opacity: 1 !important;
}}

/* Inputs */
.stApp input,
.stApp textarea,
.stApp [data-baseweb="select"] > div {{
    background-color: #FFFFFF !important;
    color: #12172E !important;
}}

/* Tables */
[data-testid="stDataFrame"] {{
    background-color: #FFFFFF !important;
    color: #12172E !important;
}}

</style>
""", unsafe_allow_html=True)

# ---------- data ----------
# ---------- data ----------
U, B, P, E = (
    LABELS["unit"],
    LABELS["booking"],
    LABELS["partner"],
    LABELS["eta"],
)

df = pd.DataFrame(
    UNITS,
    columns=[
        U,
        B,
        "Expected",
        P,
        E,
        "RTO %",
        "Util",
        "lat",
        "lon",
        "Change",
    ],
)

# Forecast shipment gap:
# positive = expected shipments are higher than current shipments
df["Forecast Gap"] = df["Expected"] - df[B]

df["Gap %"] = (
    df["Forecast Gap"].clip(lower=0) / df["Expected"] * 100
).round(0)


def status(r):
    if (
        r["Gap %"] >= T["attention_gap_pct"]
        or r[E] >= T["attention_eta"]
        or r["RTO %"] >= T["monitor_cancel"]
    ):
        return "Attention"

    if (
        r["Gap %"] >= T["monitor_gap_pct"]
        or r["RTO %"] >= T["monitor_cancel"]
    ):
        return "Monitor"

    return "Healthy"


df["Status"] = df.apply(status, axis=1)

# ---------- sidebar ----------
with st.sidebar:
    st.markdown(f"### {COMPANY['logo_text']}  {COMPANY['name']}")
    st.radio("Navigation", SIDEBAR_NAV, label_visibility="collapsed")
    st.divider()
    sel = st.multiselect(U, df[U].tolist(), default=df[U].tolist())
    st.caption(COMPANY["disclaimer"])
df = df[df[U].isin(sel)]
if df.empty:
    st.warning("Select at least one item.")
    st.stop()

# ---------- header ----------
c1, c2 = st.columns([4, 1])
with c1:
    st.markdown(
        f"<h2 style='color:#12172E !important; font-size:30px; font-weight:800; margin:0;'>"
        f"⚡ {COMPANY['title']}</h2>", unsafe_allow_html=True)
    st.markdown(
        f"<p style='color:#59627A !important; font-size:15px; margin-top:6px;'>"
        f"{COMPANY['subtitle']}</p>", unsafe_allow_html=True)
with c2:
    st.markdown(
        f"<div style='background:#FFFFFF; color:#12172E; border:1px solid #E7EAF3; "
        f"border-radius:14px; padding:16px; text-align:center; font-weight:600;'>"
        f"📅 {COMPANY['period_label']}</div>", unsafe_allow_html=True)
st.info(COMPANY["disclaimer"], icon="ℹ️")

# ---------- KPIs ----------
for col, k in zip(st.columns(len(KPIS)), KPIS):
    up = k["delta"].startswith("+")
    good = (up and k["good_when"] == "up") or (not up and k["good_when"] == "down")
    col.markdown(f"""<div class='card kpi'><div class='ic'>{k['icon']}</div><div>
        <div class='lb'>{k['label']}</div><div class='v'>{k['value']}</div>
        <div class='d'><span class='{"up" if good else "dn"}'>{"▲" if up else "▼"} {k['delta'][1:]}</span> {k['note']}</div>
        </div></div>""", unsafe_allow_html=True)
st.write("")

# shared chart look (readable on any browser theme)
CHART = dict(template="plotly_white", font=dict(color="#12172E"),
             plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF")

# ---------- map + hourly ----------
# ---------- map + hourly ----------
m, h = st.columns([1.1, 1])

with m:
    st.markdown(
        "<div class='h'>Regional Shipment Volume & RTO Risk</div>",
        unsafe_allow_html=True
    )

    fig = go.Figure(
        go.Scattermap(
            lat=df["lat"],
            lon=df["lon"],
            mode="markers+text",
            text=df[U],
            textposition="top right",

            marker=dict(
                size=(df[B] / 80).clip(lower=14, upper=42),
                color=df["RTO %"],
                colorscale="RdYlGn_r",
                cmin=df["RTO %"].min(),
                cmax=df["RTO %"].max(),
                showscale=True,
                colorbar=dict(title="RTO %"),
                opacity=0.8,
            ),

            customdata=df[
                [B, "Expected", "Forecast Gap", E, "RTO %"]
            ],

            hovertemplate=(
                "<b>%{text}</b><br>"
                "Shipments: %{customdata[0]}<br>"
                "Expected: %{customdata[1]}<br>"
                "Forecast Gap: %{customdata[2]}<br>"
                "Avg Delivery: %{customdata[3]} days<br>"
                "RTO: %{customdata[4]}%<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        map=dict(
            style="open-street-map",
            zoom=4.4,
            center=dict(lat=22.8, lon=79.0),
        ),
        height=360,
        margin=dict(l=0, r=0, t=0, b=0),
        **CHART
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "Marker size = shipment volume · "
        "Color intensity = RTO risk"
    )


with h:
    st.markdown(
        "<div class='h'>Projected Shipments vs Processing Capacity</div>",
        unsafe_allow_html=True
    )

    fig = go.Figure()

    fig.add_bar(
        x=HOURLY["hours"],
        y=HOURLY["demand"],
        name="Projected shipments",
        marker_color="#8C84F5",
    )

    fig.add_scatter(
        x=HOURLY["hours"],
        y=HOURLY["partners"],
        name="Estimated processing capacity",
        mode="lines+markers",
        line=dict(color="#16A34A", width=3),
    )

    gaps = [
        d - p
        for d, p in zip(
            HOURLY["demand"],
            HOURLY["partners"]
        )
    ]

    pk = gaps.index(max(gaps))

    fig.add_annotation(
        x=HOURLY["hours"][pk],
        y=HOURLY["demand"][pk],
        text="Peak forecast gap",
        showarrow=True,
        arrowcolor="#DC2626",
        bgcolor="#FFF1F2",
        font=dict(size=11, color="#B91C1C"),
    )

    fig.update_layout(
        height=360,
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(
            orientation="h",
            y=1.1
        ),
        hovermode="x unified",
        **CHART
    )

    fig.update_xaxes(gridcolor="#EEF0F6")
    fig.update_yaxes(gridcolor="#EEF0F6")

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ---------- ranking / alerts / actions ----------

a, b, c = st.columns([1.1, 1.1, 1])


# ---------- top regions ----------
with a:
    rows = ""

    for _, r in df.sort_values(
        B, ascending=False
    ).iterrows():

        rows += (
            f"<tr>"
            f"<td><b>{r[U]}</b></td>"
            f"<td>{r[B]}</td>"
            f"<td class='up'>▲ {r['Change']}%</td>"
            f"</tr>"
        )

    st.markdown(
        f"""
        <div class='card'>
            <div class='h'>Top Regions by Shipments</div>
            <table class='t'>
                <tr>
                    <th>{U}</th>
                    <th>{B}</th>
                    <th>Change</th>
                </tr>
                {rows}
            </table>
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------- alerts ----------
with b:

    alerts = df[
        (df["RTO %"] >= T["monitor_cancel"])
        | (df[E] >= T["attention_eta"])
        | (df["Gap %"] >= T["monitor_gap_pct"])
    ].sort_values(
        ["RTO %", E],
        ascending=False
    )

    rows = ""

    for _, r in alerts.iterrows():

        impact = (
            f"RTO {r['RTO %']}% · "
            f"{r[E]} days delivery"
        )

        rows += (
            f"<tr>"
            f"<td><b>{r[U]}</b></td>"
            f"<td>{impact}</td>"
            f"<td><span class='badge {r['Status']}'>"
            f"{r['Status']}</span></td>"
            f"</tr>"
        )

    if not rows:
        rows = (
            "<tr>"
            "<td colspan='3'>All regions within monitored thresholds ✅</td>"
            "</tr>"
        )

    st.markdown(
        f"""
        <div class='card'>
            <div class='h'>⚠️ Logistics Risk Alerts</div>
            <table class='t'>
                <tr>
                    <th>{U}</th>
                    <th>Impact</th>
                    <th>Status</th>
                </tr>
                {rows}
            </table>
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------- recommended actions ----------
with c:

    acts = []

    # Largest forecast gap
    biggest_gap = df.sort_values(
        "Forecast Gap",
        ascending=False
    ).iloc[0]

    acts.append(
        f"Review capacity planning for <b>{biggest_gap[U]}</b> "
        f"where the forecast shows a shortfall of "
        f"<b>{int(biggest_gap['Forecast Gap'])}</b> shipments."
    )

    # Highest RTO
    highest_rto = df.sort_values(
        "RTO %",
        ascending=False
    ).iloc[0]

    acts.append(
        f"Investigate the high RTO rate in "
        f"<b>{highest_rto[U]}</b> "
        f"({highest_rto['RTO %']}%) — review address quality, "
        f"delivery attempts and customer availability."
    )

    # Slowest delivery
    slowest = df.sort_values(
        E,
        ascending=False
    ).iloc[0]

    acts.append(
        f"Review delivery performance in "
        f"<b>{slowest[U]}</b>, where average delivery time "
        f"is <b>{slowest[E]} days</b>."
    )

    body = "".join(
        f"""
        <div class='act'>
            <div class='num'>{i + 1}</div>
            <div>{t}</div>
        </div>
        """
        for i, t in enumerate(acts)
    )

    st.markdown(
        f"""
        <div class='card'>
            <div class='h'>✨ Recommended Actions</div>
            {body}
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")


# ---------- performance table ----------
st.markdown(
    f"<div class='h'>Regional Logistics Performance</div>",
    unsafe_allow_html=True
)

show = df[
    [
        U,
        B,
        "Expected",
        "Forecast Gap",
        E,
        "RTO %",
        "Util",
        "Status",
    ]
].rename(
    columns={
        "Expected": "Expected Shipments",
        "Forecast Gap": "Forecast Gap",
        E: "Avg Delivery Time",
        "Util": "Utilization (%)",
    }
)

st.dataframe(
    show,
    hide_index=True,
    use_container_width=True
)

st.download_button(
    "⬇️ Export CSV",
    show.to_csv(index=False),
    "shiprocket_logistics_report.csv",
    "text/csv"
)

# ---------- performance table ----------
# ---------- performance table ----------
st.markdown(
    f"<div class='h'>Regional Logistics Performance</div>",
    unsafe_allow_html=True
)

show = df[
    [
        U,
        B,
        "Expected",
        "Forecast Gap",
        E,
        "RTO %",
        "Util",
        "Status",
    ]
].rename(
    columns={
        "Expected": "Expected Shipments",
        "Forecast Gap": "Forecast Gap",
        E: "Avg Delivery Time",
        "Util": "Utilization (%)",
    }
)

st.dataframe(
    show,
    hide_index=True,
    use_container_width=True
)

st.download_button(
    "⬇️ Export CSV",
    show.to_csv(index=False),
    "shiprocket_logistics_report.csv",
    "text/csv",
    key="shiprocket_report_download"
)
# ---------- public context (the "I did my research" strip) ----------
st.markdown("<div class='h' style='margin-top:14px'>What we know publicly</div>",
            unsafe_allow_html=True)
for col, (big, txt, src) in zip(st.columns(len(CONTEXT)), CONTEXT):
    col.markdown(f"<div class='card ctx'><b>{big}</b><small>{txt}</small><span class='src'>{src}</span></div>",
                 unsafe_allow_html=True)
st.caption(f"💡 {CONTEXT_TAKEAWAY}")
st.caption(COMPANY["prepared_by"])
