import json
import uuid

class UltimateChineseChess:
    '''
        Utils for the UltimateChineseChess
        It contains all major processing functions which would be used in the project.
    '''

    def __init__(self, skipping: bool, language: str) -> None:
        '''
            skipping: a boolean to choose to load tutorial or not
        '''
        self.__skipping = skipping
        self.__language = language
        self.currentMap = [[],[],[],[],[],[],[],[],[],[]]
        self.initialMap = [
            ["b_car","b_horse","b_elephant","b_knight","b_king","b_knight","b_elephant","b_horse","b_car"],
            ["","","","","","","","",""],
            ["","b_cannon","","","","","","b_cannon",""],
            ["b_soldier","","b_soldier","","b_soldier","","b_soldier","","b_soldier",],
            [],
            [],
            ["r_soldier","","r_soldier","","r_soldier","","r_soldier","","r_soldier",],
            ["","r_cannon","","","","","","r_cannon",""],
            ["","","","","","","","",""],
            ["r_car","r_horse","r_elephant","r_knight","r_king","r_knight","r_elephant","r_horse","r_car"],
        ]

    def startTutorial(self):
        # Loading language pack from .json
        f = open('languagePack/%s_tutorial.json' % self.__skipping, encoding='utf-8')
        languagePack = json.load(f)
        
        if not self.__tutorial:
            return [languagePack['skipping']]
        else:
            return [languagePack['welcome'], [languagePack['rule_soldier'], languagePack['rule_cannon'],languagePack['rule_car'],languagePack['rule_horse'],languagePack['rule_elephant'],languagePack['rule_knights'], languagePack['rule_king']]]

    def loadChessPlay(self, id):
        # Load user saved chess play
        f = open('SavedGamePlay/%s.json'%id)
        chessPlay = json.load(f)

    

if __name__ == '__main__':
    chess = UltimateChineseChess(True, 'en-us')
    chess.startTutorial()
    