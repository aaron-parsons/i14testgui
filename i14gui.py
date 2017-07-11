
import gui
import os
BEAMLINE = os.environ["BEAMLINE"]
gui.main('/dls_sw/'+str(BEAMLINE)+'/software/analysis/pymca.nxs')
