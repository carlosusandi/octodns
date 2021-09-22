"""
verify: reads a config from a local yaml file and compares it with a remote dns server
        it creates an output file change.yaml that will register only the diffs

Usage: 
verify <config> <domain> <nameserver>

config: contains new branch that we expect to have changes
domain: domain we are trying to verify
nameserver: use only one nameserver per invocation

example: verify config/branch.yaml dns-exercise.dev ns-179.awsdns-22.com

Created on Mon Sep 20 20:51:16 2021

@author: Carlos Usandivaras
"""
import dns
import sys
import yaml
import os.path
import loadYaml 
import getdnsinfo
 
if __name__ == "__main__": 
    
    def usage():
       print("usage: [config file] [domain] [dns server]")
                  
    if(len(sys.argv) != 4):
        usage()     
        
    config = sys.argv[1]
    domain = sys.argv[2]
    nameserver = sys.argv[3]
     
    #reads the config file (yaml) and loads it into a list
    expected = loadYaml.LoadYamlFile(config)
    
    # gets an Answer from private nameserver
    p_resolver = getdnsinfo.get_dns_info(domain, nameserver)     
    
    if p_resolver != None:
        changes = {}
        
        #get the values for each dns name and compare them
        #expected name from yaml file
        #actual name from nameserver
        for expected_entry in expected:
            expected_name = expected_entry.dns_name
            expected_type = expected_entry.dns_values["type"]
            expected_ttl = expected_entry.dns_values["ttl"]
            expected_value = expected_entry.dns_values["value"]
         
            try:
                entries = p_resolver.resolve(expected_entry.dns_name + '.' + domain, expected_type)
            except dns.exception.DNSException as e:
                print(f"error getting dns entry{expected_entry}, \nError: {e}")
               
            if(len(entries.rrset) != 1):
                raise Exception("something went wrong looking up dns name")
          
            actual_name = entries.rrset.name
            actual_type = dns.rdatatype.to_text(entries.rrset.rdtype)
            actual_ttl = entries.rrset.ttl
            actual_value = entries[0].to_text().replace('"', '')
          
            #compare them
            if(expected_value != actual_value):
                print("[CHG] ", expected_name, " records did not match")
                changes[expected_name] = {}
                changes[expected_name]["add"] = expected_value
                changes[expected_name]["delete"] = actual_value
            else:
                print("[OK] ", expected_name, " records matched")
         
        #write output to changes.yaml file (only changes)
        if(len(changes) > 0):
            with open(os.path.split(config)[0] + "/changes.yaml", "w") as f:
                yaml.dump(changes, f)
 
 
 
 
            
 

