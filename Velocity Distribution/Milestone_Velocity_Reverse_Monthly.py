import FiOps_Functions as Funcs
import pandas as pd
import numpy as np
import time
import datetime
from datetime import datetime
import sqlalchemy

def main():

    cnx = Funcs.sql_fiops_connect()

    Updated_Date = """ select Last_Refreshed_Date from fiops.milestone_velocity_reverse_monthly LIMIT 1"""
    Last_Refreshed_Date = pd.read_sql_query(Updated_Date, conn)
    Last_Refreshed_Date = Last_Refreshed_Date.loc[0, 'Last_Refreshed_Date']
    Last_Refreshed_Date

    today = datetime.today()
    today = today.strftime("%Y-%m-%d")
    today = datetime.strptime(today,"%Y-%m-%d" ).date()
    today

    if (Last_Refreshed_Date < today):
        ## Queries for Kina that determine how old Sale Closed is depending on M1/M2/M3 Submitted Dates

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
        ,	DAY(FPA.M2_Submitted_Date) as 'Day'
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
        M.TRANCHE_ID__C IN ('P1','P2','P3','P4','P5','P6','P7','P8','P9','P10')
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
        M.TRANCHE_ID__C IN ('P1','P2','P3','P4','P5','P6','P7','P8','P9','P10')
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
        M.TRANCHE_ID__C IN ('P1','P2','P3','P4','P5','P6','P7','P8','P9','P10')
        AND M.IS_TEST__C = 0
        AND M.STATUS__C <> 'Cancelled'
        AND FPA.M2_Submitted_Date IS NOT NULL
        AND FPA.M3_Submitted_Date IS NOT NULL
        """

        mosaicM1query = """
        SELECT
        	M.ID as 'ID'
        ,	M.Name as 'Project Name'
        ,	M.SALE_CLOSED__C as 'Sale_Closed_Date'
        ,	YEAR(JRSLPA.F1_Submitted_Date) as 'Year'
        ,	MONTH(JRSLPA.F1_Submitted_Date) as 'Month'
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

        purecashM1query = """
        SELECT
        	M.ID as 'ID'
        ,	M.Name as 'Project Name'
        ,	M.SALE_CLOSED__C as 'Sale_Closed_Date'
        ,	YEAR(M.SALE_CLOSED__C) as 'Year'
        ,	MONTH(M.SALE_CLOSED__C) as 'Month'
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

        kinaM1df = pd.read_sql_query(kinaM1query, cnx)
        kinaM1df['Date'] = kinaM1df.apply(lambda x:datetime.strptime("{0} {1}".format(x['Month'],x['Year']), "%m %Y"), axis = 1)
        kinaM1 = pd.pivot_table(kinaM1df, index = ['Milestone','Date','Fund'], values = ['Project Name'], columns = ['Months_to_M1'], aggfunc = np.count_nonzero, fill_value = 0, margins = True)
        kinaM1 = kinaM1.div(kinaM1.iloc[:,-1], axis = 0)
        kinaM1 = kinaM1['Project Name']
        kinaM1 = kinaM1.reset_index()
        kinaM1.drop(kinaM1.index[len(kinaM1)-1])
        kinaM1.drop('All', axis =1)

        kinaM2df = pd.read_sql_query(kinaM2query, cnx)
        kinaM2df['Date'] = kinaM2df.apply(lambda x:datetime.strptime("{0} {1}".format(x['Month'],x['Year']), "%m %Y"), axis = 1)
        kinaM2 = pd.pivot_table(kinaM2df, index = ['Milestone','Date','Fund'], values = ['Project Name'], columns = ['Months_M1_M2'], aggfunc = np.count_nonzero, fill_value = 0, margins = True)
        kinaM2 = kinaM2.div(kinaM2.iloc[:,-1], axis = 0)
        kinaM2 = kinaM2['Project Name']
        kinaM2 = kinaM2.reset_index()
        kinaM2.drop(kinaM2.index[len(kinaM2)-1])
        kinaM2.drop('All', axis =1)

        kinaM3df = pd.read_sql_query(kinaM3query, cnx)
        kinaM3df['Date'] = kinaM3df.apply(lambda x:datetime.strptime("{0} {1}".format(x['Month'],x['Year']), "%m %Y"), axis = 1)
        kinaM3 = pd.pivot_table(kinaM3df, index = ['Milestone','Date','Fund'], values = ['Project Name'], columns = ['Months_M2_M3'], aggfunc = np.count_nonzero, fill_value = 0, margins = True)
        kinaM3 = kinaM3.div(kinaM3.iloc[:,-1], axis = 0)
        kinaM3 = kinaM3['Project Name']
        kinaM3 = kinaM3.reset_index()
        kinaM3.drop(kinaM3.index[len(kinaM3)-1])
        kinaM3.drop('All', axis =1)

        mosaicM1df = pd.read_sql_query(mosaicM1query, cnx)
        mosaicM1df['Date'] = mosaicM1df.apply(lambda x:datetime.strptime("{0} {1}".format(x['Month'],x['Year']), "%m %Y"), axis = 1)
        mosaicM1 = pd.pivot_table(mosaicM1df, index = ['Milestone','Date','Fund'], values = ['Project Name'], columns = ['Months_to_M1'], aggfunc = np.count_nonzero, fill_value = 0, margins = True)
        mosaicM1 = mosaicM1.div(mosaicM1.iloc[:,-1], axis = 0)
        mosaicM1 = mosaicM1['Project Name']
        mosaicM1 = mosaicM1.reset_index()
        mosaicM1.drop(mosaicM1.index[len(mosaicM1)-1])
        mosaicM1.drop('All', axis =1)

        mosaicM2df = pd.read_sql_query(mosaicM2query, cnx)
        mosaicM2df['Date'] = mosaicM2df.apply(lambda x:datetime.strptime("{0} {1}".format(x['Month'],x['Year']), "%m %Y"), axis = 1)
        mosaicM2 = pd.pivot_table(mosaicM2df, index = ['Milestone','Date','Fund'], values = ['Project Name'], columns = ['Months_M1_M2'], aggfunc = np.count_nonzero, fill_value = 0, margins = True)
        mosaicM2 = mosaicM2.div(mosaicM2.iloc[:,-1], axis = 0)
        mosaicM2 = mosaicM2['Project Name']
        mosaicM2 = mosaicM2.reset_index()
        mosaicM2.drop(mosaicM2.index[len(mosaicM2)-1])
        mosaicM2.drop('All', axis =1)

        mosaicM3df = pd.read_sql_query(mosaicM3query, cnx)
        mosaicM3df['Date'] = mosaicM3df.apply(lambda x:datetime.strptime("{0} {1}".format(x['Month'],x['Year']), "%m %Y"), axis = 1)
        mosaicM3 = pd.pivot_table(mosaicM3df, index = ['Milestone','Date','Fund'], values = ['Project Name'], columns = ['Months_M2_M3'], aggfunc = np.count_nonzero, fill_value = 0, margins = True)
        mosaicM3 = mosaicM3.div(mosaicM3.iloc[:,-1], axis = 0)
        mosaicM3 = mosaicM3['Project Name']
        mosaicM3 = mosaicM3.reset_index()
        mosaicM3.drop(mosaicM3.index[len(mosaicM3)-1])
        mosaicM3.drop('All', axis =1)

        purecashM1df = pd.read_sql_query(purecashM1query, cnx)
        purecashM1df['Date'] = purecashM1df.apply(lambda x:datetime.strptime("{0} {1}".format(x['Month'],x['Year']), "%m %Y"), axis = 1)
        purecashM1 = pd.pivot_table(purecashM1df, index = ['Milestone','Date','Fund'], values = ['Project Name'], columns = ['Months_to_M1'], aggfunc = np.count_nonzero, fill_value = 0, margins = True)
        purecashM1 = purecashM1.div(purecashM1.iloc[:,-1], axis = 0)
        purecashM1 = purecashM1['Project Name']
        purecashM1 = purecashM1.reset_index()
        purecashM1.drop(purecashM1.index[len(purecashM1)-1])
        purecashM1.drop('All', axis =1)

        purecashM2df = pd.read_sql_query(purecashM2query, cnx)
        purecashM2df['Date'] = purecashM2df.apply(lambda x:datetime.strptime("{0} {1}".format(x['Month'],x['Year']), "%m %Y"), axis = 1)
        purecashM2 = pd.pivot_table(purecashM2df, index = ['Milestone','Date','Fund'], values = ['Project Name'], columns = ['Months_M1_M2'], aggfunc = np.count_nonzero, fill_value = 0, margins = True)
        purecashM2 = purecashM2.div(purecashM2.iloc[:,-1], axis = 0)
        purecashM2 = purecashM2['Project Name']
        purecashM2 = purecashM2.reset_index()
        purecashM2.drop(purecashM2.index[len(purecashM2)-1])
        purecashM2.drop('All', axis =1)

        purecashM3df = pd.read_sql_query(purecashM3query, cnx)
        purecashM3df['Date'] = purecashM3df.apply(lambda x:datetime.strptime("{0} {1}".format(x['Month'],x['Year']), "%m %Y"), axis = 1)
        purecashM3 = pd.pivot_table(purecashM3df, index = ['Milestone','Date','Fund'], values = ['Project Name'], columns = ['Months_M2_M3'], aggfunc = np.count_nonzero, fill_value = 0, margins = True)
        purecashM3 = purecashM3.div(purecashM3.iloc[:,-1], axis = 0)
        purecashM3 = purecashM3['Project Name']
        purecashM3 = purecashM3.reset_index()
        purecashM3.drop(purecashM3.index[len(purecashM3)-1])
        purecashM3.drop('All', axis =1)

        sr2M1df = pd.read_sql_query(sr2M1query, cnx)
        sr2M1df['Date'] = sr2M1df.apply(lambda x:datetime.strptime("{0} {1}".format(x['Month'],x['Year']), "%m %Y"), axis = 1)
        sr2M1 = pd.pivot_table(sr2M1df, index = ['Milestone','Date','Fund'], values = ['Project Name'], columns = ['Months_to_M1'], aggfunc = np.count_nonzero, fill_value = 0, margins = True)
        sr2M1 = sr2M1.div(sr2M1.iloc[:,-1], axis = 0)
        sr2M1 = sr2M1['Project Name']
        sr2M1 = sr2M1.reset_index()
        sr2M1.drop(sr2M1.index[len(sr2M1)-1])
        sr2M1.drop('All', axis =1)

        sr2M2df = pd.read_sql_query(sr2M2query, cnx)
        sr2M2df['Date'] = sr2M2df.apply(lambda x:datetime.strptime("{0} {1}".format(x['Month'],x['Year']), "%m %Y"), axis = 1)
        sr2M2 = pd.pivot_table(sr2M2df, index = ['Milestone','Date','Fund'], values = ['Project Name'], columns = ['Months_M1_M2'], aggfunc = np.count_nonzero, fill_value = 0, margins = True)
        sr2M2 = sr2M2.div(sr2M2.iloc[:,-1], axis = 0)
        sr2M2 = sr2M2['Project Name']
        sr2M2 = sr2M2.reset_index()
        sr2M2.drop(sr2M2.index[len(sr2M2)-1])
        sr2M2.drop('All', axis =1)

        sr2M3df = pd.read_sql_query(sr2M3query, cnx)
        sr2M3df['Date'] = sr2M3df.apply(lambda x:datetime.strptime("{0} {1}".format(x['Month'],x['Year']), "%m %Y"), axis = 1)
        sr2M3 = pd.pivot_table(sr2M3df, index = ['Milestone','Date','Fund'], values = ['Project Name'], columns = ['Months_M2_M3'], aggfunc = np.count_nonzero, fill_value = 0, margins = True)
        sr2M3 = sr2M3.div(sr2M3.iloc[:,-1], axis = 0)
        sr2M3 = sr2M3['Project Name']
        sr2M3 = sr2M3.reset_index()
        sr2M3.drop(sr2M3.index[len(sr2M3)-1])
        sr2M3.drop('All', axis =1)

        milestone_velocity = pd.concat([kinaM1, kinaM2, kinaM3, mosaicM1, mosaicM2, mosaicM3, purecashM1, purecashM2, purecashM3, sr2M1, sr2M2, sr2M3], axis = 0, ignore_index=True)
        milestone_velocity = milestone_velocity[['Fund','Milestone','Date', 0, 1, 2, 3, 4, 5, 6]]
        milestone_velocity = milestone_velocity[milestone_velocity.Milestone != 'All']
        milestone_velocity.columns = ['Fund','Milestone','Date','0_Months_Previous', '1_Months_Previous', '2_Months_Previous', '3_Months_Previous', '4_Months_Previous', '5_Months_Previous', '6_Months_Previous']
        cols = list(milestone_velocity)
        cols.insert(3,cols.pop(cols.index('6_Months_Previous')))
        cols.insert(4,cols.pop(cols.index('5_Months_Previous')))
        cols.insert(5,cols.pop(cols.index('4_Months_Previous')))
        cols.insert(6,cols.pop(cols.index('3_Months_Previous')))
        cols.insert(7,cols.pop(cols.index('2_Months_Previous')))
        cols.insert(8,cols.pop(cols.index('1_Months_Previous')))
        cols.insert(9,cols.pop(cols.index('0_Months_Previous')))
        milestone_velocity = milestone_velocity.ix[:,cols]

        milestone_velocity.fillna('0.000000')

        for i in range(len(milestone_velocity.index)):
            milestone_velocity.iloc[i,3] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,3]))
            milestone_velocity.iloc[i,4] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,4]))
            milestone_velocity.iloc[i,5] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,5]))
            milestone_velocity.iloc[i,6] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,6]))
            milestone_velocity.iloc[i,7] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,7]))
            milestone_velocity.iloc[i,8] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,8]))
            milestone_velocity.iloc[i,9] =  "{0:.6f}".format(float(milestone_velocity.iloc[i,9]))

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

        milestone_velocity['Date'] = [time.date() for time in milestone_velocity['Date']]
        milestone_velocity['Last_Refreshed_Date'] = today
        milestone_velocity.to_sql('milestone_velocity_reverse_monthly', cnx, flavor = 'mysql', if_exists = 'replace', index = False)

        alter_table_query = """
        ALTER TABLE fiops.milestone_velocity_reverse_monthly
        	MODIFY 6_Months_Previous decimal(7,6),
            MODIFY 5_Months_Previous decimal(7,6),
            MODIFY 4_Months_Previous decimal(7,6),
            MODIFY 3_Months_Previous decimal(7,6),
            MODIFY 2_Months_Previous decimal(7,6),
            MODIFY 1_Months_Previous decimal(7,6),
            MODIFY 0_Months_Previous decimal(7,6);
        """
        pd.io.sql.execute(alter_table_query,cnx)


    else:
        print '\n'
        print 'Milestone Velocity Reverse Monthly does not require an Update.'
