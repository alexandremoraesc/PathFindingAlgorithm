import pygame as pg
import sys
from Tiles import Tiles
from grafoTiles import Grafo

GAME_WIDTH = 500
GAME_HEIGHT = 500
FILESNUMBER = 25
SQ_SIZE = GAME_WIDTH//FILESNUMBER
MAX_FPS = 30
rcToTiles = {}
dicTiles = {}

def main():
    global rcToTiles, dicTiles
    running = True
    pg.init()
    screen = pg.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))
    tiles = setTiles(FILESNUMBER)
    drawFiles(screen)
    while running: 
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
                pg.quit()
                exit()
            elif e.type == pg.MOUSEBUTTONDOWN:
                #print('hi pressed first button')
                location = pg.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                a = findTile(row, col)
                #print(a.number)
                #print(a.vizinhos)
                if a.filled:
                    a.filled = False
                    updateNeibour(a)
                    #print(a.vizinhos)
                else:
                    a.filled = True
                    updateNeibour(a)
                    #print(a.vizinhos)
                drawFiles(screen)
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_s:
                    #print('hi pressed s')
                    location = pg.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    a = findTile(row, col)
                    if not a.start:
                        a.start = True
                        start = a.number
                    else:
                        a.start = False
                    drawFiles(screen)
                elif e.key == pg.K_e:
                    #print('hi pressed e')
                    location = pg.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    a = findTile(row, col)
                    if not a.end:
                        a.end = True
                        end = a.number
                    else:
                        a.end = False
                    drawFiles(screen)
                elif e.key == pg.K_SPACE:
                    print(start)
                    dist = getDistance(dicTiles, start)
                    drawPath(dist[1], start, end, screen)
                    print(f'A distância até o quadrado {end} é de {dist[0][end]}')



        clock.tick(MAX_FPS)
        pg.display.flip()


def drawFiles(screen):
    for r in range(FILESNUMBER):
        for c in range(FILESNUMBER):
            Tile = findTile(r,c)
            drawTile(screen, Tile)

def drawTile(screen, Tile):
    if not Tile.start:
        if not Tile.end:
            if Tile.filled:
                #print(f'Filled - Tile ({Tile.r}, {Tile.c}')
                pg.draw.rect(screen, pg.Color("Black"), pg.Rect((Tile.c)*SQ_SIZE, (Tile.r)*SQ_SIZE, SQ_SIZE, SQ_SIZE), 0)
            else:
                #print(f'Not filled - Tile ({Tile.r}, {Tile.c}')
                pg.draw.rect(screen, pg.Color("White"), pg.Rect((Tile.c)*SQ_SIZE, (Tile.r)*SQ_SIZE, SQ_SIZE, SQ_SIZE), 0)
                pg.draw.rect(screen, pg.Color("Black"), pg.Rect((Tile.c)*SQ_SIZE, (Tile.r)*SQ_SIZE, SQ_SIZE, SQ_SIZE), 1)

        else:
            pg.draw.rect(screen, pg.Color("Red"), pg.Rect((Tile.c)*SQ_SIZE, (Tile.r)*SQ_SIZE, SQ_SIZE, SQ_SIZE), 0)

    else:
        pg.draw.rect(screen, pg.Color("Yellow"), pg.Rect((Tile.c)*SQ_SIZE, (Tile.r)*SQ_SIZE, SQ_SIZE, SQ_SIZE), 0)


def setTiles(n):
    global rcToTiles, dicTiles
    tiles = []
    for r in range(FILESNUMBER):
        for c in range(FILESNUMBER):
            a = Tiles(r,c)
            if (r - 1 >= 0):
                a.vizinhos.append(Tiles(r-1, c).number)
            if (r + 1 < FILESNUMBER):
                a.vizinhos.append(Tiles(r+1, c).number)
            if (c-1 >= 0):
                a.vizinhos.append(Tiles(r,c-1).number)
            if (c + 1 < FILESNUMBER):
                a.vizinhos.append(Tiles(r, c+1).number) 
            
            tiles.append(a)
            key = (r,c)
            rcToTiles.update({key: a})
            dicTiles.update({a.number:a.vizinhos})
    return tiles 


def findTile(r,c):    
    return rcToTiles[(r,c)]

def updateNeibour(Tile):
    if Tile.filled:
        if (Tile.r - 1 >= 0):
            try:
                Tile.vizinhos.remove(Tiles(Tile.r-1, Tile.c).number)
                vizinho = findTile(Tile.r-1, Tile.c)
                vizinho.vizinhos.remove(Tile.number)
            except:
                pass

        if (Tile.r + 1 < FILESNUMBER):
            try:
                Tile.vizinhos.remove(Tiles(Tile.r+1, Tile.c).number)
                vizinho = findTile(Tile.r+1, Tile.c)
                vizinho.vizinhos.remove(Tile.number)

            except:
                pass
        if (Tile.c-1 >= 0):
            try:
                Tile.vizinhos.remove(Tiles(Tile.r,Tile.c-1).number)
                vizinho = findTile(Tile.r, Tile.c-1)
                vizinho.vizinhos.remove(Tile.number)

            except:
                pass    
        
        if (Tile.c + 1 < FILESNUMBER):
            try:
                Tile.vizinhos.remove(Tiles(Tile.r, Tile.c+1).number)
                vizinho = findTile(Tile.r, Tile.c+1)
                vizinho.vizinhos.remove(Tile.number)
            except:
                pass

#        print(dicTiles)

    else:
        if (Tile.r - 1 >= 0):
            vizinho = findTile(Tile.r-1, Tile.c)
            if not vizinho.filled:
                Tile.vizinhos.append(Tiles(Tile.r-1, Tile.c).number)
                vizinho.vizinhos.append(Tile.number)

        if (Tile.r + 1 < FILESNUMBER):
            vizinho = findTile(Tile.r+1, Tile.c)
            if not vizinho.filled:
                Tile.vizinhos.append(Tiles(Tile.r+1, Tile.c).number)
                vizinho.vizinhos.append(Tile.number)

        if (Tile.c-1 >= 0):
            vizinho = findTile(Tile.r, Tile.c-1)
            if not vizinho.filled:
                Tile.vizinhos.append(Tiles(Tile.r, Tile.c-1).number)
                vizinho.vizinhos.append(Tile.number)

        if (Tile.c + 1 < FILESNUMBER):
            vizinho = findTile(Tile.r, Tile.c+1)
            if not vizinho.filled:
                Tile.vizinhos.append(Tiles(Tile.r, Tile.c+1).number)
                vizinho.vizinhos.append(Tile.number)

 #       print(dicTiles)

def getDistance(dicTiles, vertice):
    grafo = Grafo(dicTiles)
    return grafo.Dijkstra(vertice)


def drawPath(parents, start, end, screen):
    while parents[end] != start:
        row = parents[end]//25
        col = parents[end] - 25*row
        pg.draw.rect(screen, pg.Color("Dark Green"), pg.Rect((col)*SQ_SIZE, (row)*SQ_SIZE, SQ_SIZE, SQ_SIZE), 0)
        end = parents[end]


if __name__ == "__main__":
    main()