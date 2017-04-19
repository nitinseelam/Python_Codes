import os
import time
import pandas as pd
import getpass
import pymysql
import CAC
import NTP
import M1
import M2
import M3
import FPFEFunctions as FPFE
import milestoneQueries as mq
import datetime
  
####################### FPFE Portal ##############
"""
--------------------------------------------------------
Kina FPFE Portal Process
--------------------------------------------------------
"""
# Connects to Database asking for Username and Password
print '\n'
print 'Welcome to Kina\'ole FPFE Portal'
print '\n'

hostname = 'bi.caccvpdn1wcb.us-east-1.rds.amazonaws.com'
database = 'salesforce_prod'
username = raw_input("Please enter your Sungevity username: ")
print 'Please enter your Database Password: '
password = getpass.getpass()
timenow = time.strftime("%Y-%m-%d_%I-%M-%p")
userhome = os.path.expanduser('~')

    
myConnection = pymysql.connect(host=hostname, user=username, passwd = password, db=database)

'''
If FPFE used for Milestone Submission, saves created Excel on S Drive
else saves on user's Desktop.
'''
print 'Is the FPFE being executed for a Milestone Submission?'
print 'Please type in one of the following options:  Yes  No'
print '\n'
while True:
    usage = str(raw_input())
    if (usage == 'No' or usage == 'Yes'):
        break
    else:
        print("Invalid input entered. Please type in one of the following options:  Yes  No")
print '\n'

'''
Asks user for input to run the query of interest.
'''
print '\n'
print 'Running Kina FPFE for which Milestone Submission?'
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
        print("Not an integer. Please try again")
        print('\n')
#'S:\Finance Operations\A. Funds\G. Kinaole\L. FPFE Submission Process\E. M3_Prep\Origination Report'

# sql is name of query being executed        
sql = FPFE.submissionQuery(milestoneInput)

start = time.time()
# Include params={'list':list of account  numbers} in the pd.read... to pass parameters into SQL Query
df = pd.read_sql_query(sql,myConnection)
end = time.time()


df['SGVTY_Account_Number'] = df['SGVTY_Account_Number'].astype(int)
df['Installation_Zip_Code'] = df['Installation_Zip_Code'].astype(int)

inverterList = df['Inverter_Names'].str.split(';').tolist()

for i in inverterList:
    listLength = 4
    while len(i) < listLength:
        i.append('')

Inverters = pd.DataFrame(inverterList)
df['Inverter_01'] = Inverters[0]
df['Inverter_02'] = Inverters[1]
df['Inverter_03'] = Inverters[2]
df['Inverter_04'] = Inverters[3]
print df
accountNumList = df['SGVTY_Account_Number'].tolist()
print accountNumList

Account = str(accountNumList).replace('[','(')
Account = Account.replace(']',')')
print Account

print 'Query completed in {:.4f} seconds'.format(end-start)
#print df
filename = raw_input('Please enter the desired filename for this Submission File: ')
path = userhome + '/Desktop/' + timenow + '.xlsx'
path1 = userhome + '/Desktop/' + timenow + '.xlsx'
spath = 'S://Finance Operations/A. Funds/G. Kinaole/Kina Testing/Python Test/' + filename + '.xlsx'

"""
Writing to Excel
"""
writer = pd.ExcelWriter(spath, engine='xlsxwriter', date_format='mm/dd/yyyy', datetime_format = 'mm/dd/yyyy')
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
#date_format = workbook.add_format({'num_format': 'mm/dd/yyyy'})

"""
Setting Column Formats
"""
worksheet.set_row('1:1', None, noborder_format)
worksheet.set_column('G:G', None, zipcode_format)
worksheet.set_column('AD:AF',None, twodecimals_format)
worksheet.set_column('U:Z',None, twodecimals_format)
worksheet.set_column('AA:AA', None, threedecimals_format)
#worksheet.set_column('AT:AY', None, date_format)

writer.save()

print('Do you need to create Data Upload Documents as well? Please type in "Yes" or "No". ')
while True:
    usage2 = str(raw_input())
    if (usage2 == 'No' or usage2 == 'Yes'):
        
        break
    else:
        print("Invalid input entered. Please type in one of the following options: Yes  No")
    
if usage2 == 'Yes':
    Value = raw_input("Please insert the attribute value you would like to assign in the following format 'yyyy-mm-dd': ")
    print type(Value)
    print Value
    sql2 = FPFE.dataUploadQuery(milestoneInput,Account)
    start2 = time.time()
    df = pd.read_sql_query(sql2,myConnection)

    end2 = time.time()
    print 'Query completed in {:.4f} seconds'.format(end2-start2)
    
writer2 = pd.ExcelWriter(path1, engine = 'xlsxwriter',date_format='mm/dd/yyyy', datetime_format = 'mm/dd/yyyy')
df.to_excel(writer2, sheet_name = 'Upload Sheet',index = False)
workbook = writer2.book
writer2.save()

print 'Data Upload Sheet created!'
myConnection.close()
    

    
 