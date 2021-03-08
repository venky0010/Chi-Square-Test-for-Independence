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
        return [0, 0], 0
        
    for i in range(len(tp_row)):
        if tp_row[i]==0 and fn_row[i]==0:
            return [0, 0], 0
        
    total = sum(tp_row)+sum(fn_row)
    p = sum(tp_row)/total
    q = sum(fn_row)/total
    #fval = chi_test(tp_row, fn_row, total, p, q, len(columns))
    row1, row2 = chi_test(tp_row, fn_row, total, p, q, len(tp_row))
    return scipy.stats.chi2_contingency([tp_row, fn_row]), [row1, row2]

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
        
    return fval_tp_row, fval_fn_row


import math
data = pd.read_csv('GRIT08bin.csv')
raw = pd.read_csv('GRIT08raw.csv')
orig_columns = {}
for string in raw.columns[1:]:
    for column in data.columns:
        if re.search(string, column):
            if string not in orig_columns:
                orig_columns[string]=[column]
            else:
                orig_columns[string].append(column)
                
 ant = data['SOURCE_APPLICATION_ID=PEC/QTZ_MI'].tolist()
ant = [1-i for i in ant]
cons = data['SECONDBIT=1_APP_ORGIN_RCG'].tolist()
cons = [1-i for i in cons] 

df = []
exp = []
for column in orig_columns:
    
    f, chi_vals = sensitivity(ant, cons, orig_columns[column])
    
    df.append((column, f[0], f[1]))
    
    exp.append((orig_columns[column], chi_vals))
    
    
df = sorted(df, reverse=True, key=lambda x:x[1])
df = pd.DataFrame(df, columns = ['Ccolumn', 'Chi Stat', 'P value'])

for item in exp[2:]:
    
    plt.pie(list(map(add, item[1][0],item[1][1])), radius=3, labels=item[0], autopct='%1.2f%%')
    pplt.title
    break
