from django.shortcuts import render, HttpResponse
from django.http import JsonResponse


def index(req):
    if req.method == "GET":
        return render(req, 'index.html')

def startMatch(req):
    if req.method == 'POST':
        return JsonResponse({
            ""
        })