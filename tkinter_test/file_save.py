import time
import os
import numpy as np

database = np.array(
        [["Result", "C_Mass", "H_Num", "H_Mass", "B_Num", "B_Mass", "A_Num", "A_Mass", "N_Rate", "M_Rate"]])
new_database = np.array([8, 5, 2])
t = time.localtime()
filename = 'data/savedata_%s_%s.txt' %(str(t.tm_year)+str(t.tm_mon).zfill(2)+str(t.tm_mday).zfill(2), str(t.tm_hour).zfill(2)+str(t.tm_min).zfill(2)+str(t.tm_sec).zfill(2))
print(filename)
if 'data' not in os.listdir():
    os.mkdir('data')
np.savetxt(filename, database, delimiter='\t', fmt='%s',)

