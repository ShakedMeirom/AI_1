from scipy import stats
import numpy as np

size = 100
rvs = stats.norm.rvs(loc=0, scale =1, size = size)

print('pVal is:', stats.ttest_1samp(rvs, 100)[1])
