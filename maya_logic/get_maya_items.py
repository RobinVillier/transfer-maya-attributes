import maya.cmds as cmds


def get_selected_node() -> list:
    sel = cmds.ls(selection=True)

    return sel if sel else None
