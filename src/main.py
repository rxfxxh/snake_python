import pygame
from classeCobra import Cobra
from classeComida import Comida
from classeJogo import JogoCobrinha
import random
from time import sleep as wait

if __name__ == "__main__":
    jogo = JogoCobrinha()
    jogo.loop()


