from django.shortcuts import render
import numpy as np
import pandas as pd
import os
import pickle
from tmdbv3api import TMDb,Movie,TV
import base64
tmbd=TMDb()
tmbd.api_key='2215513a27c6c9c83bc6f993628cf9dc'
names=pd.DataFrame(pickle.load(open('moviedata.pkl','rb')))
distances=pickle.load(open('distsnces.pkl','rb'))
movies=list(names['title'])
tv=TV()
show = tv.popular()
nams=[]
for i in show:
    nams.append(i.name)
# Create your views here.
def recommand(movie):
    movie_idx=names[names['title']==movie].index[0]
    distance=distances[movie_idx]
    indexes=sorted(enumerate(distance),reverse=True,key=lambda x:x[1])[1:6]
    movie_id=[]
    for i in indexes:
        movie_id.append(names.iloc[i[0]].movie_id)
    movie_posters=poster(movie_id)
    return movie_posters
def poster(name):
    mov=Movie()
    posters=[]
    for i in name:
     post=mov.details(i)
     posters.append("https://image.tmdb.org/t/p/w500/"+post.poster_path)
    return posters
def show_poster(show):
    tv1=TV()
    show = tv1.search(show)
    ids=[]
    posters=[]
    for i in show:
     ids.append(i.id)
     shows=tv.similar(ids[0])
     for j in shows:
      posters.append("https://image.tmdb.org/t/p/w500/"+j.poster_path)
    posters=posters[1:6]
    return posters 
def Home(request):
   context={
      'movies':movies,
      'shows':nams,
   }
   return render(request,'index.html',{'context':context})

def movierecommand(request):
   if request.method=="POST":
      name=request.POST['select movie']
      posters=recommand(name)
      print(posters)
      return render(request,'movies.html',{'posters':posters})
   
def showrecommand(request):
   if request.method=="POST":
      name=request.POST['select webseries']
      sh=show_poster(name) 
      return render(request,'show.html',{'show':sh})