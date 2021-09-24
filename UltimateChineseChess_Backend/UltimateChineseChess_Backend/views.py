from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .utils import UltimateChineseChess
import uuid
import shutil
import json


def index(req):
    if req.method == "GET":
        return render(req, 'index.html')
    elif req.method == "POST":
        posibleMovements = []
        player = int(req.POST["player"])
        chessID = nameConverter(req.POST["chessID"])
        currentLocation = list(map(int,req.POST["chessLocation"]))
        gameID = req.POST["matchID"]
        for i in range(10):
            for j in range(9):
                if verifyChessLocation(chessID, currentLocation, [i,j], player, gameID):
                    posibleMovements.append("%s%s"%(i,j))
        if req.POST["type"] == 'indicator':
            return JsonResponse({
                "highlight":posibleMovements
            })

def startMatch(req):
    print(req.POST["requestingMatchID"])

    if req.method == 'POST':
        if req.POST["requestingMatchID"] == 'true':
            matchID = str(uuid.uuid1())
            shutil.copy("SavedGamePlay/00000001.json", "SavedGamePlay/%s.json"%matchID)
            return JsonResponse({
                "matchID": matchID
            })
        else:
            matchID = req.POST["matchID"]
            f = open("SavedGamePlay/%s.json"%matchID)
            matchMap = json.load(f)["currentMap"]
            for n in range(len(matchMap)):
                for m in range(len(matchMap[n])):
                    matchMap[n][m] = nameConverter(matchMap[n][m])
            f.close()
            return JsonResponse({
                "matchID": matchID,
                "map":matchMap
            })


def nameConverter(name):
    if name == "":
        return ""
    fine = ''
    if "black" in name:
        fine = "b_"+name.split("-")[0]
    elif "red" in name:
        fine = "r_"+name.split("-")[0]
    elif "b_" in name:
        fine = name.split("_")[1]+"-black"
    elif "r_" in name:
        fine = name.split("_")[1]+"-red"
    else:
        raise SyntaxError("You should pass in a chess name here")
    return(fine)

def verifyChessLocation(name, initialLocation: list, finalLocation: list, player: int, gameID):
    cc = UltimateChineseChess(False,"en-us",gameID)
    return cc.verifyChess(name,initialLocation,finalLocation,player)
if __name__ == "__main__":
    verifyChessLocation("r_car",[9,0],[8,0],0, "00000001")