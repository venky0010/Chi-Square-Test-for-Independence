import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline

col_names =  ['ACTUAL_COL','ANTECEDENT_1', 'ANTECEDENT_2', 'CONSEQUENT','TP','FN','EXPECTED_TP','EXPECTED_FN','F_VALUE_TP','F_VALUE_FN']
df= pd.DataFrame(columns = col_names)
import re
col=['CCY_CD_RCG']
binary_cols=data.columns
total=[]
i_list=[]
source_appli_not_pec_qtz=data['SOURCE_APPLICATION_ID=PEC/QTZ_MI'].tolist()
source_appli_not_pec_qtz= list(map(lambda i: 2 if i==0 else i, source_appli_not_pec_qtz))    
source_appli_not_pec_qtz= list(map(lambda i: 0 if i==1 else i, source_appli_not_pec_qtz))
source_appli_not_pec_qtz= list(map(lambda i: 1 if i==2 else i, source_appli_not_pec_qtz))
cnsqnt=data['SECONDBIT=1_APP_ORGIN_RCG'].tolist()
cnsqnt= list(map(lambda i: 2 if i==0 else i, cnsqnt))    
cnsqnt= list(map(lambda i: 0 if i==1 else i, cnsqnt))
cnsqnt= list(map(lambda i: 1 if i==2 else i, cnsqnt))
ttp=0
ffn=0
for i in range(len(source_appli_not_pec_qtz)):
    if source_appli_not_pec_qtz[i]==1 and cnsqnt[i]==1:
        ttp=ttp+1
    elif source_appli_not_pec_qtz[i]==1 and cnsqnt[i]==0:
        ffn=ffn+1
tp_ratio=(ttp/(ffn+ttp))
fn_ratio=1-tp_ratio
x=0
for i in col:
  indx=0
  w=str(i)+'$'
  tp_list=[]
  fn_list=[]
  starting_index=x
  for j in binary_cols:
    
    if re.search(w, j):

      '''i_list.append(i)
    for j in range(0,len(i_list)):'''
      df.loc[x,'ACTUAL_COL']=i
      df.loc[x,'ANTECEDENT_1']='SOURCE_APPLICATION_ID!=PEC/QTZ'
      df.loc[x,'ANTECEDENT_2']=j
      df.loc[x,'CONSEQUENT']='MIDDILE_BIT_OF_APP_ORGIN=0'
      tes=data[j].tolist()
      tes_list = [tes[p] * source_appli_not_pec_qtz[p] for p in range(len(tes))]
      tp=0
      fn=0
      for ii in range(0,len(tes_list)):
          if tes_list[ii]==1 and cnsqnt[ii]==1:
              tp=tp+1
          elif tes_list[ii]==1 and cnsqnt[ii]==0:
              fn=fn+1
      tp_list.append(tp)
      fn_list.append(fn)
      df.loc[x,'TP']=tp
      df.loc[x,'FN']=fn
      x=x+1
      indx=indx+1

  for ii in range(0,indx):
    c_sum=tp_list[ii]+fn_list[ii]
    expected_tp=c_sum*tp_ratio
    expected_fn=c_sum*fn_ratio
    if expected_fn==0 and expected_tp==0:
      df.loc[(starting_index+ii),'EXPECTED_TP']=0
      df.loc[(starting_index+ii),'EXPECTED_FN']=0
      df.loc[(starting_index+ii),'F_VALUE_TP']=0
      df.loc[(starting_index+ii),'F_VALUE_FN']=0
    else:
      f_value_tp=(pow((tp_list[ii]-expected_tp),2))/expected_tp
      f_value_fn=(pow((fn_list[ii]-expected_fn),2))/expected_fn
      df.loc[(starting_index+ii),'EXPECTED_TP']=expected_tp
      df.loc[(starting_index+ii),'EXPECTED_FN']=expected_fn 
      df.loc[(starting_index+ii),'F_VALUE_TP']=f_value_tp
      df.loc[(starting_index+ii),'F_VALUE_FN']=f_value_fn 
df.to_csv('chi2_crncy.csv')
