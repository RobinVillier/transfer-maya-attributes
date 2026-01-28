from maya import cmds


def get_custom_non_hidden_attributes(node: str) -> list[str]:
    """Get custom attributes of the first selected node that are visible in the channel box"""

    attrs = cmds.listAttr(node, ud=True) or []

    vis_attrs = [
        attr for attr in attrs
        if cmds.getAttr(f"{node}.{attr}", k=True) or cmds.getAttr(f"{node}.{attr}", cb=True)
    ]

    return vis_attrs


def get_attributes(node):
    """ Gets the custom attributes of a given node """
    attr_dict = {}



    return attr_dict


def copy_attributes():
    pass



