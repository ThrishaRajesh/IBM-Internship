import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ----------------- PAGE CONFIG -----------------
st.set_page_config(page_title="HydroSense AI", page_icon="💦", layout="wide")

# ----------------- CUSTOM CSS -----------------
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0f172a, #1f2937); color: #f0f0f0 !important; }
h1,h2,h3,h4,h5,h6,p,div,span { color: #f0f0f0 !important; }
.metric-card {
    background: linear-gradient(120deg, rgba(14,116,144,0.1), rgba(79,70,229,0.1));
    border: 2px solid rgba(79,70,229,0.3); border-radius: 12px; padding: 1rem; text-align:center;
}
.status-high {background:#e11d48;color:white;padding:0.5rem 1rem;border-radius:20px;font-weight:bold;}
.status-low {background:#22c55e;color:white;padding:0.5rem 1rem;border-radius:20px;font-weight:bold;}
</style>
""", unsafe_allow_html=True)

# ----------------- HEADER -----------------
st.markdown("""
<div style='text-align:center; background: linear-gradient(135deg,#0ea5e9,#9333ea); 
            padding:2rem; border-radius:15px; font-weight:bold; box-shadow:0 8px 32px rgba(0,0,0,0.4)'>
<h1>💦 HydroSense AI</h1>
<h3>Next-Gen Water Management with Agentic AI & Prompt Engineering</h3>
<p style='font-size:0.9rem;'>Predictive insights, actionable alerts, and intelligent recommendations</p>
</div>
""", unsafe_allow_html=True)

# ----------------- INPUT SLIDERS -----------------
st.markdown("### 📊 Simulate Daily Water Usage Scenarios")
days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
default_usage = [300,310,305,680,720,350,330]

usage_values = []
cols = st.columns(len(days))
for i, day in enumerate(days):
    with cols[i]:
        val = st.slider(day, 0, 12000, default_usage[i], step=10)
        usage_values.append(val)

# ----------------- AGENTIC AI & PROMPT LOGIC -----------------
def input_agent(df):
    df["Usage"] = df["Usage"].apply(lambda x:max(x,0))
    total = df["Usage"].sum()
    return df, total

def pattern_agent(df):
    baseline = df["Usage"][:3].mean()
    std = df["Usage"].std()
    trend = "Increasing" if df["Usage"][4] > df["Usage"][3] else "Stable"
    return baseline, std, trend

def risk_agent(df, baseline, sensitivity=1.6):
    spikes = df[df["Usage"] > baseline*sensitivity]
    level = "HIGH" if not spikes.empty else "LOW"
    prob = min(95, 50 + (spikes["Usage"].max() - baseline)/baseline*50) if not spikes.empty else 10
    return level, prob, spikes

def decision_agent(level):
    return "Immediate Action Required" if level=="HIGH" else "Regular Monitoring"

def advisory_agent(level):
    if level=="HIGH":
        return [
            "Inspect all taps, toilets, and pipes immediately.",
            "Monitor water meter hourly for anomalies.",
            "Schedule plumbing inspection within 24 hours."
        ]
    else:
        return [
            "Maintain weekly monitoring.",
            "Install water-saving fixtures.",
            "Plan preventive maintenance monthly."
        ]

def responsible_ai_agent():
    return "All decisions are simulated using heuristic-based Agentic AI & Prompt Engineering. Results are indicative."

# ----------------- DATAFRAME -----------------
df = pd.DataFrame({"Day":days,"Usage":usage_values})
df_valid, total_usage = input_agent(df)
baseline, std_dev, trend = pattern_agent(df_valid)
risk_level, probability, spike_days = risk_agent(df_valid, baseline)
verdict = decision_agent(risk_level)
actions = advisory_agent(risk_level)
ai_note = responsible_ai_agent()

# ----------------- DASHBOARD -----------------
st.markdown('<div style="height:5px; background: linear-gradient(90deg,#0ea5e9,#9333ea,#facc15); border-radius:3px;margin:1rem 0;"></div>', unsafe_allow_html=True)

tabs = st.tabs(["📥 Input","📊 Pattern","⚠️ Risk","🧠 Decision","💡 Advisory","🛡 AI Guardrail"])

with tabs[0]:
    st.subheader("Input Agent")
    st.dataframe(df_valid.style.background_gradient(cmap='PuBu'), use_container_width=True)
    st.success(f"Total Weekly Usage: {total_usage} L")

with tabs[1]:
    st.subheader("Pattern Analysis Agent")
    st.markdown(f"- Baseline (Mon-Wed avg): {baseline:.1f} L/day")
    st.markdown(f"- Std Deviation: {std_dev:.1f} L")
    st.markdown(f"- Trend: {trend}")
    fig = px.bar(df_valid, x="Day", y="Usage", text="Usage", color="Usage", color_continuous_scale="Viridis")
    st.plotly_chart(fig, use_container_width=True)

with tabs[2]:
    st.subheader("Risk Agent")
    color_map = {"LOW":"#22c55e","HIGH":"#e11d48"}
    st.markdown(f"- Risk Level: <span style='color:{color_map[risk_level]}; font-weight:bold'>{risk_level}</span>", unsafe_allow_html=True)
    st.markdown(f"- Leak Probability: {probability:.1f}%")
    if not spike_days.empty:
        st.markdown(f"- Spike Days: {', '.join(spike_days['Day'].tolist())}")
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=probability,
        gauge={'axis':{'range':[0,100]}, 'bar':{'color':color_map[risk_level]}},
        title={'text': "Leak Probability"}
    ))
    st.plotly_chart(fig_gauge, use_container_width=True)

with tabs[3]:
    st.subheader("Decision Agent")
    st.markdown(f"- Verdict: **{verdict}**")
    st.progress(int(min(100,max(0,probability))))

with tabs[4]:
    st.subheader("Advisory Agent")
    for a in actions:
        st.markdown(f"- {a}")

with tabs[5]:
    st.subheader("Responsible AI Guardrail")
    st.markdown(f"- {ai_note}")

# ----------------- ADVANCED FLOW VISUALIZATION -----------------
st.subheader("💧 Multi-Agent Workflow & Water Flow Analysis")
fig_sankey = go.Figure(data=[go.Sankey(
    node = dict(
      pad=20, thickness=20, line=dict(color="black", width=0.5),
      label=["Input","Pattern","Risk","Decision","Advisory","AI Guardrail"],
      color=["#2563eb","#0ea5e9","#e11d48","#22c55e","#9333ea","#facc15"]
    ),
    link = dict(
      source=[0,1,2,3,4],
      target=[1,2,3,4,5],
      value=[total_usage,total_usage*0.8,total_usage*0.6,total_usage*0.4,total_usage*0.2]
  ))])
st.plotly_chart(fig_sankey, use_container_width=True)
