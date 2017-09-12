class Strategy:
    """
    Strategy is tells the Portfolio what to do.


    """

    reference_notional = 1000000

class Portfolio:
    """
    Portfolio has a list of Options. Strategy is tells the Portfolio what to do.


    """

    def payoff_call(self, St, strike):
        return (St - strike + abs(St - strike)) / 2

    def payoff_put(self, St, strike):
        return (strike - St + abs(St - strike)) / 2

    def profit_and_loss(self, ):