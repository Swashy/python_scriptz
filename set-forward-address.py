#!/usr/bin/python2.7
from __future__ import unicode_literals
from prompt_toolkit import prompt
import getpass
import sys
import os
import subprocess
from termcolor import colored
import re
import time

# Simple script to add aliases/forwards for addresses in iRedAdmin. Pro version allows this through web interface, but not the free version, so this script gets around that
# by directly modifing the database.

def main():
  user=getpass.getuser()
  if user != 'admin':
    print("You need to run this script as user " + colored('Admin', 'green') + " for it to work")
  else:
    addressToChange = prompt("Enter the email address you'd like to set forwarding for: \n> ")
    addressToChange = addressToChange.strip()
    getAliases = "mysql --defaults-file=/home/admin/.my.cnf -e \"SELECT goto FROM alias WHERE address = '%s';\" | sed 1d"%(addressToChange)
    aliases = subprocess.Popen(getAliases, shell=True, stdin=None, stdout=subprocess.PIPE)
    #retunred value is a tuple, so let's take the first index, and  then strip the result
    aliases = (aliases.communicate()[0]).strip()

    # If the value is "falsy", then it's empty or spaces
    if not aliases:
      print(colored("The address does not exist or is mispelled.", 'red'))
      print("If this is a new address, add it through the irdeadmin interface: https://website.net/iredadmin")
      continuing = 'n'
    else:
      print(colored("The current alias(es) for " + colored('{0}', 'cyan').format(addressToChange) + " are " + colored('\'{0}\'.', 'cyan').format(aliases) + " Would you like to modify anyway? (y/n)"))
      continuing = prompt("> ")

    if continuing[0] == 'y':
      newAliases = prompt("Enter in the new alias(es) that you'd like to set.\nFor multiple email addresses enter a comma-separated list quotes, e.g. \"mary@outlook.com, john@gmail.com\"\n> ")

      # If there's a comma and it's not surrounded by quotes, fail.
      if (newAliases.find(',') != -1 and not (newAliases[0] == "\"" and newAliases[-1] == "\"")):
        print("List of emails entered incorrectly!")
        continuing = 'n'
      # If there's a space, but there's no comma, fail
      elif (newAliases.find(' ') != -1) and not (newAliases.find(',') != -1):
        print("List of emails entered incorrectly! 2")
        continuing = 'n'
      else:
        print("You entered: " + colored('{0}', 'cyan').format(newAliases) + "\nAre you sure you'd like to set this as the alias? (y/n)")
        continuing = prompt("> ")
      if continuing[0] == 'y':
        #Do the change.
        newAliases = "".join(newAliases.split())
        theCommand = "mysql --defaults-file=/home/admin/.my.cnf -e \"UPDATE alias SET goto = '%s' WHERE address='%s';\""%(newAliases,addressToChange)
        #print(theCommand)
        output = subprocess.Popen(theCommand, shell=True, stdin=None, stdout=subprocess.PIPE)
        #Confirm the change.
        getAliases = "mysql --defaults-file=/home/admin/.my.cnf -e \"SELECT goto FROM alias WHERE address = '%s';\" | sed 1d"%(addressToChange)
        output = subprocess.Popen(getAliases, shell=True, stdin=None, stdout=subprocess.PIPE)
        output = str(output.communicate()[0])
        #print("Done. Current aliases are now '%s'"%(output))
        print("Done.")
      else: print("Quitting")
    else: print("Quitting")
try:
  main()
except KeyboardInterrupt:
  print(" Keyboard Interrupt")
except:
  raise
#  print("Script Failure")
