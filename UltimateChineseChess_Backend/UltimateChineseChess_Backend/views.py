from django.shortcuts import render, HttpResponse
from django.http import JsonResponse


def index(req):
    if req.method == "GET":
        return render(req, 'index.html')
