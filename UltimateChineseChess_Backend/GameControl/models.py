from django.db import models

class HaltingDatabase(models.Model):
    gameID = models.CharField(max_length=25)
    player0 = models.BooleanField(default=False)
    player1 = models.BooleanField(default=False)
    time_created = models.TimeField(auto_now=True)