import string 

import sys

_raw_input = raw_input

sys.stdout.write("Victim windows ip address: ")
sys.stdout.flush()
a = _raw_input()
	  
sys.stdout.write("Victim windows hostname: ")
sys.stdout.flush()
b = _raw_input()

sys.stdout.write("User account name on victim computer: ")
sys.stdout.flush()
c = _raw_input()

sys.stdout.write("Malware family of malware on victim:")
sys.stdout.flush()
d = _raw_input()

if a == "172.16.4.206" and b == "DESKTOP-V0FEH1L" and c == "alfonso.paternoster" and d=="qakbot":
    with open('keyfile.txt') as f:
        for line in f:
            print(line)
else:
    print("Wrong")


