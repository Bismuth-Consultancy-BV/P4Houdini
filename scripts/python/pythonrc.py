"""
Simple script that registers some callbacks for the session.
"""

import hou
import P4Houdini
# from importlib import reload
# reload(P4Houdini)


class P4HoudiniData(object):
    pass

def scene_event_callback(event_type):
    """
    Attaching P4Houdini plugin to Hip saving mechanism.
    """

    if not P4Houdini.check_perforce_installed():
        return

    try:
        p4houdini_data = hou.session.p4houdini
    except:
        hou.session.p4houdini = P4Houdini.P4HoudiniData()
        p4houdini_data = hou.session.p4houdini

    # Check out file
    if event_type == hou.hipFileEventType.BeforeSave:
        p4houdini_data.hip_pre_save = P4Houdini.hip_before_save_automatic()

    # Mark hip file for add
    elif event_type == hou.hipFileEventType.AfterSave:
        if not hasattr(p4houdini_data, "hip_pre_save"):
            return
        if p4houdini_data.hip_pre_save:
            P4Houdini.hip_after_save_automatic()

    # # Check if file in sync with depot
    # elif event_type == hou.hipFileEventType.BeforeLoad:
    #     P4Houdini.hip_before_load_automatic()


def hda_created_event_callback(event_type, asset_definition, **kwargs):
    pass
    #print("CREATED:", asset_definition)

def hda_saved_event_callback(event_type, asset_definition, **kwargs):
    file = asset_definition.libraryFilePath()
    P4Houdini.hda_after_save_automatic(file)
hou.hda.addEventCallback((hou.hdaEventType.AssetSaved, ), hda_saved_event_callback)


hou.hipFile.addEventCallback(scene_event_callback)
hou.hda.addEventCallback((hou.hdaEventType.AssetCreated, ), hda_created_event_callback)
