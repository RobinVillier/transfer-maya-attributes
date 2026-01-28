import maya.cmds as cmds
import maya.api.OpenMaya as om


def get_selected_node():
    sel = cmds.ls(selection=True)
    return sel[0] if sel else None


def get_custom_not_hidden_attributes(node: str) -> list[str]:
    """Get custom attributes of the first selected node that are visible in the channel box"""

    attrs = cmds.listAttr(node, ud=True) or []

    vis_attrs = [
        attr for attr in attrs
        if cmds.getAttr(f"{node}.{attr}", k=True) or cmds.getAttr(f"{node}.{attr}", cb=True)
    ]

    return vis_attrs


class SelectionWatcher(object):
    def __init__(self, on_selection_changed):
        self.callback_id = None
        self.on_selection_changed = on_selection_changed

    def start(self):
        if self.callback_id is None:
            self.callback_id = om.MEventMessage.addEventCallback(
                "SelectionChanged",
                self._selection_changed_callback
            )

    def stop(self):
        if self.callback_id is not None:
            om.MMessage.removeCallback(self.callback_id)
            self.callback_id = None

    def _selection_changed_callback(self, *args):
        self.on_selection_changed()
