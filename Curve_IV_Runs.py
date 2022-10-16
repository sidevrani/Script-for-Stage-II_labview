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
import backbone_curve

## Function used for producing IV curve for each concentration and for each of the runs.


#import magic font settings.
font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 16,
        }

#local_dir = r'C:\Users\TIDAS\OneDrive - University of Gothenburg\TietzeLab\Autodata_Exp\For_Data_analysis\10062022_Cyl.preetch_unfunc_0.02MumPR4_buffer_5Conc(1)_double dispense to valve & waste_sampleSD'
#Exp_data= accum_data_function.accu_data(local_dir)

#backbone = backbone_curve.backbone_curve(Exp_data)
def curve_i_vs_t(local_dir,backbone):
    backbone['Run'] = backbone['filename'].map(lambda x : x.split('_')[8])
    backbone['Conc(fM)'] = backbone['filename'].map(lambda x :x.split('_')[6])
    backbone['membrane'] = backbone['filename'].map(lambda x :x.split('_')[5])
    backbone['peptide'] = backbone['filename'].map(lambda x :x.split('_')[4])
    backbone['pore density'] = backbone['filename'].map(lambda x :x.split('_')[2])
    backbone['fluid']= backbone['filename'].map(lambda x :x.split('_')[7])
    backbone['date']= backbone['filename'].map(lambda x :x.split('_')[0])
    
    filenames = backbone['filename'].unique()
    runs =  backbone['Run'].unique()
    dates = backbone['date'].unique()
    #Treatments = backbone['Treatment'].unique()
    peptides = backbone['peptide'].unique()
    membranes = backbone['membrane'].unique()
    Concs = backbone['Conc(fM)'].unique()
    Fluids = backbone['fluid'].unique()


    # fig, axs = plt.subplots(nrows=round(len(Concs)/2), ncols = round(len(Concs)/2)+1, figsize=(15, 12))
    # plt.subplots_adjust(hspace=0.5)
    for date in dates:
        for peptide in peptides:
            for membrane in membranes:
                for fluid in Fluids:
                    for Conc in Concs:
                        #plot the IV Charts
                        fig, axs = plt.subplots()
                        fig.set_size_inches(50, 25)
                        lab = []

                        for run in runs:
                            mod_data_1 =  backbone.loc[(backbone['date']==date) & (backbone['Conc(fM)']==Conc) & (backbone['Run']==run)]
                        
                            if mod_data_1.empty != True:    
                                mod_data_1 = mod_data_1.sort_values(by =['Voltage(V)'])

                            # Move left y-axis and bottim x-axis to centre, passing through (0,0)
                                axs.spines['left'].set_position('center')
                                axs.spines['bottom'].set_position('zero')

                            # Eliminate upper and right axes
                                axs.spines['right'].set_color('none')
                                axs.spines['top'].set_color('none')
                                
                            # Show ticks in the left and lower axes only
                                axs.xaxis.set_ticks_position('bottom')
                                axs.yaxis.set_ticks_position('left')
                                axs.tick_params(axis='x', labelsize=27)
                                axs.tick_params(axis='y', labelsize=27)
                                axs.set_xlabel('Voltage(V)',fontdict= font,loc = 'right')
                                axs.set_ylabel('Current(nA)',fontdict= font)  
                                
                                x_volt = mod_data_1['Voltage(V)']
                                y_current = mod_data_1['current(nA)']
                                lab.append('{0}_{1}_{2}_{3}_{4}_{5}'.format(peptide,membrane,Conc,fluid,run,date))
                                plt.plot(x_volt, y_current,'o-')
                        plt.legend(lab,fontsize=12,loc = 0)
                        #axs = plt.gca()
                        plt.savefig(local_dir + '/Mem{0}_{1}_{2}(I vs V)_{3}'.format(membrane,peptide,Conc,date) +'.png')
                        #plt.show()

    return 
                                    
                                    
#curve_i_vs_t(local_dir,backbone)