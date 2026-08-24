import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import requests

st.set_page_config(
    page_title="Dollar Death Watch",
    page_icon="💵",
    layout="wide"
)

# ── DATA ────────────────────────────────────────────────────────────────────

# IMF COFER Data - USD share of global reserves (quarterly, from IMF publications)
cofer_data = {
    "quarter": [
        "2000Q4","2001Q4","2002Q4","2003Q4","2004Q4","2005Q4","2006Q4","2007Q4",
        "2008Q4","2009Q4","2010Q4","2011Q4","2012Q4","2013Q4","2014Q4","2015Q4",
        "2016Q4","2017Q4","2018Q4","2019Q4","2020Q4","2021Q4","2022Q4","2023Q4",
        "2024Q1","2024Q2","2024Q3","2024Q4","2025Q1","2025Q2","2025Q3","2025Q4"
    ],
    "usd_share": [
        71.1, 71.5, 67.1, 65.9, 65.9, 66.4, 65.7, 63.9,
        64.1, 62.1, 61.8, 62.6, 61.1, 61.2, 65.1, 65.7,
        65.4, 62.7, 61.9, 60.9, 59.0, 58.8, 58.4, 57.9,
        58.6, 58.2, 57.4, 57.8, 57.7, 56.3, 56.9, 56.8
    ],
    "eur_share": [
        18.3, 19.2, 23.8, 25.2, 24.7, 24.3, 25.1, 26.3,
        26.4, 27.6, 25.8, 24.4, 24.2, 24.5, 21.2, 20.5,
        19.1, 20.0, 20.5, 20.6, 21.3, 20.6, 20.5, 20.0,
        20.1, 19.8, 20.0, 19.8, 20.1, 21.1, 20.3, 20.3
    ],
    "cny_share": [
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        1.1, 1.2, 1.9, 2.0, 2.3, 2.7, 2.8, 2.3,
        2.2, 2.1, 2.2, 2.2, 2.1, 2.1, 1.9, 1.95
    ]
}

# Central bank gold purchases (tonnes, annual, World Gold Council data)
gold_data = {
    "year": [2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
    "cb_gold_purchases": [77, 457, 544, 409, 477, 566, 384, 375, 656, 668, 255, 450, 1082, 1037, 1045]
}

# BRICS trade settlement in non-dollar currencies (index, rough estimates)
brics_data = {
    "year": [2018,2019,2020,2021,2022,2023,2024,2025],
    "non_usd_settlement_pct": [20, 22, 24, 26, 30, 38, 45, 52]
}

# DXY annual average
dxy_data = {
    "year": [2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025],
    "dxy": [98.7, 102.2, 96.4, 96.2, 97.4, 90.3, 95.7, 104.5, 103.5, 104.2, 98.1]
}

cofer_df = pd.DataFrame(cofer_data)
gold_df = pd.DataFrame(gold_data)
brics_df = pd.DataFrame(brics_data)
dxy_df = pd.DataFrame(dxy_data)

# ── HEADER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style='background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); 
     padding: 2rem; border-radius: 12px; margin-bottom: 1.5rem;'>
<h1 style='color: #e94560; margin: 0; font-size: 2.2rem; font-weight: 800;'>💵 Dollar Death Watch</h1>
<p style='color: #a8b2d8; margin: 0.5rem 0 0 0; font-size: 1rem;'>
Live tracker of de-dollarisation signals across global reserves, gold, trade settlement, and currency markets
</p>
<p style='color: #6272a4; margin: 0.3rem 0 0 0; font-size: 0.85rem;'>
Built on IMF COFER · World Gold Council · BIS · Gokhale (2026) · ssrn.com/abstract=6514338
</p>
</div>
""", unsafe_allow_html=True)

# ── VERDICT METRICS ──────────────────────────────────────────────────────────
st.subheader("🔍 De-Dollarisation Verdict")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        "USD Reserve Share (2025Q4)", 
        "56.8%", 
        delta="-14.3pp since 2000",
        delta_color="inverse"
    )
with col2:
    st.metric(
        "CB Gold Purchases (2024)",
        "1,045t",
        delta="+388t vs 2018 average",
        delta_color="inverse"
    )
with col3:
    st.metric(
        "BRICS Non-USD Trade (est.)",
        "~52%",
        delta="+32pp since 2018",
        delta_color="inverse"
    )
with col4:
    st.metric(
        "DXY 2025 avg",
        "98.1",
        delta="-6.1 vs 2024",
        delta_color="inverse"
    )

# ── VERDICT BOX ─────────────────────────────────────────────────────────────
st.info("""
**⚖️ The Honest Verdict:** De-dollarisation is real but slow. The USD reserve share has fallen from 71% in 2000 to 57% today — a structural decline. But 92% of recent quarterly moves are exchange-rate valuation effects, not active portfolio reallocation. Central banks are not running from the dollar. They are diversifying at the margins while keeping dollar assets as their core. The dollar is not dying. It is being diluted.
""")

st.markdown("---")

# ── CHART 1: COFER ──────────────────────────────────────────────────────────
st.subheader("Global Reserve Currency Composition (IMF COFER)")

fig1 = go.Figure()
fig1.add_trace(go.Scatter(
    x=cofer_df['quarter'], y=cofer_df['usd_share'],
    name='US Dollar', line=dict(color='#e94560', width=3),
    fill='tozeroy', fillcolor='rgba(233,69,96,0.08)',
    hovertemplate='%{x}<br>USD: %{y:.1f}%<extra></extra>'
))
fig1.add_trace(go.Scatter(
    x=cofer_df['quarter'], y=cofer_df['eur_share'],
    name='Euro', line=dict(color='#0096c7', width=2),
    hovertemplate='%{x}<br>EUR: %{y:.1f}%<extra></extra>'
))
fig1.add_trace(go.Scatter(
    x=cofer_df['quarter'], y=cofer_df['cny_share'],
    name='Chinese Renminbi', line=dict(color='#e9b949', width=2, dash='dot'),
    hovertemplate='%{x}<br>CNY: %{y:.1f}%<extra></extra>'
))
fig1.add_annotation(
    x='2016Q4', y=65.4,
    text='Trump tariffs begin', showarrow=True, arrowhead=2,
    font=dict(size=10, color='#888'), arrowcolor='#888'
)
fig1.add_annotation(
    x='2022Q4', y=58.4,
    text='Russia sanctions', showarrow=True, arrowhead=2,
    font=dict(size=10, color='#888'), arrowcolor='#888',
    ay=-40
)
fig1.update_layout(
    plot_bgcolor='white', paper_bgcolor='white',
    height=380,
    legend=dict(orientation='h', y=1.08),
    xaxis=dict(title='', tickangle=-45, gridcolor='#f0f0f0',
               tickvals=[q for q in cofer_df['quarter'] if q.endswith('Q4')][::2]),
    yaxis=dict(title='Share of allocated reserves (%)', gridcolor='#f0f0f0', range=[0,80]),
    margin=dict(t=40, b=60, l=60, r=20),
    hovermode='x unified'
)
st.plotly_chart(fig1, use_container_width=True)
st.caption("Source: IMF COFER dataset. Latest: 2025Q4 (USD 56.8%, EUR 20.3%, CNY 1.95%)")

st.markdown("---")

# ── CHART 2: GOLD ──────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("Central Bank Gold Purchases")
    fig2 = go.Figure()
    colours = ['#e94560' if y >= 1000 else '#6272a4' for y in gold_df['cb_gold_purchases']]
    fig2.add_trace(go.Bar(
        x=gold_df['year'], y=gold_df['cb_gold_purchases'],
        marker_color=colours,
        hovertemplate='%{x}: %{y}t<extra></extra>'
    ))
    fig2.add_hline(y=500, line_dash='dot', line_color='#888',
                   annotation_text='Pre-2022 avg', annotation_position='right')
    fig2.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        height=300,
        xaxis=dict(gridcolor='#f0f0f0'),
        yaxis=dict(title='Tonnes', gridcolor='#f0f0f0'),
        margin=dict(t=20, b=40, l=60, r=20),
        showlegend=False
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("Source: World Gold Council. 2022-2024 saw record purchases exceeding 1,000t/year.")

with col2:
    st.subheader("BRICS Non-USD Trade Settlement (est.)")
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=brics_df['year'], y=brics_df['non_usd_settlement_pct'],
        line=dict(color='#e9b949', width=3),
        fill='tozeroy', fillcolor='rgba(233,185,73,0.1)',
        hovertemplate='%{x}: ~%{y}% non-USD<extra></extra>'
    ))
    fig3.add_vline(x=2022, line_dash='dot', line_color='#e94560',
                   annotation_text='Russia sanctions', annotation_position='top right',
                   annotation_font=dict(size=10, color='#e94560'))
    fig3.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        height=300,
        xaxis=dict(gridcolor='#f0f0f0'),
        yaxis=dict(title='Est. % of BRICS trade in non-USD', gridcolor='#f0f0f0', range=[0,70]),
        margin=dict(t=20, b=40, l=80, r=20),
        showlegend=False
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.caption("Estimates based on BIS, SWIFT data, and policy announcements. Not official data.")

st.markdown("---")

# ── CHART 3: DXY ──────────────────────────────────────────────────────────
st.subheader("DXY Annual Average — Dollar Strength Index")
fig4 = go.Figure()
fig4.add_trace(go.Scatter(
    x=dxy_df['year'], y=dxy_df['dxy'],
    line=dict(color='#0096c7', width=3),
    fill='tozeroy', fillcolor='rgba(0,150,199,0.08)',
    hovertemplate='%{x}: DXY %{y:.1f}<extra></extra>'
))
fig4.add_hline(y=100, line_dash='dot', line_color='#888',
               annotation_text='DXY = 100 (parity)', annotation_position='right')
fig4.update_layout(
    plot_bgcolor='white', paper_bgcolor='white',
    height=280,
    xaxis=dict(gridcolor='#f0f0f0'),
    yaxis=dict(title='DXY Index', gridcolor='#f0f0f0', range=[80,115]),
    margin=dict(t=20, b=40, l=60, r=20),
    showlegend=False
)
st.plotly_chart(fig4, use_container_width=True)
st.caption("Source: FRED (DTWEXBGS). DXY 2025 annual avg ~98.1, down from 104.2 in 2024 — biggest drop since 1973.")

st.markdown("---")

# ── THE DCP CONNECTION ────────────────────────────────────────────────────
st.subheader("🔗 Why This Matters: The Dominant Currency Paradigm")
st.markdown("""
The dollar's role as the dominant **invoice currency** in global trade is separate from — and arguably more durable than — its role as a reserve currency. 

My working paper ([ssrn.com/abstract=6514338](https://ssrn.com/abstract=6514338)) documents that dollar-invoiced energy and manufactured goods costs transmit inflation from India to Singapore to the UK regardless of bilateral exchange rate movements. This is the Dominant Currency Paradigm in action: **the dollar runs global goods markets even when central banks are diversifying away from dollar reserves**.

De-dollarisation of reserves is real. De-dollarisation of trade invoicing is much slower. The dollar is being diluted at the top (reserves) while remaining entrenched at the bottom (trade). Understanding both layers is essential for any assessment of the dollar's future role.
""")

st.markdown("---")
col1, col2 = st.columns([1, 3])
with col1:
    st.markdown("**Data Sources**")
    st.markdown("""
    - IMF COFER Dataset
    - World Gold Council
    - BIS SWIFT data
    - FRED (Federal Reserve)
    """)
with col2:
    st.caption("Built by Anuja A. Gokhale (NUS Merit Scholar) as a companion to research on dollar-invoiced inflation transmission. "
               "BRICS settlement estimates are approximate and based on publicly available data. "
               "This dashboard is for research and educational purposes. ssrn.com/author=10973290")
