# notes 

## miscellaneous 

* thoughts on below routine: 
    * well, it's up to the point where I can fit 
```python

# Run set up with intial lorenziatians
s1 = Spectrum('/mnt/c/Users/Research/Documents/GitHub_LFS/Steiner/thaddaeus/1050360113/jspipe/js_ni1050360113_0mpu7_silver_GTI1-bin.pds')

s1.ignore('20.0-**')

m1 = Model("loren+loren", setPars={1: 0, 4: 0})

# access component names: m1.componentNames

m1.lorentz.LineE.frozen = True
m1.lorentz_2.LineE.frozen = True

Fit.query = "yes"
Fit.perform()

m1.lorentz.Width.frozen = True
m1.lorentz.norm.frozen = True
m1.lorentz_2.Width.frozen = True
m1.lorentz_2.norm.frozen = True

frozen_vals = []

for i in range(1, 7):
    frozen_vals.append(m1(i).values[0])

labels = list(range(1, 7))

pairs = np.array([labels, frozen_vals]).T.tolist()

for i in range(len(pairs)):
    pairs[i][0] = int(pairs[i][0])

param_dict = dict(pairs)

param_dict[7] = 1.5

# remove other models first? 

m2 = Model("loren+loren+loren", setPars=param_dict)

```

* Plot stuff 
    ```python
    Plot("data")
    xVals = Plot.x()
    yVals = Plot.y()
    yVals2 = Plot.y(2)  # Gets values for data in the second plot group
    modVals = Plot.model()
    # To get a background array, Plot.background must be set prior to plot
    Plot.background = True
    Plot("data")
    bkg = Plot.backgroundVals()
    # Retrieve error arrays
    xErrs = Plot.xErr()
    yErrs = Plot.yErr()
    ```