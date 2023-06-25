import numpy as np
import random as rnd

print('Testing nanmean')
print(np.nanmean([np.nan,np.nan]))
print(np.nanmean([np.nan,1]))
print(np.nanmean([]))
# print(np.nanmean([None]))

print('Testing nanstd')
print(np.nanstd([np.nan,np.nan,np.nan]))
print(np.nanstd([np.nan,1,3]))
print(np.nanstd([]))

print('Testing nansum')
print(np.nansum([np.nan,np.nan]))
print(np.nansum([np.nan,1]))
print(np.nansum([]))

print('Testing rnd.choices')
print(rnd.choices([1,2,3,4,5,6,7,8,9,10],[np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan],k=1)[0])
print(rnd.choices([1,2,3,4,5,6,7,8,9,10],[np.nan,1,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan],k=1)[0])
print(rnd.choices([1,2,3,4,5,6,7,8,9,10],[0,1,0,0,0,0,0,0,0,0],k=1)[0])
print(rnd.choices([1,2,3,4,5,6,7,8,9,10],[0,0,0,0,0,0,0,0,0,0],k=1)[0])
# print(rnd.choices([],[]))


print('Testing np.nan')
print(np.nan)


print('Testing any')
print(any(np.isnan([np.nan,np.nan])))
print(any([np.nan,1]))
print(any([]))
print(any([None]))
print(any([0,0]))