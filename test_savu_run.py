'''
test savu can run form pythoh

'''

from subprocess import Popen, PIPE
import select

# def follow(thefile):
#     thefile.seek(0,2)
#     while True:
#         line = thefile.readline()
#         if not line:
#             time.sleep(0.1)
#             continue
#         yield line
# 
# if __name__ == '__main__':
#     import time
#     import os
#     log_file = "/dls/i08/data/2017/cm16789-3/processing/savu/10471_pymca/user.log"
#     while not os.path.exists(log_file):
#         time.sleep(1)
#     logfile = open(log_file,"r")
#     loglines = follow(logfile)
#     for line in loglines:
#         print line,


