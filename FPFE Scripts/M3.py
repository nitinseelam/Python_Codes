# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 09:41:00 2016
@author: nseelam

Contains Submission and Data Upload Queries for M3
"""
import os

def M3Sub():
    query = ("""
SELECT DISTINCT
	'M3' As Milestone
    , 	M.Name as 'Project_Name'
    ,   '' as 'Error Message'
	, 	M.ACCOUNT_NUMBER__C as 'SGVTY_Account_Number'
    , 	iQuote_Doc_LSC.Signer_Name__c AS 'Last_Name'
	, 	M.SITE_STREET__C AS 'Installation_Address'
    , 	M.SITE_CITY__C AS 'Installation_City'
    , 	zip.Name AS 'Installation_Zip_Code'
    , 	s2.Installation_State AS 'Installation_State'
	,	CASE
        WHEN M.SITE_STATE_PROVINCE__C IN ('MA' , 'MD', 'NJ', 'DE', 'CT', 'AZ') THEN 'ALL'
        WHEN JRSP.Utility_Name = 'Alameda Power & Telecom' THEN 'Alameda Power & Telecom'
        WHEN JRSP.Utility_Name = 'Anaheim Public Utility' THEN 'Anaheim Public Utility'
        WHEN JRSP.Utility_Name = 'Burbank Water & Power' THEN 'Burbank Water & Power'
        WHEN JRSP.Utility_Name = 'Glendale Water & Power' THEN 'Glendale Water & Power'
        WHEN JRSP.Utility_Name = 'City of Palo Alto Utilities' THEN 'City of Palo Alto Utilities'
        WHEN JRSP.Utility_Name = 'Imperial Irrigation District' THEN 'Imperial Irrigation District'
        WHEN JRSP.Utility_Name = 'LAWDP' THEN 'LAWDP'
        WHEN JRSP.Utility_Name = 'Modesto Irrigation District' THEN 'Modesto Irrigation District'
        WHEN JRSP.Utility_Name = 'Pasadena Water & Power' THEN 'Pasadena Water & Power'
        WHEN JRSP.Utility_Name = 'PGE' THEN 'PGE'
        WHEN JRSP.Utility_Name = 'Redding Electric Utility' THEN 'SCE'
        WHEN JRSP.Utility_Name = 'SCE' THEN 'SCE'
        WHEN JRSP.Utility_Name = 'SDGE' THEN 'SDGE'
        WHEN JRSP.Utility_Name = 'Silicon Valley Power' THEN 'Silicon Valley Power'
        WHEN JRSP.Utility_Name = 'SMUD' THEN 'SMUD'
        WHEN JRSP.Utility_Name = 'Turlock Irrigation District' THEN 'Turlock Irrigation District'
        WHEN JRSP.Utility_Name = 'Riverside Public Utilities' THEN 'Riverside Public Utilities'
        WHEN JRSP.Utility_Name = 'Xcel - CO' THEN 'Xcel'
        WHEN JRSP.Utility_Name = 'PEPCO District of Columbia' THEN 'PEPCO District of Columbia'
        WHEN JRSP.Utility_Name = 'PNM  - NM' THEN 'PNM  - NM'
        WHEN
            JRSP.Utility_Name IN ('CHG&E (Central Hudson Gas and Electric)' , 'National Grid',
                'Orange and Rockland',
                'NYSEG (New York State Electric and Gas)',
                'Rochester Gas and Electric')
        THEN
            'Upstate'
        WHEN JRSP.Utility_Name = 'ConEd (Consolidated Edison New York)' THEN 'Downstate'
        WHEN JRSP.Utility_Name = 'PSE&G - NY (Long Island)' THEN 'Long Island'
    END AS 'Region'
        
    , 	M.PROPERTY_TYPE__C AS 'Property_Type'
    , 	JRSP.Utility_Name As 'Utility_Name'
    , 	FPA.Credit_Approved_Date As 'Credit_Approved_Date'
    ,	JRSP.Last_Signed_Contract_Date As 'Last_Signed_Contract_Date'
    , 	IF(CAC_Submission_Date IS NOT NULL, CAC_Submission_Date, CURDATE()) AS 'CAC_Submission_Date'
	, 	s2.kW_STC AS 'kW_STC'
	, 	s2.Estimated_Annual_kWh_YR_1 as 'Estimated_Annual_kWh_YR_1'
	, 	O.TOTAL_ANNUAL_USAGE__C as 'Previous 12 Month Usage kWh'
	, 	s2.Product_Type as 'Product_Type'
	, 	M.Lease_Payment_Type__c as 'Lease_Payment_Type'
	, 	s2.Escalator_Percentage as 'Escalator_Percentage'
	, 	s2.Down_Payment_Pre_Tax as 'Down_Payment_Pre_Tax'
	,   s2.Lease_Payment_Pre_Tax as 'Lease_Payment_Pre_Tax'
    ,	s2.Rev_Per_Watt AS 'Dollars_Per_Watt'
    ,	s2.EPC as 'Caclulated_EPC'
	, 	s2.Total_Upfront_Incentives as'Total_Upfront_Incentives'
	, 	s2.Production_Factor_Year_1 as 'Production_Factor_Year_1'
	, 	((LSC_SP.PAYMENT_PRE_TAX__C * 12) / System_LSC.ANNUAL_KWH__C) as 'PPA_Rate'
    , 	IF(M.STATUS__C = 'Active' OR M.STATUS__C = 'Complete', 'Yes', 'No') AS 'Active_YesNo'
	,	M.CANCELLATION_DATE__C As 'Cancellation_Date'
    ,	(s2.EPC*0.5) as 'Financing_Partner_Payment_01'
    ,	(s2.EPC*0.4) as 'Financing_Partner_Payment_02'
    ,	(s2.EPC*0.1) as 'Financing_Partner_Payment_03'
    ,	IF(FPA.M1_Submitted_Date IS NOT NULL, FPA.M1_Submitted_Date, '') As 'M1_Submitted_Date'
    ,	IF(CAC_Submission_Date IS NULL, System_LSC.Module_Name__c, System_SV4B.Module_Name__c) AS 'Module_Name'
    ,	IF(CAC_Submission_Date IS NULL, System_LSC.Total_Number_of_Panels__c, System_SV4B.Total_Number_of_Panels__c) AS 'Total_Number_of_Panels'
    ,	IF(CAC_Submission_Date IS NULL, System_LSC.INVERTER_NAMES__C, System_SV4B.INVERTER_NAMES__C) AS 'Inverter_Names' -- remember to change destination for text to columns so don't override Total_Number_Of_Inverters
    ,	IF(CAC_Submission_Date IS NULL, System_LSC.TOTAL_NUMBER_OF_INVERTERS__C, System_SV4B.TOTAL_NUMBER_OF_INVERTERS__C) AS 'Total_Number_Of_Inverters'
	,	'' as 'Inverter_01' 
	,	'' as 'Inverter_02'
	,	'' as 'Inverter_03'
	,	'' As 'Inverter_04'
    ,	M.Monitoring_System__c AS Meter_Brand_Model
    ,	M.Monitoring_Serial_Number__c AS Meter_MAC_Address
    ,	M.Monitoring_System_2__c AS Meter_Brand_Model_2
    ,	M.MONITORING_SERIAL_NUMBER_2__C AS Meter_MAC_Address_2
    , 	M.INSPECTION_DATE__C As 'Inspection_Date'
    ,	IF(FPA.M2_Submitted_Date IS NULL,IF(M2_Ready_to_Submit_Date IS NOT NULL,CURDATE(),''),FPA.M2_Submitted_Date) As 'M2_Submission_Date'
    , 	IF(M.FINAL_INTER_SUBMITTED__C IS NULL, '', M.FINAL_INTER_SUBMITTED__C) As 'PTO_Submitted_Date'
    ,	IF(M.FINAL_INTER_APPROVED_RECEIVED__C IS NOT NULL, M.FINAL_INTER_APPROVED_RECEIVED__C,'') As 'PTO_Approved_Date'
    ,	IF(FPA.M3_Submitted_Date IS NOT NULL, FPA.M3_Submitted_Date, CURDATE()) As 'M3_Submission_Date'
    ,	'' As 'Last_Changed_Date'
    ,	'' AS 'Kinaole_ApprovalDate'
    ,	'' AS 'Kinaole_Requested_Follow_Up_Date'
    , 	'' As 'Kinaole_Requested_Follow_Up_Reason'
    ,	s2.Credit_Tier As 'Credit_Tier'
    
    
    -- Additional Fields needed for Kina Val Error
    , M.TRANCHE_STATUS__C as 'Tranche Status'
    , t.Name as 'Tranche Name'
    , FPA.M2_Ready_to_Submit_Date as 'M2 Ready to Submit Date'
    , System_LSC.Name as 'LSC System'
    ,	System_SV4B.Name as 'SV4B System'
    ,	System_SV4B.CONSUMPTION_OFFSET__C as 'Consumption Offset'
    ,	FP.Name as 'Funding Product'
    ,	FP.PRODUCT_TYPE__C as 'Product Type'
    ,	M.LEASE_PAYMENT_TYPE__C
    


FROM
	salesforce_prod.Opportunity O
		LEFT JOIN salesforce_prod.Lead Lead ON O.ID = lead.CONVERTEDOPPORTUNITYID 
			AND Lead.Name NOT LIKE '%%testsungevity%%'
			AND Lead.Name NOT LIKE '%%sungevitytest%%'
			AND lead.`STATUS` NOT LIKE 'Qualified Duplicate'
	  LEFT JOIN salesforce_prod.iQuote__c ON O.Id = iQuote__c.Opportunity__c
        LEFT JOIN salesforce_prod.Account Account ON iQuote__c.Account__c = Account.Id
        LEFT JOIN salesforce_prod.Milestone1_Project__c M ON M.Id = iQuote__c.Project__c 
        LEFT JOIN salesforce_prod.Tranche__c t ON (t.id = M.Tranche__c)
        LEFT JOIN salesforce_prod.User pm ON (pm.id = M.OwnerID)
        LEFT JOIN salesforce_prod.User ilm ON (ilm.id = M.Installation_Logistics_Manager__c)
        LEFT JOIN salesforce_prod.User fm ON (fm.id = M.Field_Manager__c)
        LEFT JOIN salesforce_prod.FieldOffices__c fo ON (fo.id = M.Field_Office_Name__c)
        LEFT JOIN salesforce_prod.System__c System_SV4B ON iQuote__c.Id = System_SV4B.iQuote__c AND System_SV4B.SV4B__c = 1
        LEFT JOIN salesforce_prod.System__c System_LSC ON iQuote__c.Id = System_LSC.iQuote__c AND System_LSC.LSC__c = 1
        LEFT JOIN salesforce_prod.System__c System_LEPC ON iQuote__c.Id = System_LEPC.iQuote__c AND System_LEPC.LEPC__c = 1
        LEFT JOIN salesforce_prod.AHJ__c ON M.AHJ_Name__c = AHJ__c.Id
        LEFT JOIN salesforce_prod.Funding_Product__c FP ON (FP.Project__c = M.Id AND FP.Selected_Product__c = 1)
        LEFT JOIN salesforce_prod.Funding_Provider__c ON Funding_Provider__c.Id = FP.Funding_Provider__c   
        LEFT JOIN salesforce_prod.Funding_Provider__c final ON final.Id = FP.FINAL_ASSET_OWNER__C 
        LEFT JOIN salesforce_prod.jrs_project JRSP ON M.Id = JRSP.ProjectId
        LEFT JOIN salesforce_prod.jrs_funding_product_attribute FPA ON FP.Id = FPA.Funding_Product__c
        LEFT JOIN salesforce_prod.Region__c zip ON zip.Name = LEFT(iQuote__c.Postal_Code__c,5)
        LEFT JOIN salesforce_prod.RecordType ON M.RecordTypeID = RecordType.ID
        LEFT JOIN (SELECT * FROM salesforce_prod.AccountContactRole WHERE Role = 'Decision Maker/Borrower') acr1 ON (acr1.AccountId = Account.Id)
        LEFT JOIN salesforce_prod.contact b1 ON (b1.Id = acr1.ContactId) 
        LEFT JOIN (SELECT * FROM salesforce_prod.AccountContactRole WHERE Role = 'Decision Maker/Co-Borrower') acr2 ON (acr2.AccountId = Account.Id)
        LEFT JOIN salesforce_prod.contact b2 ON (b2.Id = acr2.ContactId) 
        LEFT JOIN salesforce_prod.System_Price__c LSC_SP ON (System_LSC.id=LSC_SP.System__c AND FP.Id = LSC_SP.Funding_Product__c AND LSC_SP.Active_Pricing__c = 1)
        LEFT JOIN salesforce_prod.`Case` c ON (M.Id = c.PROJECT__C AND c.SUBJECT = '20116 - Compliance Check - Kinaole')
        LEFT JOIN salesforce_prod.user cuser ON c.OWNERID = cuser.ID
        LEFT JOIN salesforce_prod.user samuser ON Account.SAM_ASSIGNED__C = samuser.ID
        LEFT JOIN salesforce_prod.utility__c Util ON M.UTILITY__C = Util.ID
        LEFT JOIN fiops.kina_epc_schedule_2 s2 ON M.ID = s2.Project_ID
        LEFT JOIN fiops.epc epc ON M.ID = epc.Project_ID
        LEFT JOIN salesforce_prod.iQuote_Document__c iQuote_Doc_LSC ON System_LSC.ID = iQuote_Doc_LSC.SYSTEM__C AND iQuote_Doc_LSC.Document_Type__c IN ('kinaole_ppa' , 'kinaole_lease','sunfinco_ppa','sunfinco_lease')AND iQuote_Doc_LSC.Status__c IN ('Externally Countersigned' , 'Fully Executed', 'Approved')
						
WHERE
FPA.M3_Submitted_Date IS NULL 
AND FPA.M3_Approval_Date IS NULL
AND FPA.M2_Ready_to_Submit_Date IS NOT NULL
AND FPA.M1_Approval_Date IS NOT NULL 
AND M.FINAL_INTER_APPROVED_RECEIVED__C IS NOT NULL
AND	M.Status__c <>'Test' 
AND M.STATUS__C IN ('Active','Complete')
AND FP.Selected_Product__c = 1
AND M.IS_TEST__C = 0
AND t.Name NOT IN ('Test Project','Cash')
AND FP.name IN ('kinaole_lease','kinaole_ppa','sunfinco_lease','sunfinco_ppa')
""")
    
    return query

def M3SubPath(usage):
    print 'Please enter desired filename for M3 Submission File'
    filename = str(raw_input())
    
    if usage == 1:
        path = 'S://Finance Operations/A. Funds/G. Kinaole/L. FPFE Submission Process/E. M3_Prep/Origination Report/' + filename + '.xlsx'
    else:
        userhome = os.path.expanduser('~')
        path = userhome + '/Desktop/' + filename + '.xlsx'
        
    return path    

def M3Upload(Attribute,Account):
    query = ("""
SELECT DISTINCT
	M.Name As 'Project Name'
, 	FPA.ATTRIBUTE_NAME__C AS 'FPO Attribute Name'
, 	FPA.ID AS 'FPO_Attribute_ID'
,	IF(FPA.ATTRIBUTE_NAME__C = 'M3 Submitted Date', {}, System_SV4B.NAME) As 'Attribute_Value'
, 	M.TRANCHE_STATUS__C AS 'Tranche Status'
,	M.ID As 'ProjectId'

FROM
	salesforce_prod.Opportunity O
		LEFT JOIN salesforce_prod.Lead Lead ON O.ID = lead.CONVERTEDOPPORTUNITYID
			AND Lead.Name NOT LIKE '%testsungevity%'
			AND Lead.Name NOT LIKE '%sungevitytest%'
			AND lead.`STATUS` NOT LIKE 'Qualified Duplicate'
		LEFT JOIN salesforce_prod.iQuote__c ON O.Id = iQuote__c.Opportunity__c
		LEFT JOIN salesforce_prod.Account Account ON iQuote__c.Account__c = Account.Id
        LEFT JOIN Milestone1_Project__c M ON M.Id = iQuote__c.Project__c
        LEFT JOIN Funding_Product__c FP ON (FP.Project__c = M.Id AND FP.Selected_Product__c = 1)
        LEFT JOIN salesforce_prod.funding_product_attribute__c FPA on FPA.Funding_Product__c = FP.ID
		LEFT JOIN Funding_Provider__c ON Funding_Provider__c.Id = FP.Funding_Provider__c
        LEFT JOIN salesforce_prod.System__c System_SV4B ON iQuote__c.Id = System_SV4B.iQuote__c AND System_SV4B.SV4B__c = 1
        LEFT JOIN salesforce_prod.System__c System_LSC ON iQuote__c.Id = System_LSC.iQuote__c AND System_LSC.LSC__c = 1
        LEFT JOIN salesforce_prod.System__c System_LEPC ON iQuote__c.Id = System_LEPC.iQuote__c AND System_LEPC.LEPC__c = 1

WHERE
FPA.ATTRIBUTE_NAME__C IN ('M3 Submitted Date','M3 Submitted System Name')
AND M.Account_Number__c IN {}""".format(Attribute,Account))   

    
    return query
    
def M3UploadPath():
    userhome = os.path.expanduser('~')
    print 'Please enter desired filename for M3 Data Upload File'
    filename = str(raw_input())
    path = userhome + filename
    
    return path