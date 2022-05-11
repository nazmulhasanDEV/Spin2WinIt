# import os
# import base64
#
# code = base64.b64encode(os.urandom(8)).decode('ascii')
# print(code)

my_s = "343sdfskdjlsad"
word = "Geeks for geeks"

def CheckNumber(s):
    return any(s.isdigit() for s in s)

print(CheckNumber(my_s))

print(word.find('geeks'))