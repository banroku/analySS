# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 12:47:46 2018
@author: Fuji Sakai
Protocol of extract flexural data (average/deviation) from data files of 
RDC automatic flexural tester (2014-2018). 

output: 
    grades = list of grade names (total 865 grades)
    flexural_data = list of flexural data. dim = 865 x 14
        see col_label of 14 items in flexural_data
"""
import os
import shutil
import csv
import pickle


folder = '.\\test\\flexural\\'
folder_to = '.\\test\\flexural_RL\\'
col_label = [grade, width, thickness, FM, FS_max, FS_break, FE_max, FE_break, 
             d_width, d_thickness, d_FM, d_FS_max, 
             d_FS_break, d_FE_max, d_FE_break, ]


'''list up all files named "xxx.rlt". '''
print('■検索中のフォルダ: ', folder)
rltfiles = []
for root, directories, filenames in os.walk(folder):
    for filename in filenames:
        if 'rlt.csv' in filename:
            rltfiles.append(os.path.join(root, filename))


'''pick files begin from "RL" ''' 
RLfiles = []
for filename in rltfiles: 
    if 'RL' in filename: 
        RLfiles.append(filename)

'''HERE! To do: copy files in RLfiles to folder folder_to'''
for file in RLfiles:
    copy_to = os.path.join(folder_to, os.path.basename(file))
    shutil.copyfile(file, copy_to)
    

'''list grade names '''
files = os.listdir(folder_to)
grades = []
for file in files:
    grades.append(file[:6])

'''list data'''
flexural_data = []
for file in files:
    data_all = []
    with open(os.path.join(folder_to, file)) as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',', )
        for row in csvReader:
            data_all.append(row)
    data = [data_all[len(data_all)-2][3:10], data_all[len(data_all)-1][3:10]]
    data_flattened = [item for sublist in data for item in sublist] #see below
    ''' this oneliner means:
    data_flattend = []
    for sublist in data:
        for item in sublist:
            data_flattened.append(item) '''
    flexural_data.append(data_flattened)

''' save grades and flexural_data in pickle files '''
with open('./grades.pickle', mode ='wb') as f:
    pickle.dump(grades, f)

with open('./flexural_data.pickle', mode='wb') as f:
    pickle.dump(flexural_data, f)



'''
combine formula_table and flexural_data




'''

''' load pickled data '''
# with open('./grades.pickle', mode ='rb') as f:
#     grades = pickle.load(f)
# with open('./flexural_data.pickle', mode='rb') as f:
#     flexural_data = pickle.load(f)

''' open formula.xlsx '''
wb = openpyxl.load_workbook('./test/formula.xlsx')
ws = wb['formula_table']

''' creat grade list in formula.xlsx '''
gradelist = []
for i in range(1, 3100):
    gradelist.append(ws.cell(i, 1).value)

''' fill flexural data in formula_table '''
ok = 0
ng = 0
for grade in grades:
    print(grade)
    try:
        idx = gradelist.index(grade)
        print(idx)
        for i in range(0, 14):
            ws.cell(idx+1, 125+i).value = \
                flexural_data[grades.index(grade)][i]
        ok = ok + 1
    except:
        print('error')
        ng = ng + 1
print('ok', ok)
print('ng', ng)

wb.save('./test/formura_comp.xlsx')




    

        




    
    
    



