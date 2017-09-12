import csv
import collections
from scipy.stats import norm
from math import sqrt, exp, log
from datetime import datetime
from pprint import pprint as pp

with open(r'c:\Users\temes\Documents\python_quiz\spx_vols.txt', mode='r', encoding='ascii') as spx_file:
    reader = csv.reader(spx_file)
    headers = [col.lower() for col in next(reader)]  # get headers in lower case
    Data = collections.namedtuple("Data", headers)
    for data in map(Data._make, reader):
        spot = float(data[2])
        strike = round(float(data[2]),-1)
        start_date = datetime.strptime(data[0], "%Y%m%d").date()
        maturity_date = datetime.strptime(data[1], "%Y%m%d.0").date()
        days = (maturity_date-start_date).days
        vol = float(data[3])
        pp((spot,strike,days,vol))

# inputs
stock = 66.24  # St: current stock price
strike = 45  # K: strike price
time_to_maturity_in_days = 202  # days until maturity
time = time_to_maturity_in_days / 365  # T-t: time to maturity (expressed in years)
sigma = .7082  # volatility standard derivation of stock's return
rate = 0.0025  # r: annualized risk-free interest rate

# Black–Scholes model statistics
sigma_squared_time = sigma * sqrt(time)
ert = exp(-rate*time)
d1 = (log(stock/strike)+(rate+.5*(sigma**2)*time))/sigma_squared_time
d2 = d1 - sigma_squared_time

# outputs
call_price = round(stock*norm.cdf(d1)-strike*ert*norm.cdf(d2), 4)
put_price = round(strike*ert*norm.cdf(-d2)-stock*norm.cdf(-d1), 4)

greek_delta_call = norm.cdf(d1)
greek_delta_put = norm.cdf(d1)-1
greek_gamma = norm.pdf(d1)/ (stock * sigma_squared_time)
greek_vega = stock * norm.pdf(d1) * sqrt(time)
greek_theta_call = (-(stock * norm.pdf(d1) * sigma)/(2 * sqrt(time)) - rate * strike * ert * norm.cdf(d2))/365
greek_theta_put =  (-(stock * norm.pdf(d1) * sigma)/(2 * sqrt(time)) + rate * strike * ert * norm.cdf(-d2))/365

print("{0:<15s} {1:8.4f}".format('Call price:', call_price))
print("{0:<15s} {1:8.4f}".format('Put price:', put_price))
print("{0:<15s} {1:8.4f}".format('Call Delta:', greek_delta_call))
print("{0:<15s} {1:8.4f}".format('Put Delta:', greek_delta_put))
print("{0:<15s} {1:8.4f}".format('Gamma:', greek_gamma))
print("{0:<15s} {1:8.4f}".format('Vega:',  greek_vega))
print("{0:<15s} {1:8.4f}".format('Call Theta:',  greek_theta_call))
print("{0:<15s} {1:8.4f}".format('Put Theta:',  greek_theta_put))


# with open(r'c:\Users\temes\Documents\python_quiz\report.txt', mode='w', encoding='ascii') as outfile:
#    writer = csv.writer(outfile)