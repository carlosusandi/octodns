# -*- coding: utf-8 -*-
"""
loadYaml:
#Function to load a yaml file into a local list
Created on Mon Sep 20 20:51:16 2021

@author: Carlos Usandivaras
"""
import yaml


def LoadYamlFile(file_name):
    '''
    class instance looks like this:
        'foo.sub':
            ttl: 60
            type: A
            value: 2.2.3.3
   '''
    class dnsEntry:
       def __init__(self, dns_name, dns_values):
           self.dns_name = dns_name
           self.dns_values = dns_values
     
    dnsLocalList = []
    dictionary = {}
    print("Loading YAML file...")
    
    #read input file and load into dict
    with open(file_name, 'r') as stream:
        try:
            dictionary = yaml.load(stream, Loader=yaml.FullLoader)
                        
        except yaml.YAMLError as e:
            print(f"Error parsing yaml file {file_name}, \nError: {e}")
    
    if dictionary:
        print("YAML file loaded")
        for key, value in dictionary.items():
            dnsLocalList.append(dnsEntry(key, value))

    return dnsLocalList 
 