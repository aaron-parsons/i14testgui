import QtQuick 2.6
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.3

ApplicationWindow {

    width: 1000
    height: 800

    signal modified(int idx, string attr, variant value)
    signal finished()

    // ==========================
    // Simple UI
    // ==========================

    RowLayout {
        anchors.fill: parent
        anchors.margins: 10

        // Left column
        // A list view that renders one pluginDelegate
        // for each item in pluginModel
        ListView {
            id: forms
            Layout.fillWidth: true
            Layout.fillHeight: true

            model: pluginModel
            delegate: pluginDelegate
        }

        // Right Column: TODO, just a button
        Item {
            id: save
            Layout.fillWidth: true
            Layout.fillHeight: true

            Row {
                width: parent.width
                Button {
                    activeFocusOnPress: true
                    text: "Save"
                    onClicked: {
                        finished()
                    }
                }
            }
        }
    }

    // ==========================
    // Plugin UI
    // ==========================
    // Defines how to render each of the plugin containers

    ListModel {
        id: pluginModel
    }

    Component {
        id: pluginDelegate

        Column {
            width: parent.width

            // Header
            Rectangle {
                width: parent.width
                height: 30
                color: 'blue'
                radius: 3

                Text {
                    anchors.centerIn:parent
                    text: name
                    color: 'white'
                }
            }

            // Param container
            // Contains another list view that renders `pdata` attribute
            GroupBox {
                width: parent.width

                ListView {
                    spacing: 3
                    model: pdata
                    width: parent.width
                    delegate: paramDelegate
                    onContentHeightChanged: {
                        this.height = this.contentHeight;
                    }
                }

            }
        }
    }

    // ==========================
    // Param UI
    // ==========================
    // Defines how to render each of the key/value pairs

    Component {
        id: paramDelegate

        // It is going to be a row (horizontal layout)
        RowLayout {
            id: root
            width: parent.width
            height: 30

            // First the name in a standard Label
            Text {
                Layout.fillWidth: true
                height: parent.height
                verticalAlignment: Text.AlignVCenter
                text: name
            }

            // Then either a TextField or a SpinBox, depending on
            // whether it is string, int or float
            TextField { // For text
                id: input
                implicitWidth: 300
                height: parent.height
                visible: ptype == 0
                text: model.value

                onEditingFinished: updateModel(text);
            }

            SpinBox { // For int or floats
                id: spin
                implicitWidth: 300
                height: parent.height
                visible: ptype > 0
                decimals: ptype == 1? 0 : 4
                stepSize: ptype == 1? 1 : 0.1
                value: ptype == 1? ivalue : fvalue

                onEditingFinished: updateModel(value)
            }

            function updateModel(value) {
                modified(i, name, value);
            }
        }
    }

    // ==========================
    // Functions
    // ==========================

    function isInt(n){
        return n === +n && n === (n|0) && n != 0;
    }

    function isFloat(n){
        return n === +n && n !== (n|0);
    }

    function loadPlugins(data) {
        var i = pluginModel.count;
        data['pdata'] = [];
        for ( var key in data['data'] ) {
            var value = data['data'][key];
            var ptype = -1;
            if ( typeof(value) === 'string' ) {
                ptype = 0;
            } else if ( typeof(value) === 'number' ) {
                ptype = isInt(value) ? 1 : 2;
            }
            if ( ptype >= 0 ) {
                data['pdata'].push({
                    name: key, value: value.toString(), ptype: ptype,
                    ivalue: parseInt(value), fvalue: parseFloat(value),
                    i: i
                });
            }
        }
        // Append the plugin data to the whole model to be rendered
        pluginModel.append(data);
    }

}