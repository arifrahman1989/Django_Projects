from django.shortcuts import render
from django.http import HttpResponse
from myApp.models import Musician, Album
from myApp import forms
from django.db.models import Avg

# Create your views here.


def index(recive):
    musician_list = Musician.objects.order_by('first_name')
    diction = {'title': 'This index page', 'musician_list': musician_list,}
    return render(recive, 'myApp/index.html', context=diction)

def album_list(recive, artist_id):
    artist_info = Musician.objects.get(pk=artist_id)
    album_list = Album.objects.filter(artist=artist_id).order_by('name')
    artist_rating = Album.objects.filter(artist=artist_id).aggregate(Avg('num_stars'))
    diction = {'title': 'This album list', 'artist_info': artist_info, 'album_list': album_list, 'artist_rating': artist_rating}
    return render(recive, 'myApp/album_list.html', context=diction)

def musician_form(recive):
    form = forms.MusicianForm()
    if recive.method == 'POST':
        form = forms.MusicianForm(recive.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(recive)

    diction = {'title': 'This Musician Form', 'musician_form': form }
    return render(recive, 'myApp/musician_form.html', context=diction)

def album_form(recive):
    form = forms.AlbumForm()
    if recive.method == 'POST':
        form = forms.AlbumForm(recive.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(recive)
    diction = {'title': 'This Album Form', 'album_form': form}
    return render(recive, 'myApp/album_form.html', context=diction)

def edit_artist(recive, artist_id):
    artist_info = Musician.objects.get(pk=artist_id)
    form = forms.MusicianForm(instance=artist_info)
    if recive.method == 'POST':
        form = forms.MusicianForm(recive.POST, instance=artist_info)
        if form.is_valid():
            form.save(commit=True)
            return album_list(recive, artist_id)

    diction = {'edit_form': form}
    return render(recive, 'myApp/edit_artist.html', context=diction)

def edit_album(recive, album_id):
    album_info = Album.objects.get(pk=1)
    form = forms.AlbumForm(instance=album_info)
    diction = {}
    if recive.method == 'POST':
        form = forms.AlbumForm(recive.POST, instance=album_info)
        if form.is_valid():
            form.save(commit=True)
            diction.update({'success_text': 'Successfully Updated!'})
    diction.update({'edit_form':form})
    diction.update({'album_id':album_id})
    return render(recive, 'myApp/edit_album.html', context=diction)

def delete_album(recive, album_id):
    album = Album.objects.get(pk=album_id).delete()
    diction = {'sucessfull_delete': 'Album Deleted!'}
    return render(recive, 'myApp/delete.html', context=diction)

def delete_musician(recive, artist_id):
    artist_info = Musician.objects.get(pk=artist_id).delete(0)
    diction = {'sucessfull_delete': 'Musician Deleted!'}
    return render(recive, 'myApp/delete.html', context=diction)