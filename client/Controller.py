from PyQt5.QtCore import pyqtSlot, Qt
class Controller():
    def __init__(self, widgetsDict):
        self.widgetsDict = widgetsDict

        controlsWidget = self.widgetsDict['control']


