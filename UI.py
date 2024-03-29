import maya.cmds as mc
import maya.mel
import pymel.core as pm
import importlib

import save_load_manager
importlib.reload(save_load_manager)

""""""""""""""""""
   #Tool Mode#
""""""""""""""""""
toolModeList = ['Use', 'Test', 'Debug']
toolMode = toolModeList[1]


""""""""""""""""""
   #UI Functions#
""""""""""""""""""
def timeRange(value):
    mc.text('endTimeLabelText', edit = True, enable = not value)
    mc.intField('endTime', edit = True, enable = not value)
    mc.text('startTimeLabelText', edit = True, l = 'Export Frame')
    
def unityModelOn(value):
    mc.text('clipTypeLabelText', edit = True, l = "Model Name:")
    mc.text('clipNameLabelText', edit = True, l = "Model Type:", en = True)  
    mc.textField('clipTypeText', edit = True, tx = '')
    mc.textField('clipNameText', edit = True, tx = 'UnityModel', en = True) 
    
def unityAnimOn(value):
    mc.text('clipTypeLabelText', edit = True, l = "Clip Type:")
    mc.text('clipNameLabelText', edit = True, l = "Clip Name:", en = True)
    mc.textField('clipTypeText', edit = True, tx = 'Animation')
    mc.textField('clipNameText', edit = True, tx = 'Animation', en = True)
    mc.text('startTimeLabelText', edit = True, l = 'Start Time')
    resetClipName()
    
def marmAnimOn(value):
    mc.text('clipTypeLabelText', edit = True, l = "Clip Name:")
    mc.text('clipNameLabelText', edit = True, l = "Clip Type:", en = True)
    mc.textField('clipTypeText', edit = True, tx = '')
    mc.textField('clipNameText', edit = True, tx = 'MarmosetAnim', en = True)
    mc.text('startTimeLabelText', edit = True, l = 'Start Time')
    
def marmModelOn(value):
    mc.text('clipTypeLabelText', edit = True, l = "Model Name:")
    mc.text('clipNameLabelText', edit = True, l = "Model Type:", en = True)  
    mc.textField('clipTypeText', edit = True, tx = '')
    mc.textField('clipNameText', edit = True, tx = 'MarmosetModel', en = True)


def saveOn(value):
    mc.checkBox('defaultCB', edit = True, enable = value)
    if mc.checkBox('defaultCB', q = True, value = True):
        mc.textField('saveLocTxt', edit = True, enable = False)
        mc.button('saveLocButton', edit = True, enable = False)
    else:
        mc.textField('saveLocTxt', edit = True, enable = True)
        mc.button('saveLocButton', edit = True, enable = True)

def saveOff(value):
    mc.checkBox('defaultCB', edit = True, enable = value)
    mc.textField('saveLocTxt', edit = True, enable = False)
    mc.button('saveLocButton', edit = True, enable = False)
    
    
def custTextField(value):
    mc.textField('saveLocTxt', edit = True, enable = not value)
    mc.button('saveLocButton', edit = True, enable = not value)

def objectTypeToggleActive(value):
    print(value)


""""""""""""""""""""""""""""""""""""""""""
             #Testing UI#
""""""""""""""""""""""""""""""""""""""""""

def testUI():
    if toolMode == toolModeList[0]:
        mc.text(l = " ")
    elif toolMode == toolModeList[1]:
        mc.rowColumnLayout(nc = 2, cw = [(1, 50), (2, 50)])
        mc.text(l = " ")
        mc.checkBox('exportCB', l = 'exp', v = False)
        mc.setParent('..')

""""""""""""""""""""""""""""""""""""""""""
            #Error Window#
""""""""""""""""""""""""""""""""""""""""""
def errorWindow(message1, message2, message3, message4):
    errorWindowID = 'errorWindow'
    if mc.window(errorWindowID, q = True, exists = True):
        mc.deleteUI(errorWindowID)
    mc.window(errorWindowID, t = 'ERROR!', w = 300, h = 150, s = False)
    mc.showWindow(errorWindowID)
    
    errorLayout = mc.rowColumnLayout(adj = True)
    mc.separator(h=20)
    mc.text(l = message1, fn = 'boldLabelFont')
    mc.separator(h=20)   
    if message2 != None: 
        mc.text(l = '1: ' + message2)
    if message3 != None: 
        mc.text(l = '2: ' + message3)
    if message4 != None: 
        mc.text(l = '3: ' + message4)
    mc.separator(h=20)
    mc.button('Close', c = "mc.deleteUI('%s')" % errorWindowID)

 
""""""""""""""""""""""""""""""""""""""""""
              #ExportType
""""""""""""""""""""""""""""""""""""""""""
def exportTypeUI():
    
    typeLayout = mc.rowColumnLayout(nc = 2, cw = [(1, 50), (2,350)])
    mc.text('Type:', al = 'center')
    mc.radioButtonGrp(
        'exportType',
        la4 = ['Unity Anim', 'Unity Model', 'Marm Anim', 'Marm Model'],
        numberOfRadioButtons = 4,
        sl = 1,
        cl4 = ('left', 'left', 'left', 'left'),
        cw4 = (80, 87, 82, 80),
        cc2 = timeRange,
        cc4 = timeRange,
        on1 = unityAnimOn,
        on2 = unityModelOn,
        on3 = marmAnimOn,
        on4 = marmModelOn,
        
        
        )


""""""""""""""""""""""""""""""""""""""""""
          #Save Export File#
""""""""""""""""""""""""""""""""""""""""""
def saveExportFileUI(layout):
    filePath = mc.file(f = True, sn = True, q = True)
    if 'Export' in filePath:
        saveToggle = False
    else:
        saveToggle = True
    
    saveLayout = mc.rowColumnLayout(nc = 4, cw = [(1,100), (2,50), (3,150), (4,150)])
    mc.text(l ='Save Export File:', al = 'center')
    mc.checkBox('saveToggle', al = 'left', l = 'Y/N', v = saveToggle, ofc = saveOff, onc = saveOn)
    mc.checkBox('defaultCB', l = 'Default location', v = True, cc = custTextField, en = saveToggle)
    mc.text(l = '')
    mc.separator( style='none', h=5)
    saveDefaultLayout = mc.rowColumnLayout(nc = 4, p = layout, cw = [(1,100), (2,200), (3,100)])
    mc.text(l = 'Custom Location:', al = 'center')
    mc.textField('saveLocTxt', ed = True, en = False, tx = save_load_manager.getFilePath()[1])
    mc.button('saveLocButton', l = 'Browse', en = False, c = lambda *args: save_load_manager.exportLocation('saveLocTxt'))
    
    
""""""""""""""""""""""""""""""""""""""""""
          #Reference Import#
""""""""""""""""""""""""""""""""""""""""""
def importReferenceUI():

    if mc.ls(type = 'reference') == []:
        refCB = False
    else:
        refCB = True
    refClayout = mc.rowColumnLayout(nc = 2, cw = [(1,100), (2,300)])
    mc.text(l ='Import Reference:', al = 'center')
    mc.checkBox('importRef', al = 'left', l = 'Y/N', v = refCB, en = refCB)


""""""""""""""""""""""""""""""""""""""""""
            #Object Export Selection
""""""""""""""""""""""""""""""""""""""""""


def objectSelectionUI():
    objectExportLayout = mc.rowColumnLayout(nc = 2, cw = [(1,40), (2, 375)])
    autoObjectExportLayout = mc.rowColumnLayout(nc = 1, cw = [(1, 40)])
    centeringLayout = mc.rowColumnLayout(nr =2, rh = [(1,40), (2, 20)])
    mc.text(l = 'Auto', p = centeringLayout)
    centeringCBLayout = mc.rowColumnLayout(nc = 2, cw = [(1, 10), (2,30)], p = centeringLayout)
    mc.text('')
    mc.checkBox('autoCB', l='', v = False, w = 10)
    objectsToExportLayout = mc.rowColumnLayout(nr = 3, rh = [(1,30), (2, 25), (3,30)], p = objectExportLayout)
    handExportLayout = mc.rowColumnLayout(nc = 2, cw = [(1,75), (2,300)], p = objectsToExportLayout)
    mc.text(l ='Hands:', al = 'center')
    mc.radioButtonGrp('handExport', la4 = ['None','Both', 'Right', 'Left'], numberOfRadioButtons = 4, sl = 1, cw4 = [60,60,60,60])
    mc.separator(p=objectsToExportLayout)
    ToolExportLayout = mc.rowColumnLayout(nc = 2, cw = [(1,75), (2,300)], p = objectsToExportLayout)
    mc.text(l ='Tools:', al = 'center')
    mc.radioButtonGrp('toolExport', la4 = ['None','Both', 'Right', 'Left'], numberOfRadioButtons = 4, sl = 1, cw4 = [60,60,60,60])



""""""""""""""""""""""""""""""""""""""""""
              #TIME RANGE#
""""""""""""""""""""""""""""""""""""""""""
def timeRangeUI(layout):
    timeRangeLayout = mc.rowColumnLayout(nc = 3, parent = layout, cw = [(1,100), (2,100), (3,100)])
    mc.text(l = "Time Range:")
    mc.text('startTimeLabelText', l = "Start Time")
    mc.text('endTimeLabelText', l = "End Time")
    mc.text(l = " ")
    mc.intField('startTime', ed = True, v = 1)
    mc.intField('endTime', ed = True, v = 2)


""""""""""""""""""""""""""""""""""""""""""
              #Clip Info#
""""""""""""""""""""""""""""""""""""""""""
def clipInfoUI(layout):
    clipTypeExportLayout = mc.rowColumnLayout(nc = 3, parent = layout, cw = [(1,100), (2,200), (3,100)])
    mc.text('clipTypeLabelText', l = "Clip Type:")
    mc.textField('clipTypeText', ed=True, tx = 'Animation')

    clipNameExportLayout = mc.rowColumnLayout(nc = 5, parent = layout, cw = [(1,100), (2,200), (3,25), (4,50), (5,25)])
    mc.text('clipNameLabelText', l = "Clip Name:")
    clipNameTxt = mc.textField('clipNameText', ed=True, tx = save_load_manager.getFilePath()[3])
    mc.text('')
    mc.button('Refresh', c = 'resetClipName()')


""""""""""""""""""""""""""""""""""""""""""
            #Export Location#
""""""""""""""""""""""""""""""""""""""""""
def exportLocationUI(layout):
    exportLayout = mc.rowColumnLayout(nc = 3, parent = layout, cw = [(1,100), (2,200), (3,100)])
    mc.text(l = "Export Location:")
    mc.textField('exportLocationText', ed=True)
    mc.button(l = "Browse", c = lambda *args: save_load_manager.exportLocation('exportLocationText'))


""""""""""""""""""""""""""""""""""""""""""
              #Go Buttons#
""""""""""""""""""""""""""""""""""""""""""
def goButtonsUI(layout):
    goLayout = mc.rowColumnLayout(nc = 4, parent = layout, cw = [(1,100), (2,100), (3,100), (4,100)])
    testUI()
    mc.button(l = "--> GO <--", c = "exportProcess()")
    mc.button(l = "Cancel", c = "mc.deleteUI(handExportWindowID)")

    

""""""""""""""""""""""""""""""""""""""""""
              #Main UI#
""""""""""""""""""""""""""""""""""""""""""
def makeUI():
    filePath = mc.file(f = True, sn = True, q = True)
    if 'Export' in filePath:
        saveToggle = False
    else:
        saveToggle = True
                
    handExportWindowID = "handExportWindow"
    if mc.window(handExportWindowID, exists=True):
        mc.deleteUI(handExportWindowID)
    mc.window(handExportWindowID, t = "Hand Export")
    mc.showWindow(handExportWindowID)

    fullLayout = mc.columnLayout()
    mainLayout = mc.frameLayout(l = "Hand Exporter", w = 400)
    
    mc.separator(style = 'in')
    mc.setParent(mainLayout)
    
    exportTypeUI()
    
    mc.setParent(mainLayout)
    mc.separator()

    saveExportFileUI(mainLayout)

    mc.setParent(mainLayout)
    mc.separator()

    importReferenceUI()
    
    mc.setParent(mainLayout)
    mc.separator()

    objectSelectionUI()

    mc.setParent(mainLayout)
    mc.separator()
    
    timeRangeUI(mainLayout)

    mc.setParent(mainLayout)
    mc.separator()

    clipInfoUI(mainLayout)

    mc.setParent(mainLayout)
    mc.separator()

    exportLocationUI(mainLayout)

    mc.setParent(mainLayout)
    mc.separator()

    goButtonsUI(mainLayout)

""""""""""""""""""""""""""""""""""""""""""
          #Refresh UI Elements# 
""""""""""""""""""""""""""""""""""""""""""    

def resetClipName():
    mc.textField('clipNameText', e = True, tx = save_load_manager.getFilePath()[3])