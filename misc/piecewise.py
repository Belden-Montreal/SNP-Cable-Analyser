import matplotlib.pyplot as plt
import numpy as np


f = np.linspace(1e6,16e6, 1000)


z =  lambda f: 20 * np.log10(10 ** -((23.2 - 15*np.log(f/16e6))/20) + 2 * (10 ** (-(33.9 - 20 * np.log(f/16e6))/20)))
plt.semilogx(z(f))
print z(8e6)
plt.ylabel('some numbers')
plt.show()
