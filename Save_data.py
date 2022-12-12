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
import Hyst_actual_data
import Curve_ivst
import Curve_IV_Runs
import Curve_IV_Conc
import standard_deviation_calculation
import Fluo_vs_runs

#local_dir = r'C:\Users\xdevsh\OneDrive - University of Gothenburg\TietzeLab\Autodata_Exp\25102022_Cyl_preetch_ATCUN_0.03MumPR12_HS_4conc_secondrunsawtooth_edit'
local_dir = r'C:\Users\xdevsh\OneDrive - University of Gothenburg\TietzeLab\Autodata_Exp\05122022_Con_selfetch_unfunc_XXMumSE17_HS_9conc_Selectivity&Sensitivityagain'

def save_data(local_dir):
     identifier = local_dir.split('\\')[-1]
     writer = pd.ExcelWriter(local_dir+ '\Results_{0}.xlsx'.format(identifier), engine = 'xlsxwriter')
     try:
          Exp_data = accum_data_function.accu_data(local_dir)
          Exp_data.to_excel(writer, sheet_name= 'Accumulated Data', index = False)
     except:
          next 

     try:
          Fluo_vs_runs.curve_flo_vs_runs(local_dir,Exp_data)
           
     except:
          next
          
     try:
          Hyst_data = Hyst_actual_data.hist_calc(Exp_data)
          Hyst_data.to_excel(writer, sheet_name= 'Hysterisis Data', index = False)
     except:
          next
     try:     
          backbone = backbone_curve.backbone_curve(Exp_data)
          backbone.to_excel(writer, sheet_name= 'backbone', index = False)
     except:
          next
     try: 
          Curve_ivst.curve_i_vs_t(local_dir)
     except:
          next
     try: 
          Curve_IV_Conc.curve_IV(local_dir,backbone)
     except:
          next
     
     try:
          Curve_IV_Runs.curve_i_vs_t(local_dir,backbone)
     except:
          next
     writer.close()
     try:
          standard_deviation_calculation.SD(backbone,local_dir)
           
     except:
          next
     
     return 


save_data(local_dir)


