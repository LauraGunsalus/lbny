from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

chunksize = 50
i = 1
binz = range(0,27)
total = np.zeros(26)

data1 = pd.read_csv('hamming_distances_test.csv', chunksize=50, iterator=True, header = None)

for chunk in data1:
    print('Chunk Thing?')

"""

for chunk in pd.read_csv('hamming_distances_test.csv', header = None):
    print('Something at least')
    subtotal, e = np.histogram(list(chunk), bins=binz)
    total += subtotal.astype(np.uint)

    i+=1

    if i in [1,5,10,15]:
        print('Read ' + str(i*1000) + ' entries')

plt.hist(bins = binz,align='left',rwidth=0.75,weights=total)
plt.xticks(binz)
plt.show()
"""
