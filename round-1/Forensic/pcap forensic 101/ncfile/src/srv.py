import string 

import sys

_raw_input = raw_input

sys.stdout.write("ATTACK NAME: ")
sys.stdout.flush()
a = _raw_input()
	  
sys.stdout.write("ATTACK CVE: ")
sys.stdout.flush()
b = _raw_input()

sys.stdout.write("haldlagiin daraa shiljsen directory: ")
sys.stdout.flush()
c = _raw_input()

if a == "log4j" and b == "CVE-2021-44228" and c == "webapps":
    with open('keyfile.txt') as f:
        for line in f:
            print(line)
else:
    print("Wrong")


