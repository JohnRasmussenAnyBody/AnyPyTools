# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 11:40:42 2012

@author: mel
"""
import os.path as op
import csv
import numpy as np
import os
import h5py_wrapper as h5py
from scipy.interpolate import interp1d



def anydatah5_generator(folder=None, match = ''):    
    if folder is None:
        folder = os.getcwd()
    def func(item):
        return item.endswith('h5') and item.find(match)!= -1
    filelist = filter(func,  os.listdir(folder)) 
    for filename in filelist:
        try:
            with h5py.File(op.join(folder,filename)) as h5file:
                yield (h5file, filename)
        except IOError:
            pass
    
def anyoutputfile_generator(folder =None, match = "", DEBUG = False):
    if folder is None:
        folder = os.getcwd()

#    filelist = [_ for _ in os.listdir(folder) if _.endswith('.txt') or  _.endswith('.csv')]
    def func(item):
        return (item.endswith('.txt') or item.endswith('.csv')) and  item.find(match)!= -1
    filelist = filter(func,  os.listdir(folder)) 
    

    
    for filename in filelist:
        filepath = op.join(folder,filename)
        data, header, const = open_anyoutputfile(filepath,DEBUG)
        if data is None:
            continue
            
        yield (data, header, const, os.path.basename(filepath))
        
def open_anyoutputfile(filepath,DEBUG = False):
    def is_scinum(str):
        try:
            np.float(str)
            return True
        except ValueError:
            return False

    with open(filepath,'r') as anyoutputfile:
        constants = {}       
        reader = iter(anyoutputfile.readline, b'')       
        #Check when the header section ends
        fpos1 = 0
        fpos0 = 0
        for row in reader:
            if is_scinum(row.split(',')[0]):
                break
            #Save constant from AnyOutput file
            const,value= _parse_anyoutputfile_constants(row)
            if const is not None:
                constants[const] = value
            fpos1 = fpos0
            fpos0 = anyoutputfile.tell()
        else:
            if DEBUG: print "No numeric data in " + os.path.basename(filepath)
            return (None,None,None)
        # Read last line of the header section if there is a header
        if fpos0 != 0:
            anyoutputfile.seek(fpos1)
            header = reader.next().strip('\n').split(',')
        else:
            header = None
        data = np.array([[float(col) for col in row.strip('\n').split(',')] for row in reader])
    return (data, header, constants)   
        


def _parse_anyoutputfile_constants(strvar):
    varname = None
    value = None
    if strvar.count('=') == 1 and strvar.startswith('Main'):
        (first, last) = strvar.split('=')
        first = first.strip()
        last = last.strip('\n').replace('{','[').replace('}',']')
        varname = first.strip()
        try:
            value = np.array(eval(last))
        except:
            value = np.array(eval('"'+last+'"') )
    return (varname, value)



def interp_percent(data, indices):
    data = np.array(data)
    data = data.squeeze()
    indices = np.array(indices)
    x = np.linspace(0,100,len(indices))
    xnew = np.arange(0,100)
    y = data[indices]   
    ipolfun = interp1d(x,y)
    return ipolfun(xnew)
    
def any_eval(string):
    string = string.split('//',1)[0]
    string  = string.split("=",1)[-1].split(";",1)[0].strip()
    
    string = string.replace('{','[')
    string = string.replace('}',']')
    return eval(string)
    
    

if __name__ == '__main__':
#    for data,header,filename in csv_trial_data('C:\Users\mel\SMIModelOutput', DEBUG= True):
#        print header
        
    outvars = ['/Output/Validation/EMG'] 
        
