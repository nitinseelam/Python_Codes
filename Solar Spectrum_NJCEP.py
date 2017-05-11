import pyPortal as p
import bi
import datetime as dt
import time

def log_in(portal):
    portal.fill_text_id('email','njforms@solarspectrum.com')
    portal.fill_text_id('password','Solar4all!')
    portal.click_id('subbtn')

def sect_1(portal):
    #Site Host Contact and Installation Address
    portal.fill_text_id('premise_firstname',portal.data['c.FIRSTNAME'])
    portal.fill_text_id('premise_lastname',portal.data['c.LASTNAME'])
    portal.fill_text_id('premise_company',portal.data['c.NAME'])
    portal.fill_text_id('premise_acct_number',portal.data['p.UTILITY_ACCOUNT_NUMBER__C'])
    portal.fill_text_id('premise_address',portal.data['p.SITE_STREET__C'])
    portal.fill_text_id('premise_city',portal.data['p.SITE_CITY__C'])
    portal.select_drop_down_name('premise_state','NEW JERSEY')
    portal.fill_text_id('premise_zip',portal.data['p.SITE_ZIP_POSTAL_CODE__C'])
    portal.fill_text_id('premise_phone',portal.data['a.PHONE'])
    portal.fill_text_id('premise_email',portal.data['p.EMAIL__C'])
    raw_input('Site Host Contact and Installation Address complete. Please QA and hit Enter.\n')

def sect_2(portal):
    #SREC Owner
    if portal.data['fp.NAME'] in ['sungevity_cash','sungevity_sunrun_cash']:
        portal.fill_text_id('primary_firstname',portal.data['c.FIRSTNAME'])
        portal.fill_text_id('primary_lastname',portal.data['c.LASTNAME'])
        portal.fill_text_id('primary_company',portal.data['c.NAME'])
        portal.fill_text_id('primary_address',portal.data['p.SITE_STREET__C'])
        portal.fill_text_id('primary_city',portal.data['p.SITE_CITY__C'])
        portal.select_drop_down_name('primary_state','NEW JERSEY')
        portal.fill_text_id('primary_zip',portal.data['p.SITE_ZIP_POSTAL_CODE__C'])
        portal.fill_text_id('primary_phone',portal.data['a.PHONE'])
        portal.fill_text_id('primary_email',portal.data['p.EMAIL__C'])
    else:
        raw_input('Third Party Owner identified.\nPlease select the SREC owner ("System Owner" on InstallAgmt) in the dropdown menu.\n Press Enter to continue.\n')

def sect_3(portal):
    #Solar Installer
    portal.select_drop_down_name('contcontlistselect','Solar Spectrum Inc. 66 Franklin St.')
    #Electrical Contractor

    if 'SunnyMac' in portal.data['p.PREFERRED_INSTALLER_PARENT_ACCOUNT__C']:
        portal.fill_text_id('FF99116','SunnyMac, LLC')
        portal.fill_text_id('FF99117','Mark A LaMarra')
        portal.fill_text_id('FF99118','34EB01576900')
    elif 'Skyline' in portal.data['p.PREFERRED_INSTALLER_PARENT_ACCOUNT__C']:
        portal.fill_text_id('FF99116','Skyline Solar')
        portal.fill_text_id('FF99117','Joseph R. Horling, III')
        portal.fill_text_id('FF99118','34EB01741000')
    elif 'Solar Mite' in portal.data['p.PREFERRED_INSTALLER_PARENT_ACCOUNT__C']:
        portal.fill_text_id('FF99116','Solar Mite Solutions, LLC')
        portal.fill_text_id('FF99117','Stephen S. Martiak')
        portal.fill_text_id('FF99118','34EB00504600')
    else:
        raw_input('Installer not recognized - please manually enter\n')
    portal.fill_text_id('FF99119','03/31/2018')
    raw_input('Electrical Contractor complete. Please QA and hit enter to proceed.\n')
    #System Information
    portal.select_drop_down_name('FF99213','New Application')
    portal.select_drop_down_name('FF99081','NA')
    if portal.data['fp.NAME'] in ['sungevity_cash','sungevity_sunrun_cash']:
        portal.fill_text_id('FF99215',str(portal.data['sp.PURCHASE_PRICE__C']))
    else:
        portal.fill_text_id('FF99215',str(portal.data['p.SYSTEM_KW_STC__C']*3530))
    portal.fill_text_id('FF98905',dt.date.today().strftime("%m/%d/%Y"))
    portal.fill_text_id('FF102453',str(portal.data['p.SYSTEM_KW_STC__C']))
    portal.fill_text_id('FF105860',str(portal.data['s.ANNUAL_KWH__C']))
    raw_input('System Information Complete. Please QA and hit enter to proceed.\n')
    #Warranty Information
    portal.fill_text_id('FF108453','25')
    portal.fill_text_id('FF108455','10')
    portal.fill_text_id('FF108454','.80')
    portal.fill_text_id('FF108456','20')
def sect_4(portal):
    for array in portal.arrays:
        portal.click_xpath("//table[@id='vdsmtopaddmenu']/tbody/tr/td/div")
        time.sleep(1)
        portal.switch_frame()
        portal.click_xpath("//div[@id='col']/div/div")
        time.sleep(1)
        portal.click_xpath("//div[@id='col']/div/div")
        time.sleep(1)
        portal.click_xpath("//div[@id='dsm.searchequipmentbycategoryiddisplay']/form/table/tbody/tr[3]/td[2]/a/img")
        portal.fill_text_id('kW_Impact',str(array['module kw']))
        portal.fill_text_id('QUANTITY',"{:.0f}".format(array['num modules']))
        portal.fill_text_id('Manufacturer',str(array['module manu']))
        portal.fill_text_id('Model',str(array['module model']))
        portal.select_drop_down_name('location_sel','Roof')
        portal.fill_text_id('Direction',str(array['azimuth']))
        portal.fill_text_id('Tilt_Angle', str(array['pitch']))
        portal.select_drop_down_name('TYPE_SEL','Fixed')
        portal.fill_text_id('Percent', str(array['shading']/100))
        raw_input("Please QA this array's information and hit enter to proceed.\n")
        portal.click_xpath("//div[@id='sender']/form/fieldset[2]/div/button")
        portal.default_frame()
        time.sleep(1)
def sect_5(portal):
    for array in portal.arrays:
        if array['shared inverter'] == 0:
            portal.click_xpath("//table[@id='vdsmtopaddmenu']/tbody/tr/td/div")
            portal.switch_frame()
            time.sleep(1)
            portal.click_xpath("//div[@id='col']/div")
            time.sleep(1)
            portal.click_xpath("//div[@id='col']/div")
            time.sleep(1)
            portal.click_xpath("//tr[1]/td[2]/a/img")
            portal.fill_text_id('Manufacturer',str(array['inverter manu']))
            portal.fill_text_id('Model',str(array['inverter model']))
            portal.fill_text_id('Wattage',str(array['inverter nameplate']))
            portal.fill_text_id('Efficiency','.975')
            portal.select_drop_down_name('location_sel','Outdoor')
            portal.fill_text_id('Location','Near Meter')
            raw_input('Please QA inverter information and hit enter to proceed.\n')
            portal.click_xpath("//div[@id='sender']/form/fieldset[2]/div/button")
            portal.default_frame()
            portal.click_xpath("//div[@id='v_fullrow']/button")
def sect_6(portal):
    portal.select_drop_down('FF99216','No')
    portal.select_drop_down('FF99045','Residential')
    if portal.data['fp.NAME'] in ['sungevity_cash','sungevity_sunrun_cash']:
        portal.select_drop_down('FF99039','No')
    else:
        portal.select_drop_down('FF99039','Yes')
    portal.select_drop_down('FF99076','None')
    if portal.data['p.PROJECT_UTILITY__C'] == 'ACE (Atlantic City Electric)':
        portal.select_drop_down('FF99079','AC Electric')
    elif portal.data['p.PROJECT_UTILITY__C'] == 'JCP&L (Jersey Central Power and Light Co.)':
        portal.select_drop_down('FF99079','JCP&L')
    elif portal.data['p.PROJECT_UTILITY__C'] == 'PSE&G - NJ':
        portal.select_drop_down('FF99079','PSE&G')
    elif portal.data['p.PROJECT_UTILITY__C'] == 'Rockland Electric':
        portal.select_drop_down('FF99079','Orange Rockland Electric')
    constructiondate = dt.date.today() + dt.timedelta(days=20)
    portal.fill_text_id('FF99040',constructiondate.strftime("%m/%d/%Y"))
    PTOdate = dt.date.today() + dt.timedelta(days=40)
    portal.fill_text_id('FF99041',PTOdate.strftime("%m/%d/%Y"))
    raw_input('Please QA fields and hit enter to proceed\n')
    portal.click_xpath("//div[@id='v_section']/div[4]/button")
    time.sleep(1)
    portal.click_xpath("//div[@id='v_section']/div[4]/button")

project = raw_input('\nNJCEP Online Portal\n\nProject #? ')
portal = p.Portal('https://njcepsolar.programprocessing.com/login/?ref=apply&ft=B9F3869B1DFD44F89CC90ABAE7895338',project, chrome=True)

active = True
run = 1
while active:
    if run == 1:
        menu = '1'

    else:
        menu = raw_input('\nMain Menu\n\n1 - Another Project\n2 - Exit\n\n')

    if menu == '1':
        if run == 2:
            project = raw_input('New Project #?\n\n')
            portal.new_proj(project)
            portal.load_page('https://njcepsolar.programprocessing.com/login/?ref=apply&ft=B9F3869B1DFD44F89CC90ABAE7895338')

        log_in(portal)
        raw_input('\nPlease review application documents for submission prior to portal data entry:\n\n1. SREC Registration form\n2. Installation Agreement (review system owner, equipment, price, and dates)\n3. Site Plan\n\nPress enter to proceed.\n')
        sect_1(portal)
        sect_2(portal)
        sect_3(portal)
        sect_4(portal)
        sect_5(portal)
        sect_6(portal)
        raw_input('Portal data entry complete. Please upload required documents and submit application.\n\n Press enter to return to menu.')
    #portal.click_id('btnSubmitStep2')

    elif menu == '2':
        portal.close()
        active = False

    run = 2
