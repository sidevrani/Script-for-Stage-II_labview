import math
import os
#import matplotlib.pyplot as plt
import operator
import os
import sys
sys.path.append(r'C:\Users\TIDAS\OneDrive - University of Gothenburg\TietzeLab\Pyhton scripts_labview\Script for Stage II_labview')
import accum_data_function
import numpy as np
import pandas as pd

local_dir = r'C:\Users\xdevsh\Desktop\14082022_Cyl_preetch_func_0.03Mumerror_buffer_9concn_wrong prep memb_trail'

Exp_data= accum_data_function.accu_data(local_dir)

def backbone_curve(Exp_data):
    Exp_data_1 = Exp_data.iloc[:, -7:]
    #file_name = inputFile.split('\\')[-1]
    
    backbone = pd.DataFrame(columns = {'filename','Voltage(V)','current(nA)','Norm_current'})
    # Filter through the files
    filenames = Exp_data_1['filename'].unique()
    # date = file_name.split('_')[0]
    # user = file_name.split('_')[1]
    # pore_density = file_name.split('_')[2]
    # treat = file_name.split('_')[3]
    # peptide = file_name.split('_')[4]
    # memb = file_name.split('_')[5]
    # conc = file_name.split('_')[6]
    # fluid = file_name.split('_')[7]
    # run = file_name.split('_')[8]
    for filename in filenames:
        Mod_Exp_data = Exp_data_1[(Exp_data_1['filename']== filename)]
        #Mod_Exp_data['voltage(V)'] = Mod_Exp_data['voltage(V)'].astype(float)
        #voltage_values = Mod_Exp_data['voltage(V)'].astype(np.float64)
        voltage_values = Mod_Exp_data['voltage(V)'].unique()
        voltage_values = np.sort(voltage_values)
        #voltage_values = voltage_values.sort('voltage(V)')

        for voltage in voltage_values:
            _ = pd.DataFrame(Mod_Exp_data['current(nA)'][Mod_Exp_data['voltage(V)'] == voltage])
            _1 = pd.DataFrame(Mod_Exp_data['Norm_Curr'][Mod_Exp_data['voltage(V)'] == voltage])
            #_ = _.astype(np.float64)
            
            #backbone['Voltage(V)'].loc[len(backbone)] = voltage
            backbone=backbone.append({'filename': filename ,'Norm_current':_1['Norm_Curr'].mean(),'Voltage(V)':voltage ,'current(nA)':_['current(nA)'].mean()},ignore_index=True)
            backbone['current(nA)_shift'] = backbone['current(nA)'].shift(1)


            #backbone.sort_values(by =['Voltage(V)'], axis = 0,ascending=True, inplace = True)
            #backbone['current(nA)'].loc[len(backbone)] = _.mean()
            
        Threshold_voltage = backbone.apply(lambda x: True if x['current(nA)_shift'] > 0 and x['current(nA)'] < 0 else False, axis =1)
    

    return backbone

a = backbone_curve(Exp_data)