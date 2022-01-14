from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout,QHBoxLayout, QLabel,QListWidget, QListWidgetItem, QTreeWidget, QTreeWidgetItem, QGridLayout, QGroupBox
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt


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
        turnlabel = self.widgetsDict['turnlabel']

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


        wl1.addWidget(board1, stretch = 20)
        wl1.addWidget(turnlabel, stretch = 2)
        wl2.addWidget(board2)



    def ControlViewInit(self):
        self.tab1layout = QHBoxLayout()
        self.tab1.setLayout(self.tab1layout)
        tabWidgets = self.widgetsDict['control']

        count = 0

        cur_layout = QVBoxLayout()

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

        fetchButton = self.controlWidgets['setup_info']['fetch_button']

        fetchButton.clicked.connect(self.fetchPushed)
        updateButton = self.controlWidgets['setup_info']['update_button']
        updateButton.clicked.connect(self.updatePushed)

        checkButton = self.controlWidgets['check_user']['button']
        checkButton.clicked.connect(self.checkPushed)

        changeButton = self.controlWidgets['change_password']['button']
        changeButton.clicked.connect(self.changePushed)

        refreshOnlineButton = self.controlWidgets['startgame']['refreshbutton']
        refreshOnlineButton.clicked.connect(self.refreshPushed)

        startGameButton = self.controlWidgets['startgame']['startbutton']
        startGameButton.clicked.connect(self.startGamePushed)

        uploadshipButton = self.controlWidgets['startgame']['uploadshipbutton']
        uploadshipButton.clicked.connect(self.uploadShipPushed)


    @pyqtSlot()
    def fetchPushed(self):
        self.controller.fetch()

    @pyqtSlot()
    def updatePushed(self):
        self.controller.update()

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

    @pyqtSlot()
    def checkPushed(self):
        self.controller.check_user()

    @pyqtSlot()
    def changePushed(self):
        self.controller.change_password()

    @pyqtSlot()
    def refreshPushed(self):
        self.controller.refreshOnlineUsers()

    @pyqtSlot()
    def startGamePushed(self):
        self.controller.startGame()

    @pyqtSlot()
    def uploadShipPushed(self):
        self.controller.uploadShip()

    def keyPressEvent(self, event):
        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return):
            self.controller.shoot()
