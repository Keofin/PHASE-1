import json
from workers import Response
from calculators import calculate_emi, calculate_dti_ratio, get_financial_verdict

async def on_fetch(request, env, ctx):
    # Only allow POST API requests
    if request.method != "POST":
        return Response.json({"error": "Method not allowed. Use POST."}, status=405)

    try:
        # Read customer financial details from incoming JSON payload
        body = await request.json()

        income = float(body.get("income", 0))
        existing_emis = float(body.get("existing_emis", 0))
        proposed_loan = float(body.get("proposed_loan", 0))
        rate = float(body.get("rate", 0))
        tenure_months = int(body.get("tenure_months", 1))
        customer_query = body.get("customer_query", "")

        # 1. Run our rock-solid deterministic math formulas
        new_emi = calculate_emi(proposed_loan, rate, tenure_months)
        dti_ratio = calculate_dti_ratio(income, existing_emis, proposed_new_emi=new_emi)
        verdict_data = get_financial_verdict(dti_ratio)

        # 2. Compile context details for the Cloud AI model
        financial_data_context = f"""
        CUSTOMER FINANCIAL SITUATION:
        - Monthly Income: ₹{income}
        - Existing EMIs: ₹{existing_emis}
        - New Calculated EMI: ₹{new_emi}
        - Total Debt-to-Income (DTI) Ratio: {dti_ratio}%
        - Hard Financial Verdict: {verdict_data['verdict']}
        - System Advisory Guidance: {verdict_data['reason']}
        """

        system_instruction = """You are an AI Copilot drafting messages for a human financial advisor at KeoFin.
        STRICT RULES:
        1. NEVER invent or guess financial metrics. Use ONLY the verified numbers provided in the context.
        2. Keep your tone empathetic, conversational, respectful, and perfectly aligned with mass-market Indian cash flows.
        3. Explicitly carry out the hard advisory guidance (e.g. explain why going over 50% DTI is dangerous)."""

        # 3. Call Cloudflare's Edge AI network directly
        ai_response = await env.AI.run(
            "@cf/meta/llama-3-8b-instruct",
            {
                "messages": [
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": f"{financial_data_context}\n\nCustomer's Message: {customer_query}"}
                ]
            }
        )

        # 4. Return everything back to your app frontends cleanly
        response_payload = {
            "proposed_emi": new_emi,
            "dti_ratio": dti_ratio,
            "verdict": verdict_data["verdict"],
            "status": verdict_data["status"],
            "guidance": verdict_data["reason"],
            "ai_draft": ai_response["response"]
        }

        return Response.json(response_payload, status=200)

    except Exception as e:
        return Response.json({"error": str(e)}, status=500)