'''
test savu can run form pythoh

'''

from subprocess import Popen, PIPE
import savu
savu_version = '2.0_stable'
process_list = '/dls/i08/data/2017/cm16789-3/processing/aaron/i08_pymca_process.nxs'
datafile = '/dls/i08/data/2017/cm16789-3/nexus/i08-10481.nxs'
outputfolder = '/dls/i08/data/2017/cm16789-3/processing/aaron/'
outputdir = 'pickles/'
launcher_script = savu.savuPath.split('savu')[0]+'mpi/dls/savu_launcher.sh'
p = Popen(['sh',launcher_script,savu_version,datafile,process_list,outputfolder,'-f',outputdir], stdin=PIPE, stdout=PIPE, stderr=PIPE)
output, __err = p.communicate()
# print output, __err