from maya import cmds

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

    return attr_data_dict


def copy_attributes(attrs_data_dict):
    cmds.undoInfo(openChunk=True)
    nodes = get_selected_node()
    source_node, destination_nodes = nodes[0], nodes[1:]

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

            cmds.addAttr(node, **kwargs)
            cmds.setAttr(f"{node}.{attr}", l=data_type.get("locked", False))
            if not data_type.get("keyable", True):
                cmds.setAttr(f"{node}.{attr}", cb=True)

    cmds.undoInfo(closeChunk=True)
