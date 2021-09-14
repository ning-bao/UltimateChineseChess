import json


class UltimateChineseChess:
    '''
        Utils for the UltimateChineseChess
        It contains all major processing functions which would be used in the project.
    '''

    def __init__(self, tutorial: bool, language: str) -> None:
        self.__tutorial = tutorial
        self.__language = language

    def startTutorial(self):
        languagePack = json.loads('languagePack/%s_tutorial.json' % self.__language)
        if not self.__tutorial:
            return [languagePack['tutorial']]
        else:
            return [languagePack['welcome'], [languagePack['rule_soldier'], languagePack['rule_cannon'], ]]


if __name__ == '__main__':
    chess = UltimateChineseChess(True, 'en-us')
