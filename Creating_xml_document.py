#import xml.etree.ElementTree as E
from lxml import etree as E
from Creating_json_files import *
import os
from xml.dom import minidom
import json

def convert_aECG():
    
#importing json file.
    try:                                            # check the file is exists or not 
        with open('json_data.json') as json_file:
            data = json.load(json_file) 
            Flag=0
    except FileNotFoundError:
        Flag=1
        print('Json File path is not found...', 'Cannot proceed forward..')
            
    if(Flag==0):
#importing csv_read function to read the lead values 
        from  csv_lead import csv_read
        
        path=r'D:\Nishu_works\Python_codes\TP\Record'
        if(os.path.isdir(path)):                     # if path exists checks the condition. 
            print('Valid file path  ','Started Converting XML format.... ')
        else:
            print('please enter the valid path')    
        y=csv_read(path)

# Creating Namespace for root element Tag. 
        xmlns="urn:hl7-org:v3";
        xmlns_1="urn:hl7-org:v3/voc";
        xsi="http://www.w3.org/2001/XMLSchema-instance"
        schemaLocation="urn:hl7-org:v3 ../schema/PORT_MT020001.xsd" 
        typ="Observation"

# xml tree code starts from here  
        root = E.Element('AnnotatedECG',nsmap={None:xmlns,'voc':xmlns_1,'xsi':xsi,'type':typ})

        child = E.SubElement(root,"id",data['id'])


        code = E.SubElement(root,'code',data['code'])

        effectiveTime=E.SubElement(root,'effectiveTime')
        child = E.SubElement(effectiveTime,"center", data['effectiveTime']['center'])

        child = E.SubElement(root,"confidentialityCode", data['confidentialityCode'])
        child = E.SubElement(root,"reasonCode", data['reasonCode'])

        componentof=E.SubElement(root,'componentOf')
        timepointevent=E.SubElement(componentof,'timePointEvent')
        child = E.SubElement(timepointevent,"code",data['componentOf']['timepointevent']['code'])

        sub=E.SubElement(timepointevent,'effectiveTime')
        
        low=E.SubElement(sub,'low',data['componentOf']['timepointevent']['Lvalue'])
        high=E.SubElement(sub,'high',data['componentOf']['timepointevent']['Hvalue'])
        child = E.SubElement(timepointevent,"reasonCode",data['componentOf']['timepointevent']['reasonCode'])
        
        sub=E.SubElement(timepointevent,'performer')
        sub=E.SubElement(sub,'studyEventPerformer')
#att5={'root':'','extension':''}
        child=E.SubElement(sub,'id',data['componentOf']['timepointevent']['studyEventPerformer']['id'])

        assignedPerson=E.SubElement(sub,'assignedPerson')
        Name=E.SubElement(assignedPerson,'name')
        Name.text = "JMK"

        componentOf=E.SubElement(timepointevent,'componentOf')
        subjectAssignment=E.SubElement(componentOf,'subjectAssignment')
        subject=E.SubElement(subjectAssignment,'subject')
        trialSubject=E.SubElement(subject,'trialSubject')
        child=E.SubElement(trialSubject,'id',data['componentOf']['timepointevent']['trialSubject']['id'])
        child=E.SubElement(trialSubject,'code',data['componentOf']['timepointevent']['trialSubject']['code'])
        sub=E.SubElement(trialSubject,'subjectDemographicPerson')
        name=E.SubElement(sub,'name')
        name.text='Nishanth'
        administrativeGenderCode=E.SubElement(sub,'administrativeGenderCode',data['componentOf']['timepointevent']['subjectDemographicPerson']['GenderCode'])
        birthTime=E.SubElement(sub,'birthTime',data['componentOf']['timepointevent']['subjectDemographicPerson']['birthTime'])
        raceCode=E.SubElement(sub,'raceCode',data['componentOf']['timepointevent']['subjectDemographicPerson']['raceCode'])

        sub=E.SubElement(root,'component')
        sub1=E.SubElement(sub,'series')
        
        att6_2={'{%s}type' % xsi: 'ST'}

# loop for control variable in xml doc.
        k=0  # for code loop 
        p=0  # for value loop 
        for i in range(0,3):    
            for j in range(0,1):       
                sub=E.SubElement(sub1,"controlvariable")
                sub=E.SubElement(sub,"controlvariable")
                child=E.SubElement(sub,"code", data[str(k)][1][1]['controlvariable']['code']) # or att3.
                sub_1=E.SubElement(sub,"component")
                sub_2=E.SubElement(sub_1,"controlvariable")
                child=E.SubElement(sub_2,"code", data[str(k+1)][1][1]['controlvariable']['code']) # or att3
                k=k+2
                if (i==0):
                    child=E.SubElement(sub_2,'value',data[str(0)][1][0]['controlvariable']['value'])            
                else:  
                    child=E.SubElement(sub_2,'value',att6_2)
                    child.text=data[str(p)][1][0]['controlvariable']['ST']    
                    p=p+1

        sub=E.SubElement(sub,"component")
        sub=E.SubElement(sub,"controlvariable")
        child=E.SubElement(sub,"code",data[str(6)][1][1]['controlvariable']['code']) # or att3
        child=E.SubElement(sub,'value',data[str(1)][1][0]['controlvariable']['value'])        

        component=E.SubElement(root,"component")
        sequenceSet=E.SubElement(component,'sequenceSet')
        component=E.SubElement(sequenceSet,"component")
        sequence=E.SubElement(component,"sequence")
        child=E.SubElement(sequence,'code',data['sequence']['code'])
        value=E.SubElement(sequence,'value',{'{%s}type' % xsi: 'GLIST_TS'})
        child=E.SubElement(value,'head',data['sequence']['head'])
        child=E.SubElement(value,'increament',data['sequence']['increament'])

# Sequence tag which contains 12 leads.
        for i in range(0,12):
            for j in range(0,1):
                Component=E.SubElement(sequenceSet,"component")
                sub=E.SubElement(Component,"sequence")

                child=E.SubElement(sub,'code',data[str(i)][0]['code'] )  
                value=E.SubElement(sub,'value',{'{%s}type' % xsi: 'SLIST_PQ'})
                child=E.SubElement(value,"origin",data[str(i)][0]['origin'] )   
                child=E.SubElement(value,'scale', data[str(i)][0]['scale'])    
                digits=E.SubElement(value,'digits')
                digits.text=y[(i,i)]        
               
# output displays in python ide.    
#E.dump(root)     
# writing the xml tree to a file by encoding to "utf-8" and indent to "1 tab space" to see the loops clearly on xml doc. 
        xml_file = E.tostring(root,encoding="utf-8", method="xml")
        string = minidom.parseString(xml_file).toprettyxml(indent="    ", encoding='utf-8')  # to avoid sorting of attributes remove "sort" on  minidom module xmlwrite function.  
        with open(r"Created_xml_file_Output.xml","wb") as f: # open in binary write mode. this will write the file as it is.  
            f.write(string) # or f.write(xmlstr.encode('utf-8'))
            print('File is writed!!','Finished.....')

convert_aECG()