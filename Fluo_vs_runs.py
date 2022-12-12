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

#local_dir = r'C:\Users\xdevsh\OneDrive - University of Gothenburg\TietzeLab\Autodata_Exp\05122022_Con_selfetch_unfunc_XXMumSE17_HS_9conc_Selectivity&Sensitivityagain'
#Exp_data= accum_data_function.accu_data(local_dir)

#backbone = backbone_curve.backbone_curve(Exp_data)
def curve_flo_vs_runs(local_dir,Exp_data):

    keywords = ["Acc",".png","Note.txt"]
    # Get file order
    order = open(local_dir + '\order', "r")
    order_lines = order.readlines()
    order.close()
    
    def inputFiles_gen(x):
        x1 = []
        for element in order_lines:
            x1.append(local_dir + '\\' + element.split('\n')[0])
        return x1 

    inputFiles = inputFiles_gen(order_lines)
    filenames = [inputFile.split('\\')[-1] for inputFile in inputFiles]
    y_flo = []
    x_axis = []

    # Fet files in filenames
    for file in filenames:
        Conc = file.split('_')[-3]
        Run = file.split('_')[-1]

        mod_data_1 =  Exp_data.loc[(Exp_data['Conc(fM)']== Conc) & (Exp_data['Run']== Run)]

        if mod_data_1.empty != True: 
            if (mod_data_1["Floursence"] != 0).any():
                y_flo.append(mod_data_1["Floursence"][mod_data_1["Floursence"] != 0].mean())
            else:
                y_flo.append(0)
            x_axis.append(Conc + ',' + Run)
        else: 
            pass
    
    
  
    # PLot Specifications

    fig, ax = plt.subplots()
    #ax.spines['bottom'].set_position('zero')
    fig.set_size_inches(25, 30)                           
    plt.plot(x_axis, y_flo,'o-')
    plt.xlabel("Conc,Run", fontsize=22)
    plt.ylabel("Fluorosense",fontsize=22)
    ax = plt.gca()
    #ax.set_xlim(0, 12)
    #ax.set_xlabel('X-axis')
    ax.set_xticklabels(x_axis,fontsize=15, rotation=45)
    ax.set_yticklabels(x_axis,fontsize=15, rotation=45)

    plt.savefig(local_dir + '/Flour_vs_Conc,run' + '.png')
    
    return 


#curve_flo_vs_runs(local_dir,Exp_data)