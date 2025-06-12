from django.shortcuts import render, redirect
from .forms import VideoUploadForm
import os
import subprocess
from django.conf import settings
import sqlite3
import matplotlib.pyplot as plt
import io
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Video, ProcessedData
from .methods import process_video
from django.contrib.auth import login, authenticate
from .forms import SignUpForm

def home_page(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

from django.contrib.auth.forms import AuthenticationForm

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('upload_video')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.save()

            # videos = Video.objects.filter(user=request.user).order_by('id').first()
            videos = video
            result = process_video(video.video.path, videos)
            request.session['people_count'] = result.people_count
            return redirect('show_graphh')
    else:
        form = VideoUploadForm()
    return render(request, 'upload.html', {'form': form})

@login_required
def show_graph(request):
    import matplotlib
    matplotlib.use('Agg')
    people_count = request.session.get('people_count', None)

    values = people_count
    mins = [i+1 for i in range(len(values))]

    # Create the graph
    plt.figure()
    plt.plot(mins, values)
    plt.title('People per minute')
    plt.xlabel('Minute')
    plt.ylabel('People')

    # Save it to a BytesIO object
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)

    return HttpResponse(buffer, content_type='image/png')


