from acc import *
import numpy as np
import math

stl = time.time()
str = start_acc()
erx=str[1]
ery=str[3]
erz=str[5]



def errch(v1,v2):
    if v1>v2:
        return (v1-v2)**2
    else:
        return 0

def convert(s): 
  
    # initialization of string to "" 
    new = "" 
  
    # traverse in the string  
    for x in s: 
        new += x  
  
    # return string  
    return new


while True:
    s = start_acc()
    acc = math.sqrt(errch(str[1],erx)+errch(str[3],ery)+errch(str[5],erz))*9.807
    el = time.time()-int(stl)
    speed = round((acc*el),2)
    stl = time.time()

    s = s, speed
    test_list = np.array(s)[:, None]
    string = np.array_str(test_list)
    print(string) 
    #s = str(s).strip(')')