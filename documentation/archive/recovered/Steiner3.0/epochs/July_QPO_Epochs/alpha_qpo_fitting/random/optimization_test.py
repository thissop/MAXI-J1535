import numpy as np
import matplotlib.pyplot as plt

x = np.array(list(set(np.random.randint(0, 30, 15))))
y = (2*x)+np.random.normal(0, 1.25, len(x))+1.5

test_slopes = np.linspace(0, 4, 32)
test_intercepts = np.linspace(-50, 50, 200)

plot_xs = np.array([])
plot_ys = np.array([])

red_chis = np.array([])

for test_slope in test_slopes: 
    for test_intercept in test_intercepts: 
        plot_xs = np.append(plot_xs, test_slope)
        plot_ys = np.append(plot_ys, test_intercept)
        red_chi = 0 
        for x_val, y_val in zip(x, y):
            red_chi = red_chi + np.abs((test_slope*x_val)+test_intercept-y_val)
            
        red_chi = red_chi / (len(x)-1)
        red_chis = np.append(red_chis, red_chi)


# Make plot   
from matplotlib import cm
from matplotlib.ticker import LinearLocator

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})    

ax.plot_trisurf(plot_xs, plot_ys, red_chis, cmap=cm.coolwarm)

ax.set_xlabel('m')
ax.set_ylabel('b')
ax.set_zlabel('red. '+r'$\chi^2$')

plt.show()

