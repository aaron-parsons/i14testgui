'''
A quick gui for the pymca fitting

'''

from content import Content
from PyQt5.QtWidgets import QApplication, QWidget, QFormLayout, QSpinBox, QTextEdit, QDoubleSpinBox, QGridLayout, QLabel,QPushButton
from PyQt5.QtGui import QFont
import sys
import os

# the following classes could use a refactor since it's all duplication

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
        print val
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
        print val
        self.parent.model.modify(self.parent.plugin_number, self.key, val)


class SavuTextBox(QTextEdit):
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
        value = str(self.toPlainText().rstrip('\n'))
        print value
        self.parent.model.modify(self.parent.plugin_number, self.key, value)


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
        layout.addWidget(save_stuff,1,1)
        self.setLayout(layout)
        self.setWindowTitle('I14 XRF GUI')
        self.show()

class SaveDialog(QWidget):
    def __init__(self, model):
        self.model = model
        self.output_dir_exists = None
        super(SaveDialog, self).__init__()
        
        self.visit  = QTextEdit()
        self.visit.setFixedHeight(2.0*self.visit.fontMetrics().height())
        
        self.save_name  = QTextEdit()
        self.save_name.setFixedHeight(2.0*self.save_name.fontMetrics().height())
        
        self.scan = QTextEdit()
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

        self.setLayout(form)

    def getVisitDirectory(self):
        visit = str(self.visit.toPlainText().rstrip('\n').rstrip())
        return '/dls/i14/data/2017/%s/' % visit
    
    def getSaveName(self):
        return str(self.save_name.toPlainText().rstrip('\n').rstrip())

    def getOutputDirectory(self):
        op = self.getVisitDirectory() + 'processing/savu'
        if not self.output_dir_exists:
            print("Creating output directory....")
            try:
                os.mkdir(op)
            except OSError:
                pass
            else:
                raise
            print("Done.")
            self.output_dir_exists = True
        return op 
    
    def getDataPath(self):
        scan_number = str(self.scan.toPlainText().rstrip('\n').rstrip())
        return self.getVisitDirectory()+'i14-%s.nxs' % scan_number

    def saveButtonChecked(self):
        if self.save_button.isDown():
            full_save_path  = self.getOutputDirectory()+os.sep + self.getSaveName()
            self.model.save(full_save_path)

    def runButtonChecked(self):
        if self.run_button.isDown():
            import subprocess
            print "I should run something here"
            print "On data" + self.getDataPath()

def main(process_list):
    app = QApplication([])
    model = Content()
    model.fopen(process_list)
    ex = PluginEditor(model)
    sys.exit(app.exec_())



if __name__ == '__main__':
    process_list =main(sys.argv[1])
    main()

