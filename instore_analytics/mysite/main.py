import cv2
from collections import Counter
from ultralytics import YOLO
import sys
import matplotlib.pyplot as plt
import sqlite3

import datetime
import json
from django.conf import settings
from django.core.wsgi import get_wsgi_application

# Set up Django environment
settings.configure(DEBUG=True, INSTALLED_APPS=['analytics_app'])
application = get_wsgi_application()

from mysite.analytics_app.models import Video, ProcessedData

# # Assume video is an instance of the Video model
# video = Video.objects.first()

# # Example people count data
# people_counts = [10, 15, 20]

# # Save the data to the ProcessedData model
# processed_data = ProcessedData.objects.create(video=video, people_count=people_counts)
# processed_data.save()



def process_video(video_path):
    print(f"Processing video: {video_path}")
    # Add your video processing code here


    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        minutes INTEGER,
        people INTEGER
    )
    ''')
    cursor.execute('DELETE FROM users')
    conn.commit()
    
    # cap = cv2.VideoCapture('rtsp://admin:Lemon123@172.16.100.199:554/Streaming/Channels/1101')
    # video_path = '/content/20240529165513094_L15428768_Camera 07_7_video.mov'
    # video_path = 'rtsp://admin:Lemon123@172.16.100.199:554/Streaming/Channels/1101'
    # video_path = 0
    fps = 12
    print(">>>>>>")
    
    time_interval = 60 # in seconds
    time_between_frames = 10*fps # at what intervals of time in seconds do you want the model to run
    
    # Initialise counters and lists for results
    counter = 0
    frame_count = 0
    resperinterval = []
    res = 0
    minute = 0
    
    video_capture = cv2.VideoCapture(video_path)
    if not video_capture.isOpened():
        print("Error: Could not open video.")
        sys.exit()
    people_counts = []
    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("End of video")
            break
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        frame_count += 1
        
        if counter == time_between_frames:
            model = YOLO("yolov8s.pt")  
            snapshots = [frame]
        
            results = model(snapshots)
        
            class_ids = results[0].boxes.cls.cpu().numpy()
        
            resperinterval.append(Counter(class_ids)[0.0])
            print(frame_count)
            print(resperinterval)
            counter = 0
        
    
        counter += 1
        if frame_count == fps*time_interval:
          minute += 1
          res = sum(resperinterval)//len(resperinterval)
          resperinterval = []
          frame_count = 0
          print(res)
          processed_data = ProcessedData.objects.create(people_count=res)
          processed_data.save()
          
          
    
          cursor.execute('''
          INSERT INTO users (minutes, people)
          VALUES (?, ?)
          ''', (minute, res))
          conn.commit()
          cursor.execute('SELECT * FROM users')
          rows = cursor.fetchall()
          print('Data after insertion:')
    
        #   fig, ax = plt.subplots()
        #   if rows:
        #     id, timestamps, values = zip(*rows)
        #     ax.clear()
        #     ax.plot(timestamps, values, label='Value over Time')
        #     ax.legend(loc='upper left')
        #     plt.xticks(rotation=45, ha='right')
        #     plt.subplots_adjust(bottom=0.30)
        #     plt.title('Real-Time Data Plot')
        #     plt.xlabel('Timestamp')
        #     plt.ylabel('Value')
          for row in rows:
            print(row)


          
    video_capture.release()
    cv2.destroyAllWindows()
    
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('if')
        print("Usage: python main.py <video_path>")
    else:
        print('else')
        video_path = sys.argv[1]
        process_video(video_path)
