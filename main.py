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
    hasStart = False
    hasEnd = False
    while running: 
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
                pg.quit()
                exit()
            elif e.type == pg.MOUSEBUTTONDOWN:
                location = pg.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                a = findTile(row, col)
                if a.filled:
                    a.filled = False
                    updateNeibour(a)
                else:
                    a.filled = True
                    updateNeibour(a)
                drawFiles(screen)
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_s:
                    location = pg.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    a = findTile(row, col)
                    if not hasStart:
                        if not a.start:
                            a.start = True
                            a.filled = False
                            hasStart = True
                            start = a.number
                    else:
                        if a.start:
                            a.start = False
                            hasStart = False
                    drawFiles(screen)

                elif e.key == pg.K_e:
                    location = pg.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    a = findTile(row, col)
                    
                    if not hasEnd:
                        if not a.end:
                            a.end = True
                            a.filled = False
                            hasEnd = True
                            end = a.number

                    else:
                        if a.end:
                            a.end = False
                            hasEnd = False
                    drawFiles(screen)
                elif e.key == pg.K_SPACE:
                    print(start)
                    dist = getDistance(dicTiles, start, end)
                    drawVisitados(dist[2], screen, start, end)
                    drawPath(dist[1], start, end, screen)
                    print(f'A distância de {start} até o quadrado {end} é de {dist[0][end]}')

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
                pg.draw.rect(screen, pg.Color("Black"), pg.Rect((Tile.c)*SQ_SIZE, (Tile.r)*SQ_SIZE, SQ_SIZE, SQ_SIZE), 0)
            else:
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
            a = Tiles(r,c, filesnumber= FILESNUMBER)
            if (r - 1 >= 0):
                a.vizinhos.append(Tiles(r-1, c, filesnumber= FILESNUMBER).number)
            if (r + 1 < FILESNUMBER):
                a.vizinhos.append(Tiles(r+1, c, filesnumber= FILESNUMBER).number)
            if (c-1 >= 0):
                a.vizinhos.append(Tiles(r,c-1, filesnumber= FILESNUMBER).number)
            if (c + 1 < FILESNUMBER):
                a.vizinhos.append(Tiles(r, c+1, filesnumber= FILESNUMBER).number) 
            
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
                Tile.vizinhos.remove(Tiles(Tile.r-1, Tile.c, filesnumber= FILESNUMBER).number)
                vizinho = findTile(Tile.r-1, Tile.c)
                vizinho.vizinhos.remove(Tile.number)
            except:
                pass

        if (Tile.r + 1 < FILESNUMBER):
            try:
                Tile.vizinhos.remove(Tiles(Tile.r+1, Tile.c, filesnumber= FILESNUMBER).number)
                vizinho = findTile(Tile.r+1, Tile.c)
                vizinho.vizinhos.remove(Tile.number)

            except:
                pass
        if (Tile.c-1 >= 0):
            try:
                Tile.vizinhos.remove(Tiles(Tile.r,Tile.c-1, filesnumber= FILESNUMBER).number)
                vizinho = findTile(Tile.r, Tile.c-1)
                vizinho.vizinhos.remove(Tile.number)

            except:
                pass    
        
        if (Tile.c + 1 < FILESNUMBER):
            try:
                Tile.vizinhos.remove(Tiles(Tile.r, Tile.c+1, filesnumber= FILESNUMBER).number)
                vizinho = findTile(Tile.r, Tile.c+1)
                vizinho.vizinhos.remove(Tile.number)
            except:
                pass
    else:
        if (Tile.r - 1 >= 0):
            vizinho = findTile(Tile.r-1, Tile.c)
            if not vizinho.filled:
                Tile.vizinhos.append(Tiles(Tile.r-1, Tile.c, filesnumber= FILESNUMBER).number)
                vizinho.vizinhos.append(Tile.number)

        if (Tile.r + 1 < FILESNUMBER):
            vizinho = findTile(Tile.r+1, Tile.c)
            if not vizinho.filled:
                Tile.vizinhos.append(Tiles(Tile.r+1, Tile.c, filesnumber= FILESNUMBER).number)
                vizinho.vizinhos.append(Tile.number)

        if (Tile.c-1 >= 0):
            vizinho = findTile(Tile.r, Tile.c-1)
            if not vizinho.filled:
                Tile.vizinhos.append(Tiles(Tile.r, Tile.c-1, filesnumber= FILESNUMBER).number)
                vizinho.vizinhos.append(Tile.number)

        if (Tile.c + 1 < FILESNUMBER):
            vizinho = findTile(Tile.r, Tile.c+1)
            if not vizinho.filled:
                Tile.vizinhos.append(Tiles(Tile.r, Tile.c+1, filesnumber= FILESNUMBER).number)
                vizinho.vizinhos.append(Tile.number)

def getDistance(dicTiles, vertice, final):
    grafo = Grafo(dicTiles)
    return grafo.Dijkstra(vertice, final)


def drawPath(parents, start, end, screen):
    while parents[end] != start:
        row = parents[end]//FILESNUMBER
        col = parents[end] - FILESNUMBER*row
        pg.draw.rect(screen, pg.Color("Dark Green"), pg.Rect((col)*SQ_SIZE + 1, (row)*SQ_SIZE + 1, SQ_SIZE-2, SQ_SIZE-2), 0)
        end = parents[end]

def drawVisitados(visitados, screen, start, end):
    for visitado in visitados:
        if visitado != end and visitado != start:
            row = visitado//FILESNUMBER
            col = visitado - FILESNUMBER*row
            pg.draw.rect(screen, pg.Color("Blue"), pg.Rect((col)*SQ_SIZE + 1, (row)*SQ_SIZE +1, SQ_SIZE -2, SQ_SIZE-2), 0)


if __name__ == "__main__":
    main()