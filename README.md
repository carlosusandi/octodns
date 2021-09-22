# octodns-verifier
 
Welcome to Carlos' version of octodns!
 
Usage: verify <config> <domain> <nameserver>

config: contains new branch that we expect to have changes
domain: domain we are trying to verify
nameserver: use only one nameserver per invocation

for example:
verify config/branch.yaml dns-exercise.dev ns-179.awsdns-22.com

 this tool will create a new file change.yaml in the same folder where the verify script is
 
Note: the tool has been tested agains the following nameservers:
ns-179.awsdns-22.com
ns-1219.awsdns-24.org
ns-964.awsdns-56.net
ns-1775.awsdns-29.co.uk
 
 
 

