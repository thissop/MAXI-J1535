def first(): 

    import multiprocessing
    import time
    import math

    N = 5000000

    def cube(x):
        return math.sqrt(x), x

    with multiprocessing.Pool() as pool:
        ans, xs = pool.map(cube, range(10,12))
    print("Program finished!")
    print(ans,xs)

def second(): 
    import myglobals 

    myglobals.data = "asdfas"

    print(myglobals.data)

second()