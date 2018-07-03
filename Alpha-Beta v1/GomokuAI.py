import datetime
import pygame
from pygame.locals import *
from sys import exit
import numpy as np
import random
import math


# 1 refers to black, 2 refers to white
class GomokuBoard:
    # get GUI sources
    def __init__(self):
        self.GUIInit()
        self.board =  [[0 for i in range(15)] for j in range(15)]
        self.dirs = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        self.dot_list = [
            (i * 35 - self.white.get_width() / 2 + 21, j * 35 - self.white.get_width() / 2 + 21) for i
            in range(15) for j in range(15)]
    def GUIInit(self):
        self.background_image = 'source/qp.jpg'
        self.white_image = 'source/baiz.png'
        self.black_image = 'source/heiz.png'
        self.Width = 530
        self.Height = 530
        pygame.init()
        self.screen = pygame.display.set_mode((self.Width, self.Height))
        pygame.display.set_caption('Gomoku Game')
        self.background = pygame.image.load(self.background_image).convert()
        self.white = pygame.image.load(self.white_image).convert_alpha()
        self.black = pygame.image.load(self.black_image).convert_alpha()
        self.screen.blit(self.background, (0, 0))
        self.font = pygame.font.SysFont("黑体", 40)
    # reset the board
    def reset(self):
        self.board = [[0 for i in range(15)] for j in range(15)]
        self.dot_list = [
            (i * 35 - self.white.get_width() / 2 + 21, j * 35 - self.white.get_width() / 2 + 21) for i
            in range(15) for j in range(15)]
    def getBoard(self):
        return self.board
    # to check if there is a winner
    # rtvalue: 0 no one, 1 black, 2 white
    def check(self):
        board = self.board
        dirs = ((1, -1), (1, 0), (1, 1), (0, 1))
        for i in range(15):
            for j in range(15):
                if board[i][j] == 0: continue
                id = board[i][j]
                for d in dirs:
                    x, y = j, i
                    count = 0
                    for k in range(5):
                        if board[y][x] != id: break
                        y += d[0]
                        x += d[1]
                        count += 1
                    if count == 5:
                        self.won = {}
                        r, c = i, j
                        for z in range(5):
                            self.won[(r, c)] = 1
                            r += d[0]
                            c += d[1]
                        return id
        return 0

    ## old code in the first time coding
    # used by pvpGUI to check the winner
    def _checkIsWin(self, x, y, array):
        count1, count2, count3, count4 = 0, 0, 0, 0
        i = x - 1
        while (i >= 0):
            if array[i][y] == 1:
                count1 += 1
                i -= 1
            else:
                break
        i = x + 1
        while i < 13:
            if array[i][y] == 1:
                count1 += 1
                i += 1
            else:
                break
        j = y - 1
        while (j >= 0):
            if array[x][j] == 1:
                count2 += 1
                j -= 1
            else:
                break
        j = y + 1
        while j < 13:
            if array[x][j] == 1:
                count2 += 1
                j += 1
            else:
                break

        i, j = x - 1, y - 1
        while (i >= 0 and j >= 0):
            if array[i][j] == 1:
                count3 += 1
                i -= 1
                j -= 1
            else:
                break
        i, j = x + 1, y + 1
        while (i <= 12 and j <= 12):
            if array[i][j] == 1:
                count3 += 1
                i += 1
                j += 1
            else:
                break

        i, j = x + 1, y - 1
        while (i >= 0 and j >= 0):
            if array[i][j] == 1:
                count4 += 1
                i += 1
                j -= 1
            else:
                break
        i, j = x - 1, y + 1
        while (i <= 12 and j <= 12):
            if array[i][j] == 1:
                count4 += 1
                i -= 1
                j += 1
            else:
                break
        if count1 >= 4 or count2 >= 4 or count3 >= 4 or count4 >= 4:
            return True
        else:
            return False
    # people vs people based on pygame GUI
    def pvpGUI(self):
        self.white_list = np.zeros((15, 15))
        self.black_list = np.zeros((15, 15))
        self.dot_list = [
            (i * 35 - self.white.get_width() / 2 + 21, j * 35 - self.white.get_width() / 2 + 21) for i
            in range(15) for j in range(15)]
        flag = True
        continueFlag = 1
        while True:
            if continueFlag == 0:
                break
            for event in pygame.event.get():
                if event.type == QUIT:
                    continueFlag = 0
                    break
                # Press R to replay
                # Press E to run away
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        self.screen.blit(self.background, (0, 0))
                        self.white_list = np.zeros((15, 15))
                        self.black_list = np.zeros((15, 15))
                        self.dot_list = [
                            (i * 35 - self.white.get_width() / 2 + 21, j * 35 - self.white.get_width() / 2 + 21) for i
                            in range(15) for j in range(15)]
                        flag = True
                    elif event.key == K_e:
                        continueFlag = 0
                        break
                if event.type == MOUSEBUTTONDOWN:
                    # for item in dot_list:
                    #     screen.blit(white, item)
                    x, y = pygame.mouse.get_pos()
                    if 0 <= x <= 530 and 0 <= y <= 530:
                        m = int(round((x - 21) / 35))
                        n = int(round((y - 21) / 35))
                        try:
                            if flag:
                                flag = not flag
                                self.screen.blit(self.black, self.dot_list[15 * m + n])
                                self.black_list[n][m] = 1
                                if self._checkIsWin(n, m, self.black_list):
                                    self.screen.blit(self.font.render('GAME OVER,Black WIN!', True, (0, 0, 0)),
                                                     (56 + 35, 56 + 35))
                            else:
                                flag = not flag
                                self.screen.blit(self.white, self.dot_list[15 * m + n])
                                self.white_list[n][m] = 1
                                if self._checkIsWin(n, m, self.white_list):
                                    self.screen.blit(self.font.render('GAME OVER,White WIN!', True, (0, 0, 0)),
                                                     (56 + 35, 56 + 35))
                            self.dot_list[15 * m + n] = ''
                        except:
                            pass
            pygame.display.update()
    ## end of first time old coding
    # people vs AI
    def pve(self,searcher):
        self.board = [[0 for i in range(15)] for j in range(15)]
        self.dot_list = [
            (i * 35 - self.white.get_width() / 2 + 21, j * 35 - self.white.get_width() / 2 + 21) for i
            in range(15) for j in range(15)]
        self.searcher = searcher
        continueFlag = 1
        while True:
            if continueFlag == 0:
                break
            for event in pygame.event.get():
                if event.type == QUIT:
                    continueFlag = 0
                    break
                # Press R to replay
                # Press E to run away
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        self.reset()
                    elif event.key == K_e:
                        continueFlag = 0
                        break
                if event.type == MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 0 <= x <= 530 and 0 <= y <= 530:
                        m = int(round((x - 21) / 35))
                        n = int(round((y - 21) / 35))
                        try:
                            self.screen.blit(self.black, self.dot_list[15 * m + n])
                            self.board[m][n] = 1
                            if self.check() == 1:
                                self.screen.blit(self.font.render('GAME OVER,Black WIN!', True, (0, 0, 0)),
                                                (56 + 35, 56 + 35))

                            score, x, y = self.searcher.search(turn=2, board=self.getBoard(),depth=1)
                            self.board[x][y] = 2
                            self.screen.blit(self.white, self.dot_list[15 * x + y])
                            self.dot_list[15 * x + y] = ''
                            if self.check() == 2:
                                self.screen.blit(self.font.render('GAME OVER,White WIN!', True, (0, 0, 0)),
                                                     (56 + 35, 56 + 35))
                        except Exception as e:
                            print(e)
            pygame.display.update()

    # print the board in console
    def show(self):
        for i in range(15):
            print(self.board[i])
        print('')
def psyco_speedup():
    try:
        import psyco
        psyco.bind(chessboard)
        psyco.bind(evaluation)
    except:
        pass
    return 0

psyco_speedup()

# to evaluate the profit value of the current board
class Evaluator:
    def __init__(self):
        self.board = [[0 for i in range(15)] for j in range(15)]
        self.FiveLinked = [[1,1,1,1,1]]
        self.LiveFour = [[0,1,1,1,1,0],[0,1,0,1,1,1,0],[0,1,1,1,0,1,0],[0,1,1,0,1,1,0]]
        self.SleptFour = [[0,1,1,1,1,2],[0,1,1,1,0,1,2],[0,1,1,1,0,1,2],[0,1,1,0,1,1,2],[0,1,0,1,1,1,2],
                        [2, 1, 1, 1, 1, 0],[2, 1, 0,1, 1, 1, 0],[2, 1, 1,0, 1, 1, 0],[2, 1, 1, 1, 0,1, 0]]
        self.LiveThree = [[0,1,1,1,0],[0,1,1,0,1,0],[0,1,0,1,1,0]]
        self.SleptThree = [[2, 1, 1, 1, 0],[2, 1, 0,1, 1, 0],[2, 1, 1,0, 1, 0],
                           [0, 1, 1, 1, 2],[0, 1,0,1, 1, 2],[0, 1, 1,0, 1, 2]]
        self.LiveTwo = [[0, 1, 1, 0],[0,1,0,1,0]]
        self.SleptTwo = [[2, 1, 1, 0],[2, 1, 0,1, 0],[0, 1, 1, 2],[0, 1,0, 1, 2]]
        self.modes = []
        self.modes.append(self.FiveLinked)
        self.modes.append(self.LiveFour)
        self.modes.append(self.SleptFour)
        self.modes.append(self.LiveThree)
        self.modes.append(self.SleptThree)
        self.modes.append(self.LiveTwo)
        self.modes.append(self.SleptTwo)
        self.countModes = [0 for i in range(len(self.modes))]
        self.base = [[0 for i in range(15)] for j in  range(15)]
        self.base[7][7] = 10
        for i in range(15):
            for j in range(15):
                temp = max(abs(i - 7), abs(j - 7))
                self.base[i][j] = 10 - temp
        self.POS = self.base
        # two live three
        # two live two to consist two live three
    def _tranverse(self, turn):
        dturn = 2 if turn == 1 else 1
        for i in range(15):
            for j in range(15):
                if self.board[i][j] == turn:
                    self.board[i][j] = 1
                elif self.board[i][j] == dturn:
                    self.board[i][j] = 2
                else:
                    self.board[i][j] = 0
    def _mathcing(self,longs,subs):
        res = 0
        for i in range(len(longs)-len(subs)+1):
            if longs[i] == subs[0]:
                cnt = 1
                while cnt+i<len(longs) and cnt<len(subs) and longs[i+cnt] == subs[cnt]:
                    cnt+=1
                if cnt == len(subs):
                    res += 1
        return res
    def _evaluate_line(self,line):
        for i in range(len(self.modes)):
            for mode in self.modes[i]:
                self.countModes[i] += self._mathcing(line,mode)
    def _evaluate_lines(self):
        # horizon analysis
        for i in range(15):
            self._evaluate_line(self.board[i])
        # vertical analysis
        for j in range(15):
            line = []
            for i in range(15):
                line.append(self.board[i][j])
            self._evaluate_line(line)
        # main diagonal line analysis
        for i in range(15):
            line = []
            x = i
            y = 0
            while x < 15 and y < 15:
                line.append(self.board[x][y])
                x += 1
                y += 1
            self._evaluate_line(line)
            x = 0
            y = i
            while x < 15 and y < 15:
                line.append(self.board[x][y])
                x += 1
                y += 1
            self._evaluate_line(line)
        # second diagonal line analysis
        for i in range(15):
            line = []
            x = i
            y = 0
            while x >= 0 and x < 15 and y < 15:
                line.append(self.board[x][y])
                x -= 1
                y += 1
            self._evaluate_line(line)
            x = 14
            y = i
            while x >= 0 and x < 15 and y >= 0 and y < 15:
                line.append(self.board[x][y])
                x -= 1
                y += 1
            self._evaluate_line(line)
    def _evaluate(self,turn):
        self.countModes = [0 for i in range(len(self.modes))]
        self._tranverse(turn)
        self._evaluate_lines()
        score = 0
        if self.countModes[0]>0:   score+=10000
        if self.countModes[1]>0:   score+=10000
        if self.countModes[2]>1:
            score += 10000
        elif self.countModes[2]> 0:
            score += 3000
        if self.countModes[3] > 1:
            score += 2000
        elif self.countModes[3]>0:
            score += 500
        score += (self.countModes[4])*10
        score += (self.countModes[5])*4
        score += (self.countModes[6])
        if turn == 2:
            self._tranverse(2)
        print(self.countModes)
        return score
    def evaluate(self,board,turn):
        self.board = board
        #self.board = copy.deepcopy(board)
        dturn = 1 if turn == 2 else 2
        myScore = self._evaluate(turn)
        #self.board = copy.deepcopy(board)
        dScore = self._evaluate(dturn)
        return  myScore- dScore*1.1
# to give the best position according to the evaluator
class Searcher:
    def __init__(self):
        self.board = [[0 for i in range(15)] for j in range(15)]
        self.evaluator = Evaluator()
        self.base = np.zeros((15, 15))
        self.base[7][7] = 70
        for i in range(15):
            for j in range(15):
                temp = max(abs(i - 7), abs(j - 7))
                self.base[i][j] = 70- temp * 10
        self.moves = []
        for i in range(15):
            for j in range(15):
                self.moves.append((self.base[i][j],i,j))
        self.moves.sort(reverse=True)
        self.depthLimit = 3
        self.bestmove = (-1,-1)
        self.maxn = -1
    def _search(self,turn,depth,maxn=-1e9+7,minn=1e9+7):
        score = self.evaluator.evaluate(self.board,turn)
        if depth< 0:
            return score
        bestmove = (-1,-1)
        for s, x, y in self.moves:
            if self.board[x][y] != 0:
                continue
            self.board[x][y] = turn
            dturn = 1 if turn == 2 else 2
            score =- self._search(dturn, depth-1,-minn,-maxn )
            self.board[x][y] = 0
            if score > maxn:
                maxn = score
                bestmove = (x,y)
                if maxn >= minn:
                    break
                    break
        if depth == self.depthLimit:
            self.bestmove = bestmove
        return maxn
    def search(self,board,turn,depth=3):
        self.board = board
        self.depthLimit = depth
        self.bestmove = (-1,-1)
        self.maxn = self.evaluator.evaluate(board,turn)
        score = self._search(turn,depth)
        x,y = self.bestmove
        print((x,y))
        return score,x,y



if (__name__ == "__main__"):
    board = GomokuBoard()
    searcher = Searcher()
    #board.pve(searcher)
    board.pvpGUI()