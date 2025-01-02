import pygame
from random import choice, uniform
from os.path import join

screenWidth, screenHeight = 1280, 720
size = {'paddle': (40, 100), 'ball': (30,30)}
speed = {'player' : 500, 'opponent': 500, 'ball': 450}
colours = {
    'bg' : (146, 232, 198),
    'paddle' : '#ee322c',
    'paddleShadow' : '#ee622c',
    'ball' : '#c14f24',
    'ballShadow': '#002633' 
}