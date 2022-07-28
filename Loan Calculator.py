import math
import argparse
import sys

error = "Incorrect parameters"

if len(sys.argv) < 4:
    print(error)
else:
    if len(sys.argv) >= 4:
        parser = argparse.ArgumentParser()
        parser.add_argument("--type", type=str, help="What to count")
        parser.add_argument("--payment", type=int, help="Monthly payment")
        parser.add_argument("--principal", type=int, help="Starting balance")
        parser.add_argument("--periods", type=int, help="Years and months to pay")
        parser.add_argument("--interest", type=float, help="Interest rate")
        args = parser.parse_args()

        if (args.payment or args.principal or args.periods or args.interest) < 0:
            print(error)
        else:
            if args.type not in ("annuity", "diff"):
                print(error)
            else:
                if args.type == 'diff' and args.payment is not None:
                    print(error)
                else:
                    if args.interest is None:
                        print(error)
                    else:
                        i = args.interest / (12 * 100)

                        if args.type == 'diff':
                            payments = []
                            for month in range (0, args.periods):
                                month += 1
                                payment = (args.principal / args.periods) + (i *(args.principal - ((args. principal * (month - 1)) / args.periods)))
                                payment = math.ceil(payment)
                                payments.append(payment)
                                print(f'Month {month}: paid out {payment}')
                            print(f'\nOverpayment = {math.ceil(sum(payments) - args.principal)}')

                        elif args.type == 'annuity':
                            if (args.principal and args.periods) is not None:
                                annuity_payment = (args.principal * (i * ((1 + i) ** args.periods)) / (
                                ((1 + i) ** args.periods) - 1))
                                annuity_payment = math.ceil(annuity_payment)
                                print(f'Your annuity payment = {annuity_payment}!\nOverpayment = {(annuity_payment * args.periods) - args.principal}')

                        if (args.payment and args.periods) is not None:
                            credit_principal = args.payment / ((i * ((1 + i) ** args.periods)) / (((1 + i) ** args.periods) - 1))
                            credit_principal = math.ceil(credit_principal)
                            print(credit_principal)

                        if (args.principal and args.payment) is not None:
                            periods_count = math.log(args.payment / (args.payment - (i * args.principal)), 1 + i)
                            periods_count = math.ceil(periods_count)
                            if periods_count <= 12:
                                print(f'You need {periods_count} months to repay this credit!')
                            elif periods_count > 12 and periods_count % 12 == 0:
                                print(f'You need {periods_count // 12} years to repay this credit!')
                            else:
                                print(f'You need {periods_count // 12} years and {periods_count % 12} months to repay this credit!')
                            print(f'Overpayment = {(periods_count * args.payment) - args.principal}')