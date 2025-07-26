from os import walk
import pygame

def importFolder(path):
    surfaceList = []

    for folder,subfolder,imgFiles in walk(path):
        # Sort files numerically to ensure correct frame order
        imgFiles = sorted(imgFiles, key=lambda x: int(x.split('.')[0]))
        for image in imgFiles:
            # path + image to get full path
            fullPath = path + '/' + image 
            # import pygame and use fullPath to import one specific surface
            imageSurf =  pygame.image.load(fullPath).convert_alpha()
            surfaceList.append(imageSurf)

    return surfaceList

def importFolderDictionary(path):
    surfaceDict = {}
    for folder,subfolder,imgFiles in walk(path):
        for image in imgFiles:
            # path + image to get full path
            fullPath = path + '/' + image 
            imageSurf =  pygame.image.load(fullPath).convert_alpha()
            surfaceDict[image.split('.')[0]] = imageSurf
    return surfaceDict