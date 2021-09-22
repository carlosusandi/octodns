# -*- coding: utf-8 -*-
"""
loadYaml: loads a yaml file into a local list

Created on Mon Sep 20 20:51:16 2021

@author: Carlos Usandivaras
"""
import dns

def get_dns_info(domain, name_server):
        #returns resolver object from private dns namserver
        print("Getting private nameserver info...")        
        private_resolver = None
        
        try:
            primary_resolver = dns.resolver.Resolver()
            resolver_ip_lookup_result = primary_resolver.resolve(name_server, 'A')                   
            #to setup private nameserver need to pass its IP address
            private_resolver = dns.resolver.Resolver()
            private_resolver.nameservers = [resolver_ip_lookup_result[0].to_text()]            
        except dns.exception.DNSException as e:
             print(f"error setting private DNS server {name_server}, \nError: {e}")
        
        
        return private_resolver 