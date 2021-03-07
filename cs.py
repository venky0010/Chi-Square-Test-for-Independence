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
    
    total = sum(tp_row)+sum(fn_row)
    p = sum(tp_row)/total
    q = sum(fn_row)/total
    fval = chi_test(tp_row, fn_row, total, p, q, len(columns))
    return fval

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
    fval = sum(fval_fn_row)+sum(fval_tp_row)
    return fval

import math
data = pd.read_csv('GRIT06.csv')
cols = ['CCY']
di = {}
for string in cols:
    for column in data.columns:
        if re.search(string, column):
            if string not in di:
                di[string]=[column]
            else:
                di[string].append(column)
                
                
a=data['SOURCE_APPLICATION_ID=PEC/QTZ_MI'].tolist()
a = [1-i for i in a]
b=data['SECONDBIT=1_APP_ORGIN_RCG'].tolist()
b=[1-i for i in b]    
print(sensitivity(a, b, di['CCY'][:-1]))
