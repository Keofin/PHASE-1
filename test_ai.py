import ollama
from calculators import calculate_emi, calculate_dti_ratio, get_financial_verdict

def test_run():
    # 1. Run the math tools manually for a test user
    income = 40000
    existing_emis = 15000
    
    # Calculate a new loan proposal (₹1.5 Lakhs at 14.5% interest for 2 years)
    new_emi = calculate_emi(150000, 14.5, 24)
    dti = calculate_dti_ratio(income, existing_emis, new_emi)
    verdict = get_financial_verdict(dti)
    
    # 2. Package everything into a text block for Llama to read
    financial_data_context = f"""
    User Income: ₹{income}
    Existing EMIs: ₹{existing_emis}
    New Calculated EMI: ₹{new_emi}
    Total Debt-to-Income Ratio: {dti}%
    Our Advisory Rule Verdict: {verdict['verdict']} ({verdict['reason']})
    """
    
    print("🤖 Processing context through your local Llama model...")
    
    # 3. Ask your local Llama model to draft the final response text
    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "system",
                "content": "You are a friendly financial advisor helper. Explain the numbers calmly to an everyday Indian user using no corporate jargon."
            },
            {
                "role": "user",
                "content": f"{financial_data_context}\n\nCustomer wants a loan for an iPhone. Explain our verdict to them."
            }
        ]
    )
    
    print("\n📝 Here is the AI Draft Response:")
    print(response['message']['content'])

if __name__ == "__main__":
    test_run()