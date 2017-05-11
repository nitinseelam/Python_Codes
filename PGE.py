import pyPortal as p
import bi
import datetime as dt
import time
import getpass

def PGE(portal):
    portal.fill_text_id('electric_account_number',portal.data['p.UTILITY_ACCOUNT_NUMBER__C'])
    portal.fill_text_id('meter_number',portal.data['p.UTILITY_ELECTRIC_METER_NUMBER__C'])
    captcha = raw_input('Please enter Security captcha into command prompt and press Enter.')
    portal.fill_text_id('captchaValid',captcha)
    portal.click_id('btn-next-1')
    portal.fill_text_id('methodOfContactEmail',portal.data['p.EMAIL__C'])
    portal.fill_text_id('methodOfContactConfirmEmail',portal.data['p.EMAIL__C'])
    portal.click_id('agreementType')
    portal.select_drop_down('customerSector','Residential')
    meteraccess = raw_input('Please review Interconnection Agreement for Meter Access issues.\n\nPress 1 for meter in building or behind locked gate\nPress 2 for unrestrainted animal at meter or AC Disconnect switch\nPress 3 for Other.\nPress Enter if none.')
    if meteraccess == '1':
        portal.click_id('meterInBuilding')
        portal.fill_text_id('meterAccessIssueContactName',portal.data['p.UTILITY_ACCOUNT_HOLDER__C'])
        portal.fill_text_id('meterAccessIssueContactPhone',portal.data['c.PHONE'])
    elif meteraccess == '2':
        portal.click_id('animalAtMeter')
        portal.fill_text_id('meterAccessIssueContactName',portal.data['p.UTILITY_ACCOUNT_HOLDER__C'])
        portal.fill_text_id('meterAccessIssueContactPhone',portal.data['c.PHONE'])
    elif meteraccess == '3':
        portal.click_id('meterAccessOther')
        reason = raw_input('Please enter "Other" reason into command prompt and hit enter.\n')
        portal.fill_text_id('meterAccessIssueDetailsTextDesc',reason)
        portal.fill_text_id('meterAccessIssueContactName',portal.data['p.UTILITY_ACCOUNT_HOLDER__C'])
        portal.fill_text_id('meterAccessIssueContactPhone',portal.data['c.PHONE'])
    portal.click_xpath("//form[@id='faciltiyAndResponsiblePartiesForm']/fieldset[6]/div/div/div[2]/div[2]/div/input")
    portal.fill_text_id('tpCompanyName','Sungevity Inc.')
    portal.fill_text_id('tpEmail','forms@sungevity.com')
    portal.fill_text_id('tpConfirmEmail','forms@sungevity.com')
    portal.click_id('tpContactFirstName')
    user = getpass.getuser()
    query = '''SELECT u.FIRSTNAME as firstname
        , u.LASTNAME as lastname
        , u.PHONE as phone
        FROM user as u
        WHERE u.COMMUNITYNICKNAME = %(user)s'''
    df = bi.query_bi(query,params_in={'user':user})
    portal.fill_text_id('tpContactFirstName',df['firstname'][0])
    portal.fill_text_id('tpContactLastName',df['lastname'][0])
    portal.fill_text_id('tpContactPhoneNum',df['phone'][0])
    portal.click_id('btn-next-1')
    portal.click_id('generatingFacilityTypeSolar')
    portal.click_id('btn-next-1')
    cecac = round(portal.data['s.KW_CEC__C']*1.2,2)
    estprod = round(cecac*1664)
    portal.fill_text_id('cecac', str(cecac))
    portal.click_id('btn-next-1')
    bldgsizereq = raw_input('Building size requested? (y/n)')
    if bldgsizereq == 'y':
        size = raw_input('Please enter building size into command prompt and press Enter.')
        portal.fill_text_id('size',size)
        portal.click_id('btn-next-1')
        if estprod > (float(size)*3.32):
            portal.fill_text_id('increase',str(estprod-float(size)*3.32))
            portal.click_id('btn-next-1')
        warning = raw_input('Did the warning window pop up? (y/n)')
        if warning == 'y':
            portal.click_xpath("//div[@id='capacityCheckWarningModal']/div[2]/input")
        portal.click_id('btn-next-1')
    elif estprod > (float(portal.data['p.TOTAL_ANNUAL_USAGE__C'])*1.1):
        portal.fill_text_id('increase',str(estprod-float(portal.data['p.TOTAL_ANNUAL_USAGE__C'])))
        portal.click_id('btn-next-1')
        warning = raw_input('Did the warning window pop up? (y/n)')
        if warning == 'y':
            portal.click_xpath("//div[@id='capacityCheckWarningModal']/div[2]/input")
            portal.click_id('btn-next-1')
        #portal.click_id('btn-next-1')
    else:
        warning = raw_input('Did the warning window pop up? (y/n)')
        if warning == 'y':
            portal.click_xpath("//div[@id='capacityCheckWarningModal']/div[2]/input")
        portal.click_id('btn-next-1')
    EV = raw_input('EV? (y/n) ')
    if EV == 'y':
        EVquantity = raw_input('EV quantity? ')
        portal.click_xpath("//form[@id='rateSelectionForm']/fieldset[2]/div/div/div/input")
        portal.fill_text_id('electricVehicleCount',EVquantity)
    else:
        portal.click_xpath("//form[@id='rateSelectionForm']/fieldset[2]/div/div[2]/div/input")
    raw_input('Please review rate in portal and update Inter Agreement if necessary.\n\nPress Enter to continue.')
    portal.click_id('btn-next-1')
    raw_input('Please review application and note any warnings or transformer notices.\n\nPress Enter to continue.')
    portal.click_id('readAgreement')
    portal.click_id('btn-next-1')
    time.sleep(1)
    portal.click_id('printEsignButton')
    portal.click_id('doneEsignButton')
    portal.click_id('btn-authToApptyToHomePage')
    portal.click_xpath("//div[@id='goImage7']/input")
    portal.fill_text_id('electric_account_number',portal.data['p.UTILITY_ACCOUNT_NUMBER__C'])
    portal.fill_text_id('meter_number',portal.data['p.UTILITY_ELECTRIC_METER_NUMBER__C'])
    captcha = raw_input('Please close Inter Agmt and enter Security captcha into command prompt and press Enter.')
    portal.fill_text_id('captchaValid',captcha)
    portal.click_id('btn-next-1')
    raw_input('Please upload Inter Agmt to portal and submit application.\n\nPress Enter to return to menu.')

project = raw_input('\nPG&E Online Portal\n\nProject #? ')
portal = p.Portal('https://www.pge.com/solar/nemLanding/build?execution=e1s2',project, chrome=True)
portal.click_id('go-btn')

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
            portal.load_page('https://www.pge.com/solar/nemLanding/build?execution=e1s2')

        PGE(portal)

    elif menu == '2':
        portal.close()
        active = False

    run = 2
