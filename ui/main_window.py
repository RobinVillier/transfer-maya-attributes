from pathlib import Path

from PySide2 import QtWidgets, QtCore, QtGui

from TransferAttrs.config import load
from TransferAttrs.config import settings
from TransferAttrs.maya_logic import get_maya_items as gmi
from TransferAttrs.maya_logic import attribute_tools as at


class TransferAttributesWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(TransferAttributesWindow, self).__init__(parent)

        self.setWindowTitle(f"{settings.APP_NAME}  |  v{settings.VERSION}")
        self.resize(300, 600)
        self.setWindowIcon(QtGui.QIcon(f"{settings.ROOT_DIR}/resources/icons/transfer_attr_icon_black.png"))

        stylesheet = load.load_qss_with_fixed_urls(rf"{settings.ROOT_DIR}/resources/styles/style.qss")
        self.setStyleSheet(stylesheet)

        self.build_ui()
        self.refresh_list()

    # UI
    def build_ui(self):
        master_layout = QtWidgets.QVBoxLayout(self)
        master_layout.setContentsMargins(10, 10, 10, 10)
        master_layout.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)

        self.build_attr_list_section()
        self.build_btm_button_section()
        self.build_templates_section()

        master_layout.addWidget(self.list_title)
        master_layout.addWidget(self.attr_list_widget)
        master_layout.addLayout(self.btm_button_layout)
        master_layout.addSpacing(5)
        master_layout.addWidget(self.templates_divider)
        master_layout.addSpacing(5)
        master_layout.addWidget(self.templates_title)
        master_layout.addWidget(self.templates_cbb)
        master_layout.addLayout(self.io_button_layout)

    def build_attr_list_section(self):
        self.list_title = QtWidgets.QLabel("Attributes List :")
        self.list_title.setObjectName("Titles")

        self.attr_list_widget = QtWidgets.QListWidget()
        self.attr_list_widget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

    def build_btm_button_section(self):
        refresh_button = QtWidgets.QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_list)

        transfer_attrs_button = QtWidgets.QPushButton("Transfer Attributes")
        transfer_attrs_button.setObjectName("validation_btn")
        transfer_attrs_button.clicked.connect(self.transfer_attrs)

        self.btm_button_layout = QtWidgets.QHBoxLayout()
        self.btm_button_layout.addWidget(refresh_button)
        self.btm_button_layout.addWidget(transfer_attrs_button)

    def build_templates_section(self):
        self.templates_divider = self.create_divider()

        self.templates_title = QtWidgets.QLabel("Templates :")
        self.templates_title.setObjectName("Titles")

        self.templates_cbb = QtWidgets.QComboBox()
        self.templates_cbb.addItems(load.open_json(f"{settings.DATA_PATH}/templates.json").keys())
        self.templates_cbb.setEditable(True)

        self.export_button = QtWidgets.QPushButton("Export")
        self.export_button.setObjectName("cancel_btn")
        self.export_button.clicked.connect(lambda: at.export_attrs(self))

        self.import_button = QtWidgets.QPushButton("Import")
        self.import_button.setObjectName("validation_btn")
        self.import_button.clicked.connect(lambda: at.import_attrs(self))

        self.io_button_layout = QtWidgets.QHBoxLayout()
        self.io_button_layout.addWidget(self.export_button)
        self.io_button_layout.addWidget(self.import_button)

    # CUSTOM WIDGETS
    @staticmethod
    def create_divider():
        divider = QtWidgets.QFrame()
        divider.setFrameShape(QtWidgets.QFrame.HLine)
        divider.setFrameShadow(QtWidgets.QFrame.Sunken)

        return divider

    # SIGNALS
    def refresh_list(self):
        self.attr_list_widget.clear()

        source_node = gmi.get_selected_node()
        if source_node is None:
            return

        attrs_list = at.get_custom_non_hidden_attributes(source_node[0])
        self.attr_list_widget.addItems(attrs_list)

    def transfer_attrs(self):
        source_node = gmi.get_selected_node()
        if source_node is None:
            return

        attrs_list = at.get_custom_non_hidden_attributes(source_node[0])
        selected_attrs = [i.text() for i in self.attr_list_widget.selectedItems()]
        attrs_data_dict = {k: v for k, v in at.get_attributes_data(attrs_list).items()
                           if k in selected_attrs}
        at.transfer_attributes(attrs_data_dict)
