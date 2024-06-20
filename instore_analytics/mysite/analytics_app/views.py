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


# @login_required
# def upload_video(request):
#     if request.method == 'POST':
#         form = VideoUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             video = form.save(commit=False)
#             video.user = request.user
#             video.save()

#             # Call main.py with the video path
#             video_path = video.video.path
#             result = subprocess.run(['python', 'main.py', video_path], capture_output=True, text=True)

#             # Output for debugging
#             print("STDOUT:", result.stdout)
#             print("STDERR:", result.stderr)

#             # Redirect after successful upload
#             return redirect('show_graphh')
#     else:
#         form = VideoUploadForm()
#     return render(request, 'upload.html', {'form': form})

@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.save()

            # Call main.py with the video path
            videos = Video.objects.filter(user=request.user).order_by('id').first()
            result = process_video(video.video.path, videos)
            print(result)
            print(result.people_count)
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
    
    # Filter data for the logged-in user
    videos = Video.objects.filter(user=request.user).order_by('-id').first()

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

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'index.html')

# def upload_video(request):
#     if request.method == 'POST':
#         form = VideoUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             video = form.cleaned_data['video']
#             title = form.cleaned_data['title']

#             # Save the file
#             video_path = os.path.join(settings.MEDIA_ROOT, 'videos', video.name)
#             with open(video_path, 'wb+') as destination:
#                 for chunk in video.chunks():
#                     destination.write(chunk)

#             # Call main.py with the video path
#             result = subprocess.run(['python', 'main.py', video_path], capture_output=True, text=True)

#             # Output for debugging
#             print("STDOUT:", result.stdout)
#             print("STDERR:", result.stderr)

#             # Redirect after successful upload
#             return redirect('show_graphh')
#     else:
#         form = VideoUploadForm()
#     return render(request, 'upload.html', {'form': form})

def upload_success(request):
    return render(request, 'upload_success.html')


# def show_graph(request):
#     import matplotlib
#     matplotlib.use('Agg')
#     # Connect to the database
#     conn = sqlite3.connect(os.path.join(settings.BASE_DIR, 'example.db'))
#     cursor = conn.cursor()

#     # Query the data
#     cursor.execute('SELECT people FROM users')
#     rows = cursor.fetchall()
#     values = rows
#     conn.close()
#     mins = [i for i in range(len(rows))]

#     # Create the graph
#     plt.figure()
#     plt.plot(mins, values)
#     plt.title('People per minute')
#     plt.xlabel('Minute')
#     plt.ylabel('People')

#     # Save it to a BytesIO object
#     buffer = io.BytesIO()
#     plt.savefig(buffer, format='png')
#     plt.close()
#     buffer.seek(0)

#     return HttpResponse(buffer, content_type='image/png')

def update_graph_data(request):
    print('updating')
    # Connect to the database
    conn = sqlite3.connect(os.path.join(settings.BASE_DIR, 'example.db'))
    cursor = conn.cursor()

    # Query the latest data
    cursor.execute('SELECT people FROM users')  # Example: Fetching latest 10 entries
    rows = cursor.fetchall()
    values = rows
    conn.close()

    # Return JSON response
    return JsonResponse({'values': values})

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm  # Import the custom form

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after registration
            return redirect('home')  # Redirect to a home page or another page
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
