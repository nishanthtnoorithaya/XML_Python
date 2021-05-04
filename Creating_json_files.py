# -*- coding: utf-8 -*-
"""
Created on Friday 21-05-2020 17:40:06

@author: Nishanth T (Junior Python Developer)

"""


#creating json file
import json
from merge_dict import mergeDict 
from datetime import datetime

now = datetime.now() # current date and time
date_time = now.strftime("%Y%m%d%H%M%S")


xsi="http://www.w3.org/2001/XMLSchema-instance"

# lead defination in aECG format 
leadname=['MDC_ECG_LEAD_I','MDC_ECG_LEAD_II','MDC_ECG_LEAD_V1','MDC_ECG_LEAD_V2','MDC_ECG_LEAD_V3','MDC_ECG_LEAD_V4',
          'MDC_ECG_LEAD_V5','MDC_ECG_LEAD_V6','MDC_ECG_LEAD_III','MDC_ECG_LEAD_AVR','MDC_ECG_LEAD_AVL','MDC_ECG_LEAD_AVF']

codes=['LOW_PASS','CUTOFF_FREQ','HIGH_PASS','DESCRIPTION','NOTCH','DESCRIPTION','NOTCH_FREQ']
displayname=['Low pass filter','Cutoff Frequency','high pass filter','filter type','Notch filter','filter type','notch frequency']
value=['150','60'];ST=['FIR','Adaptive']
# intialise the variables
data={}
lead_code={};lead={};convar={};controlvar={};data1={};data2={}
count=0


# assign the value and key in dict manner 
data['id']={'root':'61d1a24f-b47e-41aa-ae95-f8ac302f4eeb'}
data['code']={'code':'93000','codeSystem':'2.16.840.1.113883.6.12', 'codeSystemName':'CPT-4'}
data['effectiveTime']={};
data['effectiveTime']['center']={'value':date_time}
data['confidentialityCode']={'code':'B','codeSystem':'1.2.3.4.5','codeSystemName':'???CDISC???','displayName':'Blinded to Sponsor and Investigator'}
data['reasonCode']={'code':'PER_PROTOCOL','codeSystem':'1.2.3.4.5','codeSystemName':'???CDISC???','displayName':'The protocol specified that a measurement be performed at this point in the trial'}
data['componentOf']={};data['componentOf']['timepointevent']={}
data['componentOf']['timepointevent']['code']={'code':"VISIT_3",'codeSystem':"2.16.840.1.113883.3.2",'codeSystemName':"PUK-123-PROT-C1",'displayName':"3rd Visit"}
data['componentOf']['timepointevent']['Lvalue']={'value':"200211220737"}
data['componentOf']['timepointevent']['Hvalue']={'value':"200211221023"}
data['componentOf']['timepointevent']['reasonCode']={'code':"S",'codeSystem':"1.2.3.4.5",'codeSystemName':"???CDISC???",'displayName':"Scheduled Visit"}
data['componentOf']['timepointevent']['studyEventPerformer']={}
data['componentOf']['timepointevent']['studyEventPerformer']['id']={'root':"2.16.840.1.113883.3.400",'extension':"SC-342"}
data['componentOf']['timepointevent']['trialSubject']={}
data['componentOf']['timepointevent']['trialSubject']['id']={'root':"2.16.840.1.113883.3.400",'extension':"SBJ-001"}
data['componentOf']['timepointevent']['trialSubject']['code']={'code':"ENROLLED",'codeSystem':"2.16.840.1.113883.5.111",'codeSystemName':"ResearchSubjectRoleBasis",'displayName':"Enrolled in trial"}
data['componentOf']['timepointevent']['subjectDemographicPerson']={}
data['componentOf']['timepointevent']['subjectDemographicPerson']['GenderCode']={'code':"M",'codeSystem':"2.16.840.1.113883.5.1"}
data['componentOf']['timepointevent']['subjectDemographicPerson']['birthTime']={'value':"19920808"}
data['componentOf']['timepointevent']['subjectDemographicPerson']['raceCode']={'code':"2106-3",'codeSystem':"2.16.840.1.113883.5.104",'codeSystemName':"Race",'displayName':"Asian"}


# add the values to filter specification. 
for i in range(0,7):
    convar['controlvariable']={}
    convar['controlvariable']['code']={'code':'MDC_ECG_CTL_VBL_ATTR_FILTER'+'_'+codes[i],'codeSystem':"2.16.840.1.113883.6.24",'codeSystemName':"MDC",'displayName':displayname[i]}					                    
    if (i<2): 
        data1['controlvariable']={}
        data1['controlvariable']['value']={'{%s}type' % xsi:'PQ','value':value[i],'unit':"Hz"}
        data1['controlvariable']['ST']=ST[i]
    controlvar[count]=convar
    data2[count]=data1
    convar={} 
    data1={}
    count+=1

# lead parameters defination by dict manner adding values. 
data['sequence']={}
data['sequence']['code']={'code':"TIME_ABSOLUTE",'codeSystem':"2.16.840.1.113883.5.4",'codeSystemName':"ActCode",'displayName':"Absolute Time"}
data['sequence']['head']={'value':'20021122091000.000'}
data['sequence']['increament']={'value':"0.002",'unit':"s"}

# for loop for 12 lead data
count=0  
for j in range(0,12):        
    lead_code['code']={'code':leadname[j],'codeSystem':'2.16.840.1.113883.6.24','codeSystemName':'MDC'}    
    lead_code['origin']={'value':"0",'unit':"uV"}
    lead_code['scale']={'value':"2.5",'unit':'uV'}
    lead[count]=lead_code
    lead_code={}
    count+=1

# merge the 2 dictionary vairable.
data1={**data,**lead}      
dict1=mergeDict(controlvar,data2) # merge the 2 dictionary vairable which having same keys. 
data=mergeDict(dict1,data1)    # merge the 2 dictionary vairable which having same keys. 

with open(r'json_data.json', 'w') as outfile:
    json.dump(data,outfile,sort_keys=False,indent=4) # "sort_keys=True"used for sorting keys. 
    outfile.close()    