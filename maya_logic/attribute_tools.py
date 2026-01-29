from maya import cmds

from PySide2 import QtWidgets

from TransferAttrs.config import settings
from TransferAttrs.config import load
from TransferAttrs.maya_logic.get_maya_items import get_selected_node


def get_custom_non_hidden_attributes(node=None) -> list[str]:
    """Get custom attributes of the first selected node that are visible in the channel box"""
    all_attrs = cmds.listAttr(node, ud=True) or []
    if not all_attrs:
        cmds.warning("No custom attributes found.")

    attrs_list = [
        attr for attr in all_attrs
        if cmds.getAttr(f"{node}.{attr}", k=True) or cmds.getAttr(f"{node}.{attr}", cb=True)
    ]

    return attrs_list


def get_attributes_data(attr_list):
    """ Return attribute metadata (min, max, default, type) for given attributes """
    attr_data_dict = {}
    node = get_selected_node()[0]

    for attr in attr_list:
        attr_data_dict[attr] = {
            "min": cmds.attributeQuery(attr, n=node, min=True)[0]
            if cmds.attributeQuery(attr, n=node, mne=True) else None,

            "max": cmds.attributeQuery(attr, n=node, max=True)[0]
            if cmds.attributeQuery(attr, n=node, mxe=True) else None,

            "default": cmds.attributeQuery(attr, n=node, listDefault=True)[0],
            "type": cmds.attributeQuery(attr, n=node, attributeType=True),
            "keyable": cmds.getAttr(f"{node}.{attr}", k=True),
            "locked": cmds.getAttr(f"{node}.{attr}", l=True)
        }

        if attr_data_dict[attr].get("type") == "enum":
            attr_data_dict[attr]["enum_list"] = cmds.attributeQuery(attr, node=node, listEnum=True)[0].split(":")

    return attr_data_dict


def transfer_attributes(attrs_data_dict):
    nodes = get_selected_node()
    source_node, destination_nodes = nodes[0], nodes[1:]

    add_custom_attributes(attrs_data_dict, destination_nodes)


def export_attrs(window: QtWidgets.QDialog):
    source_node = get_selected_node()
    if source_node is None:
        cmds.warning("No Data Saved: No selection found.")
        return

    current_text = window.templates_cbb.currentText()
    templates_file_path = f"{settings.DATA_PATH}/templates.json"
    templates_dict = load.open_json(templates_file_path)

    # Add text to combo box
    cbb_items = [window.templates_cbb.itemText(i) for i in range(window.templates_cbb.count())]
    if current_text not in cbb_items:
        window.templates_cbb.addItem(current_text)
    window.templates_cbb.setCurrentText("")

    # Save data to json (create json if doesn't exists)
    attrs_list = get_custom_non_hidden_attributes(source_node[0])
    selected_attrs = [i.text() for i in window.attr_list_widget.selectedItems()]
    attrs_data_dict = {k: v for k, v in get_attributes_data(attrs_list).items()
                       if k in selected_attrs}
    templates_dict[current_text] = attrs_data_dict

    load.save_json(templates_file_path, templates_dict)

    print(f"--## {source_node[0]}'s attributes have been saved to : {templates_file_path} ##--")


def import_attrs(window: QtWidgets.QDialog):
    destination_node = get_selected_node()
    if destination_node is None:
        cmds.warning("No Data Imported: No selection found.")
        return

    current_text = window.templates_cbb.currentText()
    templates_file_path = f"{settings.DATA_PATH}/templates.json"
    templates_dict = load.open_json(templates_file_path)
    template_attrs = templates_dict.get(current_text)

    add_custom_attributes(attrs_data_dict=template_attrs, destination_nodes=destination_node)

    print(f"--## {current_text}'s attributes have been imported on {destination_node} from : {templates_file_path} ##--")


def add_custom_attributes(attrs_data_dict: dict, destination_nodes: list[str]):
    cmds.undoInfo(openChunk=True)

    for node in destination_nodes:
        for attr, data_type in attrs_data_dict.items():
            if cmds.attributeQuery(attr, n=node, exists=True):
                continue

            kwargs = {
                "longName": attr,
                "k": data_type["keyable"],
                "attributeType": data_type["type"],
                "dv": data_type.get("default"),
            }

            if data_type.get("min") is not None:
                kwargs["min"] = data_type["min"]

            if data_type.get("max") is not None:
                kwargs["max"] = data_type["max"]

            if data_type.get("type") == "enum":
                enum_string = ":".join(attrs_data_dict[attr]["enum_list"])
                kwargs["enumName"] = enum_string

            cmds.addAttr(node, **kwargs)

            # Set lock and non-keyable attributes
            cmds.setAttr(f"{node}.{attr}", l=data_type.get("locked", False))
            if not data_type.get("keyable", True):
                cmds.setAttr(f"{node}.{attr}", cb=True)

    cmds.undoInfo(closeChunk=True)
