import math
import numpy as np
tens = [10.0, 20.0, 30.0, 40.0, 50.0]
units = [1.0, 2.0, 3.0, 4.0, 5.0]

zipped = list(zip(units, tens))
##zipped = [ ( x*x, y*y) for x, y in zipped]
zipped = [ [math.sqrt(x*x + y*y)] for x, y in zipped]
list_list = list(map(list, zipped))
i = np.array(list_list)
print(i.flatten())
##x_axis = i[:, 0]
##y_axis = i[:, 1]
##print(f'x_axis = {x_axis}, y-axis={y_axis}')