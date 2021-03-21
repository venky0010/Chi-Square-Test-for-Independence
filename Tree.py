def calculate_p_value(ante, cons, column):
    
    tp_row, fn_row = [0]*len(column), [0]*len(column)
    tp, fn = 0, 0
    k=0
    
    for col in column:
        ante2 = data[col].tolist()
        antecedent = [ante[i]*ante2[i] for i in range(len(ante2))]
        for i in range(len(antecedent)):
            if antecedent[i] == 1 and consequent[i] == 1:
                tp+=1
            elif antecedent[i] == 1 and consequent[i] == 0:
                fn+=1
                
        tp_row[k] = tp
        fn_row[k] = fn
        k+=1
        
    f = scipy.stats.chi2_contingency([tp_row, fn_row])
    return f
    

def chisq(antecedent, consequent, df):
    
    
    df = []
    for column in total_columns:
        
        chi_val = calculate_p_value(antecedent, consequent, column)
        df.append((column, f[0], f[1]))                             #f[0] is chistat and f[1] is p value
        
    df = sorted(df, key = lambda x: x[2])
    
    #Child nodes of column with lowest p value
    
    raw_column = df[0][0]
    child_nodes = []
    for column in data.columns:
        if re.search(raw_column, column):
            child_nodes.append(column)
            
    return child_nodes
