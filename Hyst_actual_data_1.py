import math
import os
import sys
import  re
from tokenize import Double
from typing import Any
import xlsxwriter
sys.path.append(r'C:\Users\xdevsh\OneDrive - University of Gothenburg\TietzeLab\Autodata_Exp\Pyhton scripts_labview\Script for Stage II_labview')

import matplotlib
from openpyxl import load_workbook
import statistics
import hysteresis as hys
import operator
import numpy as np
import pandas as pd
import openpyxl as oxl
from openpyxl import load_workbook
from sklearn.preprocessing import MinMaxScaler
Scale = MinMaxScaler(feature_range=(-1,1))
import accum_data_function

#local_dir = r'C:\Users\xdevsh\OneDrive - University of Gothenburg\TietzeLab\Autodata_Exp\For_Data_analysis\01082022_Cyl_preetch_func_0.01Mumerror_buffer_9concn_wrong prep memb'

#Exp_data= accum_data_function.accu_data(local_dir)


def hist_calc_1(Exp_data):
    Exp_data_1 = Exp_data.iloc[:, -7:]
    #Exp_data
    files = []
    Rem_pos = []
    Rem_neg = []
    Hyst_area = []
    Hyst_area_norm = []
    cum_Area = []
    slope_grad = []
    Area = []
    date = []
    user = []
    pore_density = []
    treat = []
    peptide = []
    memb = []
    conc = []
    fluid = []
    run = []
    pos_cond = []
    neg_cond = []
    Rect_factor = []
    florescense = []


    # Filter through the files
    filenames = Exp_data_1['filename'].unique()
    for filename in filenames:
        Mod_Exp_data = Exp_data_1[(Exp_data_1['filename']== filename)]
        Mod_Exp_data['Floursence'] = Mod_Exp_data['Floursence'].astype(np.float64)

    # Exp_data
 
        # Variables for identifiycing key voltage piints for averaging later. 
        max_voltage = Mod_Exp_data['Norm_Volt'].max()
        min_voltage = Mod_Exp_data['Norm_Volt'].min()
        avg_voltage = round(Mod_Exp_data['Norm_Volt'].mean(),1)
        voltage_values = Mod_Exp_data['voltage(V)'].unique()
        voltage_values.sort()

        for voltage in voltage_values:
            Mod_Exp_data_1 = Mod_Exp_data[(Mod_Exp_data['voltage(V)']== voltage)]
            values_to_plot = Mod_Exp_data[['voltage(V)','current(nA)','Norm_Volt','Norm_Curr']].mean()
            values_to_plot = values_to_plot.T
    
    return voltage_values


#hist_calc_1(Exp_data)