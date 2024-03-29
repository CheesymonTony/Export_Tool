import maya.cmds as mc



""""""""""""""""""""""""""""""""""""""""""
      #Delete All Namespaces#
""""""""""""""""""""""""""""""""""""""""""        

def nameSpaceChange():
    allNodes = mc.ls()
    allNameSpaces = []
    
    for obj in allNodes:
        if ':' in obj:
            if obj.split(':')[0] not in allNameSpaces:
                allNameSpaces.append(obj.split(':')[0])
    if allNameSpaces != []:    
        for curNameSpace in allNameSpaces:
            if mc.namespace(exists = curNameSpace):
                mc.namespace(rm = curNameSpace, mnr = True)
                nameSpaceChange()
            else:
                nameSpaceChange()

""""""""""""""""""""""""""""""""""""""""""
       #Import Reference File#
""""""""""""""""""""""""""""""""""""""""""

def importRefFile():
    refs = mc.ls(type = 'reference')
    for i in refs:
        if mc.objExists(i):
            rFile = mc.referenceQuery(i, f = True)
            mc.file(rFile, importReference = True)