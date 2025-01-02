from settings import *

def import_image(*path, format = 'png', alpha = True): #unpaths the files
    fullPath = join(*path) + f'.{format}'
    return pygame.image.load(fullPath).convert_alpha() if alpha else pygame.image.load(fullPath).convert()

# the code above is useful if you are importing a lot of images

def import_folder(*path):
    frames = []
    for folderPath, subFolders, fileNames in walk(join(*path)):
        for fileName in sorted(fileNames, key = lambda name: int(name.split('.')[0])):
                fullPath = join(folderPath, fileName)
                surf = pygame.image.load(fullPath).convert_alpha()
                frames.append(surf)
        return frames

def audioImport(*path):
    audioDict = {}
    for folderPath, subFolders, fileNames in walk(join(*path)):
        for fileName in fileNames:
            fullPath = join(folderPath, fileName)
            audioDict[fileName.split('.')[0]] = pygame.mixer.Sound(fullPath)
    return audioDict
