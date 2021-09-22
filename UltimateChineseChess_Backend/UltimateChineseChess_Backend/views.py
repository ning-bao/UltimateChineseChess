from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
try:
    from . import utils
except:
    pass


def index(req):
    if req.method == "GET":
        return render(req, 'index.html')
    elif req.method == "POST":
        ChessComponent = utils.UltimateChineseChess(False, "en-us", req.POST["matchID"])
        posibleMovements = []
        for i in range(8):
            for j in range(8):
                if ChessComponent.verifyChess("b_knight", [0,3], [i,j], 1):
                    posibleMovements.append("%s%s"%(i,j))
        print(posibleMovements)
        if req.POST["type"] == 'indicator':
            return JsonResponse({
                "highlight":[11,52,31,56]
            })

def startMatch(req):
    if req.method == 'POST':
        if req.POST["requestingMatchID"]:
            return JsonResponse({
                "matchID":"00000001"
            })
        else:
            for n in req.POST:
                print(n)

def nameConverter(name):
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

if __name__ == "__main__":
    nameConverter('yhfe8w')