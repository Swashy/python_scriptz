#!/usr/bin/python2.7
import subprocess
import time
import sys
import os

# Script to curl websites and then create a simple html page of the results

def curl (ip, siteArray):
  list = []
  for i in siteArray:
    # k is for insecure
    #theCommand = "curl -kI --header 'Host https://%s' https://%s "%(i,ip)
    theCommand = "curl -Is --max-redirs 3 -m 10 --header 'Host https://%s' https://%s "%(i,ip)
    result = subprocess.check_output('curl', '-Iks', '--max-redirs', '3', '-m10', '--header', '\'Host https://%s\''%(i), 'https://'
    result = result.communicate()[0].strip()
    print(result)
    list.append(result)
  return list

results = curl("45.33.124.204", ["tragichistory.com","google.com"])
print(results)


