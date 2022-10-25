from datetime import date
from enum import Enum

from dateutil.relativedelta import relativedelta


class InvestmentType(Enum):
    ETFS = 1
    SINGLE_STOCKS = 2
    REAL_ESTATE = 3
    BONDS = 4
    CASH = 5


YOY_RETURN_ESTIMATES = {
    InvestmentType.SINGLE_STOCKS: 7,
    InvestmentType.ETFS: 7,  # TODO
    InvestmentType.REAL_ESTATE: 5.8,  # TODO confirm
    InvestmentType.BONDS: 4.0,  # TODO recalculate with failing percentages van cursus TODO - vermeld verlies van recurrente interest hier laten vallen <-> herinvesteer jaarlijks terug in bonds voor simplicity's sake.
    InvestmentType.CASH: 0.05,  # TODO explain that we assume some return on cash <-> savings accounts etc.
}

MOM_RETURN_MULTIPLIER = {
    InvestmentType.SINGLE_STOCKS: (1 + (YOY_RETURN_ESTIMATES[InvestmentType.SINGLE_STOCKS] / 100)) ** (1 / float(12)),
    InvestmentType.ETFS: (1 + (YOY_RETURN_ESTIMATES[InvestmentType.ETFS] / 100)) ** (1 / float(12)),
    InvestmentType.REAL_ESTATE: (1 + (YOY_RETURN_ESTIMATES[InvestmentType.REAL_ESTATE] / 100)) ** (1 / float(12)),
    InvestmentType.BONDS: (1 + (YOY_RETURN_ESTIMATES[InvestmentType.BONDS] / 100)) ** (1 / float(12)),
    InvestmentType.CASH: (1 + (YOY_RETURN_ESTIMATES[InvestmentType.CASH] / 100)) ** (1 / float(12)),
}


class Portfolio:
    def __init__(self, starting_date: date, starting_cash, monthly_deposit, monthly_percentages):
        self.starting_date = starting_date
        self.date = starting_date
        self.starting_cash = starting_cash
        self.allocation = dict()
        self.monthly_deposit = monthly_deposit
        self.monthly_percentages = dict
        self.set_monthly_deposit_allocation(monthly_percentages)
        for investment_type in InvestmentType:
            self.allocation.update({investment_type: 0})  # start each investment_type at 0
        self.allocation.update({InvestmentType.CASH: starting_cash})

    def print_allocation(self):
        """For debugging"""
        for key, val in self.allocation.items():
            print(f"{key.name} -> {val}")
        print("-----")

    def set_monthly_deposit_allocation(self, monthly_percentages: dict):
        """allocation should be a dict containing InvestmentType -> percentage"""
        total = 0
        for _, percentage in monthly_percentages.items():
            total += percentage
        if total != 100:
            raise Exception(f"Not everything of the monthly deposit is allocated, only {total}%")
        self.monthly_percentages = monthly_percentages

    def invest_percentage_of_starting_cash(self, investment_type, percentage_of_starting_cash):
        """Invests percentage of starting cash if there is enough, if not enough, invest the last bit remaining"""
        amount = percentage_of_starting_cash/100 * self.starting_cash
        if self.allocation[InvestmentType.CASH] - amount > 0:
            self.allocation[InvestmentType.CASH] = self.allocation[InvestmentType.CASH] - amount
            self.allocation[investment_type] = self.allocation[investment_type] + amount
        else:
            self.allocation[investment_type] = self.allocation[investment_type] + self.allocation[InvestmentType.CASH]
            self.allocation[InvestmentType.CASH] = 0

    def simulate_one_month(self):
        # TODO parametrize percentage of starting cash => slightly more into single stocks because of first big chunk into ETF's
        # getting starting cash invested
        self.invest_percentage_of_starting_cash(InvestmentType.SINGLE_STOCKS, 0.92)
        self.invest_percentage_of_starting_cash(InvestmentType.ETFS, 0.92)

        # allocation of monthly deposit
        for investment_type, percent in self.monthly_percentages.items():
            self.allocation[investment_type] += percent/100 * self.monthly_deposit

        # rise in value:
        for investment_type, worth in self.allocation.items():
            self.allocation[investment_type] *= MOM_RETURN_MULTIPLIER[investment_type]

        self.date = self.date + relativedelta(months=1)

    def get_portfolio_worth(self):
        total = 0
        for investment_type, worth in self.allocation.items():
            total += worth

        return total


if __name__ == "__main__":
    p = Portfolio(starting_date=date.today(),
                  starting_cash=500000,
                  monthly_deposit=2000,
                  monthly_percentages={InvestmentType.ETFS: 50, InvestmentType.SINGLE_STOCKS: 50}
                  )

    p.invest_percentage_of_starting_cash(InvestmentType.ETFS, 33)
    p.invest_percentage_of_starting_cash(InvestmentType.BONDS, 17)

    while p.allocation[InvestmentType.CASH] != 0:
        p.simulate_one_month()
    p.print_allocation()
    print(p.date)
    print(p.get_portfolio_worth())

    # TODO here stop initial cash investing things

    while p.date < p.starting_date + relativedelta(years=5):
        p.simulate_one_month()
    p.print_allocation()
    print(p.date)
    print(p.get_portfolio_worth())

    # TODO here 6 months of saving the monthly deposit, then get mortgage for ... / calculate new monthly allocation
    # TODO write something for mortgage + adjust get_portfolio_worth

    # TODO lose some percentages (3%?) when selling bonds

    # TODO implement rental income (be very conservative:x% of real_estate type - (25% costs and repairs + 25% of labour costs)) ------- monthly deposit.

    # TODO remove temp below to see after 25 years current thing:
    while p.date < p.starting_date + relativedelta(years=25):
        p.simulate_one_month()
    p.print_allocation()
    print(p.date)
    print(p.get_portfolio_worth())
