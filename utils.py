import maya.cmds as mc

def getExportSettings():
    #build an dictionary of the export settings to use in the export function
    if mc.radioButtonGrp('handExport', sl = True, q = True) == 1:
        side = ['']
    elif mc.radioButtonGrp('handExport', sl = True, q = True) == 2:
        side = ['_R_']
    else:
        side = ['_L_']


""""""""""""""""""""""""""""""""""""""""""
      #Get all hierarchy objects#
""""""""""""""""""""""""""""""""""""""""""
def getObjList(obj_list):
    """
    Retrieves a list of objects and their children.

    Args:
        obj_list (list): The list of objects to traverse.

    Returns:
        list: The updated list of objects, including all children found.
    """
    # Initialize a separate list to store all children found
    all_children = []
    
    # Traverse the original list and look for children
    for obj in obj_list:
        children = mc.listRelatives(obj, typ='transform')
        if children is not None:
            # Extend the all_children list with new children, avoiding duplicates
            all_children.extend(child for child in children if child not in obj_list and child not in all_children)

    # Append all unique children to the original list
    obj_list.extend(all_children)


""""""""""""""""""""""""""""""""""""""""""
      #Get all bones to be Keyed#
""""""""""""""""""""""""""""""""""""""""""
def getKeyBones(side):
    """
    Returns a list of key bones based on the given side.

    Args:
        side (str): The side of the bones ('L' for left, 'R' for right).

    Returns:
        list: A list of key bones that match the given side.

    """
    # The ls command lists all objects of type 'joint'
    allBoneList = mc.ls(type='joint')
    
    # List comprehension to filter and create the key bone list in one line
    keyBoneList = [bone for bone in allBoneList if 'Bn' in bone and side[0] in bone and 'Drv' not in bone]

    return keyBoneList

""""""""""""""""""""""""""""""""""""""""""
      #Bake bones for export#
""""""""""""""""""""""""""""""""""""""""""
def bakeBones(bbList, bakeEndTime=None, cleanConnections=False):
    """
    Bakes the animation curves of the given bone list.

    Args:
        bbList (list): List of bone names to bake.
        bakeEndTime (int, optional): The end time to bake until. If not provided, uses the value from the 'endTime' intField. Defaults to None.
        cleanConnections (bool, optional): Flag to indicate whether to clean up connections after baking. Defaults to False.
    """
    startTimeInput = mc.intField('startTime', q=True, v=True)
    endTimeInput = bakeEndTime if bakeEndTime is not None else mc.intField('endTime', q=True, v=True)
    mc.bakeResults(bbList, t=(startTimeInput, endTimeInput))
    
    if cleanConnections:
        connectList = []
        animCurveTypes = ["animCurveTU", "animCurveTL", "animCurveTA"]
        
        for curveType in animCurveTypes:
            connections = mc.listConnections(bbList, s=True, type=curveType)
            if connections:
                connectList.extend(connections)
                
        if connectList:
            mc.delete(connectList)
