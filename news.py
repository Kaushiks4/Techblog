import json
import requests
import socket
from flask import Flask
from flask import request
from flask import render_template
from flask import url_for
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
from flask import flash
from flask import session
import sys

api_key='39418bd897a04e5faa5fff7286ffaeb7'

raw_url='https://newsapi.org/v2/everything?q={0}&sortBy=recent&apiKey={1}'
urlg=[]
titleg=[]
urla=[]
titlea=[]
urlt=[]
titlet=[]

def Google():
    google_url=raw_url.format('Google',api_key)
    google_resp=requests.get(google_url)
    google_res=google_resp.json()
    if google_res['status']=='ok':
        for i in range(4):
                l=google_res['articles'][i]['url']
                urlg.append(l)
                ll=google_res['articles'][i]['title']
                titleg.append(ll)
    else:
        print("record not found")

    return urlg,titleg

def Apple():
    apple_url=raw_url.format('Apple',api_key)
    apple_resp=requests.get(apple_url)
    apple_res=apple_resp.json()
    if apple_res['status']=='ok':
        for i in range(4):
                l=apple_res['articles'][i]['url']
                urla.append(l)
                ll=apple_res['articles'][i]['title']
                titlea.append(ll)
    else:
        print("record not found")

    return urla,titlea

def Tesla():
    tesla_url=raw_url.format('Tesla',api_key)
    tesla_resp=requests.get(tesla_url)
    tesla_res=tesla_resp.json()
    if tesla_res['status']=='ok':
        for i in range(4):
                l=tesla_res['articles'][i]['url']
                urlt.append(l)
                ll=tesla_res['articles'][i]['title']
                titlet.append(ll)
    else:
        print("record not found")

    return urlt,titlet

