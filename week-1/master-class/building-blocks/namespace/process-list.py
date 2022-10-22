#!/usr/bin/env python

import subprocess
ps = subprocess.Popen("ps -U 0", shell=True, stdout=subprocess.PIPE)
print ps.stdout.read()
ps.stdout.close()
ps.wait()
