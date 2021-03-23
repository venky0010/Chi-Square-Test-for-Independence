import csv
from collections import defaultdict
import pydotplus
import scipy.stats
import pandas as pd
import re
class DecisionTree:
    """Binary tree implementation with true and false branch. """
    def __init__(self, branches=[]):
       # self.col = col
        self.branches=branches

def growDecisionTreeFrom(dataset,cnsqnt,ante,df_with_antecedent):
    #dataset dataframe does not contain antecedent columns
    if len(dataset) == 0: return DecisionTree()
    child=p_value(ante, cnsqnt, dataset,df_with_antecedent)#function to find the column in raw file with lowest p value.Fuction should return a tuple with child_name and p_value
    #print(ante)
    branch=[]
    print(ante)
    for x in child:
        data_copy_=dataset.copy()
        data_copy=data_copy_.loc[data_copy_[x] == 1]
        del data_copy[x]
        data_copy=data_copy.loc[:, (data_copy != 0).any(axis=0)]#deleting columns with all values in the column=0

        df_with_ante=df_with_antecedent.copy()
        df_with_ante=df_with_ante.loc[df_with_ante[x] == 1]
      

        antecedent=ante.copy() 
        antecedent.append(x)
  
        branch.append(growDecisionTreeFrom(data_copy,cnsqnt,antecedent,df_with_ante))
      
    return DecisionTree( branches=branch) 

def find_columns(df):
    
    raw = pd.read_csv('GRIT10Raw.csv')
    
    total_columns = {}
    for string in raw.columns[1:]:
        for column in df.columns:
            if re.search(string, column):
                if string not in total_columns:
                    total_columns[string]=[column]
                else:
                    total_columns[string].append(column)
                    
    return total_columns
    
def calculate_p_value(ante, cons, column, df,df_with_ante): #ante and cons are column names and not list
    
    tp_row, fn_row = [0]*len(column), [0]*len(column)
    consequent = df_with_ante[cons].tolist()
    n = len(consequent)
    ante1 = [1]*n

    for i in ante:
        a = df_with_ante[i].tolist()
        ante1 = [a[j]*ante1[j] for j in range(n)]
    
    k = 0
    
    for col in column:
        tp, fn = 0, 0
        ante2 = df_with_ante[col].tolist()
        antecedent = [ante1[i]*ante2[i] for i in range(len(ante2))]
        for i in range(len(antecedent)):
            if antecedent[i] == 1 and consequent[i] == 1:
                tp+=1
            elif antecedent[i] == 1 and consequent[i] == 0:
                fn+=1
                
        tp_row[k] = tp
        fn_row[k] = fn
        k+=1
    for i in range(len(tp_row)):
        if tp_row[i] == 0 and fn_row[i] == 0:
          return [0, 1, 0]

    if len(tp_row) == 1:
        return [0, 1, 0]
    if sum(tp_row) == 0 or sum(fn_row) == 0:
        return [0, 1, 0]

    chi_val = scipy.stats.chi2_contingency([tp_row, fn_row])
    return chi_val
    

def p_value(antecedent, consequent, df,df_with_ante):
    
    list_of_columns = []
    
    total_columns = find_columns(df_with_ante)

    for column in total_columns:
        
        chi_val = calculate_p_value(antecedent, consequent, total_columns[column], df,df_with_ante)
        list_of_columns.append((column, chi_val[0], chi_val[1]))                             #f[0] is chistat and f[1] is p value
        
    list_of_columns = sorted(list_of_columns, key = lambda x: x[2])
    
    #Child nodes of column with lowest p value
    
    raw_column = list_of_columns[0][0]
    child_nodes = []
    for column in df.columns:
        if re.search(raw_column, column):
            child_nodes.append(column)
            
    return child_nodes


cnsqnt='not_SECONDBIT=1_APP_ORGIN_RCG'
ante=['not_PEC/QTZ_SOURCE_APPLICATION_ID_MI']
data1= pd.read_csv('GRIT23Bin.csv')

data=data1.loc[data1['not_PEC/QTZ_SOURCE_APPLICATION_ID_MI'] == 1]

data=data.loc[:, (data != 0).any(axis=0)]#deleting columns with all values in the column=0
gg=data.copy()
del data[ 'PEC_SOURCE_APPLICATION_ID_MI']
del data['not_PEC/QTZ_SOURCE_APPLICATION_ID_MI']

decisionTree = growDecisionTreeFrom(data,cnsqnt,ante,gg)
#result = plot(decisionTree)
'''dot_data = dotgraph(decisionTree)
graph = pydotplus.graph_from_dot_data(dot_data)
graph.write_png("iris.png")'''
