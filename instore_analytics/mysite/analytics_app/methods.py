def process_video(video_path, videos):
    import cv2
    from collections import Counter
    from ultralytics import YOLO

    import matplotlib.pyplot as plt

    from .models import Video, ProcessedData
    print(f"Processing video: {video_path}")
    processed_data = ProcessedData.objects.create(video = videos, people_count=[])

    # cap = cv2.VideoCapture('rtsp://admin:Lemon123@172.16.100.199:554/Streaming/Channels/1101')
    # video_path = '/content/20240529165513094_L15428768_Camera 07_7_video.mov'
    # video_path = 'rtsp://admin:Lemon123@172.16.100.199:554/Streaming/Channels/1101'
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
        video_capture.release()
        cv2.destroyAllWindows()
        return processed_data
    people_counts = []
    model = YOLO("yolov8s.pt")
    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("End of video")
            video_capture.release()
            cv2.destroyAllWindows()
            return processed_data
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        frame_count += 1
        
        if counter == time_between_frames:  
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
          processed_data.people_count.append(res)
          print(processed_data.people_count)


          
    video_capture.release()
    cv2.destroyAllWindows()
    

