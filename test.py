import re
import math
import scipy.stats
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

%matplotlib inline

import scipy.stats
def sensitivity(ant1, consequent, columns):
    
    tp_row = [0]*len(columns)
    fn_row = [0]*len(columns)
    k=0
    for column in columns:
        tp=0
        fn=0
        ant2 = data[column].tolist()
        antecedent = [ant1[i]*ant2[i] for i in range(len(ant1))] 
        for i in range(len(antecedent)):
            if   antecedent[i]==1 and consequent[i]==1:         #Ante present, Cons present
                tp+=1
            elif antecedent[i]==1 and consequent[i]==0:         #Ante present, Cons not present
                fn+=1
        tp_row[k]=tp
        fn_row[k]=fn
        k+=1
    
    if sum(tp_row) == 0 or sum(fn_row) == 0:
        return [0, 0], 0, 0, 0
        
    for i in range(len(tp_row)):
        if tp_row[i]==0 and fn_row[i]==0:
            return [0, 0], 0, 0, 0
        
    total = sum(tp_row)+sum(fn_row)
    p = sum(tp_row)/total
    q = sum(fn_row)/total
    #fval = chi_test(tp_row, fn_row, total, p, q, len(columns))
    row1, row2, ex_row1, ex_row2 = chi_test(tp_row, fn_row, total, p, q, len(tp_row))
    return scipy.stats.chi2_contingency([tp_row, fn_row]), [row1, row2], [ex_row1, ex_row2], [tp_row, fn_row]

def chi_test(row1, row2, total, p, q, n):
    
    ex_tp_row = [0]*n
    ex_fn_row = [0]*n
    
    fval_tp_row = [0]*n
    fval_fn_row = [0]*n
    
    for i in range(n):
        
        a = row1[i]
        b = row2[i]
        
        ex_tp_row[i] = p*(a+b)
        ex_fn_row[i] = q*(a+b)
        
        fval_tp_row[i] = pow(a-ex_tp_row[i], 2)/ex_tp_row[i]
        fval_fn_row[i] = pow(b-ex_fn_row[i], 2)/ex_fn_row[i]
        
    return fval_tp_row, fval_fn_row, ex_tp_row, ex_fn_row
  
  import math
data = pd.read_csv('GRIT10Bin.csv')
raw = pd.read_csv('GRIT10Raw.csv')
orig_columns = {}
for string in raw.columns[1:]:
    for column in data.columns:
        if re.search(string, column):
            if string not in orig_columns:
                orig_columns[string]=[column]
            else:
                orig_columns[string].append(column)
                
                
ant = data['PEC/QTZ_SOURCE_APPLICATION_ID_MI'].tolist()
ant = [1-i for i in ant]
cons = data['SECONDBIT=1_APP_ORGIN_RCG'].tolist()
cons = [1-i for i in cons]

f, frows, exrows, rows = sensitivity(ant, cons, orig_columns['PRCACCOUNTENGLISHNAME_IAS_PRC'])

x = ['#000000','#190000','#330000','#330000','#4c0000','#660000','#7f0000','#990000','#b20000','#b20000','#cc0000','#e50000','#e50000','#ff0000','#ff1919','#ff3232', '#ff3232','#ff4c4c', '#ff4c4c','#ffb2b2','#ffb2b2','#ffcccc','#ffe5e5','#ffe5e5','#ffffff']
x = x[::-1]
y = ['#000000','#02180a', '#02180a','#043014', '#043014','#06491f', '#06491f','#086129','#0b7a34','#0d923e','#0faa48','#11c353','#13db5d','#16f468','#16f468','#2df577','#44f686','#5bf795','#73f8a4','#8af9b3','#a1fac2','#b9fbd1','#d0fce0','#e7fdef']


Good = []
Bad = []
for i in range(len(orig_columns['PRCACCOUNTENGLISHNAME_IAS_PRC'])):
    if rows[0][i]>exrows[0][i]:
        Good.append((orig_columns['PRCACCOUNTENGLISHNAME_IAS_PRC'][i], frows[0][i]+frows[1][i]))
    elif rows[0][i]<=exrows[0][i]:
        Bad.append((orig_columns['PRCACCOUNTENGLISHNAME_IAS_PRC'][i], frows[0][i]+frows[1][i]))
        
Good = sorted(Good, reverse = True, key = lambda x : x[1])
Bad = sorted(Bad, key = lambda x:x[1])
Total = Good+Bad

plt.pie([i[1] for i in Good], radius=3, labels=[i[0] for i in Good], colors=y, autopct='%1.2f%%')
plt.legend(loc="lower center", bbox_to_anchor=(4,2))


plt.pie([i[1] for i in Total], radius=3, labels=[i[0] for i in Total], colors = y+x, autopct='%1.2f%%')
plt.legend(loc="lower center", bbox_to_anchor=(3,2))

