
import gui
import os
BEAMLINE = os.environ["BEAMLINE"]
gui.main('/dls_sw/'+str(BEAMLINE)+'/software/analysis/pymca.nxs')
# gui.main('/home/clb02321/DAWN_stable/I14GUI/pymca.nxs')
