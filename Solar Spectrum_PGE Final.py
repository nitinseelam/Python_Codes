import pyPortal as p
import bi
import datetime as dt
import time
import getpass

def PGEfinal(portal):
    portal.fill_text_id('electric_account_number',portal.data['p.UTILITY_ACCOUNT_NUMBER__C'])
    portal.fill_text_id('meter_number',portal.data['p.UTILITY_ELECTRIC_METER_NUMBER__C'])
    captcha = raw_input('Please enter Security captcha into command prompt and press Enter.')
    portal.fill_text_id('captchaValid',captcha)
    portal.click_id('btn-next-1')
    portal.click_id('btn-next-1')
    if portal.data['fp.NAME'] in ['sungevity_cash','sungevity_sunrun_cash']:
        portal.click_xpath("//form[@id='partyForm']/fieldset/div[2]/div/div/input")
        portal.fill_text_id('systemCost',str(portal.data['sp.PURCHASE_PRICE__C']))
        portal.click_xpath("//form[@id='partyForm']/div/fieldset[2]/div[2]/div[2]/div/input")
    else:
        portal.click_xpath("//form[@id='partyForm']/fieldset/div[2]/div[2]/div/input")
        portal.fill_text_id('itc',str(portal.data['p.SYSTEM_KW_STC__C']*3530))
        portal.fill_text_id('developerNameSale','Solar Spectrum LLC')
        if 'lease' in portal.data['p.SELECTED_FUNDING_PRODUCT__C']:
            portal.select_drop_down_name('contractType','Lease')
        else:
            portal.select_drop_down_name('contractType','PPA')
    portal.click_xpath("//form[@id='partyForm']/fieldset[2]/div/div[2]/div/input")
    portal.click_xpath("//form[@id='partyForm']/fieldset[3]/div/div[2]/div/input")
    portal.fill_text_id('installerCompanyName','Solar Spectrum LLC')
    portal.fill_text_id('installerCslbLicenseNumber','909236')
    portal.fill_text_id('contractorStreetAddress','66 Franklin St. #310')
    portal.fill_text_id('contractorCity','Oakland')
    portal.fill_text_id('contractorZip','94607')
    portal.fill_text_id('contractorEmail1','forms@solarspectrum.com')
    portal.click_xpath("//form[@id='partyForm']/fieldset[5]/div/div/div[2]/div[2]/div/input")
    user = getpass.getuser()
    query = '''SELECT u.NAME as name
        , u.PHONE as phone
        FROM user as u
        WHERE u.COMMUNITYNICKNAME = %(user)s'''
    df = bi.query_bi(query,params_in={'user':user})
    portal.fill_text_id('contractorPhoneNumber',df['phone'][0])
    portal.fill_text_id('preparerName',df['name'][0])
    portal.fill_text_id('preparerCompanyName', 'Solar Spectrum LLC')
    portal.fill_text_id('preparedDate',dt.date.today().strftime("%m/%d/%Y"))
    portal.click_id('interconnection')

    side = raw_input('Customer side (c) or line side tap (l)?')
    if side == 'C' or side == 'c':
        portal.click_xpath("//form[@id='interconnectionForm']/fieldset/div/div/div/div/input")
        disco = raw_input('How many disconnects? (0/1/2)')
        if disco == '0':
            portal.click_xpath("//div[@id='displayInstallation']/fieldset/div/div/div/input")
        elif disco == '1':
            portal.click_xpath("//div[@id='displayInstallation']/fieldset/div/div[2]/div/input")
            portal.click_xpath("//div[@id='acdDistance']/fieldset/div/div/div/div/input")
        elif disco == '2' :
            portal.click_xpath("//div[@id='displayInstallation']/fieldset/div/div[3]/div/input")
        portal.click_xpath("//div[@id='dih']/fieldset/div/div/div/div/input")
    elif side == 'L' or side == 'l':
        portal.click_xpath("//form[@id='interconnectionForm']/fieldset/div/div/div[2]/div/input")
        portal.click_xpath("//div[@id='page1']/div/input")
        portal.click_xpath("//div[@id='pgeBP']/fieldset/div[2]/div/div[2]/div/input")
    portal.click_id('showVarianceModal')
    portal.click_id('pvType')
    portal.click_id('btn-next-1')
    portal.select_drop_down_name('mountingMethod','Rooftop')
    portal.select_drop_down_name('trackingType','Fixed')
    array = portal.arrays[0]
    portal.fill_text_id('azimuth',str('{0:g}'.format(array['azimuth'],0)))
    portal.fill_text_id('tilt',str('{0:g}'.format(array['pitch'],0)))
    portal.click_xpath("//div[@id='pv']/fieldset/div[2]/div/div/div/input")
    time.sleep(1)
    portal.click_id('thirdParty')
    portal.fill_text_id('listName','Solar Spectrum LLC')
    portal.click_id('btn-next-1')

    #determines # and type of unique inverters
    inverter = str(portal.data['p.SYSTEM_INVERTER_NAMES__C'])
    if ';' in inverter:
        inv_split = inverter.split('; ')
        inv_num = len(inv_split)
        x=0
        mod_quant= [0,0]
        while x < inv_num:
            #for loop sums # modules for each unique inverter
            for array in portal.arrays:
                if array['inverter model'] in inv_split[x]:
                    mod_quant[x] = mod_quant[x] + array['num modules']
            #inputs inverter info (have to select from dropdown, not exact name match), multiple if unique inverters
            portal.select_drop_down('inverter-manu_{}_0'.format(x),array['inverter manu'])
            if 'SE 3000A-US (240V)' in inv_split[x]:
                portal.select_drop_down('inverter-Model_{}_0'.format(x),'SE3000 (240V) w/ -ER-US or A-US (240V)')
            if 'SE 3800A-US (240V)' in inv_split[x]:
                portal.select_drop_down('inverter-Model_{}_0'.format(x),'SE3800 (240V) w/ -ER-US or A-US (240V)')
            if 'SE 4000A-US (240V)' in inv_split[x]:
                portal.select_drop_down('inverter-Model_{}_0'.format(x),'SE4000 (240V) w/ -ER-US or A-US (240V)')
            if 'SE 5000A-US (240V)' in inv_split[x]:
                portal.select_drop_down('inverter-Model_{}_0'.format(x),'SE5000 (240V) w/ -ER-US or A-US (240V)')
            if 'SE 6000A-US (240V)' in inv_split[x]:
                portal.select_drop_down('inverter-Model_{}_0'.format(x),'SE6000 (240V) w/ -ER-US or A-US (240V)')
            if 'SE 7600A-US (240V)' in inv_split[x]:
                portal.select_drop_down('inverter-Model_{}_0'.format(x),'SE7600 (240V)')
            if 'SE 10000A-US (240V)' in inv_split[x]:
                portal.select_drop_down('inverter-Model_{}_0'.format(x),array['inverter model'])
            if 'SE 11400A-US (240V)' in inv_split[x]:
                portal.select_drop_down('inverter-Model_{}_0'.format(x),array['inverter model'])
            #inputs module data per inverter
            portal.fill_text_id('quantity_{}_0'.format(x),1)
            portal.select_drop_down('inverter-phase_{}_0'.format(x),'1')
            portal.select_drop_down('pvPanel-manu_{}_0'.format(x),array['module manu'])
            portal.select_drop_down('pvPanel-Model_{}_0'.format(x),array['module model'])
            portal.fill_text_id('pvPanel-quantity_{}_0'.format(x),'{0:g}'.format(mod_quant[x],0))
            if x < (inv_num-1):
                portal.click_id('addGenerator')
            x += 1
        if disco == '1' or disco == '2':
            portal.click_id('disconnect_checkbox_1_0')
    else:
        #inputs single inverter and module info
        portal.select_drop_down('inverter-manu_0_0',array['inverter manu'])
        if array['inverter model'] == 'SE 3000A-US (240V)':
            portal.select_drop_down('inverter-Model_0_0','SE3000 (240V) w/ -ER-US or A-US (240V)')
        if array['inverter model'] == 'SE 3800A-US (240V)':
            portal.select_drop_down('inverter-Model_0_0','SE3800 (240V) w/ -ER-US or A-US (240V)')
        if array['inverter model'] == 'SE 4000A-US (240V)':
            portal.select_drop_down('inverter-Model_0_0','SE4000 (240V) w/ -ER-US or A-US (240V)')
        if array['inverter model'] == 'SE 5000A-US (240V)':
            portal.select_drop_down('inverter-Model_0_0','SE5000 (240V) w/ -ER-US or A-US (240V)')
        if array['inverter model'] == 'SE 6000A-US (240V)':
            portal.select_drop_down('inverter-Model_0_0','SE6000 (240V) w/ -ER-US or A-US (240V)')
        if array['inverter model'] == 'SE 7600A-US (240V)':
            portal.select_drop_down('inverter-Model_0_0','SE7600 (240V)')
        if array['inverter model'] == 'SE 10000A-US (240V)':
            portal.select_drop_down('inverter-Model_0_0',array['inverter model'])
        if array['inverter model'] == 'SE 11400A-US (240V)':
            portal.select_drop_down('inverter-Model_0_0',array['inverter model'])
        portal.fill_text_id('quantity_0_0','{0:g}'.format(portal.data['s.TOTAL_NUMBER_OF_INVERTERS__C'],0))
        portal.select_drop_down('inverter-phase_0_0','1')
        portal.select_drop_down('pvPanel-manu_0_0',array['module manu'])
        portal.select_drop_down('pvPanel-Model_0_0',array['module model'])
        portal.fill_text_id('pvPanel-quantity_0_0','{0:g}'.format(portal.data['s.TOTAL_NUMBER_OF_PANELS__C'],0))
    if disco == '1' or disco == '2':
        portal.click_id('disconnect-manu_1_0')
        raw_input('Please enter AC Disconnect info on portal and hit enter when done.')
    LD = raw_input('Is line diagram basic (b) or custom (c)?')
    if LD == 'b' or LD =='B':
        voltage = raw_input('Panel Voltage?')
        mainbreaker = raw_input('Main Breaker Amperage?')
        pvbreaker = raw_input('PV Breaker Size?')
        portal.fill_text_id('pvPanelVoltage',voltage)
        portal.fill_text_id('pvMainBreaker',mainbreaker)
        portal.fill_text_id('pvBreakerSize',pvbreaker)
    else:
        portal.click_xpath("//form[@id='form1']/fieldset[3]/div/div[3]/fieldset/div/div/div/input")
    if portal.data['s.TOTAL_NAMEPLATE_RATING__C'] > 11.0:
        portal.fill_text_id('scir','10000')
    if disco == '1' or disco == '2':
        if ';' in inverter:
            portal.click_xpath("//form[@id='form1']/fieldset[7]/div/fieldset/div/div[2]/div/input")
        else:
            portal.click_xpath("//form[@id='form1']/fieldset[5]/div/fieldset/div/div[2]/div/input")
    else:
        if ';' in inverter:
            portal.click_xpath("//form[@id='form1']/fieldset[6]/div/fieldset/div/div[2]/div/input")
        else:
            portal.click_xpath("//form[@id='form1']/fieldset[4]/div/fieldset/div/div[2]/div/input")
    portal.click_id('btn-next-1')
    raw_input('Please review page, checking for relevant warnings, and hit Enter to continue.\n')
    portal.click_id('btn-next-1')
    raw_input('Please complete permit and payment info and submit application PGE web portal.\n\nPress Enter to return to Menu.')

project = raw_input('\nPG&E Online Portal (Final)\n\nProject #? ')
portal = p.Portal('https://www.pge.com/solar/nemLanding/build?execution=e1s2',project, chrome=True)
portal.click_xpath("//div[@id='goImage3']/input")

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

        PGEfinal(portal)

    elif menu == '2':
        portal.close()
        active = False

    run = 2
