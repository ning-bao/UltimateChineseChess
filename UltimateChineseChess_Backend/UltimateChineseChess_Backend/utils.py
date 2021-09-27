import json
import uuid
import os
from django import shortcuts


class UltimateChineseChess:
    '''
        Utils for the UltimateChineseChess
        It contains all major processing functions which would be used in the project.
    '''

    def __init__(self, skipping: bool, language: str, gameId: str) -> None:
        '''
            skipping: a boolean to choose to load tutorial or not
        '''
        self.__skipping = skipping
        self.__language = language
        # print(gameId)
        if __name__ == "__main__":
            f = open('./UltimateChineseChess_Backend/SavedGamePlay/%s.json' % gameId)
        else:
            f = open('./SavedGamePlay/%s.json' % gameId)
        self.currentMap = json.load(f)["currentMap"]
        # print(self.currentMap)
        f.close()
        # print(self.currentMap)
        self.initialMap = [
            ["b_car", "b_horse", "b_elephant", "b_knight", "b_king", "b_knight", "b_elephant", "b_horse", "b_car"],
            ["", "", "", "", "", "", "", "", ""],
            ["", "b_cannon", "", "", "", "", "", "b_cannon", ""],
            ["b_soldier", "", "b_soldier", "", "b_soldier", "", "b_soldier", "", "b_soldier", ],
            [],
            [],
            ["r_soldier", "", "r_soldier", "", "r_soldier", "", "r_soldier", "", "r_soldier", ],
            ["", "r_cannon", "", "", "", "", "", "r_cannon", ""],
            ["", "", "", "", "", "", "", "", ""],
            ["r_car", "r_horse", "r_elephant", "r_knight", "r_king", "r_knight", "r_elephant", "r_horse", "r_car"],
        ]
        self.chessPlay = {}
        self.gameID = gameId
        self.player = -1

    def startTutorial(self):
        # Loading language pack from .json
        f = open('./UltimateChineseChess_Backend/languagePack/%s_tutorial.json' % self.__language, encoding='utf-8')
        languagePack = json.load(f)

        if self.__skipping:
            return [languagePack['skipping']]
        else:
            return [languagePack['welcome'],
                    [languagePack['rule_soldier'], languagePack['rule_cannon'], languagePack['rule_car'],
                     languagePack['rule_horse'], languagePack['rule_elephant'], languagePack['rule_knights'],
                     languagePack['rule_king']]]

    def loadChessPlay(self):
        # Load user saved chess play
        if __name__ == "__main__":
            f = open('UltimateChineseChess/SavedGamePlay/%s.json' % self.gameID)
        else:
            f = open('SavedGamePlay/%s.json' % self.gameID)
        self.chessPlay = json.load(f)
        # Load Player
        operation = self.chessPlay["GamePlay"]
        self.player = len(operation) % 2

    def saveChessPlay(self, newOperation):
        operation = self.chessPlay["GamePlay"]
        self.chessPlay["GamePlay"]["%s" % len(operation)] = newOperation
        json.dump(self.chessPlay, "SavedGamePlay/%s.json" % self.gameID)

    def moveChess(self, initialLocation: list, finalLocation: list):

        '''
        Passing in locations [row, column]
        '''
        chessMap = self.currentMap
        
        # [Left][right]
        chessName = chessMap[initialLocation[0]][initialLocation[1]]

        # Verify if it's valid to move the chess
        self.verifyChess(chessName, initialLocation, finalLocation, self.player)

        gamePlayOperation = [chessName, "%s" % initialLocation, "%s" % finalLocation]
        self.saveChessPlay(gamePlayOperation)

        return self.currentMap

    def verifyChess(self, name, initialLocation: list, finalLocation: list, player: int):
        # print(initialLocation)
        # print(finalLocation)
        # Check if initial and final are in the chess board

        # print(name,initialLocation,finalLocation,player)
        if not (0 <= initialLocation[0] <= 9 and 0 <= initialLocation[1] <= 8 and 0 <= finalLocation[0] <= 9 and 0 <=
                finalLocation[1] <= 8):
            return False

        # Check if the initial location is empty
        if self.currentMap[initialLocation[0]][initialLocation[1]] == "":
            return False

        # Check if the Player No. matches the chess moving
        if not player:
            if 'r_' not in name:
                return False
        else:
            if 'b_' not in name:
                return False
        verticalMovement = finalLocation[0] - initialLocation[0]
        horizontalMovement = finalLocation[1] - initialLocation[1]

        # Game Rules
        if not player:
            if "r_" in self.currentMap[finalLocation[0]][finalLocation[1]]:
                return False
        else:
            if "b_" in self.currentMap[finalLocation[0]][finalLocation[1]]:
                return False

        enemySide = True  # for soldiers
        if 'car' in name:
            if finalLocation[0] == initialLocation[0]:
                if finalLocation[1] == initialLocation[1]:
                    return False

                # Check if there are anything in the way
                    # Judging direction of moving(left or right)
                for i in range(1, abs(horizontalMovement)):
                    if horizontalMovement > 0:
                        if self.currentMap[initialLocation[0]][initialLocation[1] + i] != "":
                            return False
                    else:
                        if self.currentMap[initialLocation[0]][initialLocation[1] - i] != "":
                            return False
            else:
                if finalLocation[1] != initialLocation[1]:
                    return False
                for i in range(1, abs(verticalMovement)):
                    # Judging direction of moving(down or up)
                    # print(i)
                    # print(initialLocation)
                    if verticalMovement > 0:
                        if self.currentMap[initialLocation[0] + i][initialLocation[1]] != "":
                            return False
                    else:
                        if self.currentMap[initialLocation[0] - i][initialLocation[1]] != "":
                            return False

        elif 'horse' in name:
            if ((abs(verticalMovement) == 2 and abs(
                    horizontalMovement) == 1) or (
                    abs(verticalMovement) == 1 and abs(
                horizontalMovement) == 2)):
                # Check if there are obstacles
                if abs(verticalMovement) == 2:
                    if self.currentMap[initialLocation[0] + int(verticalMovement / 2)][initialLocation[1]] != "":
                        return False

                elif abs(horizontalMovement) == 2:
                    if self.currentMap[initialLocation[0]][initialLocation[1] + int(horizontalMovement / 2)] != "":
                        return False
            else:
                return False

        elif 'elephant' in name:
            if abs(verticalMovement) == 2 and abs(horizontalMovement)==2:
                if self.currentMap[initialLocation[0] + int(verticalMovement / 2)][
                    initialLocation[1] + int(horizontalMovement / 2)] != "":
                    return False
            else:
                return False

        elif 'knight' in name:
            if 3 <= finalLocation[1] <= 5 and (7 <= finalLocation[0] <= 9 or 3 <= finalLocation[1] <= 5):
                if not (abs(verticalMovement) == 1 and abs(horizontalMovement) == 1):
                    return False
            else:
                return False

        elif 'cannon' in name:
            obstacleCount = 0
            if finalLocation[0] == initialLocation[0]:
                if finalLocation[1] == initialLocation[1]:
                    return False

                # Check if there are anything in the way
                for i in range(1, abs(horizontalMovement)):
                    # Judging direction of moving(down or up)
                    if horizontalMovement > 0:
                        if self.currentMap[initialLocation[0]][initialLocation[1] + i] != "":
                            obstacleCount += 1
                    else:
                        if self.currentMap[initialLocation[0]][initialLocation[1] - i] != "":
                            obstacleCount += 1
            else:
                if finalLocation[1] != initialLocation[1]:
                    return False
                for i in range(1, abs(verticalMovement)):
                    # Judging direction of moving(left or right)

                    if verticalMovement > 0:
                        if self.currentMap[initialLocation[0] + i][initialLocation[1]] != "":
                            obstacleCount += 1
                    else:
                        if self.currentMap[initialLocation[0] - i][initialLocation[1]] != "":
                            obstacleCount += 1
            if obstacleCount > 1:
                return False
            if obstacleCount == 1 and self.currentMap[finalLocation[0]][finalLocation[1]] == "":
                return False
            if obstacleCount == 0 and self.currentMap[finalLocation[0]][finalLocation[1]] != "":
                return False

        elif name == "b_soldier":
            if 3 <= initialLocation[0] <= 4:
                enemySide = False
            if enemySide:
                if not (abs(horizontalMovement) == 1 or verticalMovement == 1):
                    return False
            else:
                if not verticalMovement == 1 and horizontalMovement == 0:
                    return False

        elif name == 'r_soldier':
            if 5 <= initialLocation[0] <= 6:
                enemySide = False
            if enemySide:
                if not ((abs(horizontalMovement) == 1 and verticalMovement==0) or (verticalMovement == -1 and horizontalMovement==0)):
                    return False
            else:
                if not (verticalMovement == -1 and horizontalMovement == 0):
                    return False

        elif 'king' in name:
            if 3 <= finalLocation[1] <= 5 and (7 <= finalLocation[0] <= 9 or 0 <= finalLocation[0] <= 2):
                if not ((abs(horizontalMovement) == 1 and verticalMovement==0) or (abs(verticalMovement) == 1 and horizontalMovement==0)):
                    return False
            else:
                return False

        else:
            return False
    
        return True


if __name__ == '__main__':
    print(os.getcwd())
    chess = UltimateChineseChess(True, 'en-us', '00000001')
    print(chess.startTutorial())
    '''
    About variable Naming:
        b_soldier: Black Soldier
        r_soldier: Red Soldier
    '''
    print(chess.verifyChess("r_king",[9,4],[8,4],0))