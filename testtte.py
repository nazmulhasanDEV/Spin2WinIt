import os
import base64

code = base64.b64encode(os.urandom(8)).decode('ascii')
print(code)