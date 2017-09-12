
from enum import Enum
from datetime import date
from scipy.stats import norm
from math import sqrt, exp, log

class OptionType(Enum):
    CALL = 1
    PUT = -1

class Option:
    """
    Generic Option class extension point for other models

    Parameters
    ----------
    option_type : OptionType
        defines if Call or Put option
    stock : float
        St: current stock price
    strike : float
        K: strike price
    start_date : date
        contract start date
    maturity_date : date
        date of maturity
    sigma : float
        volatility standard derivation of stock's return
    rate : float

    Attributes
    -------
    option_type : OptionType
        sets or gets the option type for the object
    """

    def __init__(self, option_type, stock, strike, start_date, maturity_date, sigma, rate = 0.0, dividend = 0.0):
        self._option_type = OptionType(option_type)  # Option type Call or Put
        self._stock = stock  # St: current stock price
        self._strike = strike  # K: strike price
        self._start_date = start_date  # contract start date
        self._maturity_date = maturity_date  # Date of maturity
        days_to_maturity = (self._maturity_date-self._start_date).days  # days until maturity
        self._time = days_to_maturity / 365  # T-t: time to maturity (expressed in years)
        self._sigma = sigma # volatility standard derivation of stock's return
        self._rate = rate  # r: annualized risk-free interest rate
        self._dividend = dividend  # no dividend in the test

    @property
    def option_type(self):
        return self._option_type

    @option_type.setter
    def option_type(self, type):
        self._option_type = OptionType(type)

    def payoff(self, St):
        if self._option_type == OptionType.CALL:
            return (St - self._strike + abs(St - self._strike)) / 2
        else:
            return (self._strike - St + abs(St - self._strike)) / 2

class BlackScholesMerton(Option):
    """
    Black-Scholes-Merton model
        ref: https://en.wikipedia.org/wiki/Black–Scholes_model

    Properties
    -------
    delta : float
        Greek Delta
    gamma : float
        Greek Gamma
    vega : float
        Greek Vega
    theta : float
        Greek Theta
    price : float
        Theoretical price
    """

    def __init__(self, option_type, stock, strike, start_date, maturity_date, sigma, rate):
        super(BlackScholesMerton, self).__init__(option_type, stock, strike, start_date, maturity_date, sigma, rate)

    @property
    def d1(self):
        return (log(self._stock/self._strike)+
                (self._rate+.5*(self._sigma**2)*self._time))/(self._sigma * sqrt(self._time))

    @property
    def d2(self):
        return self.d1 - self._sigma * sqrt(self._time)

    @property
    def delta(self):
        ert = exp(-self._rate * self._time)
        if self._option_type == OptionType.CALL:
            return norm.cdf(self.d1)
        else:
            return norm.cdf(self.d1)-1

    @property
    def gamma(self):
        return norm.pdf(self.d1)/ (self._stock * self._sigma * sqrt(self._time))

    @property
    def vega(self):
        return self._stock * norm.pdf(self.d1) * sqrt(self._time)

    @property
    def theta(self):
        ert = exp(-self._rate * self._time)
        if self._option_type == OptionType.CALL:
            return (-(self._stock * norm.pdf(self.d1) * self._sigma)/(2 * sqrt(self._time)) -
                    self._rate * self._strike * ert * norm.cdf(self.d2))/365
        else:
            return (-(self._stock * norm.pdf(self.d1) * self._sigma)/(2 * sqrt(self._time)) +
                    self._rate * self._strike * ert * norm.cdf(-self.d2))/365

    @property
    def price(self):
        ert = exp(-self._rate * self._time)
        if self._option_type == OptionType.CALL:
            return self._stock * norm.cdf(self.d1) - self._strike * ert * norm.cdf(self.d2)
        else:
            return self._strike*ert*norm.cdf(-self.d2)-self._stock*norm.cdf(-self.d1)
