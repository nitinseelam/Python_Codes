#! Python27
# -*- coding: utf-8 -*-

"""
Created on Sun Sep 18 10:47:03 2016
@author: nseelam

FiOps Portals contains a various functionalities of the original FPFE. Such as creating Submission Files and Data Upload Files.
Additional procedures for FPFE functionalities will be added to this file and simply enabled as an option in the FPFE Python File.
Each Portal needs a connection as an input.
"""

import Validation_Error_Messages as ValErrors
import pandas as pd
import time
import CAC
import NTP
import M1
import M2
import M3


def Kina_Submission_Portal(cnx):
    print '\n'
    print 'Welcome to Kina\'ole FPFE Portal'
    print '\n'
    myConnection = cnx
    
    print 'Is this process being executed for a Milestone Submission?'
    print '1. Yes'
    print '2. No'
    print '\n'
   
    while True:
        try:
            usage = int(raw_input('Please enter the number associated with your choice of Yes or No: '))
            if (usage >=1 and usage <=2):
                break
            else:
                print('Invalid input entered. Please try again.')
        except(TypeError, ValueError):
            print("Not an integer. Please try again.")
    
    print '\n'
    
    print 'Please select a Milestone'
    print '1. CAC'
    print '2. NTP'
    print '3. M1'
    print '4. M2'
    print '5. M3'
    print '\n'
    while True:
        try:
            milestoneInput = int(raw_input('Please enter the number associated with the Milestone: '))
            if (milestoneInput >=1 and milestoneInput <=5):
                break
            else:
                print('Not a valid input. Please try again.')
                print('\n')
        except(TypeError, ValueError):
            print("Not an integer. Please try again.")
        
    if milestoneInput == 1:
        query = CAC.CACSub()
        path = CAC.CACSubPath(usage)
        
    if milestoneInput == 2:
        query = NTP.NTPSub()
        path = NTP.NTPSubPath(usage)
        
    if milestoneInput == 3:
        query = M1.M1Sub()
        path = M1.M1SubPath(usage)
        
    if milestoneInput == 4:
        query = M2.M2Sub()
        path = M2.M2SubPath(usage)
        
    if milestoneInput == 5:
        query = M3.M3Sub()
        path = M3.M3SubPath(usage)
        
    # Paths are incorrect for several milestones
    
    startQuery = time.time()    
    df = pd.read_sql_query(query, myConnection)
    endQuery = time.time()
    print 'Query completed in {:.4f} seconds'.format(endQuery-startQuery)
    
    print len(df.index)
    
    #df = utf8_strings(df,)
    
    if len(df.index) == 0:
        print 'No projects qualified at the moment. Please try again later'
        
    else:
        start_file_creation = time.time()
        df['SGVTY_Account_Number'] = df['SGVTY_Account_Number'].astype(int)
        df['Installation_Zip_Code'] = df['Installation_Zip_Code'].astype(int)
        
        # Kina Val Errors Here
        if milestoneInput == 1:
            df = ValErrors.CACValidation(df)
            
        if milestoneInput == 2:
            df = ValErrors.NTPValidation(df)
            
        if milestoneInput == 3:
            df = ValErrors.M1Validation(df)
            
        if milestoneInput == 4:
            df = ValErrors.M2Validation(df)
            
        if milestoneInput == 5:
            df = ValErrors.M3Validation(df) 
            
        
        # Splitting concatenated Inverter Names over 4 columns
        inverterList = df['Inverter_Names'].str.split(';').tolist()
        print inverterList
      # Error check for Inverter Names -- if Invetrer Names Null, program crashes  
        for i in inverterList:
            print type(i)
            listLength = 4
            while len(i) < listLength:
                i.append('')
        
        Inverters = pd.DataFrame(inverterList)
        df['Inverter_01'] = Inverters[0]
        df['Inverter_02'] = Inverters[1]
        df['Inverter_03'] = Inverters[2]
        df['Inverter_04'] = Inverters[3]
        
        print df
        #if milestoneInput == 1 or milestoneInput ==3:
            #df = df.loc[:,['Milestone','Project_Name','Error Message','SGVTY_Account_Number','Last_Name','Installation_Address','Installation_City','Installation_Zip_Code','Installation_State','Region','Property_Type','Utility_Name','Credit_Approved_Date','Last_Signed_Contract_Date','CAC_Submission_Date','kW_STC','Estimated_Annual_kWh_YR_1','Previous 12 Month Usage kWh','Product_Type','Lease_Payment_Type','Escalator_Percentage','Down_Payment_Pre_Tax','Lease_Payment_Pre_Tax','Dollars_Per_Watt','Calculated_EPC','Total_Upfront_Incentives','Production_Factor_Year_1','PPA_Rate','Active_YesNo','Cancellation_Date','Financing_Partner_Payment_01','Financing_Partner_Payment_02','Financing_Partner_Payment_03','M1_Submitted_Date',	'Module_Name',	'Total_Number_of_Panels','Inverter_Names','Total_Number_Of_Inverters','Inverter_01','Inverter_02','Inverter_03','Inverter_04','Meter_Brand_Model','Meter_MAC_Address','Meter_Brand_Model_2',	'Meter_MAC_Address_2',	'Inspection_Date','M2_Submission_Date','PTO_Submitted_Date','PTO_Approved_Date','M3_Submission_Date','Last_Changed_Date','Kinaole_ApprovalDate','Kinaole_Requested_Follow_Up_Date','Kinaole_Requested_Follow_Up_Reason','Credit_Tier']]
        #else:
            #df = df.loc[:,['Milestone','Project_Name','Error Message','SGVTY_Account_Number','Last_Name','Installation_Address','Installation_City','Installation_Zip_Code','Installation_State','Region','Property_Type','Utility_Name','Credit_Approved_Date','Last_Signed_Contract_Date','CAC_Submission_Date','kW_STC','Estimated_Annual_kWh_YR_1','Previous 12 Month Usage kWh','Product_Type','Lease_Payment_Type','Escalator_Percentage','Down_Payment_Pre_Tax','Lease_Payment_Pre_Tax','Dollars_Per_Watt','Calculated_EPC','Total_Upfront_Incentives','Production_Factor_Year_1','PPA_Rate','Active_YesNo','Cancellation_Date','Financing_Partner_Payment_01','Financing_Partner_Payment_02','Financing_Partner_Payment_03','M1_Submitted_Date',	'Module_Name',	'Total_Number_of_Panels','Inverter_Names','Total_Number_Of_Inverters','Inverter_01','Inverter_02','Inverter_03','Inverter_04','Meter_Brand_Model','Meter_MAC_Address','Meter_Brand_Model_2',	'Meter_MAC_Address_2',	'Inspection_Date','M2_Submission_Date','PTO_Submitted_Date','PTO_Approved_Date','M3_Submission_Date','Last_Changed_Date','Kinaole_ApprovalDate','Kinaole_Requested_Follow_Up_Date','Kinaole_Requested_Follow_Up_Reason']]
        """
        Writing to Excel
        """
        writer = pd.ExcelWriter(path, engine='xlsxwriter',options={'encoding':'utf-8'}, date_format='mm/dd/yyyy', datetime_format = 'mm/dd/yyyy')
        df.to_excel(writer,sheet_name='Submission File', index=False)
        workbook = writer.book
        worksheet = writer.sheets['Submission File']
        
        """
        Excel Formatting Options
        """
        noborder_format = workbook.add_format().set_border(False)
        zipcode_format = workbook.add_format({'num_format':'00000'})
        twodecimals_format = workbook.add_format({'num_format': '0.00'})
        threedecimals_format = workbook.add_format({'num_format': '0.000'})
        text_wrap = workbook.add_format({'text_wrap':True})
        highlight_format = workbook.add_format({'bg_color': '#FFC7CE','font_color': '#9C0006'})
        #date_format = workbook.add_format({'num_format': 'mm/dd/yyyy'})
        
        """
        Setting Column Formats
        """
        worksheet.set_row('1:1', None, noborder_format)
        worksheet.set_column('G:G', None, zipcode_format)
        worksheet.set_column('AD:AF',None, twodecimals_format)
        worksheet.set_column('U:Z',None, twodecimals_format)
        worksheet.set_column('AA:AA', None, threedecimals_format)
        worksheet.set_column('C2:C1000', 57,text_wrap)
      
        worksheet.conditional_format('C2:C1000',{'type':'no_blanks','format': highlight_format})
        worksheet.freeze_panes(1,4)
       
            
        writer.save()
        
        end_file_creation = time.time()
        print 'File formatted and created in {:.4f} seconds'.format(end_file_creation-start_file_creation)
        print 'Please find the created file in the following path:'
        print path
        print '\n'
        print 'Done! Directing back to Portal Menu'
        
   
    
   
    
    
def Kina_Upload_Portal(cnx):
    print '\n'
    print 'Welcome to the Kina Data Upload Portal'
    print 'Currently this process is limited to creating Data Upload files for uploading date values for Milestone.'
    print '\n'
    myConnection = cnx
    
    Value = str(raw_input('Please enter the date value to upload, in the following format: yyyy-mm-dd'))
    #Instead ask for filename
    Acct_Nums = str(raw_input('Please enter Project Account Numbers seperated by a \',\' for which this Data Upload Sheet is being created.'))
    
    print 'Please select a Milestone'
    print '1. CAC'
    print '2. NTP'
    print '3. M1'
    print '4. M2'
    print '5. M3'
    while True:
        try:
            milestoneInput = int(raw_input('Please enter the number associated with the Milestone: '))
            if (milestoneInput >=1 and milestoneInput <=5):
                break
            else:
                print('Not a valid input. Please try again.')
                print('\n')
        except(TypeError, ValueError):
            print("Not an integer. Please try again")
            
    if milestoneInput == 1:
        query = CAC.CACUpload(Value, Acct_Nums)
        path = CAC.CACUploadPath()
        
    if milestoneInput == 2:
        query = NTP.NTPUpload(Value, Acct_Nums)
        path = NTP.NTPUploadPath()
        
    if milestoneInput == 3:
        query = M1.M1Upload(Value, Acct_Nums)
        path = M1.M1UploadPath()
        
    if milestoneInput == 4:
        query = M2.M2Upload(Value, Acct_Nums)
        path = M2.M2UploadPath()
        
    if milestoneInput == 5:
        query = M3.M3Upload(Value, Acct_Nums)
        path = M3.M3UploadPath()
        
    df = pd.read_sql_query(query, myConnection, params={'Account':Acct_Nums, 'Attribute':Value})
    
    writer = pd.ExcelWriter(path, engine = 'xlsxwriter',date_format='mm/dd/yyyy', datetime_format = 'mm/dd/yyyy')
    df.to_excel(writer, sheet_name = 'Upload Sheet',index = False)
    writer.save()
    
    print 'Data Upload File Created!'
    print 'Please find the Data Upload File in the following path:'
    print path
    
    print '\n'
    print 'Exitting...'
    
    exit()
    

    
    
    