import math
#import matplotlib.pyplot as plt
import operator
import os
from queue import Empty
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


sys.path.append(r'C:\Users\xdevsh\OneDrive - University of Gothenburg\TietzeLab\Autodata_Exp\Pyhton scripts_labview\Script for Stage II_labview')
import accum_data_function
import backbone_curve




## Function used for producing IV curve for each concentration averaged over all the runs.


#import magic font seetings
font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 16,
        }

#local_dir = r'C:\Users\TIDAS\OneDrive - University of Gothenburg\TietzeLab\Autodata_Exp\For_Data_analysis\10062022_Cyl.preetch_unfunc_0.02MumPR4_buffer_5Conc(1)_double dispense to valve & waste_sampleSD'

#Exp_data= accum_data_function.accu_data(local_dir)

#backbone = backbone_curve.backbone_curve(Exp_data)
def curve_IV(local_dir,backbone):
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
    for peptide in peptides:
        for membrane in membranes:
            for fluid in Fluids:
            #plot the IV Charts
                fig, axs = plt.subplots()
                fig.set_size_inches(50, 25)
                lab = []
            

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
                axs.set_ylabel('Current(nA)',fontdict= font,loc = 'top')  
                
                #
                #
                for date in dates:
                    for Conc in Concs:
                        _ = pd.DataFrame()   

                        for run in runs:
                            mod_data_1 =  backbone.loc[(backbone['date']==date) &(backbone['Conc(fM)']==Conc) & (backbone['Run']==run)]
                            if mod_data_1.empty != True:
                                mod_data_1 = mod_data_1.sort_values('Voltage(V)',ascending=True)
                                _1 = mod_data_1['current(nA)'].astype(np.float64)
                                #_['Run {0}'.format(run)]= mod_data_1['current(nA)']
                                #_1=_1.reset_index()
                                _ = pd.concat([_.reset_index(),_1.reset_index()],axis =1)
                                _ = _.drop('index', axis=1)
                                x_volt = mod_data_1['Voltage(V)']
                                
                                
                        lab.append('{0}_{1}_{2}_{3}_{4}'.format(peptide,membrane,Conc,fluid,date))
                            #_= _.reset_index()
                        
                    #_ = _.drop('index', axis=1, inplace=True)
                    
                        _['Avg_current(nA)'] = _.mean(axis=1) 
                    
                        y_current = _['Avg_current(nA)']
                        #y = y_current.shape
                        #z = _['Avg_current(nA)'].shape
                        if (x_volt.shape == y_current.shape):
                            plt.plot(x_volt, y_current,'o-')
                        else:
                            pass
                        
                
                    plt.legend(lab,fontsize=12,loc = 0)
                    #axs = plt.gca()
                    plt.savefig(local_dir + '/Mem{0}_{1}_{2}(I-V)_{3}'.format(membrane,peptide,Fluids,date) +'.png')
                    #plt.show()
    return

                        

#curve_IV(local_dir,backbone)



    