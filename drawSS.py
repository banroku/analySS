# coding=utf-8
def thinningSS(file, max_strain=10, interval=0.1):
    '''a function to conduct data thinning of SS curve at range (0, MAX_STRAIN), with INTERVAL
    This returns np.series of stress with strain in the index. 
    FILE should be passed as dictionary containing following: 
        'name': name of sample like 'RL7785'
        'crv': path(relative) of xxx_crv.csv file
        'rlt': path(relative) of xxx_rlt.csv file
        'set': path(relative) of xxx_set.csv file
    '''
    import pandas as pd
    import numpy as np
    
    # read files and parameters
    data = pd.read_csv(file['crv'], sep=',', encoding='shift_jis', skiprows=1, index_col=0)
    data_rlt = pd.read_csv(file['rlt'], sep=',', encoding='shift_jis')
    L = 64  # span
    b = float(data_rlt.iloc[2, 3]) # width of first specimen
    h = float(data_rlt.iloc[2, 4]) # height of first specimen
    #print('span, width, height of first specimen:', L, ',', b, ',', h)#cut out curve of first specimen
    col = ['mm', 'N']
    data = data.reindex(columns=col)
    data.dropna(subset=['mm'], inplace=True)
    
    #%% convert (mm, N) to (%, MPa)
    # sigma = 3*F*L / (2*b*h^2)
    # epsilon = 6*100*s*h / (L^2)
    # F: load, L:span = 64 mm, b:width, h:height, s=strain/mm
    data['strain'] = data['mm'] * 6 * 100 * h / L / L
    data['stress'] = data['N'] * 3 * L / (2 * b * h * h)
    
    #%% data thinnings
    interval_steps = int(max_strain/interval)
    marker = pd.DataFrame({'strain': np.round(np.linspace(0, max_strain, interval_steps, endpoint=False), 2), 'marker': True})
    data_marked = pd.merge(data, marker, on='strain', how='outer')
    data_marked.rename(data_marked['strain'], inplace=True)
    data_marked.sort_values(by=['strain'], inplace=True)
    data_marked.interpolate(method='slinear', limit=1, inplace=True)
    data_marked['marker'].fillna('False', inplace=True)
    data_skipped = data_marked[data_marked['marker']==True]
    thinnedSS = data_skipped['stress']
    thinnedSS.name = file['name']
    
    return thinnedSS


#%%
def parameters(file):
    '''a function to pick following parameters as pd.Series: 
    parameters = ['width', 'height', 'FM', 'FS_max', 'FS_break', 'FE_max', 'FE_break', 
              'd_width', 'd_height', 'd_FM', 'd_FS_max', 'd_FS_break', 'd_FE_max', 'd_FE_break']
    FILE should be passed as dictionary containing following: 
        'name': name of sample like 'RL7785'
        'crv': path(relative) of xxx_crv.csv file
        'rlt': path(relative) of xxx_rlt.csv file
        'set': path(relative) of xxx_set.csv file '''

    file_rlt = file['rlt']
    data_rlt = pd.read_csv(file_rlt, sep=',', skiprows=[1,2], index_col=0, encoding='shift_jis')
    parameters = ['幅', '厚さ', '弾性率', '最大点', '破壊点', '最大点.1', '破壊点.1']
    data_rlt = data_rlt.loc[['単純平均', '標準偏差'], parameters]
    data_rlt.index = ['average', 'stdev']
    data_rlt.columns = ['width', 'height', 'FM', 'FS_max', 'FS_break', 'FE_max', 'FE_break']
    data_rlt = data_rlt.values
    data_flattened = [item for sublist in data_rlt for item in sublist] #see below
    parameters = ['width', 'height', 'FM', 'FS_max', 'FS_break', 'FE_max', 'FE_break', 
                  'd_width', 'd_height', 'd_FM', 'd_FS_max', 'd_FS_break', 'd_FE_max', 'd_FE_break']
    data_rlt = pd.Series(data_flattened, index=parameters) 
    data_rlt.name = file['name']
    
    return data_rlt