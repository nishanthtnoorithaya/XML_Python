# -*- coding: utf-8 -*-
"""
Created on Friday 21-05-2020 17:40:06

@author: Nishanth T (Junior Python Developer)

"""

import os 
import pandas as pd

def csv_read(path):
    y=dict()
    count=0
    c=os.listdir(path)
    lead=['L1','L2','V1','V2','V3','V4','V5','V6','L3','aVR','aVL','aVF']
    for i in range(0,len(c)):
        n1=c[i].split('_');n2=n1[3].split('.');n1.remove(n1[3])
        n1='_'.join(n1);n3=n1+'_'+lead[1]+'.'+n2[1]            
        fullpath=os.path.join(str(path),n3)
        with open(fullpath,encoding='utf-8') as f:
            df=pd.read_csv(f)
            idx=df.to_string(index=False) #remove the index
            g=idx.replace("\n","")
            #data1=g.replace("  ","")
            y[count,i]=g
            count+=1 
    return y       
