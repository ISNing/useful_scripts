# 用于拟合生成详细的背光曲线数据

# Data points
from xml.etree import ElementTree as ET
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
x_data = [0, 1, 2, 3, 4, 5]
y_data = [1, 2, 3, 4, 4, 3]
x_xml = None
y_xml = None

# Target Generating Mode:0: by step, 1:by array, 2:by XML
mode = 0
arr = []
target_xml = None
print_xml = False

start = 0
step_size = 5
stop = 255

# Function type: number: polyfit_nth, None:custom func
func_type = None


def custom_func(x, a, b, c, d):
    return   a*x + b*x**2 + c*x**2.000000033 + d


if x_xml:
    x_data = []
    root = ET.fromstring(x_xml)
    for child in root:
        x_data.append(int(child.text))

if y_xml:
    y_data = []
    root = ET.fromstring(y_xml)
    for child in root:
        y_data.append(int(child.text))

if mode == 2:
    arr = []
    root = ET.fromstring(target_xml)
    for child in root:
        arr.append(int(child.text))


def polyfit_nth(x_data, y_data, n):
    # Fit a nth degree polynomial to the data
    coefs = np.polyfit(x_data, y_data, n)
    # Generate the fitted function

    def fitted_function(x):
        y = 0
        for i in range(n+1):
            y += coefs[i]*x**(n-i)
        return y
    return fitted_function


def custom_fit(x_data, y_data, func):
    params, cov = curve_fit(func, x_data, y_data)
    # Generate the fitted function

    def  fitted_function(x):
        return custom_func(x,  *params)
    return fitted_function


def convert_to_int(arr):
    return np.around(arr, decimals=0).astype(int)


plt.scatter(x_data, y_data, label='data points', color='black')
print(f'X Dataset: {x_data}')
print(f'Y Dataset: {y_data}')

print("\ncalculating...")

# plot the polynomial fitting curve for different order
for j in range(0, func_type if func_type else 1):
    i = j + 1
    fitted_func = polyfit_nth(x_data, y_data, i) if func_type else custom_fit(
        x_data, y_data, custom_func)
    x_values = np.linspace(min(x_data), max(x_data), 100)
    y_values = fitted_func(x_values)
    label = f'{i}th degree polynomial' if func_type else 'Custom function'
    plt.plot(x_values, y_values, label=label)
    if mode == 0:
        x_values = np.arange(start, stop + step_size, step_size)
    elif mode == 1 or mode == 2:
        x_values = np.array(arr)
    else:
        raise RuntimeError('target x must be given!!!')
    y_values = fitted_func(x_values)
    y_values_rounded = convert_to_int(y_values)
    print(f'\n\nnth: {i}')
    print(f'Original: {y_values}')
    print(f'Rounded: {y_values_rounded}')
    print('')
    if print_xml:
        for y in y_values_rounded:
            print(f'<item>{y}</item>')


plt.legend()
plt.show()