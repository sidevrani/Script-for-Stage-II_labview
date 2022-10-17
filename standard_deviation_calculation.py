import math
import os
#import matplotlib.pyplot as plt
import operator
import os
from queue import Empty
import sys
sys.path.append(r'C:\Users\TIDAS\OneDrive - University of Gothenburg\TietzeLab\Pyhton scripts_labview\Script for Stage II_labview')
import accum_data_function
import backbone_curve
import numpy as np
import pandas as pd
import openpyxl as oxl
from openpyxl import load_workbook


# local_dir = r'C:\Users\xdevsh\OneDrive - University of Gothenburg\TietzeLab\Autodata_Exp\14102022_Cyl_preetch_unfunc_0.03MumPR10_buffer_selectivity with Ni & Cu'

# Exp_data= accum_data_function.accu_data(local_dir)

# backbone = backbone_curve.backbone_curve(Exp_data)


def SD(backbone,local_dir):
    backbone['Run'] = backbone['filename'].map(lambda x : x.split('_')[8])
    backbone['Conc(fM)'] = backbone['filename'].map(lambda x :x.split('_')[6])
    backbone['membrane'] = backbone['filename'].map(lambda x :x.split('_')[5])
    backbone['peptide'] = backbone['filename'].map(lambda x :x.split('_')[4])
    backbone['pore density'] = backbone['filename'].map(lambda x :x.split('_')[2])
    backbone['fluid']= backbone['filename'].map(lambda x :x.split('_')[7])
    backbone['date']= backbone['filename'].map(lambda x :x.split('_')[0])

    runs =  backbone['Run'].unique()
    Concs = backbone['Conc(fM)'].unique()
    voltages = backbone['Voltage(V)'].unique()
    identifier = local_dir.split('\\')[-1]
    for conc in Concs:
       
        df_conc = pd.DataFrame()
        for voltage in voltages:
            df = pd.DataFrame()
            for run in runs:
                new_entry = {}
                A = backbone[(backbone['Conc(fM)']== conc) & (backbone['Run']== run) & (backbone['Voltage(V)']== voltage)]
                
                if A.empty != True:
                    df['voltage'] = A['Voltage(V)'].values
                    new_entry = {voltage:A['current(nA)'].values}
                    #new_row.update(new_entry)
                    df['{0}_run{1}'.format(conc,run)] = A['current(nA)'].values

            df_conc = df_conc.append(df, ignore_index = True)
        B = df_conc.iloc[:, 1:]
        df_conc['Average']  = B.mean(axis=1) 
        df_conc['Standard Dev.'] = B.std(axis= 1)
        df_conc['Variance'] = B.var(axis= 1)
        df_conc['%SD_of_mean'] = df_conc['Standard Dev.']/df_conc['Average'] *100

        #Save Concentration Statistics
        #writer = pd.ExcelWriter(local_dir+ '\Acc_results4.xlsx', engine = 'xlsxwriter')
        with pd.ExcelWriter(local_dir+ '\Results_{0}.xlsx'.format(identifier), engine='openpyxl', mode='a') as writer: 
            df_conc.to_excel(writer,sheet_name= '{0}_Statistics'.format(conc), index = False) 
            #writer.save()
            #writer.close()    
    return 


#SD(backbone,local_dir)