from django.shortcuts import render
from . import models

# Create your views here.
def halting(req):
    if req.method == "POST":
        gameID = req.POST['gameID']
        player = req.POST['player']

        # Check if there are existing record
        if len(models.HaltingDatabase.objects.filter(gameID=gameID))==0:
            # hd - Halting Database
            if player:
                hd = models.HaltingDatabase(gameID=gameID, player1=True)
            else:
                hd = models.HaltingDatabase(gameID=gameID, player0=True)
            hd.save()
        else:
            hd = models.HaltingDatabase.objects.get(gameID=gameID)
            if player:
                hd['player1'] = True
            else:
                hd['player0'] = True

def checkHalt(gameID):
    game = models.HaltingDatabase.objects.get(gameID=gameID)
    
