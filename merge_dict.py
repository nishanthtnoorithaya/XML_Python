# -*- coding: utf-8 -*-
"""
Created on Thursday 21-05-2020 17:40:06

@author: Nishanth T (Junior Python Developer)

"""

def mergeDict(dict1, dict2):
   ''' Merge dictionaries and keep values of common keys in list'''
   dict3 = {**dict1, **dict2}
   for key, value in dict3.items():
       if key in dict1 and key in dict2:
               dict3[key] = [value , dict1[key]]
 
   return dict3
