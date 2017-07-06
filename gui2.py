'''
A quick gui for the pymca fitting

'''

from content import Content
import sys

from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine


if __name__ == '__main__':
    process_list = '/dls_sw/apps/savu/dawn_version/Savu/test_data/test_process_lists/pymca_test.nxs'
    model = Content()
    model.fopen(process_list)

    ##################################
    # Callbacks from QML
    ##################################

    def on_modified(idx, name, value):
        print(idx, name, value)
        prev = model.plugin_list.plugin_list[idx]['data'][name]
        if type(prev) == int:
            value = int(value)
        elif type(prev) == float:
            value = float(value)
        model.plugin_list.plugin_list[idx]['data'][name] = value

    def on_finished():
        print(model.plugin_list.plugin_list)
        # It is modified in place, do something with it

    ##################################
    # QML WINDOW
    ##################################

    QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    myApp = QGuiApplication(sys.argv)

    # Create a label and set its properties
    engine = QQmlApplicationEngine()
    engine.load(QUrl.fromLocalFile('Main.qml'))
    window = engine.rootObjects()[0]

    ##################################
    # Python <-> QML Bindings
    ##################################

    # Send plugins from python to QML
    for plugin in model.plugin_list.plugin_list:
        plugin['name'] = plugin['name'].tostring()  # numpy to str
        window.loadPlugins(plugin)  # QML Function

    # Connect QML signals to Python
    window.modified.connect(on_modified)
    window.finished.connect(on_finished)

    # Show window
    window.show()

    # Execute the Application and Exit
    sys.exit(myApp.exec_())
