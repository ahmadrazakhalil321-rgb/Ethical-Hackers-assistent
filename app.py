import time
import streamlit as st
from google import genai
from google.genai import types
from streamlit_option_menu import option_menu

# Page Configuration with Dark Theme Styling
st.set_page_config(
    page_title="SpectreOps AI | Red Team Architect",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Cyber/Red Team Theme
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    .stButton>button {
        background-color: #8b0000;
        color: #ffffff;
        border-radius: 4px;
        border: 1px solid #ff4d4d;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #ff0000;
        border-color: #ffffff;
        color: #ffffff;
    }
    div[data-baseweb="select"] > div {
        background-color: #1a1c23;
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# Helper function to invoke Gemini Flash with Retry Logic
def query_gemini_flash(prompt, system_instruction, api_key):
    client = genai.Client(api_key=api_key)
    
    max_retries = 3
    backoff = 2
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.3,
                )
            )
            return response.text
        except Exception as e:
            error_str = str(e)
            if ("503" in error_str or "UNAVAILABLE" in error_str) and attempt < max_retries - 1:
                time.sleep(backoff ** (attempt + 1))
                continue
            else:
                raise e

# System Instruction Guardrail
RED_TEAM_SYSTEM_PROMPT = """
You are SpectreOps AI, an expert Red Team Security Consultant and Offensive Security Specialist operating within legal, authorized penetration testing parameters.
Your goal is to assist authorized security professionals, researchers, and ethical hackers in simulating realistic cyber threats, planning adversary emulation, analyzing attack vectors, and documenting security vulnerabilities.

Guidelines:
- Provide technical, highly detailed, and practical guidance tailored to offensive security.
- Use official security frameworks (MITRE ATT&CK, OWASP, CVSS v3.1).
- Always include context around safety, authorization, and ethical usage.
"""

# Header
st.title("🎯 SpectreOps AI — Red Team Assessment & Threat Emulation")
st.caption("Authorized Red Team Orchestrator, Payload Analysis & Adversary Emulation Framework")

# Sidebar Configuration
st.sidebar.header("⚙️ Configuration")
api_key_input = st.sidebar.text_input("Gemini API Key", type="password", help="Enter key from Google AI Studio")
gemini_api_key = st.secrets.get("GEMINI_API_KEY", api_key_input)

if not gemini_api_key:
    st.sidebar.warning("⚠️ Enter your Gemini API Key to activate SpectreOps AI.")

# Navigation Menu Options (Syntax-Corrected)
selected_option = option_menu(
    menu_title=None,
    options=["Target Recon & Profiler", "Kill Chain & ATT&CK Planner", "Payload & Evasion Audit", "Report Generator"],
    icons=["crosshair", "diagram-3", "code-slash", "file-earmark-text"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#1a1c23"},
        "icon": {"color": "#ff4d4d", "font-size": "16px"},
        "nav-link": {"font-size": "14px", "text-align": "center", "margin": "0px", "--hover-color": "#262933"},
        "nav-link-selected": {"background-color": "#8b0000", "color": "#ffffff"},
    }
)

# -------------------------------------------------------------------
# OPTION 1: Target Recon & Profiler
# -------------------------------------------------------------------
if selected_option == "Target Recon & Profiler":
    st.subheader("🔍 Attack Surface & Target Profiler")
    st.write("Generate custom active/passive recon strategies and scanning methodologies based on target scope.")

    col1, col2 = st.columns(2)
    with col1:
        target_type = st.selectbox("Target Type", ["External Web Application", "Internal Corporate Network", "Active Directory Domain", "Cloud Infrastructure (AWS/Azure/GCP)"])
        known_ports = st.text_input("Known Services / Ports (e.g., 80, 443, 88, 445, 3389)", placeholder="80, 443, 22")
    with col2:
        tech_stack = st.text_input("Tech Stack / OS (If known)", placeholder="e.g., Ubuntu, IIS 10, Apache Tomcat, ASP.NET")
        recon_depth = st.select_slider("Recon Depth Level", options=["Passive OSINT Only", "Standard Active Scan", "Aggressive Threat Surface Mapping"])

    if st.button("Generate Recon Strategy", type="primary"):
        if not gemini_api_key:
            st.error("Please configure your Gemini API key in the sidebar.")
        else:
            prompt = f"""
            Target Scope: {target_type}
            Known Ports/Services: {known_ports if known_ports else 'Unknown'}
            Known Tech Stack/OS: {tech_stack if tech_stack else 'Unknown'}
            Recon Depth: {recon_depth}

            Generate a comprehensive Reconnaissance Plan containing:
            1. Recommended Nmap/Masscan syntax tailored to this scope.
            2. Key OSINT sources and enumeration strategies.
            3. Specific service enumeration tools (e.g., Gobuster, Enum4linux, BloodHound) to deploy next.
            4. Potential low-hanging vulnerability checks to execute.
            """
            with st.spinner("Analyzing target profile and compiling recon strategy..."):
                try:
                    result = query_gemini_flash(prompt, RED_TEAM_SYSTEM_PROMPT, gemini_api_key)
                    st.markdown(result)
                except Exception as e:
                    st.error(f"Error generating profile: {str(e)}")

# -------------------------------------------------------------------
# OPTION 2: Kill Chain & ATT&CK Planner
# -------------------------------------------------------------------
elif selected_option == "Kill Chain & ATT&CK Planner":
    st.subheader("⚔️ Cyber Kill Chain & MITRE ATT&CK Planner")
    st.write("Emulate specific threat actors and design tactical execution paths.")

    col1, col2 = st.columns(2)
    with col1:
        target_environment = st.selectbox("Target Environment", ["Windows 11 / Enterprise Domain", "Linux Server Cluster", "Hybrid Active Directory", "Kubernetes Container Cluster"])
        initial_access_vector = st.selectbox("Initial Access Vector", ["Spearphishing Attachment/Link", "Exposed Vulnerable Service", "Valid Stolen Credentials", "Supply Chain / Third-Party"])
    with col2:
        primary_objective = st.selectbox("Primary Simulation Objective", ["Domain Admin Escalation", "Data Exfiltration Emulation", "Ransomware Defense Simulation", "Persistence & Lateral Movement"])
        evasion_requirement = st.select_slider("EDR / Security Control Evasion Level", options=["Low (Basic AV)", "Medium (Standard EDR)", "High (Strict SOC + Managed EDR)"])

    if st.button("Generate Emulation Plan", type="primary"):
        if not gemini_api_key:
            st.error("Please configure your Gemini API key in the sidebar.")
        else:
            prompt = f"""
            Environment: {target_environment}
            Initial Access Vector: {initial_access_vector}
            Primary Objective: {primary_objective}
            Security Evasion Level: {evasion_requirement}

            Construct a detailed Red Team Threat Emulation Plan:
            1. Map the attack path using MITRE ATT&CK Framework IDs (e.g., T1059, T1003).
            2. Detail step-by-step tactics: Initial Access -> Privilege Escalation -> Credential Access -> Lateral Movement -> Persistence.
            3. Identify likely defensive telemetry and log artifacts generated (for Blue Team detection verification).
            """
            with st.spinner("Mapping MITRE ATT&CK vectors and adversary simulation steps..."):
                try:
                    result = query_gemini_flash(prompt, RED_TEAM_SYSTEM_PROMPT, gemini_api_key)
                    st.markdown(result)
                except Exception as e:
                    st.error(f"Error creating plan: {str(e)}")

# -------------------------------------------------------------------
# OPTION 3: Payload & Evasion Audit
# -------------------------------------------------------------------
elif selected_option == "Payload & Evasion Audit":
    st.subheader("💻 Code Security Analysis & Obfuscation Research")
    st.write("Audit custom test scripts for dynamic detection triggers and explore bypass concepts for authorized testing.")

    script_lang = st.selectbox("Script Language", ["PowerShell", "Python", "Bash", "C / C++", "C#"])
    code_input = st.text_area("Paste Script / Proof-of-Concept Code", height=200, placeholder="Paste your test script or PoC snippet here...")

    if st.button("Audit Code for Evasion & Quality", type="primary"):
        if not gemini_api_key:
            st.error("Please configure your Gemini API key in the sidebar.")
        elif not code_input.strip():
            st.warning("Please paste code before auditing.")
        else:
            prompt = f"""
            Language: {script_lang}
            
            Code Snippet:
            ```{script_lang.lower()}
            {code_input}
            ```

            Perform a technical offensive security analysis:
            1. Identify signature triggers or behavior patterns likely to be flagged by EDR/AV/AMSI.
            2. Explain modern evasion techniques (e.g., obfuscation, API unhooking, dynamic resolution) applicable to this code logic.
            3. Provide an optimized, refactored version designed for authorized research and testing.
            """
            with st.spinner("Analyzing script mechanics and signature detection triggers..."):
                try:
                    result = query_gemini_flash(prompt, RED_TEAM_SYSTEM_PROMPT, gemini_api_key)
                    st.markdown(result)
                except Exception as e:
                    st.error(f"Error auditing code: {str(e)}")

# -------------------------------------------------------------------
# OPTION 4: Report Generator
# -------------------------------------------------------------------
elif selected_option == "Report Generator":
    st.subheader("📑 Red Team Executive Summary & Finding Reporter")
    st.write("Convert technical exploitation notes into structured, executive-ready penetration testing reports.")

    vuln_title = st.text_input("Vulnerability / Finding Title", placeholder="e.g., Unauthenticated Remote Code Execution in Web App")
    severity = st.selectbox("Severity Level", ["Critical (CVSS 9.0-10.0)", "High (CVSS 7.0-8.9)", "Medium (CVSS 4.0-6.9)", "Low (CVSS 0.1-3.9)"])
    raw_notes = st.text_area("Exploitation Details & Execution Logs", height=180, placeholder="Paste raw terminal logs, HTTP requests, or exploitation steps here...")

    if st.button("Generate Professional Report", type="primary"):
        if not gemini_api_key:
            st.error("Please configure your Gemini API key in the sidebar.")
        elif not raw_notes.strip():
            st.warning("Please provide execution details or notes.")
        else:
            prompt = f"""
            Finding Title: {vuln_title}
            Assessed Severity: {severity}
            
            Technical Notes & Proof of Concept:
            {raw_notes}

            Format this finding into a complete Red Team / PenTest Report Section:
            1. **Executive Summary**: Non-technical explanation of business impact.
            2. **Technical Risk Analysis**: Detailed breakdown of the vulnerability mechanics.
            3. **Proof of Concept (PoC)**: Clear, reproducible step-by-step instructions.
            4. **Strategic Remediation**: Detailed step-by-step instructions for Blue Team / IT to patch and secure the weakness.
            """
            with st.spinner("Formatting professional engagement report..."):
                try:
                    result = query_gemini_flash(prompt, RED_TEAM_SYSTEM_PROMPT, gemini_api_key)
                    st.markdown(result)
                except Exception as e:
                    st.error(f"Error generating report: {str(e)}")
