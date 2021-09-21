"""
Created on Mon Sep 20 20:51:16 2021

@author: carlo
"""
import dns.resolver
import dns.zone
import dns.query
import dns.message
import dns.rdtypes
import dns.rdata
import sys
import yaml
import os.path
import loadYaml 
 
if __name__ == "__main__": 
    def usage():
       print("usage: [master file] [domain] [dns server]")
     
    if(len(sys.argv) != 4):
       usage()
     
    config = sys.argv[1]
    domain = sys.argv[2]
    name_server = sys.argv[3]
     
    expected = loadYaml.LoadYamlFile(config)
    
    print("Getting Nameserver info...")
    primary_resolver = dns.resolver.Resolver()
    resolver_ip_lookup_result = primary_resolver.resolve(name_server, 'A')
    print(f"nameserver={name_server}, IP={resolver_ip_lookup_result[0]}") 
    
    #setup private nameserver here. You name to specify its IP address
    private_resolver = dns.resolver.Resolver()
    private_resolver.nameservers = [resolver_ip_lookup_result[0].to_text()]
     
    #get the values for each dns name and compare them
    #expected name from yaml file
    #actual name from nameserver
    changes = {}
    
    for expected_entry in expected:
       expected_name = expected_entry.dns_name
       expected_type = expected_entry.dns_values["type"]
       expected_ttl = expected_entry.dns_values["ttl"]
       expected_value = expected_entry.dns_values["value"]
     
       entries = private_resolver.resolve(expected_entry.dns_name + '.' + domain, expected_type)
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
 
 
 
 
            
 

