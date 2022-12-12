from fileinput import filename
import math
import os
import sys

sys.path.append(r'C:\Users\xdevsh\OneDrive - University of Gothenburg\TietzeLab\Autodata_Exp\Pyhton scripts_labview\Script for Stage II_labview')

import operator
import numpy as np
import pandas as pd
import xlsxwriter
import hysteresis as hys
import openpyxl as oxl
from openpyxl import load_workbook
from sklearn.preprocessing import MinMaxScaler
Scale = MinMaxScaler(feature_range=(-1,1))
local_dir = r'C:\Users\xdevsh\Desktop\half time report\Caliberation'


files = os.listdir(local_dir)
df_final = pd.DataFrame()
for file in files:
    df = pd.DataFrame()
    date = file.split('_')[1]
    #user = file.split('_')[1]
    #pore_density = file.split('_')[2]
    shape = file.split('_')[2]
    peptide = file.split('_')[4]
    memb = file.split('_')[5]
    conc = '0fM'
    fluid = file.split('_')[6]

    df['date'] = date
    df['shape'] = shape
    df['peptide'] = peptide
    df['conc'] = conc
  
    
    df = df.reindex(columns= ['date','shape','peptide','conc'] )

    df = pd.read_excel(local_dir+'/'+ file, sheet_name='0fM_Statistics')
    df.reset_index()
    df_final = pd.concat([df_final,df] ,  axis = 0)    #Exp_data = pd.concat([Exp_data,df], axis = 0)
   
    
    
df_final

# def con_data(local_dir):
# filenamekeywords = ["POS","NEG"]
# dir_list = os.listdir(local_dir)
# #dir_list = [i for i in dir_list if keywords in dir_list]
# Exp_data = pd.DataFrame()
# for filename in dir_list:
#     df = pd.DataFrame()
#     Exp_data['filename'] = filename

#     file = open(local_dir+ "/" + filename , "r" )
#     lines = file.readlines()
#     file.close()
#     reducedLines = []
	# No Reduction of amount of data now, maybe later we could Skip time values
    
    #reducedLines.append(filename,lines )



    # Exp_data = pd.DataFrame()
    # # Extract Data from file
    # #order = open(local_dir + '\order', "r")
    # #order_lines = order.readlines()
    # #order.close()

    
    # # def inputFiles_gen(x):
    # #     x1 = []
    # #     for element in order_lines:
    # #         x1.append(local_dir + '\\' + element.split('\n')[0])
    # #     return x1 

    # inputFiles = inputFiles_gen(order_lines)
    
    # for inputFile in inputFiles:
    #     # Get file Classification Data
    #     file_name = inputFile.split('\\')[-1]
    #     date = file_name.split('_')[0]
    #     user = file_name.split('_')[1]
    #     pore_density = file_name.split('_')[2]
    #     treat = file_name.split('_')[3]
    #     peptide = file_name.split('_')[4]
    #     memb = file_name.split('_')[5]
    #     conc = file_name.split('_')[6]
    #     fluid = file_name.split('_')[7]
    #     run = file_name.split('_')[8]
    
    # # Extract Data from file
    #     file = open(inputFile, "r")
    #     lines = file.readlines()
    #     file.close()
    #     reducedLines = []
	# # No Reduction of amount of data now, maybe later we could Skip time values
    #     for line in lines:
    #         index = line.find('\t')
    #         reducedLines.append(date + '\t' + user + '\t' + pore_density + '\t' + treat + '\t' + peptide + '\t' + memb + '\t' + conc + '\t' + fluid + '\t' + run + '\t'  + file_name +  '\t' +line)

    #     reducedLines = [str(line.replace(',','.')).split() for line in reducedLines]
    
	# # Made a dataframe.
    #     df = pd.DataFrame(reducedLines)
    
    #Exp_data = pd.concat([Exp_data,df], axis = 0)
    
    
    # Name the columns, normalize data, reset index the final Exp_data
    # Exp_data = Exp_data.rename(columns = {0 : 'date', 1 : 'Supervisor', 2 : 'pore_density',3 : 'Treatment' ,4 : 'peptide', 5 : 'Membrane_name',6 : 'Conc(fM)',7 : 'Fluid', 8 : 'Run', 9: 'filename',10: 'time(sec)' , 11: 'voltage(V)',12 : 'current(nA)',13 : 'Floursence'})
    # Exp_data['time(sec)'] = Exp_data['time(sec)'].astype(float)
    # Exp_data['voltage(V)'] = Exp_data['voltage(V)'].astype(float)
    # Exp_data['current(nA)'] = Exp_data['current(nA)'].astype(float)
    # Exp_data['Floursence'] = Exp_data['Floursence'].astype(float)
    # Exp_data['Norm_Volt']= Scale.fit_transform(Exp_data['voltage(V)'].iloc[:].values.reshape(-1,1))
    # Exp_data['Norm_Curr']= Scale.fit_transform(Exp_data['current(nA)'].iloc[:].values.reshape(-1,1))

    # Exp_data = Exp_data.reindex(columns= ['date','Supervisor','pore_density','Treatment' ,'peptide','Membrane_name','Conc(fM)','Fluid', 'Run','filename','time(sec)' ,'voltage(V)','current(nA)','Norm_Volt','Norm_Curr' , 'Floursence'] )
    #return #
#con_data