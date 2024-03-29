import maya.cmds as mc
import maya.mel
import pymel.core as pm
from pathlib import Path
import sys
import os


homeDir = Path(os.getenv('USERPROFILE', os.getenv('HOME', '')))
if not homeDir:
    print('Error: Unable to determine home directory.')
    sys.exit(1)

sansOneDrive = homeDir / 'Documents'
oneDriveDir = homeDir / 'OneDrive' / 'Documents'

if (oneDriveDir / 'maya' / 'scripts' / 'Export_Tool').exists():
    documentsDir = oneDriveDir
else:
    documentsDir = sansOneDrive

scriptLocation = documentsDir / 'maya' / 'scripts' / 'Export_Tool'
sys.path.append(str(scriptLocation))
import importlib

import UI
import save_load_manager
import handle_errors
import cleanUp

importlib.reload(UI)
importlib.reload(save_load_manager)
importlib.reload(handle_errors)
importlib.reload(cleanUp)



    

""""""""""""""""""""""""""""""""""""""""""
      #Get all hierarchy objects#
""""""""""""""""""""""""""""""""""""""""""

def getObjList(list):
    for obj in list:
        children = mc.listRelatives(obj, typ = 'transform')
        if children != None:
            for node in children:
                if node not in list:
                    list.append(node)

# """"""""""""""""""""""""""""""""""""""""""
#        #Import Reference File#
# """"""""""""""""""""""""""""""""""""""""""

# def importRefFile():
#     refs = mc.ls(type = 'reference')
#     for i in refs:
#         if mc.objExists(i):
#             rFile = mc.referenceQuery(i, f = True)
#             mc.file(rFile, importReference = True)
        
        
# """"""""""""""""""""""""""""""""""""""""""
#       #Delete All Namespaces#
# """"""""""""""""""""""""""""""""""""""""""        

# def nameSpaceChange():
#     allNodes = mc.ls()
#     allNameSpaces = []
    
#     for obj in allNodes:
#         if ':' in obj:
#             if obj.split(':')[0] not in allNameSpaces:
#                 allNameSpaces.append(obj.split(':')[0])
#     if allNameSpaces != []:    
#         for curNameSpace in allNameSpaces:
#             if mc.namespace(exists = curNameSpace):
#                 mc.namespace(rm = curNameSpace, mnr = True)
#                 nameSpaceChange()
#             else:
#                 nameSpaceChange()

""""""""""""""""""""""""""""""""""""""""""
      #Get all bones to be Keyed#
""""""""""""""""""""""""""""""""""""""""""

def getKeyBones(side):
    allBoneList = mc.ls(type = 'joint')
    keyBoneList = []
    for bone in allBoneList:
        if 'Bn' in bone and side[0] in bone:
            if 'Drv' not in bone:
                keyBoneList.append(bone)
        else:
            pass
    
    return keyBoneList

""""""""""""""""""""""""""""""""""""""""""
     #Bake all bones for animations#
""""""""""""""""""""""""""""""""""""""""""
    
def bakeAnimBones(bbList):
    startTimeInput = mc.intField('startTime', q = True, v = True)
    endTimeInput = mc.intField('endTime', q = True, v = True)
    mc.bakeResults(bbList, t = (startTimeInput, endTimeInput))

""""""""""""""""""""""""""""""""""""""""""
      #Bake all bones for models#
""""""""""""""""""""""""""""""""""""""""""
    
def bakeModelBones(bbList):
    startTimeInput = mc.intField('startTime', q=True, v=True)
    print(startTimeInput)
    mc.bakeResults(bbList, t=(startTimeInput, startTimeInput))
    connectList = []
    animCurveTypes = ["animCurveTU", "animCurveTL", "animCurveTA"]
    
    for curveType in animCurveTypes:
        connections = mc.listConnections(bbList, s=True, type=curveType)
        if connections:
            connectList += connections
            
    mc.delete(connectList)


""""""""""""""""""""""""""""""""""""""""""
               #Tool Codes#
""""""""""""""""""""""""""""""""""""""""""

def toolCodes():
    toolCode = [
        '_MayoSS_',
        '_Scalpl_',
        '_OlHeND_',
        '_DebFor_',
        '_HaMoHe_',
        '_SpaHok_',
        '_PaHaRe_',
        '_RoCaHe_',
        '_CriHem_',
        '_KelHem_',
        '_MetSci_',
        '_BackTC_',
        '_MayoND_',
        '_AdRaFo_',
        '_BrAdFo_']
        
    return toolCode

""""""""""""""""""""""""""""""""""""""""""
   #Clear objects for Unity Animation#
""""""""""""""""""""""""""""""""""""""""""

def clearForUniAnim(toolList, side):
    
    #Gather data to make decisions
    
    toolcode = toolCodes()
    
    if side == ['_R_']:
        toolList = [toolList[0]]
        lowSide = 'r'
        handIndex = 1
    elif side == ['_L_']:
        toolList = [toolList[1]]
        lowSide = 'l'
        handIndex = 1
    else:
        side = ['_R_', '_L_']
        handIndex = 2
    
    #Clear Tier 1 Objects
    
    mc.delete('|Global_Hands_01|Grp_Controls_01')
    mc.delete('|Global_Hands_01|Grp_Geometry_01')
    mc.delete('|Global_Hands_01|Grp_Extras_01')
    
    #Clear Tier 2 Objects
    
    for i in range(handIndex):
        tools = []
        if handIndex == 2:
            if i == 0:
                lowSide = 'r'
            else:
                lowSide = 'l'
        for x in range(len(toolcode)):
            tools.append('Grp_' + lowSide + toolcode[x] + 'World_01')
        for k in range(len(tools)):
            if toolList[i] == 0:
                mc.delete(tools)
                break
            elif toolList[i] == k+1:
                
                inUseToolCode = toolCodes()[k]
            else:
                mc.delete(tools[k])
    
    if side == ['_R_']:

        mc.delete('Grp_LeftHand_Instruments_01')
    elif side == ['_L_']:

        mc.delete('Grp_RightHand_Instruments_01')
    else:
        pass
    
    #Gather which objects should remain
    
    remainingBones = mc.ls(type = 'joint')
    keeping = []
    for bone in remainingBones:
        if 'Be' in bone:
            if 'Drv' not in bone:
                keeping.append(bone)
        

    for obj in keeping:
        parent = mc.listRelatives(obj, p = True)
        if parent != None and parent not in keeping:
            keeping.append(parent[0])
        if parent == None:
            top = obj
            
    #Delete all objects that should not remain
    
    toPass = mc.listRelatives(top, ad = True, type = 'transform')
    mc.select(toPass)
    expSelect = []
    for obj in toPass:
        if obj not in keeping:
            if mc.objExists(obj):
                mc.delete(obj)
                
    #Unparent the uppermost nodes from the Global node 
    
    toWorld = mc.listRelatives(top, c = True, type = 'transform')
    for obj in toWorld:
        mc.parent(obj, world = True)
        expSelect.append(obj)
        
    mc.delete(top)
    return expSelect


""""""""""""""""""""""""""""""""""""""""""
    #Clear Objects for Unity Model#
""""""""""""""""""""""""""""""""""""""""""
    
def clearUniModel(toolList, side, hierList):

    #Gather data to make decisions
    toolcode = toolCodes()
    
    if side == ['_R_']:
        toolList = [toolList[0]]
        lowSide = 'r'
        handIndex = 1
    elif side == ['_L_']:
        toolList = [toolList[1]]
        lowSide = 'l'
        handIndex = 1
    else:
        side = ['_R_', '_L_']
        handIndex = 2

    #Clear Tier 1 Common Objects
    mc.delete('|Global_Hands_01|Grp_Controls_01')
    mc.delete('|Global_Hands_01|Grp_Extras_01')
                 
    #Clear Tier 2 Common Objects
    
    if side == ['_R_']:
        mc.delete('BdBn_L_ArmRoot_01')
        mc.delete('Grp_LeftHand_Instruments_01')
        mc.delete('Geo_L_Hand_Mesh_01')
    elif side == ['_L_']:
        mc.delete('BdBn_R_ArmRoot_01')
        mc.delete('Grp_RightHand_Instruments_01')
        mc.delete('Geo_R_Hand_Mesh_01')
    else:
        pass

    #Gather which objects should remain

    getObjList(hierList)
    
    keepTypes = ['BdBn', 'BdBe', 'Geo']
    keeping = []
    for obj in hierList:
        if keepTypes[0] in obj or keepTypes[1] in obj or keepTypes[2] in obj:
            keeping.append(obj)

    for obj in keeping:
        parent = mc.listRelatives(obj, p = True)
        if parent != None and parent not in keeping:
            keeping.append(parent[0])
        if parent == None:
            top = obj
    
    #Delete all objects that should not remain
    
    toPass = mc.listRelatives(top, ad = True, type = 'transform')
    for obj in toPass:
        print('this is in toPass: ' + obj)
    for obj in toPass:
        if obj not in keeping:
            if mc.objExists(obj):
                mc.delete(obj)
                
    #Unparent the uppermost nodes from the Global node
    
    toWorld = mc.listRelatives(top, c = True, type = 'transform')
    expSelect = []
    for obj in toWorld:
        mc.parent(obj, world = True)
        expSelect.append(obj)
        
    mc.delete(top)
    return expSelect


""""""""""""""""""""""""""""""""""""""""""
  #Clear Objects For Marmoset#
""""""""""""""""""""""""""""""""""""""""""

def clearForMarm(toolList, side, hierList):
    
    #Gather data to make decisions
    
    toolcode = toolCodes()
    
    if side == ['_R_']:
        toolList = [toolList[0]]
        lowSide = 'r'
        handIndex = 1
    elif side == ['_L_']:
        toolList = [toolList[1]]
        lowSide = 'l'
        handIndex = 1
    else:
        side = ['_R_', '_L_']
        handIndex = 2
    
    #Clear Tier 1 common objects
    mc.delete('|Global_Hands_01|Grp_Controls_01')
    mc.delete('|Global_Hands_01|Grp_Extras_01')
    
    #Clear Tier 2 common objects
    
    for i in range(handIndex):
        tools = []
        if handIndex == 2:
            if i == 0:
                lowSide = 'r'
            else:
                lowSide = 'l'
        for x in range(len(toolcode)):
            tools.append('Grp_' + lowSide + toolcode[x] + 'World_01')
        for k in range(len(tools)):
            if toolList[i] == 0:
                mc.delete(tools)
                break
            elif toolList[i] == k+1:
                
                inUseToolCode = toolCodes()[k]
            else:
                mc.delete(tools[k])
    
    if side == ['_R_']:
        mc.delete('BdBn_L_ArmRoot_01')
        mc.delete('Grp_LeftHand_Instruments_01')
        mc.delete('Geo_L_Hand_Mesh_01')
    elif side == ['_L_']:
        mc.delete('BdBn_R_ArmRoot_01')
        mc.delete('Grp_RightHand_Instruments_01')
        mc.delete('Geo_R_Hand_Mesh_01')
    else:
        pass
    
    #Gather which objects should remain
    
    getObjList(hierList)
    
    keepTypes = ['BdBn', 'BdBe', 'Geo_']
    keeping = []
    for obj in hierList:
        if keepTypes[0] in obj or keepTypes[1] in obj or keepTypes[2] in obj:
            keeping.append(obj)

    for obj in keeping:
        parent = mc.listRelatives(obj, p = True)
        if parent != None and parent not in keeping:
            keeping.append(parent[0])
        if parent == None:
            top = obj

    #Delete all objects that should not remain

    toPass = mc.listRelatives(top, ad = True, type = 'transform')
    for obj in toPass:
        print('this is in toPass: ' + obj)
    for obj in toPass:
        if obj not in keeping:
            if mc.objExists(obj):
                mc.delete(obj)
                
    #Unparent the uppermost nodes from the Global node
    toWorld = mc.listRelatives(top, c = True, type = 'transform')
    expSelect = []
    for obj in toWorld:
        mc.parent(obj, world = True)
        expSelect.append(obj)
        
    mc.delete(top)
    return expSelect




""""""""""""""""""""""""""""""""""""""""""
          #Main Logic Process#
""""""""""""""""""""""""""""""""""""""""""

def exportProcess():
    #save current scene
    # mc.file(s = True)
    
    #get save state conditions
    yesNoCheckBox = mc.checkBox('saveToggle', q = True, v = True)
    defaultLocCheckBox = mc.checkBox('defaultCB', q = True, v = True)
    if mc.textField('saveLocTxt', q = True, tx = True) == 'No default path located':
        customPath = False
    else:
        customPath = True
        
    if yesNoCheckBox == True:
        save_load_manager.saveLoc(yesNoCheckBox, defaultLocCheckBox, customPath)
     
    
    #store the top most node in a variable for use throughout this function
    #Have 1 object selected within the rig, 
    sele = mc.ls(sl = True, l = True)
    topNode = sele[0].split('|')[1]
    mc.select(topNode)
    hierList = mc.ls(sl = True, an = True)
    
    #import the referenced file
    if mc.checkBox('importRef', q = True, v = True):
        checkRef = mc.ls(type = 'reference')
        if len(checkRef) > 0:
            cleanUp.importRefFile()

    #creat a list of all nodes within the rig
    getObjList(hierList)

    #rename all nodes within the list in order to remove the necessary nodes from the namespace
    cleanUp.nameSpaceChange()
    
    #Get the list of bones that will be baked down
    if mc.radioButtonGrp('handExport', sl = True, q = True) == 1:
        side = ['']
    elif mc.radioButtonGrp('handExport', sl = True, q = True) == 2:
        side = ['_R_']
    else:
        side = ['_L_']
        
    #set current time
    curTime = mc.intField('startTime', q = True, v = True)
    pm.mel.currentTime(curTime, edit = True)

        
    #get bones to bake and bake them
    bakeBoneList = getKeyBones(side)

    print('boneList: ', bakeBoneList)
    
    if mc.radioButtonGrp('exportType', sl = True, q = True) == 1 or mc.radioButtonGrp('exportType', sl = True, q = True) == 3:
        bakeAnimBones(bakeBoneList)
        isAnim = True
    elif mc.radioButtonGrp('exportType', sl = True, q = True) == 2 or mc.radioButtonGrp('exportType', sl = True, q = True) == 4:
        bakeModelBones(bakeBoneList)
        isAnim = False
    
    
    mc.select(topNode)
    hierList = mc.ls(sl = True, an = True)
    
    #determine which nodes will not be needed entirely and just get rid of them right away, to make next search more efficient
    leftToolNum = mc.getAttr('Ctrl_Global_Hands_01.LeftHandTool')
    rightToolNum = mc.getAttr('Ctrl_Global_Hands_01.RightHandTool')
    toolList = [rightToolNum, leftToolNum]
    
    
    if mc.radioButtonGrp('exportType', sl = True, q = True) == 1:
        expSelect = clearForUniAnim(toolList, side)
    elif mc.radioButtonGrp('exportType', sl = True, q = True) == 2:
        expSelect = clearUniModel(toolList, side, hierList)
    else:
        expSelect = clearForMarm(toolList, side, hierList)
        
    
    

    #Select remaining Objects
    mc.select(expSelect)

    #Export the remain objects as an FBX file
    if mc.radioButtonGrp('exportType', sl = True, q = True) == 2:
        symbol = '_'
    else:
        symbol = '@'
        
    filePath = mc.textField('exportLocationText', q=True, tx=True)
    clipType = mc.textField('clipTypeText', q=True, tx=True)
    clipName = mc.textField('clipNameText', q=True, tx=True)
    exportNamePath = (filePath + "/" + clipType + symbol + clipName + ".fbx")
    if UI.toolMode == UI.toolModeList[0]:
        pm.mel.FBXExport(s = True, f=exportNamePath, v = True)
    elif UI.toolMode == UI.toolModeList[1]:
        if mc.checkBox('exportCB', q = True, v = True):
            pm.mel.FBXExport(s = True, f=exportNamePath, v = True)

    

    
UI.makeUI()

