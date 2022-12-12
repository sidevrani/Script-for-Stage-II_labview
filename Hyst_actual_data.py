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

#local_dir = r'C:\Users\xdevsh\OneDrive - University of Gothenburg\TietzeLab\Autodata_Exp\21112022_Con_selfetch_func_XXMumSE15_HS_8conc_sen&sel1V20pointsSD=3'

#Exp_data= accum_data_function.accu_data(local_dir)

def hist_calc(Exp_data):
    #define list of paramaters to calculate

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
    Area_trap = []


    # Filter through the files with particualr name
    filenames = Exp_data['filename'].unique()
    for filename in filenames:
        Mod_Exp_data = Exp_data[(Exp_data['filename']== filename)]
        Mod_Exp_data['Floursence'] = Mod_Exp_data['Floursence'].astype(np.float64)
 
        # Variables for identifiycing key voltage points for averaging later. 
        max_voltage = Mod_Exp_data['Norm_Volt'].max()
        min_voltage = Mod_Exp_data['Norm_Volt'].min()
        avg_voltage = round(Mod_Exp_data['Norm_Volt'].mean(),1)
        #round(avg_voltage,1)

        # Pick out indexes of avg, min, max voltage
        a1 = Mod_Exp_data['Norm_Volt'].index[Mod_Exp_data['Norm_Volt'] == max_voltage]
        b1 = Mod_Exp_data['Norm_Volt'].index[Mod_Exp_data['Norm_Volt'] == min_voltage]
        c1 = Mod_Exp_data['Norm_Volt'].index[Mod_Exp_data['Norm_Volt'] == avg_voltage]
        
        
        
        a = []
        b = []
        c = []
        # Account for multiple consequent current readings at same voltage.
        if len(a1) > 2:
        
            for i in range(0,len(a1)):
                if a1[i] != a1[i-1] + 1:
                    a.append(a1[i])
            for i in range(0,len(b1)):
                if b1[i] != b1[i-1] + 1:
                    b.append(b1[i])
            for i in range(0,len(c1)):
                if c1[i] != c1[i-1] + 1:
                    c.append(c1[i])
            
            
            Mod_Exp_data['Norm_Curr'].iloc[c[-1]] = (Mod_Exp_data['Norm_Curr'].iloc[c[-1]] +Mod_Exp_data['Norm_Curr'].iloc[c[-0]])/2
            c = c[1:]
            a_len = len(a)
            b_len = len(b)
            c_len = len(c)
            
            A = pd.DataFrame()
            B = pd.DataFrame()
            C = pd.DataFrame()
        # a = list of max voltage indexes, b = list of min voltage indexes, Hyst direction from 1 V to -1 V.
            if a[0]> b[0]:
                t = b
                b = a
                a = t 

            for i,j  in zip(a,b):     
                #if i != a_len :
                A_ = Mod_Exp_data['current(nA)'].iloc[i:j]
                A__= Mod_Exp_data['Norm_Curr'].iloc[i:j]
                volt_range_1 = Mod_Exp_data['Norm_Volt'].iloc[i:j]
                A_ = A_.reset_index()
                A__ = A__.reset_index()

                A = pd.concat([A,A_,A__],axis=1)
                A.drop('index', axis=1, inplace=True)
                A['current(nA)'] = A['current(nA)'].astype(np.float64)
                A['Norm_Curr'] = A['Norm_Curr'].astype(np.float64)

            A['Avg_current(nA)'] = A['current(nA)'].mean(axis=1)
            A['Avg_Norm_Curr'] = A['Norm_Curr'].mean(axis=1)
            A.drop('current(nA)', axis=1, inplace=True)
            A.drop('Norm_Curr', axis=1, inplace=True)
            A['Norm_Volt'] = [i for i in volt_range_1]
            
            for i, j  in zip(b,a[1:]):
                B_ = Mod_Exp_data['current(nA)'].iloc[i:j]
                B__ = Mod_Exp_data['Norm_Curr'].iloc[i:j]
                B_ = B_.reset_index()
                B__ = B__.reset_index()
                volt_range_2 = Mod_Exp_data['Norm_Volt'].iloc[i:j]
                B = pd.concat([B,B_,B__],axis=1)
                B.drop('index', axis=1, inplace=True)
                B['current(nA)'] = B['current(nA)'].astype(np.float64)
                B['Norm_Curr'] = B['Norm_Curr'].astype(np.float64)

            B['Avg_current(nA)'] = B['current(nA)'].mean(axis=1)
            B['Avg_Norm_Curr'] = B['Norm_Curr'].mean(axis=1)
            B.drop('current(nA)', axis=1, inplace=True)
            B.drop('Norm_Curr', axis=1, inplace=True)
            B['Norm_Volt'] = [i for i in volt_range_2]
            

            # B = B.drop(columns = 'Norm_Curr', axis= 1)
            
            C = pd.concat([A,B], axis = 0)
            
            # # C = pd.concat([C[C['Norm_Volt']!=0].drop_duplicates(keep='last'), C[C['Norm_Volt']==0]], axis = 0)
            x = C['Norm_Volt'].values
            y = C['Avg_current(nA)'].values
            y1 = C['Avg_Norm_Curr'].values
            xy = np.column_stack([x,y])
            xy1 = np.column_stack([x,y1])
            # Convert the x and y values to numpy arrays
            x_values = np.array(x)
            y_values = np.array(y)
            
            # Use the numpy trapz function to find the area under the curve
            area_trap = np.trapz(y_values, x_values)

            
            #fig, ax = plt.subplots()
            myHys = hys.Hysteresis(xy)
            myHys_norm = hys.Hysteresis(xy1)
            #myHys.plot(plotCycles = True)
            area = myHys.area
            netArea = myHys.getNetArea()
            netArea_norm = myHys_norm.getNetArea()
            cumulativeArea = myHys.getCumArea()
            slope = myHys.slope
            slope_grad.append(slope)
            cum_Area.append(cumulativeArea)
            Remneg, Rempos = C['Avg_current(nA)'].loc[C['Norm_Volt']==0]
            positive_cond = C['Avg_current(nA)'].loc[C['Norm_Volt']==max_voltage].values[0]
            
            negative_cond = C['Avg_current(nA)'].loc[C['Norm_Volt']==min_voltage].values[0]
        
            Rect_fac = (positive_cond / negative_cond)
            

            flo_columns = Mod_Exp_data['Floursence'][Mod_Exp_data['Floursence']>0]
            flo = np.mean(flo_columns)
            
            Area.append(area)
            Rem_pos.append(Rempos)
            Rem_neg.append(Remneg)
            files.append(filename)
            Hyst_area.append(netArea)
            Hyst_area_norm.append(netArea_norm)
            pos_cond.append(positive_cond)
            neg_cond.append(negative_cond)
            Rect_factor.append(Rect_fac)
            date.append(filename.split('_')[0])
            user.append(filename.split('_')[1])
            pore_density.append(filename.split('_')[2])
            treat.append(filename.split('_')[3])
            peptide.append(filename.split('_')[4])
            memb.append(filename.split('_')[5])
            conc.append(filename.split('_')[6])
            fluid.append(filename.split('_')[7])
            run.append(filename.split('_')[8])
            florescense.append(flo)
            Area_trap.append(area_trap)
        
        
        #df = pd.DataFrame(data= [date,user,pore_density,treat,peptide,memb,conc,fluid,run, Hyst_area, Rem_pos,Rem_neg,pos_cond,neg_cond,Rect_factor,cum_Area,Area,Hyst_area_norm, florescense])
        #df = df.T#(columns = ['files','Hyst_Area'])
        #df = df.rename(columns = {0 : 'date', 1 : 'Supervisor', 2 : 'pore_density',3 : 'Treatment' ,4 : 'peptide', 5 : 'Membrane_name',6 : 'Conc',7 : 'Fluid', 8 : 'Run', 9: 'net area', 10: 'rem. pos', 11 : 'rem. neg',12: 'positive Conductance',13: 'negative Conductance',14: 'Rectification Factor',15: 'cumulativeArea',16: 'Area',17:'net area_norm data',18: 'florosence' })
    
        else :
            flo_columns = Mod_Exp_data['Floursence'][Mod_Exp_data['Floursence']>0]
            flo = np.mean(flo_columns)
            positive_cond = Mod_Exp_data['current(nA)'].loc[Mod_Exp_data['Norm_Volt']==max_voltage].values[0]
            negative_cond = Mod_Exp_data['current(nA)'].loc[Mod_Exp_data['Norm_Volt']==min_voltage].values[0]
            Rect_fac = (positive_cond / negative_cond)


            pos_cond.append(positive_cond)
            neg_cond.append(negative_cond)
            Rect_factor.append(Rect_fac)
            florescense.append(flo)
            
            date.append(filename.split('_')[0])
            user.append(filename.split('_')[1])
            pore_density.append(filename.split('_')[2])
            treat.append(filename.split('_')[3])
            peptide.append(filename.split('_')[4])
            memb.append(filename.split('_')[5])
            conc.append(filename.split('_')[6])
            fluid.append(filename.split('_')[7])
            run.append(filename.split('_')[8])
            
        
        df = pd.DataFrame(data= [date,user,pore_density,treat,peptide,memb,conc,fluid,run, Hyst_area, Rem_pos,Rem_neg,pos_cond,neg_cond,Rect_factor,cum_Area,Area,Hyst_area_norm, florescense,Area_trap])
        df = df.T#(columns = ['files','Hyst_Area'])
        df = df.rename(columns = {0 : 'date', 1 : 'Supervisor', 2 : 'pore_density',3 : 'Treatment' ,4 : 'peptide', 5 : 'Membrane_name',6 : 'Conc',7 : 'Fluid', 8 : 'Run', 9: 'net area', 10: 'rem. pos', 11 : 'rem. neg',12: 'positive Conductance',13: 'negative Conductance',14: 'Rectification Factor',15: 'cumulativeArea',16: 'Area',17:'net area_norm data',18: 'florosence', 19: 'Area_Trap' })    


    return df


#abcd = hist_calc(Exp_data)

#print(abcd)



