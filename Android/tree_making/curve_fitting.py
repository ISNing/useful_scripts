# 用于拟合生成详细的背光曲线数据
# 使用fitted_function(x, step_size, start, stop)在指定步长，起始值和终止值之间生成函数值
from scipy.optimize import curve_fit

# Define the function to be fitted
def func(x, a, b, c):
    return a*np.exp(-b*x) + c

# Generate some data points
x_data = [0, 1, 2, 3, 4, 5]
y_data = [1, 2, 3, 2, 3, 4]

# Estimate the parameters using least squares
params, cov = curve_fit(func, x_data, y_data)

# Generate the fitted function
def fitted_function(x, step_size=0.1, start=0, stop=10):
    x_values = np.arange(start, stop + step_size, step_size)
    return func(x_values, *params)
