inflation_percent = 2
monthly_inflation_multiplier = (1 + (inflation_percent / 100)) ** (1 / float(12))

initial_amount = 500000
monthly_deposit = 2000

years = 25

total_amount = initial_amount
for i in range(0, years * 12):
    total_amount = (total_amount + monthly_deposit) * monthly_inflation_multiplier

print(f"With an inflation of {inflation_percent}% each year, "
      f"over a period of {years} years, "
      f"just to not have lost any buying power,"
      f"your investment would need to be at least {round(total_amount)}")
