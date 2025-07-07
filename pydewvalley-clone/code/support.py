from os import walk
import pygame

def importFolder(path):
    surfaceList = []

    for folder,subfolder,imgFiles in walk(path):
        for image in imgFiles:
            # path + image to get full path
            fullPath = path + '/' + image 
            # import pygame and use fullPath to import one specific surface
            imageSurf =  pygame.image.load(fullPath).convert_alpha()
            surfaceList.append(imageSurf)

    return surfaceList