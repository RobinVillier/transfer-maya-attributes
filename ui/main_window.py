from pathlib import Path

from PySide2 import QtWidgets, QtCore, QtGui

from CopyAttrs.config import load
from CopyAttrs.config import settings
from CopyAttrs.maya_logic import get_maya_items as gmi

_ROOT_DIR = Path(__file__).parent.parent


class CopyAttributesWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(CopyAttributesWindow, self).__init__(parent)

        self.setWindowTitle(f"{settings.APP_NAME}  |  v{settings.VERSION}")
        self.setMinimumSize(300, 300)
        # self.setWindowIcon(QtGui.QIcon(f"{_ROOT_DIR}/resources/icons/list_icon_black.svg"))

        stylesheet = load.load_stylesheet(f"{_ROOT_DIR}/resources/styles/style.qss")
        self.setStyleSheet(stylesheet)

        self.selection_watcher = gmi.SelectionWatcher(self.populate)
        self.selection_watcher.start()

        self.build_ui()
        self.populate()

    def build_ui(self):
        master_layout = QtWidgets.QVBoxLayout(self)
        master_layout.setContentsMargins(10, 10, 10, 10)
        master_layout.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)

    def populate(self):
        QtCore.QTimer.singleShot(0, self._refresh)

    def _refresh(self):
        self.attr_list.clear()

        node = gmi.get_selected_node()
        if not node:
            return

        attrs_list = gmi.get_custom_not_hidden_attributes(node)
        for attr in attrs_list:
            self.attr_list.addItem(attr)

    def closeEvent(self, event):
        if self.selection_watcher:
            self.selection_watcher.stop()
        super(CopyAttributesWindow, self).closeEvent(event)
