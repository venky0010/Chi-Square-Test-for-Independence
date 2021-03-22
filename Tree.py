'''This is not a working code...YOU HAVE TO ADD GRAPH VISUALIZATION PART[REFER: https://github.com/lucksd356/DecisionTrees/blob/master/dtree.py WE ARE USING SAME LOGIC )
(FOR SAVING BRANCHES WE ARE USING LIST..SO CHANGE THAT CODE ACCORDINGLY)]..VENKATESH WILL PROVIDE OTHER FUNCTIONS..)
FUNCTIONS TO BE PROVIDED
****
1.p_value()#function to find the column in raw file with lowest p value.Fuction should return a tuple with child_name and p_value
2.binary_cols_of_given_raw_col(col_with_low_p_value[0])#binary column names corresponding to the column in raw file with lowest p value
'''
import csv
from collections import defaultdict
import pydotplus


class DecisionTree:
    """Binary tree implementation with true and false branch. """
    def __init__(self, col=None, branches=[]):
        self.col = col
        self.branches=branches

def growDecisionTreeFrom(dataset,cnsqnt,ante):
    #dataset dataframe does not contain antecedent columns
    if len(dataset) == 0: return DecisionTree()
    child=p_value(ante, cnsqnt, dataset)#function to find the column in raw file with lowest p value.Fuction should return a tuple with child_name and p_value
    
   
    for x in child:
        
        branches=[]
        data_copy_=dataset.copy()
        
        data_copy=data_copy_.loc[data_copy_[x] == 1]
        
        data_copy=data_copy.loc[:, (data_copy != 0).any(axis=0)]#deleting columns with all values in the column=0
        antecedent=ante.copy() 
        antecedent.append(x)
        
        
        branches.append(growDecisionTreeFrom(data_copy_,cnsqnt,antecedent))
        i=i+1
        return DecisionTree(col=child, branches=branch)


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
    
def calculate_p_value(ante, cons, column, df): #ante and cons are column names and not list
    
    tp_row, fn_row = [0]*len(column), [0]*len(column)
    consequent = df[cons].tolist()
    n = len(consequent)
    ante1 = [1]*n
    
    for i in ante:
        a = df[i].tolist()
        ante1 = [a[j]*ante1[j] for j in range(n)]
    
    k = 0
    
    for col in column:
        tp, fn = 0, 0
        ante2 = df[col].tolist()
        antecedent = [ante1[i]*ante2[i] for i in range(len(ante2))]
        for i in range(len(antecedent)):
            if antecedent[i] == 1 and consequent[i] == 1:
                tp+=1
            elif antecedent[i] == 1 and consequent[i] == 0:
                fn+=1
                
        tp_row[k] = tp
        fn_row[k] = fn
        k+=1
    
    if len(tp_row) == 1:
        return [0, 0, 0]
    if sum(tp_row) == 0 or sum(fn_row) == 0:
        return 0, 0, 0
        
    chi_val = scipy.stats.chi2_contingency([tp_row, fn_row])
    return chi_val
    

def p_value(antecedent, consequent, df):
    
    list_of_columns = []
    
    total_columns = find_columns(df)
    
    for column in total_columns:
        
        chi_val = calculate_p_value(antecedent, consequent, total_columns[column], df)
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
if __name__ == '__main__':
    bHeader = True
    data= pd.read_csv('GRIT10Bin.csv')
    data['not_PEC/QTZ_SOURCE_APPLICATION_ID_MI'] = [1-i for i in data['PEC/QTZ_SOURCE_APPLICATION_ID_MI']]
    data=data.loc[data['not_PEC/QTZ_SOURCE_APPLICATION_ID_MI'] == 1]
    data['not_SECONDBIT=1_APP_ORGIN_RCG'] = [1-i for i in data['SECONDBIT=1_APP_ORGIN_RCG']]
    data=data.loc[:, (data != 0).any(axis=0)]#deleting columns with all values in the column=0
    decisionTree = growDecisionTreeFrom(data,cnsqnt,ante)
    result = plot(decisionTree)
    '''dot_data = dotgraph(decisionTree)
    graph = pydotplus.graph_from_dot_data(dot_data)
    graph.write_png("iris.png")'''
