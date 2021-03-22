import math
import argparse


def calc_i(i):
    return i / (12 * 100)


def calc_n(p, a, i):
    return math.ceil(math.log((a/(a - calc_i(i) * p)), 1 + calc_i(i)))


def calc_a(p, n, i):
    return math.ceil(p * (calc_i(i) * math.pow(1 + calc_i(i), n)) / (math.pow(1 + calc_i(i), n) - 1))


def calc_p(a, n, i):
    return math.floor(a / ((calc_i(i) * math.pow(1 + calc_i(i), n)) / (math.pow(1 + calc_i(i), n) - 1)))


def calc_dm(p, n, i, m):
    return math.ceil(p / n + i * (p - (p * (m - 1)) / n))


parser = argparse.ArgumentParser()
parameters = ["--type", "--payment", "--principal", "--periods", "--interest"]
for i in parameters:
    parser.add_argument(i)
args = parser.parse_args()
parameters_provided = [args.type, args.payment, args.principal, args.periods, args.interest]

CORRECT_TYPES = ["annuity", "diff"]
cond1 = len([i for i in parameters_provided if i is not None]) < 4
cond2 = args.type not in CORRECT_TYPES
cond3 = args.type == "diff" and args.payment is not None
cond4 = args.interest is None
cond5 = any([float(i) < 0 for i in parameters_provided[1:] if i is not None])
conds = [cond1, cond2, cond3, cond4, cond5]
if any(conds):
    print("Incorrect parameters.")
    exit()

for i, parameter in enumerate(parameters_provided):
    if parameter is None and not (args.type == 'diff' and args.principal is None):
        task = parameters[i].lstrip("-")
if task == 'payment':
    if args.type == 'diff':
        overpayment = -int(args.principal)
        for i in range(int(args.periods)):
            dm = calc_dm(float(args.principal), int(args.periods), calc_i(float(args.interest)), i+1)
            overpayment += dm
            print(f"Month {i+1}: payment is {dm}")
        print("\n" + f"Overpayment = {overpayment}")
    elif args.type == "annuity":
        a = calc_a(float(args.principal), int(args.periods), float(args.interest))
        overpayment = -int(args.principal) + a * int(args.periods)
        print(f"Your annuity payment = {a}!")
        print(f"Overpayment = {overpayment}")
elif task == 'principal':
    p = calc_p(float(args.payment), int(args.periods), float(args.interest))
    overpayment = -p + int(args.payment) * int(args.periods)
    print(f"Your loan principal = {p}!")
    print(f"Overpayment = {overpayment}")
elif task == 'periods':
    n = calc_n(float(args.principal), float(args.payment), float(args.interest))
    overpayment = -int(args.principal) + int(args.payment) * n
    if n % 12 == 0:
        print(f"It will take {n // 12} years to repay this loan!")
    else:
        print(f"It will take {n // 12} years and {n % 12} month{'' if n % 12 == 1 else 's'} to repay this loan!")
    print(f"Overpayment = {overpayment}")
