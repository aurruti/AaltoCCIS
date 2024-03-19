# File task2.py
# Aitor Urruticoechea 2023
from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import norm
from fitter import Fitter, get_common_distributions, get_distributions

choice = False
while not(choice):
    file = input("File to analyse (a/b/c): ")
    if file == "a":
        file = "sampling-data/distr_a.txt"
        choice = True
    elif file == "b":
        file = "sampling-data/distr_b.txt"
        choice = True
    elif file == "c":
        file = "sampling-data/distr_c.txt"
        choice = True
    else:
        print("Invalid choice")
data = np.loadtxt(file)

if file != 'sampling-data/distr_b.txt':
    f = Fitter(data,
            distributions=[
    'alpha',
    'arcsine',
    'beta',
    'betaprime',
    'bradford',
    'cauchy',
    'chi',
    'cosine',
    'dgamma',
    'dweibull',
    'expon',
    'exponnorm',
    'exponpow',
    'exponweib',
    'f',
    'foldcauchy',
    'foldnorm',
    'gamma',
    'genpareto',
    'gumbel_l',
    'gumbel_r',
    'halfcauchy',
    'halfgennorm',
    'halflogistic',
    'halfnorm',
    'hypsecant',
    'invgamma',
    'invgauss',
    'invweibull',
    'laplace',
    'laplace_asymmetric',
    'loggamma',
    'logistic',
    'loglaplace',
    'lognorm',
    'loguniform',
    'maxwell',
    'norm',
    'norminvgauss',
    'pareto',
    'powerlaw',
    'powerlognorm',
    'powernorm',
    'rayleigh',
    'rice',
    'rv_continuous',
    'rv_histogram',
    'skewcauchy',
    'studentized_range',
    't',
    'truncexpon',
    'truncnorm',
    'truncweibull_min',
    'uniform',
    'weibull_max',
    'weibull_min',
    'wrapcauchy']
    )
    f.fit()
    print(f.summary())
    print(f.get_best())
else:
    mu, std = norm.fit(data)
    plt.hist(data, bins=30, density=True, alpha=0.6, color='g', label='Data Histogram')
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2, label='Fitted Normal Distribution')
    plt.title("Fit results: mu = %.2f,  std = %.2f" % (mu, std))
    plt.legend()

plt.show()
