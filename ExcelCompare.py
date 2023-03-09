import pandas as pd
from pathlib import Path

def printdiff(diff):
    f=open('diff.txt','a',encoding='utf-8')
    print('result :',file=f)
    print(diff.keys().tolist(),file=f)
    print(diff.values,file=f)
    f.close

def get_row_status(record):
    explain = {'left_only': 'Row_added', 'right_only': 'Row_deleted', 'both': '-'}
    status = explain[record['_merge']]
    if status == '-':
        if len(record['Changes']) > 0:
            status = 'Row updated'
    return status   

def get_row_changes(record,com_cols,old_clos):
    changes_dict = {}
    for col in com_cols:
        if col in old_clos:
            old_val = record[col + '_old']           
            if pd.isna(old_val):
                old_val = None
            if record[col] != old_val:
                new_val = record[col]
                if pd.isna(new_val):
                    new_val = None
                if (old_val is not None) or (new_val is not None):
                    changes_dict[col] ='from ('+str(old_val)+') --> ('+str(new_val)+')'
    return changes_dict
    
def compare_sheet(new,old,key_column=None):
    if key_column is None:
        key_column = df_new.keys()[0]
    new_cols = list(new.columns)
    old_cols = list(old.columns)
    add_cols = [col for col in new_cols if col not in old_cols]
    del_cols = [col for col in old_cols if col not in new_cols]
    com_cols = [col for col in new_cols if col != key_column]        
    df_differences = pd.merge(new, old, on=key_column, suffixes=('', '_old'), how='outer', indicator=True)
    df_differences['Changes'] = df_differences.apply(get_row_changes,axis=1,args=(com_cols,old_cols))
    df_differences['Status'] = df_differences.apply(get_row_status, axis=1)
    cols_to_return=[key_column,'Status', 'Changes']
    
    return add_cols,del_cols,df_differences[cols_to_return]

def compare_exceL(df_old,df_new):
    diff_datas = {}
    add_sheet = []
    del_sheet = []
    old_sts=list(df_old.keys())
    new_sts=list(df_new.keys())
    for st in new_sts:
        if st in old_sts:
            old_sts.remove(st)
            st_old=df_old[st]
            st_new=df_new[st]
            add_cols,del_cols,diff_datas[st]=compare_sheet(st_old,st_new,st)
        else:
            add_sheet.append(st)
    for st in old_sts:
        del_sheet.append(st)
    return add_sheet,del_sheet,diff_datas

if __name__ == '__main__':
    file_path = Path('files')
    filename_new = file_path / 'new.xlsx'
    filename_old = file_path / 'old.xlsx'
    df_new = pd.read_excel(filename_new,sheet_name=None)
    df_old = pd.read_excel(filename_old,sheet_name=None)
    compare_exceL(df_new,df_old)
    add_sheet,del_sheet,diff=compare_sheet(df_new,df_old,df_new.keys()[0])
    printdiff(diff)



