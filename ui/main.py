from PySide2 import QtWidgets
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance


def get_maya_main_window() -> QtWidgets.QWidget:
    ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(ptr), QtWidgets.QMainWindow)


def launch():
    from TransferAttrs.ui.main_window import CopyAttributesWindow

    window = CopyAttributesWindow(get_maya_main_window())
    window.show()
