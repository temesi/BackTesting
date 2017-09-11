import csv
import collections
from math import sqrt, exp, log, erf
from pprint import pprint as pp

def N(x):
    'phi: Cumulative distribution function for the standard normal distribution'
    return (1.0 + erf(x / sqrt(2.0))) / 2.0

with open(r'c:\Users\temes\Documents\python_quiz\spx_vols.txt', mode='r', encoding='ascii') as spx_file:
    reader = csv.reader(spx_file)
    headers = [col.lower() for col in next(reader)]  # get headers in lower case
    Data = collections.namedtuple("Data", headers)
    for data in map(Data._make, reader):
        pass

# inputs
spot = 66.24  # St: current stock price
strike = 64  # K: strike price
time_to_maturity_in_days = 202  # days until maturity
time = time_to_maturity_in_days / 365  # T-t: time to maturity (expressed in years)
sigma = .7082  # volatility standard derivation of stock's return
rate = 0.0025  # r: annualized risk-free interest rate

# Black–Scholes model statistics
sigma_squared_time = sigma * sqrt(time)
ert = exp((-rate/365)*time)
d1 = (log(spot/strike)+(rate+.5*(sigma**2)*time))/sigma_squared_time
d2 = d1 - sigma_squared_time

# outputs
call_price = round(spot*N(d1)-strike*ert*N(d2), 2)
put_price = round(strike*ert*N(-d2)-spot*N(-d1), 2)

pp(call_price)
pp(put_price)


# with open(r'c:\Users\temes\Documents\python_quiz\report.txt', mode='w', encoding='ascii') as outfile:
#    writer = csv.writer(outfile)