#! Python27
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 09:48:41 2016
@author: nseelam

Portals Menu. This is the front end of what the user will see. Based on the user's Portal option, the back end 
functions/procedures will run.

- FiOps Portals contains the various functionalities of this tool.
- FiOps Functions contains a list of procedures defined as a function, for easy readability and access.
"""

import FiOps_Functions as Funcs
import FiOps_Portals as Portals

if __name__ == '__main__':
    
    print 'Welcome to FiOps Python Portal'
    print '\n'
    print 'Please begin by connecting to Sungevity\'s Database'
    cnx = Funcs.sql_fiops_connect()
    
    Active = True    
    while Active:
        print '\n'
        print 'Portals Menu:'
      
        print '1. Kina Milestone Submission'
        print '2. Data Upload File Creation'
        print '3. Exit'
        print '\n'
        
        while True:
            try:
                number = int(raw_input('Please enter the number associated with a task to proceed: '))
                if (number >=1 and number <=3):
                    break
                else:
                    print "Not a valid input. Please try again."
            except(TypeError, ValueError):
                print "Not an integer. Please try again."

        if number == 1:
            Portals.Kina_Submission_Portal(cnx)
        if number == 2:
            Portals.Kina_Upload_Portal(cnx)
        if number == 3:
            print 'Exitting...'
            Active = False
    
    cnx.close()
    
    exit()

            
        