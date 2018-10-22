from django.shortcuts import render

def getUserInfo(user):
    if not user.is_authenticated:
        return {}
    