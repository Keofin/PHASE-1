def calculate_emi(principal: float, annual_rate: float, months: int) -> float:
    """
    Calculates the monthly EMI.
    Formula: EMI = [P x r x (1+r)^n] / [((1+r)^n) - 1]
    where r is monthly interest rate (annual_rate / 12 / 100)
    """
    if annual_rate == 0:
        return round(principal / months, 2)
    
    monthly_rate = (annual_rate / 12) / 100
    emi = (principal * monthly_rate * ((1 + monthly_rate) ** months)) / (((1 + monthly_rate) ** months) - 1)
    return round(emi, 2)


def calculate_dti_ratio(monthly_income: float, total_existing_emis: float, proposed_new_emi: float = 0.0) -> float:
    """
    Calculates the Debt-to-Income (DTI) ratio as a percentage.
    """
    if monthly_income <= 0:
        return 100.0  # Avoid division by zero, assume high risk
    
    total_debt = total_existing_emis + proposed_new_emi
    dti = (total_debt / monthly_income) * 100
    return round(dti, 2)


def get_financial_verdict(dti_ratio: float) -> dict:
    """
    Returns an advisory verdict based on the 50% DTI rule.
    """
    if dti_ratio > 50.0:
        return {
            "status": "DANGER",
            "verdict": "DO NOT BORROW",
            "reason": f"Your monthly EMIs take up {dti_ratio}% of your income. This is over our safe limit of 50%. You should focus on clearing existing debt first."
        }
    elif dti_ratio > 40.0:
        return {
            "status": "WARNING",
            "verdict": "BORDERLINE / CAUTION",
            "reason": f"Your EMIs take up {dti_ratio}% of your income. You are very close to the danger zone. Borrow only if absolutely necessary."
        }
    else:
        return {
            "status": "SAFE",
            "verdict": "AFFORDABLE",
            "reason": f"Your EMIs take up {dti_ratio}% of your income. This is within a healthy and manageable range."
        }