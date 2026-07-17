import streamlit as st
import ollama
from calculators import calculate_emi, calculate_dti_ratio, get_financial_verdict

# Set up webpage title and style
st.set_page_config(page_title="KeoFin Advisor Console", layout="wide")

st.title("🛡️ KeoFin Advisor Copilot Console")
st.subheader("Phase-1 Prototype: Deterministic Guardrails + AI Draft Generation")
st.write("---")

# Layout: Split screen into 2 columns (Left for inputs, Right for AI response)
col1, col2 = st.columns([1, 1.5])

with col1:
    st.header("👤 Customer Financial Inputs")
    
    customer_query = st.text_area(
        "Customer's Message / Request:", 
        value="Hey, I need a personal loan to buy an iPhone, my friend said I can get a loan easily. What should I do?"
    )
    
    income = st.number_input("Monthly Income (₹):", min_value=0.0, value=40000.0, step=5000.0)
    existing_emis = st.number_input("Total Existing EMIs (₹):", min_value=0.0, value=15000.0, step=1000.0)
    
    st.markdown("### Proposed New Loan Details")
    proposed_loan = st.number_input("Proposed Loan Principal (₹):", min_value=0.0, value=150000.0, step=10000.0)
    rate = st.number_input("Annual Interest Rate (%):", min_value=0.0, value=14.5, step=0.5)
    tenure_months = st.number_input("Tenure (Months):", min_value=1, value=24, step=1)
    
    submit_btn = st.button("Generate Advisor Draft", type="primary")

with col2:
    st.header("🤖 AI Copilot Draft Output")
    
    if submit_btn:
        with st.spinner("Running deterministic math tools and generating draft... Please wait."):
            # 1. Run our rock-solid formulas
            new_emi = calculate_emi(proposed_loan, rate, tenure_months)
            dti_ratio = calculate_dti_ratio(income, existing_emis, proposed_new_emi=new_emi)
            verdict_data = get_financial_verdict(dti_ratio)
            
            # 2. Display the hard technical metrics at the top
            st.metric(label="Calculated Proposed New EMI", value=f"₹{new_emi:,.2f}")
            
            # Show color-coded status badge based on verdict
            if verdict_data["status"] == "DANGER":
                st.error(f"🛑 VERDICT: {verdict_data['verdict']} (DTI Ratio: {dti_ratio}%)")
            elif verdict_data["status"] == "WARNING":
                st.warning(f"⚠️ VERDICT: {verdict_data['verdict']} (DTI Ratio: {dti_ratio}%)")
            else:
                st.success(f"✅ VERDICT: {verdict_data['verdict']} (DTI Ratio: {dti_ratio}%)")
                
            st.info(f"**System Advisory Guidance:** {verdict_data['reason']}")
            st.write("---")
            
            # 3. Compile context and query the local Llama model
            financial_data_context = f"""
            CUSTOMER FINANCIAL SITUATION:
            - Monthly Income: ₹{income}
            - Existing EMIs: ₹{existing_emis}
            - New Calculated EMI: ₹{new_emi}
            - Total Debt-to-Income (DTI) Ratio: {dti_ratio}%
            - Hard Financial Verdict: {verdict_data['verdict']}
            - System Advisory Guidance: {verdict_data['reason']}
            """
            
            # System prompt matching our rulebook
            system_instruction = """You are an AI Copilot drafting messages for a human financial advisor at KeoFin.
            STRICT RULES:
            1. NEVER invent or guess financial metrics. Use ONLY the verified numbers provided in the context.
            2. Keep your tone empathetic, conversational, respectful, and perfectly aligned with mass-market Indian cash flows. Use clear analogies if helpful.
            3. Explicitly carry out the hard advisory guidance (e.g. explain why going over 50% DTI is dangerous)."""
            
            response = ollama.chat(
                model="llama3.2:3b",
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": f"{financial_data_context}\n\nCustomer's Message: {customer_query}"}
                ]
            )
            
            # Output the drafted reply in a clean text box
            st.subheader("Drafted Response for Human Advisor Review:")
            st.text_area("Copy/Edit Draft text:", value=response['message']['content'], height=300)
    else:
        st.write("Modify the input fields on the left and click **'Generate Advisor Draft'** to view calculations and AI response.")