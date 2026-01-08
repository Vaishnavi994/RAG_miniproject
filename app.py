# import streamlit as st
# import pandas as pd

# st.set_page_config(page_title="IoT Risk Dashboard", layout="wide")

# # ---------------- CUSTOM STYLES ----------------
# st.markdown("""
# <style>
# .kpi {
#     padding: 16px;
#     border-radius: 12px;
#     color: white;
#     font-weight: 600;
#     text-align: center;
# }
# .critical { background-color: #e63946; }
# .high { background-color: #f4a261; color: black; }
# .medium { background-color: #f1c453; color: black; }
# .low { background-color: #2a9d8f; }
# </style>
# """, unsafe_allow_html=True)

# st.title("🛡️ IoT Risk Dashboard")
# st.caption("Real-time, context-aware risk prioritization with deception signals")

# # ---------------- DATA ----------------
# data = {
#     "Device": ["Smart Bulb", "Camera", "Laptop", "Router"],
#     "Risk Level": ["HIGH", "CRITICAL", "LOW", "MEDIUM"],
#     "Risk Score": [75, 92, 20, 55],
#     "Honeypot Signal": [0, 100, 0, 100],  # 0 = No hit, 100 = Honeypot triggered
#     "Why": [
#         "Always online, low encryption, unknown vendor",
#         "Exposed ports, honeypot interaction detected",
#         "Short sessions, encrypted traffic",
#         "Suspicious scan detected on decoy port"
#     ]
# }

# df = pd.DataFrame(data)

# # ---------------- SORT BY SEVERITY ----------------
# severity_order = {"CRITICAL": 1, "HIGH": 2, "MEDIUM": 3, "LOW": 4}
# df["rank"] = df["Risk Level"].map(severity_order)
# df = df.sort_values("rank").drop(columns="rank")

# # ---------------- KPI ROW ----------------
# c1, c2, c3, c4 = st.columns(4)

# c1.markdown(f"<div class='kpi low'>Connected Devices<br>{len(df)}</div>", unsafe_allow_html=True)
# c2.markdown(f"<div class='kpi critical'>Critical<br>{(df['Risk Level']=='CRITICAL').sum()}</div>", unsafe_allow_html=True)
# c3.markdown(f"<div class='kpi high'>High Risk<br>{(df['Risk Level']=='HIGH').sum()}</div>", unsafe_allow_html=True)
# c4.markdown(f"<div class='kpi medium'>Avg Risk Score<br>{int(df['Risk Score'].mean())}</div>", unsafe_allow_html=True)

# st.divider()

# # ---------------- RISK LEVEL BADGE ----------------
# def risk_badge(level):
#     return {
#         "CRITICAL": "🔴 CRITICAL",
#         "HIGH": "🟠 HIGH",
#         "MEDIUM": "🟡 MEDIUM",
#         "LOW": "🟢 LOW"
#     }[level]

# df["Risk Level"] = df["Risk Level"].apply(risk_badge)

# # ---------------- TABLE ----------------
# st.dataframe(
#     df,
#     use_container_width=True,
#     hide_index=True,
#     column_config={
#         "Risk Score": st.column_config.ProgressColumn(
#             "Risk Score",
#             min_value=0,
#             max_value=100,
#             format="%d",
#         ),
#         "Honeypot Signal": st.column_config.ProgressColumn(
#             "Honeypot Signal",
#             min_value=0,
#             max_value=100,
#             format="%d",
#             help="100 indicates interaction with a decoy (honeypot) service"
#         )
#     }
# )

# # ---------------- FOOTER ----------------
# st.caption(
#     "🍯 Honeypot Signal: 0 = No interaction | 100 = Decoy port accessed  |  "
#     "Honeypot hits are treated as high-confidence malicious indicators."
# )
import streamlit as st
import pandas as pd

st.set_page_config(page_title="IoT Risk Dashboard", layout="wide")

# ---------------- CUSTOM CSS (ONLY PROGRESS COLORS) ----------------
st.markdown("""
<style>

/* Remove default gradient */
div[data-testid="stProgress"] > div > div > div {
    background-image: none !important;
}

/* CRITICAL – Red */
.severity-critical div[data-testid="stProgress"] > div > div > div {
    background-color: #e63946 !important;
}

/* HIGH – Orange */
.severity-high div[data-testid="stProgress"] > div > div > div {
    background-color: #f4a261 !important;
}

/* MEDIUM – Yellow */
.severity-medium div[data-testid="stProgress"] > div > div > div {
    background-color: #f1c453 !important;
}

/* LOW – Green */
.severity-low div[data-testid="stProgress"] > div > div > div {
    background-color: #2a9d8f !important;
}

/* KPI cards (unchanged) */
.kpi {
    padding: 16px;
    border-radius: 12px;
    color: white;
    font-weight: 600;
    text-align: center;
}
.critical { background-color: #e63946; }
.high { background-color: #f4a261; color: black; }
.medium { background-color: #f1c453; color: black; }
.low { background-color: #2a9d8f; }

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("🛡️ HomeGuard Console Dashboard")
st.caption("Real-time, context-aware risk prioritization with deception signals")

# ---------------- DATA ----------------
data = {
    "Device": ["Smart Bulb", "Camera", "Laptop", "Router"],
    "Risk Level": ["HIGH", "CRITICAL", "LOW", "MEDIUM"],
    "Risk Score": [75, 92, 20, 55],
    "Honeypot Signal": [0, 100, 0, 100],
    "Why": [
        "Always online, low encryption, unknown vendor",
        "Exposed ports, honeypot interaction detected",
        "Short sessions, encrypted traffic",
        "Suspicious scan detected on decoy port"
    ]
}

df = pd.DataFrame(data)

# ---------------- SORT BY SEVERITY ----------------
severity_order = {"CRITICAL": 1, "HIGH": 2, "MEDIUM": 3, "LOW": 4}
df["rank"] = df["Risk Level"].map(severity_order)
df = df.sort_values("rank").drop(columns="rank")

# ---------------- KPI ROW ----------------
c1, c2, c3, c4 = st.columns(4)

c1.markdown(f"<div class='kpi low'>Connected Devices<br>{len(df)}</div>", unsafe_allow_html=True)
c2.markdown(f"<div class='kpi critical'>Critical<br>{(df['Risk Level']=='CRITICAL').sum()}</div>", unsafe_allow_html=True)
c3.markdown(f"<div class='kpi high'>High Risk<br>{(df['Risk Level']=='HIGH').sum()}</div>", unsafe_allow_html=True)
c4.markdown(f"<div class='kpi medium'>Avg Risk Score<br>{int(df['Risk Score'].mean())}</div>", unsafe_allow_html=True)

st.divider()

# ---------------- RISK BADGE ----------------
def risk_badge(level):
    return {
        "CRITICAL": "🔴 CRITICAL",
        "HIGH": "🟠 HIGH",
        "MEDIUM": "🟡 MEDIUM",
        "LOW": "🟢 LOW"
    }[level]

df["Risk Level"] = df["Risk Level"].apply(risk_badge)

# ---------------- DETERMINE OVERALL SEVERITY (FOR COLOR) ----------------
max_risk = df["Risk Score"].max()

if max_risk >= 80:
    severity_class = "severity-critical"
elif max_risk >= 60:
    severity_class = "severity-high"
elif max_risk >= 40:
    severity_class = "severity-medium"
else:
    severity_class = "severity-low"

# ---------------- TABLE (UNCHANGED) ----------------
st.markdown(f"<div class='{severity_class}'>", unsafe_allow_html=True)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Risk Score": st.column_config.ProgressColumn(
            "Risk Score",
            min_value=0,
            max_value=100,
            format="%d"
        ),
        "Honeypot Signal": st.column_config.ProgressColumn(
            "Honeypot Signal",
            min_value=0,
            max_value=100,
            format="%d"
        )
    }
)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.caption(
    "🔴 Critical | 🟠 High | 🟡 Medium | 🟢 Low  |  "
    "Progress line color reflects overall severity context"
)
