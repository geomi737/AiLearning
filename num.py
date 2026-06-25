import numpy as np


data = np.random.randn(50)
data = np.append(data, [100, 200, 50 ** 2])
clean_data = (data - data.mean()) / data.std()
print(clean_data.mean())
print(clean_data.std())
print(data)
print(clean_data)
