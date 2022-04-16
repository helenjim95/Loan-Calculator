import math
import argparse
import sys
import null as null

parser = argparse.ArgumentParser()
parser.add_argument("--type", choices=["diff", "annuity"], type=str, required = True)
parser.add_argument("--principal", type=int, required=False)
parser.add_argument("--periods", type=int, required=False)
parser.add_argument("--payment", type=int, required=False)
parser.add_argument("--interest", type=float)
args = parser.parse_args()
calculation = [args.type, args.principal, args.periods, args.payment, args.interest]

type_ = args.type
if args.principal is not None:
    principal = int(args.principal)
if args.periods is not None:
    number_of_periods = int(args.periods)
if args.interest is not None:
    loan_interest = float(args.interest)
if args.payment is not None:
    monthly_payment = int(args.payment)


def convert_nominal_interest_rate(loan_interest):
    nominal_interest_rate = float(loan_interest / 100 / 12)
    return nominal_interest_rate


def calculate_number_of_periods():
    nominal_interest_rate = convert_nominal_interest_rate(loan_interest)
    base = 1 + nominal_interest_rate
    number = (monthly_payment / (monthly_payment - nominal_interest_rate * principal))
    number_of_periods = math.ceil(math.log(number, base))
    return number_of_periods


def calculate_monthly_payment():
    nominal_interest_rate = convert_nominal_interest_rate(loan_interest)
    nominator = principal * ((nominal_interest_rate) * math.pow((1 + nominal_interest_rate), number_of_periods))
    denominator = math.pow((1 + nominal_interest_rate), number_of_periods) - 1
    monthly_payment = math.ceil(nominator / denominator)
    return monthly_payment


def calculate_differentiated():
    sum_payment = 0
    nominal_interest_rate = convert_nominal_interest_rate(loan_interest)
    for i in range(number_of_periods):
        current_repayment_month = i + 1
        payment = math.ceil((principal / number_of_periods) + nominal_interest_rate * (
                principal - (principal * (current_repayment_month - 1) / number_of_periods)))
        sum_payment += payment
        print(f"Month {current_repayment_month}: payment is {payment}")
    overpayment = principal - sum_payment
    print(f"Overpayment = {overpayment}")


def calculate_principal():
    nominator = monthly_payment
    nominal_interest_rate = convert_nominal_interest_rate(loan_interest)
    denominator = ((nominal_interest_rate) * math.pow((1 + nominal_interest_rate), number_of_periods)) / (
            math.pow((1 + nominal_interest_rate), number_of_periods) - 1)
    principal = nominator / denominator
    return principal


def convert_periods():
    number_of_year = number_of_periods // 12
    number_of_month = number_of_periods % 12
    return number_of_year, number_of_month


def calculate_overpayment():
    overpayment = principal - monthly_payment * number_of_periods
    return overpayment


def calculate_length():
    length = len(calculation)
    for i in range(len(calculation)):
        if calculation[i] is None:
            length -= 1
    return length

length = calculate_length()

# Check parameter:
if type_ != "annuity" and type_ != "diff":
    print("Incorrect parameters")
# For both types, 4 parameters are needed:
# Type, 3 out of 4 (principal, payment, periods, interest)
elif length < 4:
    print("Incorrect parameters")
elif args.interest is None:
    print("Incorrect parameters")
elif type_ == "diff":
    if args.payment is not None:
        print("Incorrect parameters")
    else:
        calculate_differentiated()
elif type_ == "annuity":
    if args.principal is None:
        principal = calculate_principal()
        print(f"Your loan principal = {principal}!")
    elif args.periods is None:
        loan_interest = float(args.interest)
        nominal_interest_rate = convert_nominal_interest_rate(loan_interest)
        number_of_periods = calculate_number_of_periods()
        overpayment = calculate_overpayment()
        if number_of_periods == 1:
            print(f"It will take {number_of_periods} month to repay the loan")
        elif number_of_periods < 12:
            print(f"It will take {number_of_periods} months to repay the loan")
        else:
            number_of_year, number_of_month = convert_periods()
            print(f"It will take {number_of_year} years and {number_of_month} months to repay this loan!")
        print(f"Overpayment = {overpayment}")
    elif args.payment is None:
        monthly_payment = calculate_monthly_payment()
        overpayment = calculate_overpayment()
        print(f"Your annuity payment = {monthly_payment}!")
        print(f"Overpayment = {overpayment}")
