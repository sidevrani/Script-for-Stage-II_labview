import math
#import matplotlib.pyplot as plt
import operator
import os
import sys
from tokenize import Double
import numpy as np
import pandas as pd
from pandas import ExcelWriter
import matplotlib.pyplot as plt
import matplotlib as mlb
#import seaborn as sns
from math import e
from sklearn.preprocessing import MinMaxScaler
Scale = MinMaxScaler(feature_range=(-1,1))
import warnings
warnings.filterwarnings("ignore")
import  re
import openpyxl as oxl
from openpyxl import load_workbook
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
from scipy.integrate import simps
from numpy import trapz
import hysteresis as hys


sys.path.append(r'C:\Users\TIDAS\OneDrive - University of Gothenburg\TietzeLab\Pyhton scripts_labview\Script for Stage II_labview')
import accum_data_function



## Function used for producing current vs time curve for each concentration and for each of the runs.


#import magic font seetings
font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 16,
        }

local_dir = r'C:\Users\xdevsh\OneDrive - University of Gothenburg\TietzeLab\Autodata_Exp\13102022_Cyl_preetch_unfunc_0.03MumPR10_buffer_selectivity with Ni & Cu'


# define the curve sketch and save function
def curve_i_vs_t(local_dir):
    Exp_data= accum_data_function.accu_data(local_dir)
    mod_data = Exp_data[['date','pore_density','Treatment' ,'peptide','Membrane_name','Conc(fM)','Fluid', 'Run','time(sec)','voltage(V)', 'current(nA)','Norm_Volt','Norm_Curr']]
    
    mod_data['Conc(fM)'] = mod_data['Conc(fM)'].map(lambda x: float(x.split('f')[0].replace('X','').replace('10^','.e+')) if x != '10^10fM' else float(x.split('f')[0].replace('X','').replace('10^','1.e+')))
    #mod_data['Conc(fM)'] = mod_data['Conc(fM)'].map(lambda x: x.split('f')[0].replace('X','').replace('10^','.e+')) if x != '10^10fM' else float(x.split('f')[0].replace('X','').replace('10^','1.e+'))
    mod_data['time(sec)'] = mod_data['time(sec)'].map(lambda x :float(x))
    mod_data['voltage(V)'] = mod_data['voltage(V)'].map(lambda x :float(x))
    mod_data['current(nA)'] = mod_data['current(nA)'].map(lambda x :float(x))
    mod_data['Norm_Volt'] = mod_data['Norm_Volt'].map(lambda x :float(x))
    mod_data['Norm_Curr'] = mod_data['Norm_Curr'].map(lambda x :float(x))

    
    dates = mod_data['date'].unique()
    Treatments = mod_data['Treatment'].unique()
    peptides = mod_data['peptide'].unique()
    membranes = mod_data['Membrane_name'].unique()
    Concs = mod_data['Conc(fM)'].unique()
   
    Fluids = mod_data['Fluid'].unique()
    Runs = mod_data['Run'].unique()
    
    for date in dates:
        for Treatment in Treatments:
            for peptide in peptides:
                for membrane in membranes:
                    for Conc in Concs:
                        lab = []
                        fig, ax = plt.subplots()
                        ax.spines['bottom'].set_position('zero')
                        fig.set_size_inches(15, 10)
                        ax.xaxis.set_ticks_position('bottom')
                        ax.yaxis.set_ticks_position('left')
                        ax.tick_params(axis='x', labelsize=16)
                        ax.tick_params(axis='y', labelsize=16)
                        ax.set_xlabel('time(Sec)',fontdict= font,loc = 'right')
                        ax.set_ylabel('Current(nA)',fontdict= font,loc = 'top')  
                        for Fluid in Fluids:
                            for run in Runs:
                                mod_data_1 =  mod_data.loc[(mod_data['date']==date) & (mod_data['Treatment']==Treatment) & (mod_data['peptide']==peptide) & (mod_data['Conc(fM)']== Conc)& (mod_data['Membrane_name']==membrane) & (mod_data['Fluid']==Fluid) & (mod_data['Run']== run)]
                                if (mod_data_1.empty == False and mod_data_1['time(sec)'][0]< 0) :
                                    offset_time = mod_data_1['time(sec)'][0]
                                    mod_data_1['time(sec)'] = mod_data_1['time(sec)'].map(lambda x :x + (-1*offset_time))
                                    lab.append('Mem{0}_{1}_{2}_{3}fM_{4}_{5}'.format(membrane,peptide,Fluid,Conc,run,date))
                                    x_time = mod_data_1['time(sec)']
                                    y_current = mod_data_1['current(nA)']
                                    
                                plt.plot(x_time, y_current)
                        plt.legend(lab,fontsize=12,loc = 0)
                        ax = plt.gca()
                        plt.savefig(local_dir + '/Mem{0}_{1}_{2}fM_{3}'.format(membrane,peptide,Conc,date) +'.png')
                        
    return  
                                    
curve_i_vs_t(local_dir)