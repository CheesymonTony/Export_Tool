import maya.cmds as mc
import pymel.core as pm
import importlib


import UI
importlib.reload(UI)


""""""""""""""""""""""""""""""""""""""""""
    #Get save and export file paths#
""""""""""""""""""""""""""""""""""""""""""
            
def getFilePath():
    fullPath = mc.file(f = True, sn = True, q = True)
    if fullPath == '':
        defaultDir = 'No default path located'
        saveName = ''
        exportName = ''
        
    else:
        dirList = fullPath.split('/')
        curSceneFile = dirList[(len(dirList) - 1)]
        fileName = curSceneFile.split('.')[0]
        fileExt = curSceneFile.split('.')[1]
        defaultDir = dirList[0] + '/' + dirList[1] + '/' + dirList[2] + '/Documents/maya/TempFiles'
        saveName = '/' + fileName + '_Export.' + fileExt 
        nameDetails = fileName.split('_')
        nameDetailsLen = len(nameDetails) - 1
        joiner = '_'
        newNameDetails = []
        for obj in nameDetails:
            if obj != nameDetails[nameDetailsLen]:
                if 'Animation' not in obj:
                    newNameDetails.append(obj)
        exportName = joiner.join(newNameDetails)
     
    return fullPath, defaultDir, saveName, exportName

""""""""""""""""""""""""""""""""""""""""""
       #Save File before export#
""""""""""""""""""""""""""""""""""""""""""
            
def saveLoc(ynCB, dlCB, custPath):
    if dlCB == True:
        if custPath == False:
            message1 = 'In order to use the save feature, you must either:'
            message2 = 'Save the current scene to a location'
            message3 = 'Turn off the "Save on Export" option'
            message4 = 'Choose a custom location to save the file to'
            UI.errorWindow(message1, message2, message3, message4)
        else:
            newSavePath = getFilePath()[1] + getFilePath()[2]
            pm.saveAs(newSavePath, f = True)
            print(newSavePath)
    elif dlCB == False and custPath == False:
        message1 = 'If you want to save to a custom location:'
        message2 = 'Set the custom location by using the "Browse" button'
        message3 = None
        message4 = None
        UI.errorWindow(message1, message2, message3, message4)
    
    else:
        savePath = mc.textField('saveLocTxt', q = True, tx = True)
        exportName = getFilePath()[2]
        finalSaveLoc = savePath + exportName
        pm.saveAs(finalSaveLoc, f = True)

""""""""""""""""""""""""""""""""""""""""""
       #Determine Export Location#
""""""""""""""""""""""""""""""""""""""""""
        
def exportLocation(textInput):
    basicFilter = 'Maya Files(*.mb *.ma)'
    directory = mc.fileDialog2(fileFilter=basicFilter, dialogStyle=1, fm = 3)
    directoryName = str(directory).split("'")[1]
    mc.textField(textInput, e = True, tx = directoryName)