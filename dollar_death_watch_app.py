import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Dollar Death Watch",
    page_icon="💵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap');

.stApp {
    background-color: #f5f0e8;
    color: #1a1a1a;
    font-family: 'IBM Plex Sans', sans-serif;
}

.main .block-container {
    padding: 1.5rem 2.5rem;
    max-width: 1400px;
}

[data-testid="metric-container"] {
    background: #ede8dd;
    border: 1px solid #c8bfaa;
    border-top: 3px solid #1e5fb4;
    padding: 1rem;
    border-radius: 2px;
}

[data-testid="metric-container"] label {
    color: #5a5040 !important;
    font-size: 0.65rem !important;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 500;
}

[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #1a1a1a !important;
    font-size: 1.5rem !important;
    font-weight: 700;
    font-family: 'IBM Plex Mono', monospace !important;
}

[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-size: 0.72rem !important;
    font-family: 'IBM Plex Mono', monospace !important;
}

h1, h2, h3 {
    font-family: 'IBM Plex Sans', sans-serif !important;
    color: #1a1a1a !important;
}

hr { border-color: #c8bfaa; }

.stAlert {
    background: #ede8dd !important;
    border: 1px solid #c8bfaa !important;
    border-left: 4px solid #1e5fb4 !important;
    color: #2a2a2a !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.83rem;
    border-radius: 2px !important;
}

.stCaption {
    color: #7a6f60 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.7rem !important;
}

.section-header {
    color: #1e5fb4;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.18em;
    border-bottom: 1px solid #c8bfaa;
    padding-bottom: 0.3rem;
    margin-bottom: 1rem;
    margin-top: 0.5rem;
}

.masthead {
    border-bottom: 3px solid #1a1a1a;
    padding-bottom: 1rem;
    margin-bottom: 1.5rem;
}

.masthead-eyebrow {
    color: #1e5fb4;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    margin-bottom: 0.4rem;
}

.masthead-title {
    color: #1a1a1a;
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 2.4rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    line-height: 1.1;
}

.masthead-sub {
    color: #5a5040;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    margin-top: 0.3rem;
}

.verdict-box {
    background: #1a1a1a;
    color: #f5f0e8;
    padding: 1.2rem 1.5rem;
    border-radius: 2px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
    line-height: 1.8;
    margin: 1rem 0;
}

.dcp-box {
    background: #ede8dd;
    border: 1px solid #c8bfaa;
    border-left: 4px solid #1e5fb4;
    padding: 1.2rem 1.5rem;
    border-radius: 2px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
    color: #2a2a2a;
    line-height: 1.8;
}

.footer-bar {
    border-top: 2px solid #1a1a1a;
    padding-top: 0.6rem;
    color: #7a6f60;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    margin-top: 1.5rem;
}

.highlight-blue { color: #1e5fb4; font-weight: 600; }
.highlight-dark { color: #1a1a1a; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# Palette for charts
BG = '#f5f0e8'
BG2 = '#ede8dd'
BLUE = '#1e5fb4'
DARK = '#1a1a1a'
MUTED = '#7a6f60'
GRID = '#d8d0c0'
RED = '#c0392b'
GOLD = '#8a6e00'
GREEN = '#1a6b3c'
CREAM2 = '#ede8dd'

# ── DATA ─────────────────────────────────────────────────────────────────────
cofer_data = {
    "quarter": ["2000Q4","2001Q4","2002Q4","2003Q4","2004Q4","2005Q4","2006Q4","2007Q4",
                "2008Q4","2009Q4","2010Q4","2011Q4","2012Q4","2013Q4","2014Q4","2015Q4",
                "2016Q4","2017Q4","2018Q4","2019Q4","2020Q4","2021Q4","2022Q4","2023Q4",
                "2024Q1","2024Q2","2024Q3","2024Q4","2025Q1","2025Q2","2025Q3","2025Q4"],
    "usd": [71.1,71.5,67.1,65.9,65.9,66.4,65.7,63.9,64.1,62.1,61.8,62.6,61.1,61.2,65.1,65.7,65.4,62.7,61.9,60.9,59.0,58.8,58.4,57.9,58.6,58.2,57.4,57.8,57.7,56.3,56.9,56.8],
    "eur": [18.3,19.2,23.8,25.2,24.7,24.3,25.1,26.3,26.4,27.6,25.8,24.4,24.2,24.5,21.2,20.5,19.1,20.0,20.5,20.6,21.3,20.6,20.5,20.0,20.1,19.8,20.0,19.8,20.1,21.1,20.3,20.3],
    "cny": [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.1,1.2,1.9,2.0,2.3,2.7,2.8,2.3,2.2,2.1,2.2,2.2,2.1,2.1,1.9,1.95]
}
gold_data = {"year":[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
             "tonnes":[77,457,544,409,477,566,384,375,656,668,255,450,1082,1037,1045]}
brics_data = {"year":[2018,2019,2020,2021,2022,2023,2024,2025],"pct":[20,22,24,26,30,38,45,52]}
dxy_data = {"year":[2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025],
            "dxy":[98.7,102.2,96.4,96.2,97.4,90.3,95.7,104.5,103.5,104.2,98.1]}

cofer_df = pd.DataFrame(cofer_data)
gold_df = pd.DataFrame(gold_data)
brics_df = pd.DataFrame(brics_data)
dxy_df = pd.DataFrame(dxy_data)

# ── MASTHEAD ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class='masthead'>
  <div class='masthead-eyebrow'>GOKHALE MACRO RESEARCH · TRACKER · AUGUST 2026</div>
  <div class='masthead-title'>💵 Dollar Death Watch</div>
  <div class='masthead-sub'>De-dollarisation signals across global reserves, gold, trade settlement, and currency markets</div>
</div>
""", unsafe_allow_html=True)

# ── METRICS ──────────────────────────────────────────────────────────────────
col1,col2,col3,col4,col5 = st.columns(5)
with col1: st.metric("USD RESERVE SHARE","56.8%","-14.3pp since 2000")
with col2: st.metric("CB GOLD (2024)","1,045t","+388t vs pre-2022 avg")
with col3: st.metric("BRICS NON-USD","~52% est.","+32pp since 2018")
with col4: st.metric("DXY 2025 AVG","98.1","-6.1 vs 2024")
with col5: st.metric("CNY SHARE","1.95%","+1.95pp since 2016")

# ── VERDICT ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class='verdict-box'>
<span style='color:#f5f0e8;font-weight:700;'>VERDICT ·</span> De-dollarisation is real but slow. The USD reserve share has fallen from 71% in 2000 to 57% today. But 92% of recent quarterly moves are exchange-rate valuation effects, not active portfolio reallocation. Central banks are not running from the dollar — they are diversifying at the margins. <span style='color:#a8c4f0;font-weight:600;'>The dollar is not dying. It is being diluted.</span>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

# ── COFER CHART ───────────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>[ 01 ] Global Reserve Currency Composition · IMF COFER · 2000–2025Q4</div>", unsafe_allow_html=True)

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=cofer_df['quarter'],y=cofer_df['usd'],name='USD',
    line=dict(color=BLUE,width=2.5),fill='tozeroy',fillcolor='rgba(30,95,180,0.07)',
    hovertemplate='<b>%{x}</b><br>USD: %{y:.1f}%<extra></extra>'))
fig1.add_trace(go.Scatter(x=cofer_df['quarter'],y=cofer_df['eur'],name='EUR',
    line=dict(color=DARK,width=1.5,dash='dot'),
    hovertemplate='<b>%{x}</b><br>EUR: %{y:.1f}%<extra></extra>'))
fig1.add_trace(go.Scatter(x=cofer_df['quarter'],y=cofer_df['cny'],name='CNY',
    line=dict(color=GOLD,width=1.5,dash='dash'),
    hovertemplate='<b>%{x}</b><br>CNY: %{y:.1f}%<extra></extra>'))
for x,text,ay in [('2022Q4','Russia sanctions',-45),('2020Q4','COVID',-35)]:
    val = cofer_df[cofer_df['quarter']==x]['usd'].values[0]
    fig1.add_annotation(x=x,y=val,text=text,showarrow=True,arrowhead=1,
        arrowcolor=MUTED,font=dict(size=9,color=MUTED,family='IBM Plex Mono'),
        bgcolor=BG2,bordercolor=GRID,borderwidth=1,ay=ay,ax=0)
fig1.update_layout(plot_bgcolor=BG,paper_bgcolor=BG,height=360,
    font=dict(family='IBM Plex Mono',color=MUTED),
    legend=dict(orientation='h',y=1.06,font=dict(color=DARK,size=11),bgcolor='rgba(0,0,0,0)'),
    xaxis=dict(gridcolor=GRID,tickcolor=MUTED,linecolor=GRID,
               tickfont=dict(size=9,color=MUTED),
               tickvals=[q for q in cofer_df['quarter'] if q.endswith('Q4')][::2],tickangle=-45),
    yaxis=dict(gridcolor=GRID,tickfont=dict(size=9,color=MUTED),linecolor=GRID,
               title=dict(text='% of allocated reserves',font=dict(size=10,color=MUTED)),range=[0,80]),
    margin=dict(t=30,b=60,l=70,r=20),hovermode='x unified',
    hoverlabel=dict(bgcolor=BG2,bordercolor=BLUE,font=dict(family='IBM Plex Mono',color=DARK)))
st.plotly_chart(fig1,use_container_width=True)
st.markdown("<div class='footer-bar' style='border-top:1px solid #c8bfaa; margin-top:0;'>Source: IMF COFER dataset · Latest: 2025Q4 — USD 56.8% · EUR 20.3% · CNY 1.95%</div>", unsafe_allow_html=True)

st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

# ── GOLD + BRICS ──────────────────────────────────────────────────────────────
col1,col2 = st.columns(2)
with col1:
    st.markdown("<div class='section-header'>[ 02 ] Central Bank Gold Purchases · World Gold Council</div>", unsafe_allow_html=True)
    fig2 = go.Figure()
    colours = [RED if t>=1000 else BLUE if t>=600 else MUTED for t in gold_df['tonnes']]
    fig2.add_trace(go.Bar(x=gold_df['year'],y=gold_df['tonnes'],marker_color=colours,
        hovertemplate='<b>%{x}</b><br>%{y}t<extra></extra>'))
    fig2.add_hline(y=500,line_dash='dot',line_color=MUTED,line_width=1,
        annotation_text='pre-2022 avg',annotation_font=dict(size=9,color=MUTED,family='IBM Plex Mono'),
        annotation_position='right')
    fig2.update_layout(plot_bgcolor=BG,paper_bgcolor=BG,height=280,showlegend=False,
        font=dict(family='IBM Plex Mono',color=MUTED),
        xaxis=dict(gridcolor=GRID,tickfont=dict(size=9,color=MUTED),linecolor=GRID),
        yaxis=dict(gridcolor=GRID,tickfont=dict(size=9,color=MUTED),linecolor=GRID,
                   title=dict(text='Tonnes',font=dict(size=10,color=MUTED))),
        margin=dict(t=10,b=40,l=60,r=20),
        hoverlabel=dict(bgcolor=BG2,bordercolor=BLUE,font=dict(family='IBM Plex Mono',color=DARK)))
    st.plotly_chart(fig2,use_container_width=True)
    st.markdown("<div class='footer-bar' style='border-top:1px solid #c8bfaa;margin-top:0;'>Red = record years (>1,000t). 2022–2024: three consecutive record purchase years.</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='section-header'>[ 03 ] BRICS Non-USD Trade Settlement · Est.</div>", unsafe_allow_html=True)
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=brics_df['year'],y=brics_df['pct'],
        line=dict(color=GOLD,width=2.5),fill='tozeroy',fillcolor='rgba(138,110,0,0.07)',
        hovertemplate='<b>%{x}</b><br>~%{y}% non-USD<extra></extra>'))
    fig3.add_vline(x=2022,line_dash='dot',line_color=RED,line_width=1,
        annotation_text='Russia sanctions',annotation_position='top left',
        annotation_font=dict(size=9,color=RED,family='IBM Plex Mono'))
    fig3.update_layout(plot_bgcolor=BG,paper_bgcolor=BG,height=280,showlegend=False,
        font=dict(family='IBM Plex Mono',color=MUTED),
        xaxis=dict(gridcolor=GRID,tickfont=dict(size=9,color=MUTED),linecolor=GRID),
        yaxis=dict(gridcolor=GRID,tickfont=dict(size=9,color=MUTED),linecolor=GRID,
                   title=dict(text='Est. % non-USD',font=dict(size=10,color=MUTED)),range=[0,70]),
        margin=dict(t=10,b=40,l=60,r=20),
        hoverlabel=dict(bgcolor=BG2,bordercolor=BLUE,font=dict(family='IBM Plex Mono',color=DARK)))
    st.plotly_chart(fig3,use_container_width=True)
    st.markdown("<div class='footer-bar' style='border-top:1px solid #c8bfaa;margin-top:0;'>Estimates based on BIS, SWIFT data, and policy announcements. Not official figures.</div>", unsafe_allow_html=True)

st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

# ── DXY ──────────────────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>[ 04 ] DXY Broad Dollar Index · FRED · Annual Average</div>", unsafe_allow_html=True)
fig4 = go.Figure()
fig4.add_trace(go.Scatter(x=dxy_df['year'],y=dxy_df['dxy'],
    line=dict(color=GREEN,width=2.5),fill='tozeroy',fillcolor='rgba(26,107,60,0.07)',
    hovertemplate='<b>%{x}</b><br>DXY: %{y:.1f}<extra></extra>'))
fig4.add_hline(y=100,line_dash='dot',line_color=MUTED,line_width=1,
    annotation_text='DXY = 100',annotation_position='right',
    annotation_font=dict(size=9,color=MUTED,family='IBM Plex Mono'))
fig4.update_layout(plot_bgcolor=BG,paper_bgcolor=BG,height=250,showlegend=False,
    font=dict(family='IBM Plex Mono',color=MUTED),
    xaxis=dict(gridcolor=GRID,tickfont=dict(size=9,color=MUTED),linecolor=GRID),
    yaxis=dict(gridcolor=GRID,tickfont=dict(size=9,color=MUTED),linecolor=GRID,
               title=dict(text='DXY Index',font=dict(size=10,color=MUTED)),range=[80,115]),
    margin=dict(t=10,b=40,l=60,r=20),
    hoverlabel=dict(bgcolor=BG2,bordercolor=BLUE,font=dict(family='IBM Plex Mono',color=DARK)))
st.plotly_chart(fig4,use_container_width=True)
st.markdown("<div class='footer-bar' style='border-top:1px solid #c8bfaa;margin-top:0;'>Source: FRED (DTWEXBGS) · DXY 2025 avg ~98.1, down from 104.2 in 2024 — biggest annual drop since 1973.</div>", unsafe_allow_html=True)

st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

# ── DCP ──────────────────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>[ 05 ] The DCP Connection — Why This Matters</div>", unsafe_allow_html=True)
st.markdown("""
<div class='dcp-box'>
The dollar's role as the dominant <span class='highlight-blue'>invoice currency</span> in global trade is separate from — and more durable than — its role as a reserve currency.<br><br>
Research by Gokhale (2026) documents that dollar-invoiced energy and manufactured goods costs transmit inflation from <span class='highlight-blue'>India → Singapore → UK</span> regardless of bilateral exchange rate movements. This is the Dominant Currency Paradigm: <span class='highlight-dark'>the dollar runs global goods markets even as central banks diversify away from dollar reserves</span>.<br><br>
De-dollarisation of reserves is real. De-dollarisation of trade invoicing is much slower. Understanding both layers is essential for any honest assessment of the dollar's future role.<br><br>
<span style='color:#7a6f60;font-size:0.75rem;'>→ ssrn.com/abstract=6514338 · ssrn.com/author=10973290</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='footer-bar'>
Built by Anuja A. Gokhale · MA Applied Economics, NUS (Merit Scholar) · anujagokhale1604@gmail.com · Data from IMF COFER, World Gold Council, BIS, FRED · August 2026
</div>
""", unsafe_allow_html=True)
