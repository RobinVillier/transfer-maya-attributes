from pathlib import Path

from PySide2 import QtWidgets, QtCore, QtGui

from TransferAttrs.config import load
from TransferAttrs.config import settings
from TransferAttrs.maya_logic import get_maya_items as gmi
from TransferAttrs.maya_logic import attribute_tools as at

_ROOT_DIR = Path(__file__).parent.parent


class CopyAttributesWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(CopyAttributesWindow, self).__init__(parent)

        self.setWindowTitle(f"{settings.APP_NAME}  |  v{settings.VERSION}")
        self.setMinimumSize(300, 300)
        self.setWindowIcon(QtGui.QIcon(f"{_ROOT_DIR}/resources/icons/copy_attr_icon_black.png"))

        stylesheet = load.load_stylesheet(f"{_ROOT_DIR}/resources/styles/style.qss")
        self.setStyleSheet(stylesheet)

        self.build_ui()
        self.refresh_list()

    def build_ui(self):
        master_layout = QtWidgets.QVBoxLayout(self)
        master_layout.setContentsMargins(10, 10, 10, 10)
        master_layout.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)

        self.build_attr_list_section()
        self.build_btm_button_section()

        master_layout.addWidget(self.attr_list_widget)
        master_layout.addLayout(self.btm_button_layout)

    def build_attr_list_section(self):
        self.attr_list_widget = QtWidgets.QListWidget()
        self.attr_list_widget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

    def build_btm_button_section(self):
        refresh_button = QtWidgets.QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_list)

        copy_attrs_button = QtWidgets.QPushButton("Copy Attributes")
        copy_attrs_button.setObjectName("copy_btn")
        copy_attrs_button.clicked.connect(self.copy_attrs)

        self.btm_button_layout = QtWidgets.QHBoxLayout()
        self.btm_button_layout.addWidget(refresh_button)
        self.btm_button_layout.addWidget(copy_attrs_button)

    def refresh_list(self):
        self.attr_list_widget.clear()

        source_node = gmi.get_selected_node()
        if source_node is None:
            return

        attrs_list = at.get_custom_non_hidden_attributes(source_node[0])
        self.attr_list_widget.addItems(attrs_list)

    def copy_attrs(self):
        source_node = gmi.get_selected_node()
        if source_node is None:
            return

        attrs_list = at.get_custom_non_hidden_attributes(source_node[0])
        selected_attrs = [i.text() for i in self.attr_list_widget.selectedItems()]
        attrs_data_dict = {k: v for k, v in at.get_attributes_data(attrs_list).items()
                           if k in selected_attrs}
        at.copy_attributes(attrs_data_dict)
