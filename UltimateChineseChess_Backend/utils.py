import json
import uuid


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
        self.currentMap = [[], [], [], [], [], [], [], [], [], []]
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
        f = open('languagePack/%s_tutorial.json' % self.__skipping, encoding='utf-8')
        languagePack = json.load(f)

        if not self.__tutorial:
            return [languagePack['skipping']]
        else:
            return [languagePack['welcome'],
                    [languagePack['rule_soldier'], languagePack['rule_cannon'], languagePack['rule_car'],
                     languagePack['rule_horse'], languagePack['rule_elephant'], languagePack['rule_knights'],
                     languagePack['rule_king']]]

    def loadChessPlay(self):
        # Load user saved chess play
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
        # Check if initial and final are in the chess board
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
                for i in range(1, abs(horizontalMovement)):
                    # Judging direction of moving(down or up)
                    if horizontalMovement > 0:
                        if self.currentMap[initialLocation[0]][initialLocation[1] + i] != "":
                            return False
                    else:
                        if self.currentMap[initialLocation[0]][initialLocation[1] - i] != "":
                            return False
            else:
                for i in range(1, abs(verticalMovement)):
                    # Judging direction of moving(left or right)
                    if horizontalMovement > 0:
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
                    if self.currentMap[initialLocation[0] + verticalMovement / 2] != "":
                        return False

                elif abs(horizontalMovement) == 2:
                    if self.currentMap[initialLocation[1] + horizontalMovement / 2] != "":
                        return False
            else:
                return False

        elif 'elephant' in name:
            if abs(verticalMovement) == 2 and abs(horizontalMovement):
                if self.currentMap[initialLocation[0] + verticalMovement / 2][
                    initialLocation[1] + horizontalMovement / 2] != "":
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
                for i in range(1, abs(verticalMovement)):
                    # Judging direction of moving(left or right)
                    if horizontalMovement > 0:
                        if self.currentMap[initialLocation[0] + i][initialLocation[1]] != "":
                            obstacleCount += 1
                    else:
                        if self.currentMap[initialLocation[0] - i][initialLocation[1]] != "":
                            obstacleCount += 1
            if obstacleCount > 1:
                return False

        elif name == "b_soldier":
            if 3 <= initialLocation[0] <= 4:
                enemySide = False
            if enemySide:
                if not (abs(horizontalMovement) == 1 or verticalMovement == 1):
                    return False
            else:
                if not verticalMovement == 1:
                    return False

        elif name == 'r_soldier':
            if 5 <= initialLocation[0] <= 6:
                enemySide = False
            if enemySide:
                if not (abs(horizontalMovement) == 1 or verticalMovement == -1):
                    return False
            else:
                if not verticalMovement == -1:
                    return False

        elif name == 'king':
            if 3 <= finalLocation[1] <= 5 and (7 <= finalLocation[0] <= 9 or 3 <= finalLocation[1] <= 5):
                if not (abs(horizontalMovement) == 1 or abs(verticalMovement) == 1):
                    return False
            else:
                return False

        else:
            return False


if __name__ == '__main__':
    chess = UltimateChineseChess(True, 'en-us', '00000001')
    chess.startTutorial()
    '''
    About variable Naming:
        b_soldier: Black Soldier
        r_soldier: Red Soldier
    '''
