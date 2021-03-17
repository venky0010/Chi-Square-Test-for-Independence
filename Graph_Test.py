import re
import math
import scipy.stats
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from colour import Color

%matplotlib inline

def sensitivity(ant, consequent, columns):
    

    tp_row = [0]*len(columns)
    fn_row = [0]*len(columns)
    k=0
    for column in columns:
        tp=0
        fn=0
        ant1 = ant
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
    
    

data = pd.read_csv('GRIT10Bin.csv')
raw = pd.read_csv('GRIT10Raw.csv')
orig_columns = {}                                                         #It contains column from raw file as key and List of column names which are present in bin file as the value of that key
for string in raw.columns[1:]:
    for column in data.columns:
        if re.search(string, column):
            if string not in orig_columns:
                orig_columns[string]=[column]
            else:
                orig_columns[string].append(column)
                
                
ant = data['PEC/QTZ_SOURCE_APPLICATION_ID_MI'].tolist()
ant = [1-i for i in ant]                                                  #Complementing because our antecedent is SourceID !=PEC/QTZ
cons = data['SECONDBIT=1_APP_ORGIN_RCG'].tolist()
cons = [1-i for i in cons]                                                #Complementing because consequent is mid bit = 0


# Below code takes column name (from bin file) as the antecedent and computes the chi square test value (P value) for all the variables an saves in df                                                
df = []
for i in ['AUTORECIV_GLACCT_NBR_RCG']:                                    #Autorec is used as next antecedent because it as impure.
    
    ant = [1-j for j in data['PEC/QTZ_SOURCE_APPLICATION_ID_MI'].tolist()]
    ante2 = data[i].tolist()
    ant = [ant[i]*ante2[i] for i in range(len(ante2))]
    print(sum(ant))
    for column in orig_columns:                                           #Calculate p value for all the columns in raw file
        
        f, frows, exrows, rows = sensitivity(ant, cons, orig_columns[column])
        if f[0] == 0 and f[1] == 0:                                       #To filter out 0s from the list. (On which chi sq test was not performed)
            continue
        df.append((i, column, f[0], f[1]))
        
        
df = sorted(df, key = lambda x: x[3])
df = pd.DataFrame(df, columns = ['Ant2', 'Ant3', 'chi stat', 'P value'])  #Find the variable with least p value using this df

#This code is used to find all the variables that will appear in the split as the child nodes of the Impure node found above.

ant = [1-i for i in data['PEC/QTZ_SOURCE_APPLICATION_ID_MI'].tolist()] #This code has to be changed when we go down the tree/add more antecedents.
ant2 = data['AUTORECIV_GLACCT_NBR_RCG'].tolist()
ante = [ant[i]*ant2[i] for i in range(len(ant))]
print(sum(ante))
f, frows, exrows, rows = sensitivity(ante, cons, orig_columns['GLACCT_BAL_AMT_RCG'])

# Use below code to separate the good/bad nodes

Good = []
Bad = []
for i in range(3):
    if rows[0][i]>exrows[0][i]:
        Good.append((orig_columns['GLACCT_BAL_AMT_RCG'][i], frows[0][i]+frows[1][i])) 
    elif rows[0][i]<=exrows[0][i]:
        print(frows[0][i],frows[1][i])
        Bad.append((orig_columns['GLACCT_BAL_AMT_RCG'][i], frows[0][i]+frows[1][i]))
        
Good = sorted(Good, reverse = True, key = lambda x : x[1])
Bad = sorted(Bad, key = lambda x:x[1])
Total = Good+Bad

#Now manually visualize the nodes and draw the graph. Have to incorporate some function to automate the graph generation

''' 

Have to automate below code

#for column in orig_columns:

df = []
for i in ['Revenue_ACCOUNTMONETARYTYPE_E2K']:
    
    ant = [1-j for j in data['PEC/QTZ_SOURCE_APPLICATION_ID_MI'].tolist()]
    ante2 = data[i].tolist()
    ant3 = data['AUTORECIV_GLACCT_NBR_RCG'].tolist()
    ant4 = data['GLIS-_GLACCT_BAL_AMT_RCG'].tolist()
    ant = [ant[i]*ante2[i] for i in range(len(ante2))]
    ant = [ant[i]*ant3[i] for i in range(len(ant))]
    ant = [ant[i]*ant4[i] for i in range(len(ant))]
    print(sum(ant))
    for column in orig_columns:
        
        f, frows, exrows, rows = sensitivity(ant, cons, orig_columns[column])
        if f[0] == 0 and f[1] == 0:
            continue
        df.append((i, column, f[0], f[1]))
        
        
df = sorted(df, key = lambda x: x[3])
df = pd.DataFrame(df, columns = ['Ant2', 'Ant3', 'chi stat', 'P value'])  

'''

