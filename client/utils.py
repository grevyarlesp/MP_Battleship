from PyQt5.QtWidgets import QMessageBox

def displayMessageBox(title, message):
    box = QMessageBox()
    box.setWindowTitle(title)
    box.setText(message)
    box.exec()


def displayYesNoBox(title, message):
    reply = QMessageBox.question(None, title, message, QMessageBox.Yes, QMessageBox.No)
    return reply

