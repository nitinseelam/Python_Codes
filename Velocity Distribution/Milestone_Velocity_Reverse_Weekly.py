import FiOps_Functions as Funcs
import pandas as pd
import numpy as np
import time
import datetime
from datetime import datetime
import sqlalchemy

def main():

    conn = Funcs.sql_fiops_connect()

    Updated_Date = """ select Last_Refreshed_Date from fiops.milestone_velocity_reverse_weekly LIMIT 1"""
    Last_Refreshed_Date = pd.read_sql_query(Updated_Date, conn)
    Last_Refreshed_Date = Last_Refreshed_Date.loc[0, 'Last_Refreshed_Date']
    Last_Refreshed_Date

    today = datetime.today()
    today = today.strftime("%Y-%m-%d")
    today = datetime.strptime(today,"%Y-%m-%d" ).date()
    today

    if (Last_Refreshed_Date < today) :
        kinaM1query = """
        SELECT
        	M.ID as 'ID'
        ,	M.Name as 'Project Name'
        ,	M.SALE_CLOSED__C as 'Sale_Closed_Date'
        ,	FPA.M1_Submitted_Date as 'M1_Submitted_Date'
        ,	YEAR(FPA.M1_Submitted_Date) as 'Year'
        ,	MONTH(FPA.M1_Submitted_Date) as 'Month'
        ,	DAY(FPA.M1_Submitted_Date) as 'Day'
        ,	DATEDIFF(M.SALE_CLOSED__C, FPA.M1_Submitted_Date) as 'Days_to_M1'
        ,	'Kinaole' as 'Fund'
        ,	'Sale - M1' as 'Milestone'
        ,	CASE
        	WHEN DATEDIFF(M.SALE_CLOSED__C, FPA.M1_Submitted_Date) > -30 THEN 0
            WHEN DATEDIFF(M.SALE_CLOSED__C, FPA.M1_Submitted_Date) > -60 THEN 1
            WHEN DATEDIFF(M.SALE_CLOSED__C, FPA.M1_Submitted_Date) > -90 THEN 2
            WHEN DATEDIFF(M.SALE_CLOSED__C, FPA.M1_Submitted_Date) > -120 THEN 3
            WHEN DATEDIFF(M.SALE_CLOSED__C, FPA.M1_Submitted_Date) > -150 THEN 4
            WHEN DATEDIFF(M.SALE_CLOSED__C, FPA.M1_Submitted_Date) > -180 THEN 5
            ELSE 6
            END as 'Months_to_M1'

        FROM
        	salesforce_prod.Opportunity O
        		LEFT JOIN salesforce_prod.Lead Lead ON O.ID = lead.CONVERTEDOPPORTUNITYID
        			AND Lead.Name NOT LIKE '%%testsungevity%%'
        			AND Lead.Name NOT LIKE '%%sungevitytest%%'
        			AND lead.`STATUS` NOT LIKE 'Qualified Duplicate'
        		LEFT JOIN salesforce_prod.iQuote__c ON O.Id = iQuote__c.Opportunity__c
                LEFT JOIN salesforce_prod.Milestone1_Project__c M ON M.Id = iQuote__c.Project__c
                LEFT JOIN salesforce_prod.Tranche__c t ON (t.id = M.Tranche__c)
                LEFT JOIN salesforce_prod.Funding_Product__c FP ON (FP.Project__c = M.Id AND FP.Selected_Product__c = 1)
                -- LEFT JOIN Funding_Product_Attribute_column_view FPA ON FPA.Funding_Product__c = FP.Id
                LEFT JOIN salesforce_prod.Funding_Provider__c ON Funding_Provider__c.Id = FP.Funding_Provider__c
                LEFT JOIN salesforce_prod.Funding_Provider__c final ON final.Id = FP.FINAL_ASSET_OWNER__C
                LEFT JOIN salesforce_prod.jrs_project JRSP ON M.Id = JRSP.ProjectId
                LEFT JOIN salesforce_prod.jrs_funding_product_attribute FPA ON FP.Id = FPA.Funding_Product__c

        WHERE
        FP.name IN ('kinaole_lease','kinaole_ppa','sunfinco_lease','sunfinco_ppa')
        AND M.IS_TEST__C = 0
        AND t.Name LIKE 'Kinaole%%'
        AND M.STATUS__C <> 'Cancelled'
        AND FPA.M1_Submitted_Date IS NOT NULL
        """

        kinaM2query = """
        SELECT
        	M.ID as 'ID'
        ,	M.Name as 'Project Name'
        ,	FPA.M1_Submitted_Date as 'M1_Submitted_Date'
        ,	FPA.M2_Submitted_Date as 'M2_Submitted_Date'
        ,	YEAR(FPA.M2_Submitted_Date) as 'Year'
        ,	MONTH(FPA.M2_Submitted_Date) as 'Month'
        ,	DAY(FPA.M2_Submitted_Date) as 'Day'
        ,	DATEDIFF(FPA.M1_Submitted_Date, FPA.M2_Submitted_Date) as 'Days_M1_M2'
        ,	'Kinaole' as 'Fund'
        ,	'M1 - M2' as 'Milestone'
        ,	CASE
        	WHEN DATEDIFF(FPA.M1_Submitted_Date, FPA.M2_Submitted_Date) > -30 THEN 0
            WHEN DATEDIFF(FPA.M1_Submitted_Date, FPA.M2_Submitted_Date) > -60 THEN 1
            WHEN DATEDIFF(FPA.M1_Submitted_Date, FPA.M2_Submitted_Date) > -90 THEN 2
            WHEN DATEDIFF(FPA.M1_Submitted_Date, FPA.M2_Submitted_Date) > -120 THEN 3
            WHEN DATEDIFF(FPA.M1_Submitted_Date, FPA.M2_Submitted_Date) > -150 THEN 4
            WHEN DATEDIFF(FPA.M1_Submitted_Date, FPA.M2_Submitted_Date) > -180 THEN 5
            ELSE 6
            END as 'Months_M1_M2'

        FROM
        	salesforce_prod.Opportunity O
        		LEFT JOIN salesforce_prod.Lead Lead ON O.ID = lead.CONVERTEDOPPORTUNITYID
        			AND Lead.Name NOT LIKE '%%testsungevity%%'
        			AND Lead.Name NOT LIKE '%%sungevitytest%%'
        			AND lead.`STATUS` NOT LIKE 'Qualified Duplicate'
        		LEFT JOIN salesforce_prod.iQuote__c ON O.Id = iQuote__c.Opportunity__c
                LEFT JOIN salesforce_prod.Milestone1_Project__c M ON M.Id = iQuote__c.Project__c
                LEFT JOIN salesforce_prod.Tranche__c t ON (t.id = M.Tranche__c)
                LEFT JOIN salesforce_prod.Funding_Product__c FP ON (FP.Project__c = M.Id AND FP.Selected_Product__c = 1)
                -- LEFT JOIN Funding_Product_Attribute_column_view FPA ON FPA.Funding_Product__c = FP.Id
                LEFT JOIN salesforce_prod.Funding_Provider__c ON Funding_Provider__c.Id = FP.Funding_Provider__c
                LEFT JOIN salesforce_prod.Funding_Provider__c final ON final.Id = FP.FINAL_ASSET_OWNER__C
                LEFT JOIN salesforce_prod.jrs_project JRSP ON M.Id = JRSP.ProjectId
                LEFT JOIN salesforce_prod.jrs_funding_product_attribute FPA ON FP.Id = FPA.Funding_Product__c

        WHERE
        FP.name IN ('kinaole_lease','kinaole_ppa','sunfinco_lease','sunfinco_ppa')
        AND M.IS_TEST__C = 0
        AND t.Name LIKE 'Kinaole%%'
        AND M.STATUS__C <> 'Cancelled'
        AND FPA.M1_Submitted_Date IS NOT NULL
        AND FPA.M2_Submitted_Date IS NOT NULL
        """

        kinaM3query = """
        SELECT
        	M.ID as 'ID'
        ,	M.Name as 'Project Name'
        ,	FPA.M2_Submitted_Date as 'M2_Submitted_Date'
        ,	FPA.M3_Submitted_Date as 'M3_Submitted_Date'
        ,	YEAR(FPA.M3_Submitted_Date) as 'Year'
        ,	MONTH(FPA.M3_Submitted_Date) as 'Month'
        ,	DAY(FPA.M3_Submitted_Date) as 'Day'
        ,	DATEDIFF(FPA.M2_Submitted_Date, FPA.M3_Submitted_Date) as 'Days_M2_M3'
        ,	'Kinaole' as 'Fund'
        ,	'M2 - M3' as 'Milestone'
        ,	CASE
        	WHEN DATEDIFF(FPA.M2_Submitted_Date, FPA.M3_Submitted_Date) > -30 THEN 0
            WHEN DATEDIFF(FPA.M2_Submitted_Date, FPA.M3_Submitted_Date) > -60 THEN 1
            WHEN DATEDIFF(FPA.M2_Submitted_Date, FPA.M3_Submitted_Date) > -90 THEN 2
            WHEN DATEDIFF(FPA.M2_Submitted_Date, FPA.M3_Submitted_Date) > -120 THEN 3
            WHEN DATEDIFF(FPA.M2_Submitted_Date, FPA.M3_Submitted_Date) > -150 THEN 4
            WHEN DATEDIFF(FPA.M2_Submitted_Date, FPA.M3_Submitted_Date) > -180 THEN 5
            ELSE 6
            END as 'Months_M2_M3'

        FROM
        	salesforce_prod.Opportunity O
        		LEFT JOIN salesforce_prod.Lead Lead ON O.ID = lead.CONVERTEDOPPORTUNITYID
        			AND Lead.Name NOT LIKE '%%testsungevity%%'
        			AND Lead.Name NOT LIKE '%%sungevitytest%%'
        			AND lead.`STATUS` NOT LIKE 'Qualified Duplicate'
        		LEFT JOIN salesforce_prod.iQuote__c ON O.Id = iQuote__c.Opportunity__c
                LEFT JOIN salesforce_prod.Milestone1_Project__c M ON M.Id = iQuote__c.Project__c
                LEFT JOIN salesforce_prod.Tranche__c t ON (t.id = M.Tranche__c)
                LEFT JOIN salesforce_prod.Funding_Product__c FP ON (FP.Project__c = M.Id AND FP.Selected_Product__c = 1)
                -- LEFT JOIN Funding_Product_Attribute_column_view FPA ON FPA.Funding_Product__c = FP.Id
                LEFT JOIN salesforce_prod.Funding_Provider__c ON Funding_Provider__c.Id = FP.Funding_Provider__c
                LEFT JOIN salesforce_prod.Funding_Provider__c final ON final.Id = FP.FINAL_ASSET_OWNER__C
                LEFT JOIN salesforce_prod.jrs_project JRSP ON M.Id = JRSP.ProjectId
                LEFT JOIN salesforce_prod.jrs_funding_product_attribute FPA ON FP.Id = FPA.Funding_Product__c

        WHERE
        FP.name IN ('kinaole_lease','kinaole_ppa','sunfinco_lease','sunfinco_ppa')
        AND M.IS_TEST__C = 0
        AND t.Name LIKE 'Kinaole%%'
        AND M.STATUS__C <> 'Cancelled'
        AND FPA.M2_Submitted_Date IS NOT NULL
        AND FPA.M3_Submitted_Date IS NOT NULL
        """
        sr2M1query = """
        SELECT
        	M.ID as 'ID'
        ,	M.Name as 'Project Name'
        ,	M.SALE_CLOSED__C as 'Sale_Closed_Date'
        ,	FPA.M1_Submitted_Date as 'M1_Submitted_Date'
        ,	YEAR(FPA.M1_Submitted_Date) as 'Year'
        ,	MONTH(FPA.M1_Submitted_Date) as 'Month'
        ,	DAY(FPA.M1_Submitted_Date) as 'Day'
        ,	DATEDIFF(M.SALE_CLOSED__C, FPA.M1_Submitted_Date) as 'Days_to_M1'
        ,	'Sunrun 2' as 'Fund'
        ,	'Sale - M1' as 'Milestone'
        ,	CASE
        	WHEN DATEDIFF(M.SALE_CLOSED__C, FPA.M1_Submitted_Date) > -30 THEN 0
            WHEN DATEDIFF(M.SALE_CLOSED__C, FPA.M1_Submitted_Date) > -60 THEN 1
            WHEN DATEDIFF(M.SALE_CLOSED__C, FPA.M1_Submitted_Date) > -90 THEN 2
            WHEN DATEDIFF(M.SALE_CLOSED__C, FPA.M1_Submitted_Date) > -120 THEN 3
            WHEN DATEDIFF(M.SALE_CLOSED__C, FPA.M1_Submitted_Date) > -150 THEN 4
            WHEN DATEDIFF(M.SALE_CLOSED__C, FPA.M1_Submitted_Date) > -180 THEN 5
            ELSE 6
            END as 'Months_to_M1'

        FROM
        	salesforce_prod.Opportunity O
        		LEFT JOIN salesforce_prod.Lead Lead ON O.ID = lead.CONVERTEDOPPORTUNITYID
        			AND Lead.Name NOT LIKE '%%testsungevity%%'
        			AND Lead.Name NOT LIKE '%%sungevitytest%%'
        			AND lead.`STATUS` NOT LIKE 'Qualified Duplicate'
        		LEFT JOIN salesforce_prod.iQuote__c ON O.Id = iQuote__c.Opportunity__c
                LEFT JOIN salesforce_prod.Milestone1_Project__c M ON M.Id = iQuote__c.Project__c
                LEFT JOIN salesforce_prod.Tranche__c t ON (t.id = M.Tranche__c)
                LEFT JOIN salesforce_prod.Funding_Product__c FP ON (FP.Project__c = M.Id AND FP.Selected_Product__c = 1)
                -- LEFT JOIN Funding_Product_Attribute_column_view FPA ON FPA.Funding_Product__c = FP.Id
                LEFT JOIN salesforce_prod.Funding_Provider__c ON Funding_Provider__c.Id = FP.Funding_Provider__c
                LEFT JOIN salesforce_prod.Funding_Provider__c final ON final.Id = FP.FINAL_ASSET_OWNER__C
                LEFT JOIN salesforce_prod.jrs_project JRSP ON M.Id = JRSP.ProjectId
                LEFT JOIN salesforce_prod.jrs_funding_product_attribute FPA ON FP.Id = FPA.Funding_Product__c

        WHERE
        M.TRANCHE_ID__C IN ('P1','P2','P3','P4','P5','P6','P7','P8','P9','P10','P11','P12','P13','P14','P15','P16','P17','P18','P19','P20')
        AND M.IS_TEST__C = 0
        AND M.STATUS__C <> 'Cancelled'
        AND FPA.M1_Submitted_Date IS NOT NULL
        """

        sr2M2query = """
        SELECT
        	M.ID as 'ID'
        ,	M.Name as 'Project Name'
        ,	FPA.M1_Submitted_Date as 'M1_Submitted_Date'
        ,	FPA.M2_Submitted_Date as 'M2_Submitted_Date'
        ,	YEAR(FPA.M2_Submitted_Date) as 'Year'
        ,	MONTH(FPA.M2_Submitted_Date) as 'Month'
        ,	DAY(FPA.M2_Submitted_Date) as 'Day'
        ,	DATEDIFF(FPA.M1_Submitted_Date, FPA.M2_Submitted_Date) as 'Days_M1_M2'
        ,	'Sunrun 2' as 'Fund'
        ,	'M1 - M2' as 'Milestone'
        ,	CASE
        	WHEN DATEDIFF(FPA.M1_Submitted_Date, FPA.M2_Submitted_Date) > -30 THEN 0
            WHEN DATEDIFF(FPA.M1_Submitted_Date, FPA.M2_Submitted_Date) > -60 THEN 1
            WHEN DATEDIFF(FPA.M1_Submitted_Date, FPA.M2_Submitted_Date) > -90 THEN 2
            WHEN DATEDIFF(FPA.M1_Submitted_Date, FPA.M2_Submitted_Date) > -120 THEN 3
            WHEN DATEDIFF(FPA.M1_Submitted_Date, FPA.M2_Submitted_Date) > -150 THEN 4
            WHEN DATEDIFF(FPA.M1_Submitted_Date, FPA.M2_Submitted_Date) > -180 THEN 5
            ELSE 6
            END as 'Months_M1_M2'

        FROM
        	salesforce_prod.Opportunity O
        		LEFT JOIN salesforce_prod.Lead Lead ON O.ID = lead.CONVERTEDOPPORTUNITYID
        			AND Lead.Name NOT LIKE '%%testsungevity%%'
        			AND Lead.Name NOT LIKE '%%sungevitytest%%'
        			AND lead.`STATUS` NOT LIKE 'Qualified Duplicate'
        		LEFT JOIN salesforce_prod.iQuote__c ON O.Id = iQuote__c.Opportunity__c
                LEFT JOIN salesforce_prod.Milestone1_Project__c M ON M.Id = iQuote__c.Project__c
                LEFT JOIN salesforce_prod.Tranche__c t ON (t.id = M.Tranche__c)
                LEFT JOIN salesforce_prod.Funding_Product__c FP ON (FP.Project__c = M.Id AND FP.Selected_Product__c = 1)
                -- LEFT JOIN Funding_Product_Attribute_column_view FPA ON FPA.Funding_Product__c = FP.Id
                LEFT JOIN salesforce_prod.Funding_Provider__c ON Funding_Provider__c.Id = FP.Funding_Provider__c
                LEFT JOIN salesforce_prod.Funding_Provider__c final ON final.Id = FP.FINAL_ASSET_OWNER__C
                LEFT JOIN salesforce_prod.jrs_project JRSP ON M.Id = JRSP.ProjectId
                LEFT JOIN salesforce_prod.jrs_funding_product_attribute FPA ON FP.Id = FPA.Funding_Product__c

        WHERE
        M.TRANCHE_ID__C IN ('P1','P2','P3','P4','P5','P6','P7','P8','P9','P10','P11','P12','P13','P14','P15','P16','P17','P18','P19','P20')
        AND M.IS_TEST__C = 0
        AND M.STATUS__C <> 'Cancelled'
        AND FPA.M1_Submitted_Date IS NOT NULL
        AND FPA.M2_Submitted_Date IS NOT NULL
        """

        sr2M3query = """
        SELECT
        	M.ID as 'ID'
        ,	M.Name as 'Project Name'
        ,	FPA.M2_Submitted_Date as 'M2_Submitted_Date'
        ,	FPA.M3_Submitted_Date as 'M3_Submitted_Date'
        ,	YEAR(FPA.M3_Submitted_Date) as 'Year'
        ,	MONTH(FPA.M3_Submitted_Date) as 'Month'
        ,	DAY(FPA.M3_Submitted_Date) as 'Day'
        ,	DATEDIFF(FPA.M2_Submitted_Date, FPA.M3_Submitted_Date) as 'Days_M2_M3'
        ,	'Sunrun 2' as 'Fund'
        ,	'M2 - M3' as 'Milestone'
        ,	CASE
        	WHEN DATEDIFF(FPA.M2_Submitted_Date, FPA.M3_Submitted_Date) > -30 THEN 0
            WHEN DATEDIFF(FPA.M2_Submitted_Date, FPA.M3_Submitted_Date) > -60 THEN 1
            WHEN DATEDIFF(FPA.M2_Submitted_Date, FPA.M3_Submitted_Date) > -90 THEN 2
            WHEN DATEDIFF(FPA.M2_Submitted_Date, FPA.M3_Submitted_Date) > -120 THEN 3
            WHEN DATEDIFF(FPA.M2_Submitted_Date, FPA.M3_Submitted_Date) > -150 THEN 4
            WHEN DATEDIFF(FPA.M2_Submitted_Date, FPA.M3_Submitted_Date) > -180 THEN 5
            ELSE 6
            END as 'Months_M2_M3'

        FROM
        	salesforce_prod.Opportunity O
        		LEFT JOIN salesforce_prod.Lead Lead ON O.ID = lead.CONVERTEDOPPORTUNITYID
        			AND Lead.Name NOT LIKE '%%testsungevity%%'
        			AND Lead.Name NOT LIKE '%%sungevitytest%%'
        			AND lead.`STATUS` NOT LIKE 'Qualified Duplicate'
        		LEFT JOIN salesforce_prod.iQuote__c ON O.Id = iQuote__c.Opportunity__c
                LEFT JOIN salesforce_prod.Milestone1_Project__c M ON M.Id = iQuote__c.Project__c
                LEFT JOIN salesforce_prod.Tranche__c t ON (t.id = M.Tranche__c)
                LEFT JOIN salesforce_prod.Funding_Product__c FP ON (FP.Project__c = M.Id AND FP.Selected_Product__c = 1)
                -- LEFT JOIN Funding_Product_Attribute_column_view FPA ON FPA.Funding_Product__c = FP.Id
                LEFT JOIN salesforce_prod.Funding_Provider__c ON Funding_Provider__c.Id = FP.Funding_Provider__c
                LEFT JOIN salesforce_prod.Funding_Provider__c final ON final.Id = FP.FINAL_ASSET_OWNER__C
                LEFT JOIN salesforce_prod.jrs_project JRSP ON M.Id = JRSP.ProjectId
                LEFT JOIN salesforce_prod.jrs_funding_product_attribute FPA ON FP.Id = FPA.Funding_Product__c

        WHERE
        M.TRANCHE_ID__C IN ('P1','P2','P3','P4','P5','P6','P7','P8','P9','P10','P11','P12','P13','P14','P15','P16','P17','P18','P19','P20')
        AND M.IS_TEST__C = 0
        AND M.STATUS__C <> 'Cancelled'
        AND FPA.M2_Submitted_Date IS NOT NULL
        AND FPA.M3_Submitted_Date IS NOT NULL
        """
        purecashM1query = """
        SELECT
        	M.ID as 'ID'
        ,	M.Name as 'Project Name'
        ,	M.SALE_CLOSED__C as 'Sale_Closed_Date'
        ,	YEAR(M.SALE_CLOSED__C) as 'Year'
        ,	MONTH(M.SALE_CLOSED__C) as 'Month'
        ,	DAY(M.SALE_CLOSED__C) as 'Day'
        ,	M.SALE_CLOSED__C as 'M1_Submitted_Date'
        ,	DATEDIFF(M.SALE_CLOSED__C, M.SALE_CLOSED__C) as 'Days_to_M1'
        ,	'Pure Cash' as 'Fund'
        ,	'Sale - M1' as 'Milestone'
        ,	CASE
        	WHEN DATEDIFF(M.SALE_CLOSED__C, M.SALE_CLOSED__C) > -30 THEN 0
            WHEN DATEDIFF(M.SALE_CLOSED__C, M.SALE_CLOSED__C) > -60 THEN 1
            WHEN DATEDIFF(M.SALE_CLOSED__C, M.SALE_CLOSED__C) > -90 THEN 2
            WHEN DATEDIFF(M.SALE_CLOSED__C, M.SALE_CLOSED__C) > -120 THEN 3
            WHEN DATEDIFF(M.SALE_CLOSED__C, M.SALE_CLOSED__C) > -150 THEN 4
            WHEN DATEDIFF(M.SALE_CLOSED__C, M.SALE_CLOSED__C) > -180 THEN 5
            ELSE 6
            END as 'Months_to_M1'

        FROM
        	salesforce_prod.Opportunity O
        		LEFT JOIN salesforce_prod.Lead Lead ON O.ID = lead.CONVERTEDOPPORTUNITYID
        			AND Lead.Name NOT LIKE '%%testsungevity%%'
        			AND Lead.Name NOT LIKE '%%sungevitytest%%'
        			AND lead.`STATUS` NOT LIKE 'Qualified Duplicate'
        		LEFT JOIN salesforce_prod.iQuote__c ON O.Id = iQuote__c.Opportunity__c
        		LEFT JOIN salesforce_prod.Account a ON iQuote__c.Account__c = a.Id
                LEFT JOIN salesforce_prod.Milestone1_Project__c M ON M.Id = iQuote__c.Project__c
                LEFT JOIN salesforce_prod.Tranche__c t ON M.Tranche__c = t.Id
                LEFT JOIN salesforce_prod.Funding_Product__c FP ON FP.Project__c = M.Id AND FP.Selected_Product__c = 1
                LEFT JOIN salesforce_prod.Funding_Product_Attribute_column_view FPA ON FPA.Funding_Product__c = FP.Id
                LEFT JOIN salesforce_prod.Funding_Provider__c ON Funding_Provider__c.Id = FP.Funding_Provider__c
                LEFT JOIN salesforce_prod.Funding_Provider__c final ON final.Id = FP.FINAL_ASSET_OWNER__C
                LEFT JOIN salesforce_prod.jrs_project JRSP ON M.Id = JRSP.ProjectId
                LEFT JOIN salesforce_prod.jrs_funding_product_attribute JRSFPA ON FP.Id = JRSFPA.Funding_Product__c
        		LEFT JOIN salesforce_prod.loan_product__c LProd ON iQuote__c.ID = LProd.IQUOTE__C AND LProd.PRIMARY_PRODUCT__C = 1 AND LProd.ACTIVE__C = 1
        		LEFT JOIN salesforce_prod.jrs_loan_product_attribute JRSLPA ON LProd.ID = JRSLPA.Loan_Product_Id
        		LEFT JOIN salesforce_prod.loan_provider__c LProv ON LProd.LOAN_PROVIDER__C = LProv.ID

        WHERE
        LProv.Name IN ('HERO','EFS','Admiral','CAL First')
        AND M.IS_TEST__C = 0
        AND M.STATUS__C <> 'Cancelled'
        AND M.SALE_CLOSED__C IS NOT NULL
        """

        purecashM2query = """
        SELECT
        	M.ID as 'ID'
        ,	M.Name as 'Project Name'
        ,	YEAR( M.PERMIT_APPROVED_DATE__C) as 'Year'
        ,	MONTH( M.PERMIT_APPROVED_DATE__C) as 'Month'
        ,	DAY( M.PERMIT_APPROVED_DATE__C) as 'Day'
        ,	M.SALE_CLOSED__C as 'M1_Submitted_Date'
        ,	 M.PERMIT_APPROVED_DATE__C as 'M2_Submitted_Date'
        ,	DATEDIFF(M.SALE_CLOSED__C, M.PERMIT_APPROVED_DATE__C) as 'Days_M1_M2'
        ,	'Pure Cash' as 'Fund'
        ,	'M1 - M2' as 'Milestone'
        ,	CASE
        	WHEN DATEDIFF(M.SALE_CLOSED__C, M.PERMIT_APPROVED_DATE__C) > -30 THEN 0
            WHEN DATEDIFF(M.SALE_CLOSED__C, M.PERMIT_APPROVED_DATE__C) > -60 THEN 1
            WHEN DATEDIFF(M.SALE_CLOSED__C, M.PERMIT_APPROVED_DATE__C) > -90 THEN 2
            WHEN DATEDIFF(M.SALE_CLOSED__C, M.PERMIT_APPROVED_DATE__C) > -120 THEN 3
            WHEN DATEDIFF(M.SALE_CLOSED__C, M.PERMIT_APPROVED_DATE__C) > -150 THEN 4
            WHEN DATEDIFF(M.SALE_CLOSED__C, M.PERMIT_APPROVED_DATE__C) > -180 THEN 5
            ELSE 6
            END as 'Months_M1_M2'

        FROM
        	salesforce_prod.Opportunity O
        		LEFT JOIN salesforce_prod.Lead Lead ON O.ID = lead.CONVERTEDOPPORTUNITYID
        			AND Lead.Name NOT LIKE '%%testsungevity%%'
        			AND Lead.Name NOT LIKE '%%sungevitytest%%'
        			AND lead.`STATUS` NOT LIKE 'Qualified Duplicate'
        		LEFT JOIN salesforce_prod.iQuote__c ON O.Id = iQuote__c.Opportunity__c
        		LEFT JOIN salesforce_prod.Account a ON iQuote__c.Account__c = a.Id
                LEFT JOIN salesforce_prod.Milestone1_Project__c M ON M.Id = iQuote__c.Project__c
                LEFT JOIN salesforce_prod.Tranche__c t ON M.Tranche__c = t.Id
                LEFT JOIN salesforce_prod.Funding_Product__c FP ON FP.Project__c = M.Id AND FP.Selected_Product__c = 1
                LEFT JOIN salesforce_prod.Funding_Product_Attribute_column_view FPA ON FPA.Funding_Product__c = FP.Id
                LEFT JOIN salesforce_prod.Funding_Provider__c ON Funding_Provider__c.Id = FP.Funding_Provider__c
                LEFT JOIN salesforce_prod.Funding_Provider__c final ON final.Id = FP.FINAL_ASSET_OWNER__C
                LEFT JOIN salesforce_prod.jrs_project JRSP ON M.Id = JRSP.ProjectId
                LEFT JOIN salesforce_prod.jrs_funding_product_attribute JRSFPA ON FP.Id = JRSFPA.Funding_Product__c
        		LEFT JOIN salesforce_prod.loan_product__c LProd ON iQuote__c.ID = LProd.IQUOTE__C AND LProd.PRIMARY_PRODUCT__C = 1 AND LProd.ACTIVE__C = 1
        		LEFT JOIN salesforce_prod.jrs_loan_product_attribute JRSLPA ON LProd.ID = JRSLPA.Loan_Product_Id
        		LEFT JOIN salesforce_prod.loan_provider__c LProv ON LProd.LOAN_PROVIDER__C = LProv.ID

        WHERE
        LProv.Name IN ('HERO','EFS','Admiral','CAL First')
        AND M.IS_TEST__C = 0
        AND M.STATUS__C <> 'Cancelled'
        AND M.PERMIT_APPROVED_DATE__C IS NOT NULL
        """

        purecashM3query = """
        SELECT
        	M.ID as 'ID'
        ,	M.Name as 'Project Name'
        ,	YEAR(M.INSTALLATION_COMPLETE_DATE__C) as 'Year'
        ,	MONTH(M.INSTALLATION_COMPLETE_DATE__C) as 'Month'
        ,	DAY(M.INSTALLATION_COMPLETE_DATE__C) as 'Day'
        ,	M.PERMIT_APPROVED_DATE__C as 'M2_Submitted_Date'
        ,	M.INSTALLATION_COMPLETE_DATE__C as 'M3_Submitted_Date'
        ,	DATEDIFF(M.PERMIT_APPROVED_DATE__C,M.INSTALLATION_COMPLETE_DATE__C) as 'Days_M2_M3'
        ,	'Pure Cash' as 'Fund'
        ,	'M2 - M3' as 'Milestone'
        ,	CASE
        	WHEN DATEDIFF(M.PERMIT_APPROVED_DATE__C,M.INSTALLATION_COMPLETE_DATE__C) > -30 THEN 0
            WHEN DATEDIFF(M.PERMIT_APPROVED_DATE__C,M.INSTALLATION_COMPLETE_DATE__C) > -60 THEN 1
            WHEN DATEDIFF(M.PERMIT_APPROVED_DATE__C,M.INSTALLATION_COMPLETE_DATE__C) > -90 THEN 2
            WHEN DATEDIFF(M.PERMIT_APPROVED_DATE__C,M.INSTALLATION_COMPLETE_DATE__C) > -120 THEN 3
            WHEN DATEDIFF(M.PERMIT_APPROVED_DATE__C,M.INSTALLATION_COMPLETE_DATE__C) > -150 THEN 4
            WHEN DATEDIFF(M.PERMIT_APPROVED_DATE__C,M.INSTALLATION_COMPLETE_DATE__C) > -180 THEN 5
            ELSE 6
            END as 'Months_M2_M3'

        FROM
        	salesforce_prod.Opportunity O
        		LEFT JOIN salesforce_prod.Lead Lead ON O.ID = lead.CONVERTEDOPPORTUNITYID
        			AND Lead.Name NOT LIKE '%%testsungevity%%'
        			AND Lead.Name NOT LIKE '%%sungevitytest%%'
        			AND lead.`STATUS` NOT LIKE 'Qualified Duplicate'
        		LEFT JOIN salesforce_prod.iQuote__c ON O.Id = iQuote__c.Opportunity__c
        		LEFT JOIN salesforce_prod.Account a ON iQuote__c.Account__c = a.Id
                LEFT JOIN salesforce_prod.Milestone1_Project__c M ON M.Id = iQuote__c.Project__c
                LEFT JOIN salesforce_prod.Tranche__c t ON M.Tranche__c = t.Id
                LEFT JOIN salesforce_prod.Funding_Product__c FP ON FP.Project__c = M.Id AND FP.Selected_Product__c = 1
                LEFT JOIN salesforce_prod.Funding_Product_Attribute_column_view FPA ON FPA.Funding_Product__c = FP.Id
                LEFT JOIN salesforce_prod.Funding_Provider__c ON Funding_Provider__c.Id = FP.Funding_Provider__c
                LEFT JOIN salesforce_prod.Funding_Provider__c final ON final.Id = FP.FINAL_ASSET_OWNER__C
                LEFT JOIN salesforce_prod.jrs_project JRSP ON M.Id = JRSP.ProjectId
                LEFT JOIN salesforce_prod.jrs_funding_product_attribute JRSFPA ON FP.Id = JRSFPA.Funding_Product__c
        		LEFT JOIN salesforce_prod.loan_product__c LProd ON iQuote__c.ID = LProd.IQUOTE__C AND LProd.PRIMARY_PRODUCT__C = 1 AND LProd.ACTIVE__C = 1
        		LEFT JOIN salesforce_prod.jrs_loan_product_attribute JRSLPA ON LProd.ID = JRSLPA.Loan_Product_Id
        		LEFT JOIN salesforce_prod.loan_provider__c LProv ON LProd.LOAN_PROVIDER__C = LProv.ID

        WHERE
        LProv.Name IN ('HERO','EFS','Admiral','CAL First')
        AND M.IS_TEST__C = 0
        AND M.STATUS__C <> 'Cancelled'
        AND M.PERMIT_APPROVED_DATE__C IS NOT NULL
        AND M.INSTALLATION_COMPLETE_DATE__C IS NOT NULL
        AND M.INSTALLATION_COMPLETE_DATE_STATUS__C = 'Actual'
        """

        mosaicM1query = """
        SELECT
        	M.ID as 'ID'
        ,	M.Name as 'Project Name'
        ,	M.SALE_CLOSED__C as 'Sale_Closed_Date'
        ,	YEAR(JRSLPA.F1_Submitted_Date) as 'Year'
        ,	MONTH(JRSLPA.F1_Submitted_Date) as 'Month'
        ,	DAY(JRSLPA.F1_Submitted_Date) as 'Day'
        ,	JRSLPA.F1_Submitted_Date as 'M1_Submitted_Date'
        ,	DATEDIFF(M.SALE_CLOSED__C, JRSLPA.F1_Submitted_Date) as 'Days_to_M1'
        ,	'Mosaic' as 'Fund'
        ,	'Sale - M1' as 'Milestone'
        ,	CASE
        	WHEN DATEDIFF(M.SALE_CLOSED__C, JRSLPA.F1_Submitted_Date) > -30 THEN 0
            WHEN DATEDIFF(M.SALE_CLOSED__C, JRSLPA.F1_Submitted_Date) > -60 THEN 1
            WHEN DATEDIFF(M.SALE_CLOSED__C, JRSLPA.F1_Submitted_Date) > -90 THEN 2
            WHEN DATEDIFF(M.SALE_CLOSED__C, JRSLPA.F1_Submitted_Date) > -120 THEN 3
            WHEN DATEDIFF(M.SALE_CLOSED__C, JRSLPA.F1_Submitted_Date) > -150 THEN 4
            WHEN DATEDIFF(M.SALE_CLOSED__C, JRSLPA.F1_Submitted_Date) > -180 THEN 5
            ELSE 6
            END as 'Months_to_M1'

        FROM
        	salesforce_prod.Opportunity O
        		LEFT JOIN salesforce_prod.Lead Lead ON O.ID = lead.CONVERTEDOPPORTUNITYID
        			AND Lead.Name NOT LIKE '%%testsungevity%%'
        			AND Lead.Name NOT LIKE '%%sungevitytest%%'
        			AND lead.`STATUS` NOT LIKE 'Qualified Duplicate'
        		LEFT JOIN salesforce_prod.iQuote__c ON O.Id = iQuote__c.Opportunity__c
        		LEFT JOIN salesforce_prod.Account a ON iQuote__c.Account__c = a.Id
                LEFT JOIN salesforce_prod.Milestone1_Project__c M ON M.Id = iQuote__c.Project__c
                LEFT JOIN salesforce_prod.Tranche__c t ON M.Tranche__c = t.Id
                LEFT JOIN salesforce_prod.Funding_Product__c FP ON FP.Project__c = M.Id AND FP.Selected_Product__c = 1
                LEFT JOIN salesforce_prod.Funding_Product_Attribute_column_view FPA ON FPA.Funding_Product__c = FP.Id
                LEFT JOIN salesforce_prod.Funding_Provider__c ON Funding_Provider__c.Id = FP.Funding_Provider__c
                LEFT JOIN salesforce_prod.Funding_Provider__c final ON final.Id = FP.FINAL_ASSET_OWNER__C
                LEFT JOIN salesforce_prod.jrs_project JRSP ON M.Id = JRSP.ProjectId
                LEFT JOIN salesforce_prod.jrs_funding_product_attribute JRSFPA ON FP.Id = JRSFPA.Funding_Product__c
        		LEFT JOIN salesforce_prod.loan_product__c LProd ON iQuote__c.ID = LProd.IQUOTE__C AND LProd.PRIMARY_PRODUCT__C = 1 AND LProd.ACTIVE__C = 1
        		LEFT JOIN salesforce_prod.jrs_loan_product_attribute JRSLPA ON LProd.ID = JRSLPA.Loan_Product_Id
        		LEFT JOIN salesforce_prod.loan_provider__c LProv ON LProd.LOAN_PROVIDER__C = LProv.ID

        WHERE
        LProv.Name = 'Mosaic'
        AND M.IS_TEST__C = 0
        AND M.STATUS__C <> 'Cancelled'
        AND JRSLPA.F1_Submitted_Date IS NOT NULL
        """

        mosaicM2query = """
        SELECT
        	M.ID as 'ID'
        ,	M.Name as 'Project Name'
        ,	YEAR(JRSLPA.F2_Submitted_Date) as 'Year'
        ,	MONTH(JRSLPA.F2_Submitted_Date) as 'Month'
        ,	DAY(JRSLPA.F2_Submitted_Date) as 'Day'
        ,	JRSLPA.F1_Submitted_Date as 'M1_Submitted_Date'
        ,	JRSLPA.F2_Submitted_Date as 'M2_Submitted_Date'
        ,	DATEDIFF(JRSLPA.F1_Submitted_Date,JRSLPA.F2_Submitted_Date) as 'Days_M1_M2'
        ,	'Mosaic' as 'Fund'
        ,	'M1 - M2' as 'Milestone'
        ,	CASE
        	WHEN DATEDIFF(JRSLPA.F1_Submitted_Date,JRSLPA.F2_Submitted_Date) > -30 THEN 0
            WHEN DATEDIFF(JRSLPA.F1_Submitted_Date,JRSLPA.F2_Submitted_Date) > -60 THEN 1
            WHEN DATEDIFF(JRSLPA.F1_Submitted_Date,JRSLPA.F2_Submitted_Date) > -90 THEN 2
            WHEN DATEDIFF(JRSLPA.F1_Submitted_Date,JRSLPA.F2_Submitted_Date) > -120 THEN 3
            WHEN DATEDIFF(JRSLPA.F1_Submitted_Date,JRSLPA.F2_Submitted_Date) > -150 THEN 4
            WHEN DATEDIFF(JRSLPA.F1_Submitted_Date,JRSLPA.F2_Submitted_Date) > -180 THEN 5
            ELSE 6
            END as 'Months_M1_M2'

        FROM
        	salesforce_prod.Opportunity O
        		LEFT JOIN salesforce_prod.Lead Lead ON O.ID = lead.CONVERTEDOPPORTUNITYID
        			AND Lead.Name NOT LIKE '%%testsungevity%%'
        			AND Lead.Name NOT LIKE '%%sungevitytest%%'
        			AND lead.`STATUS` NOT LIKE 'Qualified Duplicate'
        		LEFT JOIN salesforce_prod.iQuote__c ON O.Id = iQuote__c.Opportunity__c
        		LEFT JOIN salesforce_prod.Account a ON iQuote__c.Account__c = a.Id
                LEFT JOIN salesforce_prod.Milestone1_Project__c M ON M.Id = iQuote__c.Project__c
                LEFT JOIN salesforce_prod.Tranche__c t ON M.Tranche__c = t.Id
                LEFT JOIN salesforce_prod.Funding_Product__c FP ON FP.Project__c = M.Id AND FP.Selected_Product__c = 1
                LEFT JOIN salesforce_prod.Funding_Product_Attribute_column_view FPA ON FPA.Funding_Product__c = FP.Id
                LEFT JOIN salesforce_prod.Funding_Provider__c ON Funding_Provider__c.Id = FP.Funding_Provider__c
                LEFT JOIN salesforce_prod.Funding_Provider__c final ON final.Id = FP.FINAL_ASSET_OWNER__C
                LEFT JOIN salesforce_prod.jrs_project JRSP ON M.Id = JRSP.ProjectId
                LEFT JOIN salesforce_prod.jrs_funding_product_attribute JRSFPA ON FP.Id = JRSFPA.Funding_Product__c
        		LEFT JOIN salesforce_prod.loan_product__c LProd ON iQuote__c.ID = LProd.IQUOTE__C AND LProd.PRIMARY_PRODUCT__C = 1 AND LProd.ACTIVE__C = 1
        		LEFT JOIN salesforce_prod.jrs_loan_product_attribute JRSLPA ON LProd.ID = JRSLPA.Loan_Product_Id
        		LEFT JOIN salesforce_prod.loan_provider__c LProv ON LProd.LOAN_PROVIDER__C = LProv.ID

        WHERE
        LProv.Name = 'Mosaic'
        AND M.IS_TEST__C = 0
        AND M.STATUS__C <> 'Cancelled'
        AND JRSLPA.F1_Submitted_Date IS NOT NULL
        AND JRSLPA.F2_Submitted_Date IS NOT NULL
        """

        mosaicM3query = """
        SELECT
        	M.ID as 'ID'
        ,	M.Name as 'Project Name'
        ,	YEAR(JRSLPA.F3_Submitted_Date) as 'Year'
        ,	MONTH(JRSLPA.F3_Submitted_Date) as 'Month'
        ,	DAY(JRSLPA.F3_Submitted_Date) as 'Day'
        ,	JRSLPA.F2_Submitted_Date as 'M2_Submitted_Date'
        ,	JRSLPA.F3_Submitted_Date as 'M3_Submitted_Date'
        ,	DATEDIFF(JRSLPA.F2_Submitted_Date,JRSLPA.F3_Submitted_Date) as 'Days_M2_M3'
        ,	'Mosaic' as 'Fund'
        ,	'M2 - M3' as 'Milestone'
        ,	CASE
        	WHEN DATEDIFF(JRSLPA.F2_Submitted_Date,JRSLPA.F3_Submitted_Date) > -30 THEN 0
            WHEN DATEDIFF(JRSLPA.F2_Submitted_Date,JRSLPA.F3_Submitted_Date) > -60 THEN 1
            WHEN DATEDIFF(JRSLPA.F2_Submitted_Date,JRSLPA.F3_Submitted_Date) > -90 THEN 2
            WHEN DATEDIFF(JRSLPA.F2_Submitted_Date,JRSLPA.F3_Submitted_Date) > -120 THEN 3
            WHEN DATEDIFF(JRSLPA.F2_Submitted_Date,JRSLPA.F3_Submitted_Date) > -150 THEN 4
            WHEN DATEDIFF(JRSLPA.F2_Submitted_Date,JRSLPA.F3_Submitted_Date) > -180 THEN 5
            ELSE 6
            END as 'Months_M2_M3'

        FROM
        	salesforce_prod.Opportunity O
        		LEFT JOIN salesforce_prod.Lead Lead ON O.ID = lead.CONVERTEDOPPORTUNITYID
        			AND Lead.Name NOT LIKE '%%testsungevity%%'
        			AND Lead.Name NOT LIKE '%%sungevitytest%%'
        			AND lead.`STATUS` NOT LIKE 'Qualified Duplicate'
        		LEFT JOIN salesforce_prod.iQuote__c ON O.Id = iQuote__c.Opportunity__c
        		LEFT JOIN salesforce_prod.Account a ON iQuote__c.Account__c = a.Id
                LEFT JOIN salesforce_prod.Milestone1_Project__c M ON M.Id = iQuote__c.Project__c
                LEFT JOIN salesforce_prod.Tranche__c t ON M.Tranche__c = t.Id
                LEFT JOIN salesforce_prod.Funding_Product__c FP ON FP.Project__c = M.Id AND FP.Selected_Product__c = 1
                LEFT JOIN salesforce_prod.Funding_Product_Attribute_column_view FPA ON FPA.Funding_Product__c = FP.Id
                LEFT JOIN salesforce_prod.Funding_Provider__c ON Funding_Provider__c.Id = FP.Funding_Provider__c
                LEFT JOIN salesforce_prod.Funding_Provider__c final ON final.Id = FP.FINAL_ASSET_OWNER__C
                LEFT JOIN salesforce_prod.jrs_project JRSP ON M.Id = JRSP.ProjectId
                LEFT JOIN salesforce_prod.jrs_funding_product_attribute JRSFPA ON FP.Id = JRSFPA.Funding_Product__c
        		LEFT JOIN salesforce_prod.loan_product__c LProd ON iQuote__c.ID = LProd.IQUOTE__C AND LProd.PRIMARY_PRODUCT__C = 1 AND LProd.ACTIVE__C = 1
        		LEFT JOIN salesforce_prod.jrs_loan_product_attribute JRSLPA ON LProd.ID = JRSLPA.Loan_Product_Id
        		LEFT JOIN salesforce_prod.loan_provider__c LProv ON LProd.LOAN_PROVIDER__C = LProv.ID

        WHERE
        LProv.Name = 'Mosaic'
        AND M.IS_TEST__C = 0
        AND M.STATUS__C <> 'Cancelled'
        AND JRSLPA.F2_Submitted_Date IS NOT NULL
        AND JRSLPA.F3_Submitted_Date IS NOT NULL
        """


        sr2M1df = pd.read_sql_query(sr2M1query,conn)
        sr2M1df['Week'] = 1

        for i in range(len(sr2M1df.index)):
            if sr2M1df.loc[i, 'Day'] <= 7:
                sr2M1df.loc[i, 'Week'] = 1
            elif sr2M1df.loc[i,'Day'] <= 14 and sr2M1df.loc[i, 'Day'] > 7:
                sr2M1df.loc[i, 'Week'] = 2
            elif sr2M1df.loc[i,'Day'] <= 21 and sr2M1df.loc[i, 'Day'] > 14:
                sr2M1df.loc[i, 'Week'] = 3
            elif sr2M1df.loc[i,'Day'] <= 28 and sr2M1df.loc[i, 'Day'] > 21:
                sr2M1df.loc[i, 'Week'] = 4
            else:
                sr2M1df.loc[i, 'Week'] = 4

        sr2M1df['Months_Week'] = sr2M1df.apply(lambda x: "{0} {1}".format(x['Months_to_M1'], x['Week']), axis = 1)
        sr2M1df['Date'] = sr2M1df.apply(lambda x:datetime.strptime("{0} {1}".format(x['Month'],x['Year']), "%m %Y"), axis = 1)
        sr2M1df = pd.pivot_table(sr2M1df, index = ['Milestone','Fund','Date'], values = ['Project Name'], columns = ['Months_Week'], aggfunc = np.count_nonzero, fill_value = 0, margins = True)
        sr2M1df = sr2M1df.div(sr2M1df.iloc[:,-1], axis = 0)
        sr2M1df = sr2M1df['Project Name']
        sr2M1df = sr2M1df.reset_index()
        sr2M1df.drop(sr2M1df.index[len(sr2M1df)-1])
        sr2M1df.drop('All',axis =1)


        sr2M2df = pd.read_sql_query(sr2M2query,conn)
        sr2M2df['Week'] = 1

        for i in range(len(sr2M2df.index)):
            if sr2M2df.loc[i, 'Day'] <= 7:
                sr2M2df.loc[i, 'Week'] = 1
            elif sr2M2df.loc[i,'Day'] <= 14 and sr2M2df.loc[i, 'Day'] > 7:
                sr2M2df.loc[i, 'Week'] = 2
            elif sr2M2df.loc[i,'Day'] <= 21 and sr2M2df.loc[i, 'Day'] > 14:
                sr2M2df.loc[i, 'Week'] = 3
            elif sr2M2df.loc[i,'Day'] <= 28 and sr2M2df.loc[i, 'Day'] > 21:
                sr2M2df.loc[i, 'Week'] = 4
            else:
                sr2M2df.loc[i, 'Week'] = 4

        sr2M2df['Months_Week'] = sr2M2df.apply(lambda x: "{0} {1}".format(x['Months_M1_M2'], x['Week']), axis = 1)
        sr2M2df['Date'] = sr2M2df.apply(lambda x:datetime.strptime("{0} {1}".format(x['Month'],x['Year']), "%m %Y"), axis = 1)
        sr2M2df = pd.pivot_table(sr2M2df, index = ['Milestone','Fund','Date'], values = ['Project Name'], columns = ['Months_Week'], aggfunc = np.count_nonzero, fill_value = 0, margins = True)
        sr2M2df = sr2M2df.div(sr2M2df.iloc[:,-1], axis = 0)
        sr2M2df = sr2M2df['Project Name']
        sr2M2df = sr2M2df.reset_index()
        sr2M2df.drop(sr2M2df.index[len(sr2M2df)-1])
        sr2M2df.drop('All',axis =1)


        sr2M3df = pd.read_sql_query(sr2M3query,conn)
        sr2M3df['Week'] = 1

        for i in range(len(sr2M3df.index)):
            if sr2M3df.loc[i, 'Day'] <= 7:
                sr2M3df.loc[i, 'Week'] = 1
            elif sr2M3df.loc[i,'Day'] <= 14 and sr2M3df.loc[i, 'Day'] > 7:
                sr2M3df.loc[i, 'Week'] = 2
            elif sr2M3df.loc[i,'Day'] <= 21 and sr2M3df.loc[i, 'Day'] > 14:
                sr2M3df.loc[i, 'Week'] = 3
            elif sr2M3df.loc[i,'Day'] <= 28 and sr2M3df.loc[i, 'Day'] > 21:
                sr2M3df.loc[i, 'Week'] = 4
            else:
                sr2M3df.loc[i, 'Week'] = 4

        sr2M3df['Months_Week'] = sr2M3df.apply(lambda x: "{0} {1}".format(x['Months_M2_M3'], x['Week']), axis = 1)
        sr2M3df['Date'] = sr2M3df.apply(lambda x:datetime.strptime("{0} {1}".format(x['Month'],x['Year']), "%m %Y"), axis = 1)
        sr2M3df = pd.pivot_table(sr2M3df, index = ['Milestone','Fund','Date'], values = ['Project Name'], columns = ['Months_Week'], aggfunc = np.count_nonzero, fill_value = 0, margins = True)
        sr2M3df = sr2M3df.div(sr2M3df.iloc[:,-1], axis = 0)
        sr2M3df = sr2M3df['Project Name']
        sr2M3df = sr2M3df.reset_index()
        sr2M3df.drop(sr2M3df.index[len(sr2M3df)-1])
        sr2M3df.drop('All',axis =1)


        kinaM1df = pd.read_sql_query(kinaM1query,conn)
        kinaM1df['Week'] = 1

        for i in range(len(kinaM1df.index)):
            if kinaM1df.loc[i, 'Day'] <= 7:
                kinaM1df.loc[i, 'Week'] = 1
            elif kinaM1df.loc[i,'Day'] <= 14 and kinaM1df.loc[i, 'Day'] > 7:
                kinaM1df.loc[i, 'Week'] = 2
            elif kinaM1df.loc[i,'Day'] <= 21 and kinaM1df.loc[i, 'Day'] > 14:
                kinaM1df.loc[i, 'Week'] = 3
            elif kinaM1df.loc[i,'Day'] <= 28 and kinaM1df.loc[i, 'Day'] > 21:
                kinaM1df.loc[i, 'Week'] = 4
            else:
                kinaM1df.loc[i, 'Week'] = 4

        kinaM1df['Months_Week'] = kinaM1df.apply(lambda x: "{0} {1}".format(x['Months_to_M1'], x['Week']), axis = 1)
        kinaM1df['Date'] = kinaM1df.apply(lambda x:datetime.strptime("{0} {1}".format(x['Month'],x['Year']), "%m %Y"), axis = 1)
        kinaM1df = pd.pivot_table(kinaM1df, index = ['Milestone','Fund','Date'], values = ['Project Name'], columns = ['Months_Week'], aggfunc = np.count_nonzero, fill_value = 0, margins = True)
        kinaM1df = kinaM1df.div(kinaM1df.iloc[:,-1], axis = 0)
        kinaM1df = kinaM1df['Project Name']
        kinaM1df = kinaM1df.reset_index()
        kinaM1df.drop(kinaM1df.index[len(kinaM1df)-1])
        kinaM1df.drop('All',axis =1)


        kinaM2df = pd.read_sql_query(kinaM2query,conn)
        kinaM2df['Week'] = 1

        for i in range(len(kinaM2df.index)):
            if kinaM2df.loc[i, 'Day'] <= 7:
                kinaM2df.loc[i, 'Week'] = 1
            elif kinaM2df.loc[i,'Day'] <= 14 and kinaM2df.loc[i, 'Day'] > 7:
                kinaM2df.loc[i, 'Week'] = 2
            elif kinaM2df.loc[i,'Day'] <= 21 and kinaM2df.loc[i, 'Day'] > 14:
                kinaM2df.loc[i, 'Week'] = 3
            elif kinaM2df.loc[i,'Day'] <= 28 and kinaM2df.loc[i, 'Day'] > 21:
                kinaM2df.loc[i, 'Week'] = 4
            else:
                kinaM2df.loc[i, 'Week'] = 4

        kinaM2df['Months_Week'] = kinaM2df.apply(lambda x: "{0} {1}".format(x['Months_M1_M2'], x['Week']), axis = 1)
        kinaM2df['Date'] = kinaM2df.apply(lambda x:datetime.strptime("{0} {1}".format(x['Month'],x['Year']), "%m %Y"), axis = 1)
        kinaM2df = pd.pivot_table(kinaM2df, index = ['Milestone','Fund','Date'], values = ['Project Name'], columns = ['Months_Week'], aggfunc = np.count_nonzero, fill_value = 0, margins = True)
        kinaM2df = kinaM2df.div(kinaM2df.iloc[:,-1], axis = 0)
        kinaM2df = kinaM2df['Project Name']
        kinaM2df = kinaM2df.reset_index()
        kinaM2df.drop(kinaM2df.index[len(kinaM2df)-1])
        kinaM2df.drop('All',axis =1)



        kinaM3df = pd.read_sql_query(kinaM3query,conn)
        kinaM3df['Week'] = 1

        for i in range(len(kinaM3df.index)):
            if kinaM3df.loc[i, 'Day'] <= 7:
                kinaM3df.loc[i, 'Week'] = 1
            elif kinaM3df.loc[i,'Day'] <= 14 and kinaM3df.loc[i, 'Day'] > 7:
                kinaM3df.loc[i, 'Week'] = 2
            elif kinaM3df.loc[i,'Day'] <= 21 and kinaM3df.loc[i, 'Day'] > 14:
                kinaM3df.loc[i, 'Week'] = 3
            elif kinaM3df.loc[i,'Day'] <= 28 and kinaM3df.loc[i, 'Day'] > 21:
                kinaM3df.loc[i, 'Week'] = 4
            else:
                kinaM3df.loc[i, 'Week'] = 4

        kinaM3df['Months_Week'] = kinaM3df.apply(lambda x: "{0} {1}".format(x['Months_M2_M3'], x['Week']), axis = 1)
        kinaM3df['Date'] = kinaM3df.apply(lambda x:datetime.strptime("{0} {1}".format(x['Month'],x['Year']), "%m %Y"), axis = 1)
        kinaM3df = pd.pivot_table(kinaM3df, index = ['Milestone','Fund','Date'], values = ['Project Name'], columns = ['Months_Week'], aggfunc = np.count_nonzero, fill_value = 0, margins = True)
        kinaM3df = kinaM3df.div(kinaM3df.iloc[:,-1], axis = 0)
        kinaM3df = kinaM3df['Project Name']
        kinaM3df = kinaM3df.reset_index()
        kinaM3df.drop(kinaM3df.index[len(kinaM3df)-1])
        kinaM3df.drop('All',axis =1)



        mosaicM1df = pd.read_sql_query(mosaicM1query,conn)
        mosaicM1df['Week'] = 1

        for i in range(len(mosaicM1df.index)):
            if mosaicM1df.loc[i, 'Day'] <= 7:
                mosaicM1df.loc[i, 'Week'] = 1
            elif mosaicM1df.loc[i,'Day'] <= 14 and mosaicM1df.loc[i, 'Day'] > 7:
                mosaicM1df.loc[i, 'Week'] = 2
            elif mosaicM1df.loc[i,'Day'] <= 21 and mosaicM1df.loc[i, 'Day'] > 14:
                mosaicM1df.loc[i, 'Week'] = 3
            elif mosaicM1df.loc[i,'Day'] <= 28 and mosaicM1df.loc[i, 'Day'] > 21:
                mosaicM1df.loc[i, 'Week'] = 4
            else:
                mosaicM1df.loc[i, 'Week'] = 4

        mosaicM1df['Months_Week'] = mosaicM1df.apply(lambda x: "{0} {1}".format(x['Months_to_M1'], x['Week']), axis = 1)
        mosaicM1df['Date'] = mosaicM1df.apply(lambda x:datetime.strptime("{0} {1}".format(x['Month'],x['Year']), "%m %Y"), axis = 1)
        mosaicM1df = pd.pivot_table(mosaicM1df, index = ['Milestone','Fund','Date'], values = ['Project Name'], columns = ['Months_Week'], aggfunc = np.count_nonzero, fill_value = 0, margins = True)
        mosaicM1df = mosaicM1df.div(mosaicM1df.iloc[:,-1], axis = 0)
        mosaicM1df = mosaicM1df['Project Name']
        mosaicM1df = mosaicM1df.reset_index()
        mosaicM1df.drop(mosaicM1df.index[len(mosaicM1df)-1])
        mosaicM1df.drop('All',axis =1)



        mosaicM2df = pd.read_sql_query(mosaicM2query,conn)
        mosaicM2df['Week'] = 1

        for i in range(len(mosaicM2df.index)):
            if mosaicM2df.loc[i, 'Day'] <= 7:
                mosaicM2df.loc[i, 'Week'] = 1
            elif mosaicM2df.loc[i,'Day'] <= 14 and mosaicM2df.loc[i, 'Day'] > 7:
                mosaicM2df.loc[i, 'Week'] = 2
            elif mosaicM2df.loc[i,'Day'] <= 21 and mosaicM2df.loc[i, 'Day'] > 14:
                mosaicM2df.loc[i, 'Week'] = 3
            elif mosaicM2df.loc[i,'Day'] <= 28 and mosaicM2df.loc[i, 'Day'] > 21:
                mosaicM2df.loc[i, 'Week'] = 4
            else:
                mosaicM2df.loc[i, 'Week'] = 4

        mosaicM2df['Months_Week'] = mosaicM2df.apply(lambda x: "{0} {1}".format(x['Months_M1_M2'], x['Week']), axis = 1)
        mosaicM2df['Date'] = mosaicM2df.apply(lambda x:datetime.strptime("{0} {1}".format(x['Month'],x['Year']), "%m %Y"), axis = 1)
        mosaicM2df = pd.pivot_table(mosaicM2df, index = ['Milestone','Fund','Date'], values = ['Project Name'], columns = ['Months_Week'], aggfunc = np.count_nonzero, fill_value = 0, margins = True)
        mosaicM2df = mosaicM2df.div(mosaicM2df.iloc[:,-1], axis = 0)
        mosaicM2df = mosaicM2df['Project Name']
        mosaicM2df = mosaicM2df.reset_index()
        mosaicM2df.drop(mosaicM2df.index[len(mosaicM2df)-1])
        mosaicM2df.drop('All',axis =1)


        mosaicM3df = pd.read_sql_query(mosaicM3query,conn)
        mosaicM3df['Week'] = 1

        for i in range(len(mosaicM3df.index)):
            if mosaicM3df.loc[i, 'Day'] <= 7:
                mosaicM3df.loc[i, 'Week'] = 1
            elif mosaicM3df.loc[i,'Day'] <= 14 and mosaicM3df.loc[i, 'Day'] > 7:
                mosaicM3df.loc[i, 'Week'] = 2
            elif mosaicM3df.loc[i,'Day'] <= 21 and mosaicM3df.loc[i, 'Day'] > 14:
                mosaicM3df.loc[i, 'Week'] = 3
            elif mosaicM3df.loc[i,'Day'] <= 28 and mosaicM3df.loc[i, 'Day'] > 21:
                mosaicM3df.loc[i, 'Week'] = 4
            else:
                mosaicM3df.loc[i, 'Week'] = 4

        mosaicM3df['Months_Week'] = mosaicM3df.apply(lambda x: "{0} {1}".format(x['Months_M2_M3'], x['Week']), axis = 1)
        mosaicM3df['Date'] = mosaicM3df.apply(lambda x:datetime.strptime("{0} {1}".format(x['Month'],x['Year']), "%m %Y"), axis = 1)
        mosaicM3df = pd.pivot_table(mosaicM3df, index = ['Milestone','Fund','Date'], values = ['Project Name'], columns = ['Months_Week'], aggfunc = np.count_nonzero, fill_value = 0, margins = True)
        mosaicM3df = mosaicM3df.div(mosaicM3df.iloc[:,-1], axis = 0)
        mosaicM3df = mosaicM3df['Project Name']
        mosaicM3df = mosaicM3df.reset_index()
        mosaicM3df.drop(mosaicM3df.index[len(mosaicM3df)-1])
        mosaicM3df.drop('All',axis =1)



        purecashM1df = pd.read_sql_query(purecashM1query,conn)
        purecashM1df['Week'] = 1

        for i in range(len(purecashM1df.index)):
            if purecashM1df.loc[i, 'Day'] <= 7:
                purecashM1df.loc[i, 'Week'] = 1
            elif purecashM1df.loc[i,'Day'] <= 14 and purecashM1df.loc[i, 'Day'] > 7:
                purecashM1df.loc[i, 'Week'] = 2
            elif purecashM1df.loc[i,'Day'] <= 21 and purecashM1df.loc[i, 'Day'] > 14:
                purecashM1df.loc[i, 'Week'] = 3
            elif purecashM1df.loc[i,'Day'] <= 28 and purecashM1df.loc[i, 'Day'] > 21:
                purecashM1df.loc[i, 'Week'] = 4
            else:
                purecashM1df.loc[i, 'Week'] = 4

        purecashM1df['Months_Week'] = purecashM1df.apply(lambda x: "{0} {1}".format(x['Months_to_M1'], x['Week']), axis = 1)
        purecashM1df['Date'] = purecashM1df.apply(lambda x:datetime.strptime("{0} {1}".format(x['Month'],x['Year']), "%m %Y"), axis = 1)
        purecashM1df = pd.pivot_table(purecashM1df, index = ['Milestone','Fund','Date'], values = ['Project Name'], columns = ['Months_Week'], aggfunc = np.count_nonzero, fill_value = 0, margins = True)
        purecashM1df = purecashM1df.div(purecashM1df.iloc[:,-1], axis = 0)
        purecashM1df = purecashM1df['Project Name']
        purecashM1df = purecashM1df.reset_index()
        purecashM1df.drop(purecashM1df.index[len(purecashM1df)-1])
        purecashM1df.drop('All',axis =1)



        purecashM2df = pd.read_sql_query(purecashM2query,conn)
        purecashM2df['Week'] = 1

        for i in range(len(purecashM2df.index)):
            if purecashM2df.loc[i, 'Day'] <= 7:
                purecashM2df.loc[i, 'Week'] = 1
            elif purecashM2df.loc[i,'Day'] <= 14 and purecashM2df.loc[i, 'Day'] > 7:
                purecashM2df.loc[i, 'Week'] = 2
            elif purecashM2df.loc[i,'Day'] <= 21 and purecashM2df.loc[i, 'Day'] > 14:
                purecashM2df.loc[i, 'Week'] = 3
            elif purecashM2df.loc[i,'Day'] <= 28 and purecashM2df.loc[i, 'Day'] > 21:
                purecashM2df.loc[i, 'Week'] = 4
            else:
                purecashM2df.loc[i, 'Week'] = 4

        purecashM2df['Months_Week'] = purecashM2df.apply(lambda x: "{0} {1}".format(x['Months_M1_M2'], x['Week']), axis = 1)
        purecashM2df['Date'] = purecashM2df.apply(lambda x:datetime.strptime("{0} {1}".format(x['Month'],x['Year']), "%m %Y"), axis = 1)
        purecashM2df = pd.pivot_table(purecashM2df, index = ['Milestone','Fund','Date'], values = ['Project Name'], columns = ['Months_Week'], aggfunc = np.count_nonzero, fill_value = 0, margins = True)
        purecashM2df = purecashM2df.div(purecashM2df.iloc[:,-1], axis = 0)
        purecashM2df = purecashM2df['Project Name']
        purecashM2df = purecashM2df.reset_index()
        purecashM2df.drop(purecashM2df.index[len(purecashM2df)-1])
        purecashM2df.drop('All',axis =1)


        purecashM3df = pd.read_sql_query(purecashM3query,conn)
        purecashM3df['Week'] = 1

        for i in range(len(purecashM3df.index)):
            if purecashM3df.loc[i, 'Day'] <= 7:
                purecashM3df.loc[i, 'Week'] = 1
            elif purecashM3df.loc[i,'Day'] <= 14 and purecashM3df.loc[i, 'Day'] > 7:
                purecashM3df.loc[i, 'Week'] = 2
            elif purecashM3df.loc[i,'Day'] <= 21 and purecashM3df.loc[i, 'Day'] > 14:
                purecashM3df.loc[i, 'Week'] = 3
            elif purecashM3df.loc[i,'Day'] <= 28 and purecashM3df.loc[i, 'Day'] > 21:
                purecashM3df.loc[i, 'Week'] = 4
            else:
                purecashM3df.loc[i, 'Week'] = 4

        purecashM3df['Months_Week'] = purecashM3df.apply(lambda x: "{0} {1}".format(x['Months_M2_M3'], x['Week']), axis = 1)
        purecashM3df['Date'] = purecashM3df.apply(lambda x:datetime.strptime("{0} {1}".format(x['Month'],x['Year']), "%m %Y"), axis = 1)
        purecashM3df = pd.pivot_table(purecashM3df, index = ['Milestone','Fund','Date'], values = ['Project Name'], columns = ['Months_Week'], aggfunc = np.count_nonzero, fill_value = 0, margins = True)
        purecashM3df = purecashM3df.div(purecashM3df.iloc[:,-1], axis = 0)
        purecashM3df = purecashM3df['Project Name']
        purecashM3df = purecashM3df.reset_index()
        purecashM3df.drop(purecashM3df.index[len(purecashM3df)-1])
        purecashM3df.drop('All',axis =1)

        milestone_velocity = pd.concat([kinaM1df, kinaM2df, kinaM3df, mosaicM1df, mosaicM2df, mosaicM3df, purecashM1df, purecashM2df, purecashM3df, sr2M1df, sr2M2df, sr2M3df], axis = 0, ignore_index=True)
        milestone_velocity = milestone_velocity[milestone_velocity.Milestone != 'All']
        cols = ['Fund', 'Milestone','Date', '6 4','6 3','6 2','6 1','5 4', '5 3','5 2','5 1','4 4','4 3','4 2','4 1','3 4','3 3','3 2','3 1','2 4','2 3','2 2','2 1','1 4','1 3',
                '1 2','1 1','0 4','0 3','0 2','0 1']
        milestone_velocity = milestone_velocity[cols]
        milestone_velocity.columns = ['Fund','Milestone','Date'
                                      ,'6_Months_Week4_Previous', '6_Months_Week3_Previous', '6_Months_Week2_Previous', '6_Months_Week1_Previous'
                                      ,'5_Months_Week4_Previous', '5_Months_Week3_Previous', '5_Months_Week2_Previous', '5_Months_Week1_Previous'
                                      ,'4_Months_Week4_Previous', '4_Months_Week3_Previous', '4_Months_Week2_Previous', '4_Months_Week1_Previous'
                                      ,'3_Months_Week4_Previous', '3_Months_Week3_Previous', '3_Months_Week2_Previous', '3_Months_Week1_Previous'
                                      ,'2_Months_Week4_Previous', '2_Months_Week3_Previous', '2_Months_Week2_Previous', '2_Months_Week1_Previous'
                                      ,'1_Months_Week4_Previous', '1_Months_Week3_Previous', '1_Months_Week2_Previous', '1_Months_Week1_Previous'
                                     ,'0_Months_Week4_Previous', '0_Months_Week3_Previous', '0_Months_Week2_Previous', '0_Months_Week1_Previous']

        milestone_velocity.fillna('0.000000')
        for i in range(len(milestone_velocity.index)):
            milestone_velocity.iloc[i,3] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,3]))
            milestone_velocity.iloc[i,4] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,4]))
            milestone_velocity.iloc[i,5] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,5]))
            milestone_velocity.iloc[i,6] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,6]))
            milestone_velocity.iloc[i,7] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,7]))
            milestone_velocity.iloc[i,8] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,8]))
            milestone_velocity.iloc[i,9] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,9]))
            milestone_velocity.iloc[i,10] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,10]))
            milestone_velocity.iloc[i,11] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,11]))
            milestone_velocity.iloc[i,12] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,12]))
            milestone_velocity.iloc[i,13] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,13]))
            milestone_velocity.iloc[i,14] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,14]))
            milestone_velocity.iloc[i,15] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,15]))
            milestone_velocity.iloc[i,16] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,16]))
            milestone_velocity.iloc[i,17] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,17]))
            milestone_velocity.iloc[i,18] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,18]))
            milestone_velocity.iloc[i,19] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,19]))
            milestone_velocity.iloc[i,20] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,20]))
            milestone_velocity.iloc[i,21] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,21]))
            milestone_velocity.iloc[i,22] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,22]))
            milestone_velocity.iloc[i,23] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,23]))
            milestone_velocity.iloc[i,24] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,24]))
            milestone_velocity.iloc[i,25] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,25]))
            milestone_velocity.iloc[i,26] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,26]))
            milestone_velocity.iloc[i,27] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,27]))
            milestone_velocity.iloc[i,28] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,28]))
            milestone_velocity.iloc[i,29] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,29]))
            milestone_velocity.iloc[i,30] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,30]))

        for i in range(len(milestone_velocity.index)):
            if milestone_velocity.iloc[i,3] == 'nan':
                milestone_velocity.iloc[i,3] = "{0:.6f}".format(0)
            if milestone_velocity.iloc[i,4] == 'nan':
                milestone_velocity.iloc[i,4] = "{0:.6f}".format(0)
            if milestone_velocity.iloc[i,5] == 'nan':
                milestone_velocity.iloc[i,5] = "{0:.6f}".format(0)
            if milestone_velocity.iloc[i,6] == 'nan':
                milestone_velocity.iloc[i,6] = "{0:.6f}".format(0)
            if milestone_velocity.iloc[i,7] == 'nan':
                milestone_velocity.iloc[i,7] = "{0:.6f}".format(0)
            if milestone_velocity.iloc[i,8] == 'nan':
                milestone_velocity.iloc[i,8] = "{0:.6f}".format(0)
            if milestone_velocity.iloc[i,9] == 'nan':
                milestone_velocity.iloc[i,9] = "{0:.6f}".format(0)
            if milestone_velocity.iloc[i,10] == 'nan':
                milestone_velocity.iloc[i,10] = "{0:.6f}".format(0)
            if milestone_velocity.iloc[i,11] == 'nan':
                milestone_velocity.iloc[i,11] = "{0:.6f}".format(0)
            if milestone_velocity.iloc[i,12] == 'nan':
                milestone_velocity.iloc[i,12] = "{0:.6f}".format(0)
            if milestone_velocity.iloc[i,13] == 'nan':
                milestone_velocity.iloc[i,13] = "{0:.6f}".format(0)
            if milestone_velocity.iloc[i,14] == 'nan':
                milestone_velocity.iloc[i,14] = "{0:.6f}".format(0)
            if milestone_velocity.iloc[i,15] == 'nan':
                milestone_velocity.iloc[i,15] = "{0:.6f}".format(0)
            if milestone_velocity.iloc[i,16] == 'nan':
                milestone_velocity.iloc[i,16] = "{0:.6f}".format(0)
            if milestone_velocity.iloc[i,17] == 'nan':
                milestone_velocity.iloc[i,17] = "{0:.6f}".format(0)
            if milestone_velocity.iloc[i,18] == 'nan':
                milestone_velocity.iloc[i,18] = "{0:.6f}".format(0)
            if milestone_velocity.iloc[i,19] == 'nan':
                milestone_velocity.iloc[i,19] = "{0:.6f}".format(0)
            if milestone_velocity.iloc[i,20] == 'nan':
                milestone_velocity.iloc[i,20] = "{0:.6f}".format(0)
            if milestone_velocity.iloc[i,21] == 'nan':
                milestone_velocity.iloc[i,21] = "{0:.6f}".format(0)
            if milestone_velocity.iloc[i,22] == 'nan':
                milestone_velocity.iloc[i,22] = "{0:.6f}".format(0)
            if milestone_velocity.iloc[i,23] == 'nan':
                milestone_velocity.iloc[i,23] = "{0:.6f}".format(0)
            if milestone_velocity.iloc[i,24] == 'nan':
                milestone_velocity.iloc[i,24] = "{0:.6f}".format(0)
            if milestone_velocity.iloc[i,25] == 'nan':
                milestone_velocity.iloc[i,25] = "{0:.6f}".format(0)
            if milestone_velocity.iloc[i,26] == 'nan':
                milestone_velocity.iloc[i,26] = "{0:.6f}".format(0)
            if milestone_velocity.iloc[i,27] == 'nan':
                milestone_velocity.iloc[i,27] = "{0:.6f}".format(0)
            if milestone_velocity.iloc[i,28] == 'nan':
                milestone_velocity.iloc[i,28] = "{0:.6f}".format(0)
            if milestone_velocity.iloc[i,29] == 'nan':
                milestone_velocity.iloc[i,29] = "{0:.6f}".format(0)
            if milestone_velocity.iloc[i,30] == 'nan':
                milestone_velocity.iloc[i,30] = "{0:.6f}".format(0)

        milestone_velocity['Date'] = [time.date() for time in milestone_velocity['Date']]
        milestone_velocity['Last_Refreshed_Date'] = today
        milestone_velocity.to_sql('milestone_velocity_reverse_weekly', conn, flavor = 'mysql', if_exists = 'replace', index = False)

        alter_table_query = """
            ALTER TABLE fiops.milestone_velocity_reverse_weekly
            MODIFY 6_Months_Week4_Previous decimal(7,6),
            MODIFY 6_Months_Week3_Previous decimal(7,6),
            MODIFY 6_Months_Week2_Previous decimal(7,6),
            MODIFY 6_Months_Week1_Previous decimal(7,6),
            MODIFY 5_Months_Week4_Previous decimal(7,6),
            MODIFY 5_Months_Week3_Previous decimal(7,6),
            MODIFY 5_Months_Week2_Previous decimal(7,6),
            MODIFY 5_Months_Week1_Previous decimal(7,6),
            MODIFY 4_Months_Week4_Previous decimal(7,6),
            MODIFY 4_Months_Week3_Previous decimal(7,6),
            MODIFY 4_Months_Week2_Previous decimal(7,6),
            MODIFY 4_Months_Week1_Previous decimal(7,6),
            MODIFY 3_Months_Week4_Previous decimal(7,6),
            MODIFY 3_Months_Week3_Previous decimal(7,6),
            MODIFY 3_Months_Week2_Previous decimal(7,6),
            MODIFY 3_Months_Week1_Previous decimal(7,6),
            MODIFY 2_Months_Week4_Previous decimal(7,6),
            MODIFY 2_Months_Week3_Previous decimal(7,6),
            MODIFY 2_Months_Week2_Previous decimal(7,6),
            MODIFY 2_Months_Week1_Previous decimal(7,6),
            MODIFY 1_Months_Week4_Previous decimal(7,6),
            MODIFY 1_Months_Week3_Previous decimal(7,6),
            MODIFY 1_Months_Week2_Previous decimal(7,6),
            MODIFY 1_Months_Week1_Previous decimal(7,6),
            MODIFY 0_Months_Week4_Previous decimal(7,6),
            MODIFY 0_Months_Week3_Previous decimal(7,6),
            MODIFY 0_Months_Week2_Previous decimal(7,6),
            MODIFY 0_Months_Week1_Previous decimal(7,6)
            """

        pd.io.sql.execute(alter_table_query,conn)

    else:
        print '\n'
        print 'Milestone Velocity Reverse Weekly Table does not require an update.'
        exit()
