from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout,QHBoxLayout, QLabel,QListWidget, QListWidgetItem, QTreeWidget, QTreeWidgetItem, QGridLayout, QGroupBox
from PyQt5.QtCore import pyqtSlot

class MyTabWidget(QWidget):
    def __init__(self, parent, widgetsDict, controller):
        super(QWidget, self).__init__(parent)
        self.widgetsDict = widgetsDict

        self.controller = controller

        self.layout = QVBoxLayout(self)
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300,200)

        # Add tabs
        self.tabs.addTab(self.tab1,"Control")
        self.tabs.addTab(self.tab2,"Game")

        self.ControlViewInit()
        self.GameViewInit()
       
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.slotsInit()

    def GameViewInit(self):
        board1 = self.widgetsDict['PlayerBoard']
        board2 = self.widgetsDict['EnemyBoard']

        wl1 = QVBoxLayout()
        wl2 = QVBoxLayout()

        self.tab2layout = QHBoxLayout()
        self.tab2.setLayout(self.tab2layout)

        w1 = QWidget()
        w2 = QWidget()
        self.tab2layout.addWidget(w1)
        self.tab2layout.addWidget(w2)

        w1.setLayout(wl1)
        w2.setLayout(wl2)

        wl1.addWidget(board1)
        wl2.addWidget(board2)

    def ControlViewInit(self):
        self.tab1layout = QHBoxLayout()
        self.tab1.setLayout(self.tab1layout)
        tabWidgets = self.widgetsDict['control']

        count = 0


        for key, group in tabWidgets.items():
            if (count % 2 == 0):
                cur_layout = QVBoxLayout()
                self.tab1layout.addLayout(cur_layout)
            
            w = QGroupBox()
            cur_layout.addWidget(w)
            cur_layout.addWidget(w)
            l = QVBoxLayout()
            w.setLayout(l)

            i = 0
            for key, widget in group.items():
                if (key == 'title'):
                    w.setTitle(widget)
                else:
                    # widget.sizePolicy().setVerticalStretch(policy[i])
                    l.addWidget(widget)
                    i = i + 1
            count = count + 1

    @pyqtSlot()
    def on_click(self):
        print("Switch to tab\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

    def slotsInit(self):
        self.controlWidgets = self.widgetsDict['control']
        loginButton = self.controlWidgets['login']['button']
        loginButton.clicked.connect(self.loginPushed)

        registerButton = self.controlWidgets['register']['button']
        registerButton.clicked.connect(self.registerPushed)

        connectButton = self.controlWidgets['connect']['connectbutton']
        connectButton.clicked.connect(self.connectPushed)

        closeButton = self.controlWidgets['connect']['closebutton']
        closeButton.clicked.connect(self.closePushed)

        fetchButton = self.controlWidgets['connect']['fetch_button']

        fetchButton.clicked.connect(self.fetchPushed)
        updateButton = self.controlWidgets['connect']['update_button']
        updateButton.clciked.connect(self.updatePushed)


    @pyqtSlot()
    def fetchPushed(self):
        pass

    @pyqtSlot()
    def updatePushed(self):
        pass

    @pyqtSlot()
    def closePushed(self):
        self.controller.close()

    @pyqtSlot()
    def loginPushed(self):
        item = self.controlWidgets['login']
        username = item['username'].text()
        password = item['pass'].text()
        checked = item['checkbox'].isChecked()
        self.controller.login(username, password, checked)

    @pyqtSlot()
    def registerPushed(self):
        item = self.controlWidgets['register']
        username = item['username'].text()
        password = item['pass'].text()
        checked = item['checkbox'].isChecked()
        self.controller.register(username, password, checked)

    @pyqtSlot()
    def connectPushed(self):
        server = self.controlWidgets['connect']
        self.controller.connect(server['ip'].text(), server['port'].text())

