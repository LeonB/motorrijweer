from pylab import *
from scipy import *

# if you experience problem "optimize not found", try to uncomment the following line. The problem is present at least at Ubuntu Lucid python scipy package
from scipy import optimize

# Generate data points with noise
num_points = 150
Tx = linspace(5., 8., num_points)
Ty = Tx

tX = 11.86*cos(2*pi/0.81*Tx-1.32) + 0.64*Tx+4*((0.5-rand(num_points))*exp(2*rand(num_points)**2))

# Fit the first set
fitfunc = lambda p, x: p[0]*cos(2*pi/p[1]*x+p[2]) + p[3]*x # Target function
#fitfunc = lambda p, x: p[0] + p[1] * x
errfunc = lambda p, x, y: fitfunc(p, x) - y # Distance to the target function
p0 = [-15., 0.8, 0., -1.] # Initial guess for the parameters
p1, success = optimize.leastsq(errfunc, p0[:], args=(Tx, tX))

time = linspace(Tx.min(), Tx.max(), 100)
plot(Tx, tX, "ro", time, fitfunc(p1, time), "r-") # Plot of the data and the fit

# Legend the plot
title("Oscillations in the compressed trap")
xlabel("time [ms]")
ylabel("displacement [um]")
legend(('x position', 'x fit', 'y position', 'y fit'))

ax = axes()

show()
