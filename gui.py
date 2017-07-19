'''
A quick gui for the pymca fitting

'''

from content import Content
from PyQt5.QtWidgets import QApplication, QWidget, QFormLayout, QSpinBox, QLineEdit, QDoubleSpinBox, QGridLayout, QLabel,QPushButton, QTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, Qt
import sys
import os
from subprocess import Popen, PIPE
try:
    import savu
except:
    ImportError("Savu not on the path")

# the following classes could use a refactor since it's all duplication
DEBUG = False

class SavuIntSpinBox(QSpinBox):
    '''
    widget that does spinners for ints
    '''
    def __init__(self, parent, key, value):
        super(SavuIntSpinBox, self).__init__(parent)
        self.parent = parent
#         self.widget = QSpinBox(parent)
        self.setValue(value)
        self.key = key
        self.setFixedHeight(3.0*self.fontMetrics().height())
        self.setSingleStep(1)
        self.valueChanged.connect(self.updatevalue)

    def updatevalue(self):
        val = str(self.value())
#         print val
        self.parent.model.modify(self.parent.plugin_number, self.key, val)

class SavuDoubleSpinBox(QDoubleSpinBox):
    '''
    widget that does spinners for floats
    '''
    def __init__(self, parent, key, value):
        super(SavuDoubleSpinBox, self).__init__(parent)
        self.parent = parent
#         self.widget = QSpinBox(parent)
        self.setValue(value)
        self.key = key
        self.setFixedHeight(3.0*self.fontMetrics().height())
        self.setSingleStep(0.1)
        self.valueChanged.connect(self.updatevalue)

    def updatevalue(self):
        val = str(self.value())
#         print val
        self.parent.model.modify(self.parent.plugin_number, self.key, val)


class SavuTextBox(QLineEdit):
    '''
    widget that does text editing
    '''
    def __init__(self, parent, key, value):
        super(SavuTextBox, self).__init__(parent)
        self.parent = parent
#         self.widget = QSpinBox(parent)
        self.setText(str(value))
        self.key = key
        self.setFixedHeight(3.0*self.fontMetrics().height())
        self.textChanged.connect(self.updatevalue)

    def updatevalue(self):
        value = str(self.text().rstrip('\n'))
#         print value
        self.parent.model.modify(self.parent.plugin_number, self.key, value)

class SavuLogFileTextBox(QTextEdit):
    def __init__(self):
        super(SavuLogFileTextBox, self).__init__()
        self.setReadOnly(True)
        self.filehandle = None
        self.filepath = None
        self.setDisabled(True)

    def setFile(self, filepath):
        self.filepath = filepath

    def update_text(self):
        if self.filepath:
            if not os.path.exists(self.filepath):
                self.setText("Nothing to display")
            elif os.path.exists(self.filepath) and not self.filehandle:
                self.filehandle = open(self.filepath,"r")
                self.clear()
            elif os.path.exists(self.filepath) and self.filehandle:
                lines = self.filehandle.readlines()
                self.insertPlainText("".join(lines))
                self.verticalScrollBar().setValue(self.verticalScrollBar().maximum()) # autoscroll to the bottom to view updated content.
#                 self.setText(lines)
            else:
                print "munchkins"
        else:
            self.setText("Nothing to display")
        

class PluginForm(QWidget):
    '''
    widget that does the form display for the plugins
    '''
    def __init__(self,parent, plugin_number):
        super(PluginForm, self).__init__()
        self.model = parent.model
        self.plugin_list = self.model.plugin_list.plugin_list
        self.initUI(plugin_number)

    def initUI(self, plugin_number):

        self.plugin_number = str(plugin_number + 1) # used in the widgets
        form = QFormLayout()
        for key, value in self.plugin_list[plugin_number]['data'].iteritems():
            if type(value) == float:
                form.addRow(key, SavuDoubleSpinBox(self, key, value))
            if type(value) == int:
                form.addRow(key, SavuIntSpinBox(self, key, value))
            if type(value) == str:
                form.addRow(key, SavuTextBox(self, key, value))
            if type(value) == type([]):
                form.addRow(key, SavuTextBox(self, key, value))
            else:
                print("I have missed some variables out because I didn't know how to display them!")
        self.setLayout(form)
#         self.resize(250, 250)
#         self.move(300, 300)

    def getModel(self):
        return self.model
    

class PluginEditor(QWidget):
    '''
    this does the display for all the plugins including titles and buttons to do with the model
    '''
    def __init__(self, model):
        super(PluginEditor, self).__init__()
        layout = QGridLayout()
        layout.setColumnStretch(0,3)
        layout.setColumnStretch(1,3)
        self.model = model
        self.plugin_list = self.model.plugin_list.plugin_list
        k=0
        for plugin_number in range(len(self.plugin_list)):
            name = self.plugin_list[plugin_number]['name']
            myFont=QFont()
            myFont.setBold(True)
            myFont.setUnderline(True)
            l1 = QLabel()
            l1.setText(name)
            l1.setFont(myFont)
            pluginform = PluginForm(self, plugin_number)
            layout.addWidget(l1,k,0)
            layout.addWidget(pluginform,k+1,0)
            k+=2
        save_stuff = SaveDialog(self.model)
        layout.addWidget(save_stuff,1,1,k,1)
        self.setLayout(layout)
        w = 2280; h = 1520
        self.resize(w/2,h/2)
        self.setWindowTitle('Savu Processing')
        self.show()


class SaveDialog(QWidget):
    def __init__(self, model):
        self.model = model
        self.output_dir_exists = None
        super(SaveDialog, self).__init__()
        
        self.visit  = QLineEdit()
        self.visit.setFixedHeight(2.0*self.visit.fontMetrics().height())
        self.visit.setText(str(self.getCurrentVisit())) # by default its the current visit for $BEAMLINE

        self.save_name  = QLineEdit()
        self.save_name.setFixedHeight(2.0*self.save_name.fontMetrics().height())
        self.save_name.setText(str(self.getInitialProcessList()))
        
        self.scan = QLineEdit()
        self.scan.setFixedHeight(2.0*self.scan.fontMetrics().height())

        form = QFormLayout()

        form.addRow('Visit:',self.visit)
        form.addRow('Process List Name:',self.save_name)

        self.save_button = QPushButton()
#         self.save_button.setCheckable(True)
        self.save_button.setText('Save process list')
        self.save_button.pressed.connect(self.saveButtonChecked)
        form.addWidget(self.save_button)

        form.addRow('Scan Number:',self.scan)

        self.run_button = QPushButton()
#         self.run_button.setCheckable(True)
        self.run_button.setText('Run process!')
        self.run_button.pressed.connect(self.runButtonChecked)
        form.addWidget(self.run_button)
        
        self.log_file_display = SavuLogFileTextBox()
#
        form.addWidget(self.log_file_display)
#         
        self.timer = QTimer()
        self.timer.timeout.connect(self.log_file_display.update_text)
        self.timer.start(1000)        

        self.setLayout(form)

    def getInitialProcessList(self):
        return self.model.filename.split(os.sep)[-1]
        
    def getCurrentVisit(self):
        p = Popen(['sh','/dls_sw/apps/mx-scripts/visit_tools/currentvisit',os.environ["BEAMLINE"]], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, __err = p.communicate()
        return output

    def getVisitDirectory(self):
        visit = str(self.visit.text().rstrip('\n').rstrip())
        return '/dls/%s/data/2017/%s/' % (str(os.environ['BEAMLINE']),visit)
    
    def getSaveName(self):
        return str(self.save_name.text().rstrip('\n').rstrip())

    def getOutputDirectory(self):
        op = self.getVisitDirectory() + 'processing/savu/'
        if not self.output_dir_exists:
            print("Creating output directory....")
            try:
                os.mkdir(op)
            except OSError:
                pass
            except Exception as e:
                raise e
                
            print("Done.")
            self.output_dir_exists = True
        return op 
    

    def getScanNumber(self):
        scan_number = str(self.scan.text().rstrip('\n').rstrip())
        return scan_number

    def getDataPath(self):
        scan_number = self.getScanNumber()
        if str(os.environ['BEAMLINE'])=='i14':
            return self.getVisitDirectory()+'i14-%s.nxs' % scan_number
        elif str(os.environ['BEAMLINE'])=='i08':
            return self.getVisitDirectory()+'nexus/i08-%s.nxs' % scan_number
        elif str(os.environ['BEAMLINE'])=='i18':
            return self.getVisitDirectory()+'i18-%s.nxs' % scan_number
        else:
            raise NameError("I don't recognise this beamline!")

    def saveButtonChecked(self):
        if self.save_button.isDown():
            full_save_path  = self.getOutputDirectory()+os.sep + self.getSaveName()
            self.model.save(full_save_path)

    def runButtonChecked(self):
        if self.run_button.isDown():
            global DEBUG
            if DEBUG:
                print "I should run something here"
                print "On data" + self.getDataPath()
            else:
                self.runSavu(self.getDataPath(), self.getOutputDirectory()+os.sep + self.getSaveName(), self.getOutputDirectory())


    def getSavuOutputDirectory(self):
        path = self.getOutputDirectory() + os.sep + self.getScanNumber()+'_'+self.getSaveName().split('.')[0]
        return path


    def getProcessFolder(self):
        return self.getScanNumber() + '_' + self.getSaveName().split('.')[0]

    def runSavu(self, datafile, process_list, output_directory):
        #launcher_script = savu.savuPath.split('savu')[0]+'mpi/dls/savu_launcher.sh'#
        a = Popen(['which','savu_launcher.sh'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        b = a.stdout.readline()
        launcher_script = b.splitlines()[0]
        print launcher_script
        savu_version = '2.0_stable'
        p = Popen(['sh',launcher_script,savu_version,datafile,process_list,output_directory,'-f',self.getProcessFolder()], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, __err = p.communicate()
        self.log_file_display.clear()
        self.log_file_display.filehandle = None # need to reinitialise these for second call.
        self.log_file_display.filepath = None # need to reinitialise these
        self.log_file_display.setText('Process started. Waiting for log file....')
        self.log_file_display.setFile(self.getSavuOutputDirectory()+os.sep+'user.log')
#         print "thing the log should be in:", self.getSavuOutputDirectory()+os.sep+'user.log'

def main(process_list):
    app = QApplication([])
    model = Content()
    model.fopen(process_list)
    ex = PluginEditor(model)#
    sys.exit(app.exec_())

if __name__ == '__main__':
    process_list =main(sys.argv[1])
    main()

