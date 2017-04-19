# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 13:13:47 2016
@author: nseelam

The various Kina Validation Error Checks are listed in this file. Error checks are split out by Milestone, as
different milestones have different criteria. 
"""
def CACValidation(df):
    for Index, row in df.iterrows():
        Error = ''
        
        if (row['ACH Status'] == None or row['ACH Status'] == 'Missing' or row['ACH Status'] == 'Incomplete'): 
            Error += 'ACH Status Missing; '
            
        if (str(row['LSC Signer First Name']) != str(row['Borrower First Name'])) or (str(row['LSC Signer Last Name']) != str(row['Borrower Last Name'])):
            Error += 'LSC Signer and Borrower Names not Matching; '
            
        if (row['LSC CoSigner First Name'] != row['CoBorrower First Name']) or (row['LSC CoSigner Last Name'] != row['CoBorrower Last Name']):
            Error += 'LSC CoSigner and CoBorrower Names not Matching; '
            
        if (row['LSC Doc Status'] not in ['Fully Executed','Approved'] or row['LSC Doc Status'] == None):
            Error += 'LSC Doc Status is not Fully Executed or Approved; '
            
        if row['Credit Approval Date'] == None:
            Error += 'Credit Approval Date Missing; '
            
        if row['Last_Name'] == None:
            Error += 'Last Name Missing; '
            
        if row['Credit Aging'] > 90:
            Error += 'Credit Approval > 90 Days; '
            
        if row['LSC Doc Approved By'] == None:
            Error += 'LSC Document Not Approved By; '
            
        if row['kW_STC'] < 2:
            Error += 'System Size < 2 kW; '
            
        if row['kW_STC'] > 50:
            Error += 'System Size > 50 kW; '
        
        if (row['LSC System Size'] != row['PG System Size']):
            Error += 'System Size not matching between LSC & PG Docs; '
            
        df.set_value(Index,'Error Message', Error)
        
    return df
    
def NTPValidation(df):
    for Index, row in df.iterrows():
        Error = ''
        closed_status = ['Closed', 'Closed - Duplicate', 'Closed - Cancelled']
        
        if (row['ACH Status'] == None or row['ACH Status'] == 'Missing'):
            Error += 'ACH Status Missing; '
            
        if (row['LSC Doc Status'] not in ['Fully Executed','Approved'] or row['LSC Doc Status'] == None):
            Error += 'LSC Doc Status is not Fully Executed or Approved; '
        
        if row['kW_STC'] < 2:
            Error += 'System Size < 2 kW; '
            
        if row['Auto-Inter. Geo'] == 'Yes' or (row['Auto-Inter. Geo'] == 'No' and row['AHJ Auto-Inter.'] == 'Yes'):
            Error += 'Auto Interconnect Geo/AHJ; '
            
        if row['SV4B Contract Status'] != 'Contract Valid':
            Error += 'SV4B Not Marked Contract Valid; '
            
        if row['kW_STC'] > 50:
            Error += 'System Size > 50 kW;'
            
        if row['LSC System Size'] != row['PG System Size']:
            Error += 'System Size not matching between LSC & PG Docs; '
            
        if row['LSC Doc Approved By'] == None:
            Error += 'LSC Document Not Approved By; '
            
        if row['Tranche Name'] in ['Re-Assessment','On-Deck']:
            Error += 'Tranche Name in Re-Assessment/On-Deck; '
            
        if row['Planset Complete Date'] == None:
            Error += 'Planset Complete Date Missing; '
            
        if row['AWE Case'] != None and row['AWE Case Status'] not in closed_status:
            Error += 'Active Design Revision, MSP Swap, Initial Inter., or Schedule Outstanding Work Case; '
            
        if row['SV4B System'] != row['LSC System']:
            Error += 'Mismatch between LSC and SV4B Equipment; '
            
        df.set_value(Index,'Error Message', Error)
        
    return df
            
def M1Validation(df):
    for Index, row in df.iterrows():
        Error = ''
        closed_status = ['Closed', 'Closed - Duplicate', 'Closed - Cancelled']
        
        if (row['ACH Status'] == None or row['ACH Status'] == 'Missing'):
            Error += 'ACH Status Missing; '
            
        if (row['LSC Doc Status'] != 'Fully Executed' or row['LSC Doc Status'] != 'Approved' or row['LSC Doc Status'] == None):
            Error += 'LSC Document Status Not Fully Executed or Approved; '
            
        if row['kW_STC'] < 2:
            Error += 'System Size less than 2 kW; '
            
        if row['SV4B Contract Status'] != 'Contract Valid':
            Error += 'SV4B Not Marked Contract Valid; '
            
        if row['Equipment Shipped Date'] == None:
            Error += 'Equipment Shipped Date Missing; '
            
        if row['Equipment Shipping Tracking No.'] == None:
            Error += 'Equipment Shipping Tracking No. Missing; '
            
        if row['Tranche Status'] != 'Confirmed':
            Error += 'Tranche Status not Confirmed; '
            
        if row['LSC System'] != row['SV4B System']:
            Error += 'SV4B Equipment does not match LSC Equipment; '
            
        if row['Credit Approval Date'] == None:
            Error += 'Credit Approval Date Missing; '
            
        if row['Credit Approved Aging'] >= 90:
            Error += 'Credit Approval > 90 Days; '
            
        if row['AWE Case'] != None and row['AWE Case Status'] not in closed_status:
            Error += 'Active Design Revision, MSP Swap, Initial Inter., or Schedule Outstanding Work Case; '
        
        df.set_value(Index,'Error Message', Error)
    
    return df
    
def M2Validation(df):
    for Index, row in df.iterrows():
        Error = ''
        closed_status = ['Closed', 'Closed - Duplicate', 'Closed - Cancelled']
        
        if row['Inspection_Date'] == None:
            Error += 'Inspection Date Missing; '
            
        if (row['M2 QB Case Status'] == 'Blocked' or row['M2 QB Case Status'] == 'New' or row['M2 QB Case Status'] == 'Actionable'):
            Error += 'M2 QB Case Open; '
            
        if row['PBAC Ready to Submit Date'] != None:
            Error += 'PBAC Date Populated; '
            
        if row['Tranche Status'] != 'Bank Approved':
            Error += 'Not Bank Approved; '
            
        if row['Meter_MAC_Address'] == None:
            Error += 'MAC Monitoring ID Missing; '
            
        if row['M2 QB Case']!= None and row['M2 QB Case Status'] not in closed_status:
            Error += 'Active QB Case Open; '
            
        df.set_value(Index,'Error Message', Error)
    
    return df
    
def M3Validation(df):
    for Index, row in df.iterrows():
        Error = ''
        if row['Tranche Status'] != 'Bank Approved':
            Error += 'Not Bank Approved; '
            
        if row['Meter_MAC_Address'] == None:
            Error += 'MAC Monitoring ID Missing; '

            
        if row['PTO_Approved_Date'] == None:
            Error += 'PTO Received Date Missing; '
            
        if row['M2 Ready to Submit Date'] == None:
            Error += 'M2 Ready to Submit Date Missing; '
            
        df.set_value(Index,'Error Message', Error)
                     
    return df
    

    