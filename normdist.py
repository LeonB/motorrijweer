#from __future__ import division
from math import *
def erfcc(x):
    """Complementary error function."""
    z = abs(x)
    t = 1. / (1. + 0.5*z)
    r = t * exp(-z*z-1.26551223+t*(1.00002368+t*(.37409196+
        t*(.09678418+t*(-.18628806+t*(.27886807+
        t*(-1.13520398+t*(1.48851587+t*(-.82215223+
        t*.17087277)))))))))
    if (x >= 0.):
        return r
    else:
        return 2. - r

def normcdf(x, mu, sigma):
    t = x-mu;
    y = 0.5*erfcc(-t/(sigma*sqrt(2.0)));
    if y>1.0:
        y = 1.0;
    return y

def normpdf(x, mu, sigma):
    x = float(x)
    mu = float(mu)
    sigma = float(sigma)
    u = (x-mu)/abs(sigma)
    y = (1/(sqrt(2*pi)*abs(sigma)))*exp(-u*u/2)
    return y

def normdist(x, mu, sigma, f):
    if f:
        y = normcdf(x,mu,sigma)
    else:
        y = normpdf(x,mu,sigma)
    return y

#print normcdf(20, 20, 1)

import scipy.stats
#print scipy.stats.norm.cdf(20, 20, 5)
#print scipy.stats.norm.cdf(10, 20, 5)
#print scipy.stats.norm.cdf(30, 20, 5)

#print '---------------------------------------'

#print normcdf(20, 20, 5)
#print normcdf(10, 20, 5)
#print normpdf(10, 20, 5)
#print normcdf(30, 20, 5)
#print normpdf(30, 20, 5)


#print scipy.stats.norm.pdf(20, 20, 10)
#print normpdf(20, 20, 10)

#print scipy.stats.norm.pdf(15, 20, 10)
#print normpdf(15, 20, 10)

#print scipy.stats.norm.pdf(10, 20, 10)
#print normpdf(10, 20, 10)

#print scipy.stats.norm.cdf(20, 20, 10)
#print scipy.stats.norm.cdf(15, 20, 10)
#print scipy.stats.norm.cdf(10, 20, 10)
#import sys
#sys.exit(12)

best = 23
afwijking = 8
baseline = scipy.stats.norm.pdf(best, best, afwijking)
max_punten = 4
mod = max_punten/baseline
print 'mod: %s' % mod

for i in range(30, -1, -1):
    #print normpdf(i, 20, 10)
    print '%s: %s' % (i, normpdf(i, best, afwijking)*mod)



best = 0
afwijking = 3
baseline = scipy.stats.norm.pdf(best, best, afwijking)
max_punten = 3
mod = max_punten/baseline
print 'mod: %s' % mod

for i in range(10, -1, -1):
    #print normpdf(i, 20, 10)
    print '%s: %s' % (i, normpdf(i, best, afwijking)*mod)
