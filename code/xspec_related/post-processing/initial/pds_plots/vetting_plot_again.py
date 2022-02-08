from matplotlib.pyplot import plt

plt.style.use("/mnt/c/Users/Research/Documents/GitHub/sunnyhills/other/aesthetics/science.mplstyle")
fig, ax = plt.subplots(figsize=(5,3))
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']


def loren(E, EL, σ, K):
        return K*(σ/(2*3.1415659265))/((E-EL)**2+(σ/2)**2)

x1 = 2.56228
x_loren_1 = np.linspace(x1-1,x1+1,30)

y_loren_1 = loren(x_loren_1,x1,0.230605,0.00205078)

ax.plot(x_loren_1,y_loren_1,color=colors[2],lw=1)

x2 = 5.0827
x_loren_2 = np.linspace(x2-1,x2+1,30)
y_loren_2 = loren(x_loren_2,x2,0.559012,0.00108073)

ax.plot(x_loren_2,y_loren_2,color=colors[3],lw=1)