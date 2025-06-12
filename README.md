# Instore Visitor Analytics

## Overview

**Instore Visitor Analytics** is a machine learning-based project designed to detect and count the number of people present in each frame of a video feed from a retail store. The system then generates a time-series plot of visitor counts over the course of a day, helping store managers and analysts gain insights into customer traffic patterns and peak hours for operational efficiency.

---

## Features

- Detects and counts people in each frame using pre-trained deep learning models.
- Aggregates the count over time to build a timeline of visitor traffic.
- Generates a time vs. people-count plot for visual trend analysis.
- Helps businesses optimize staff deployment, layout decisions, and marketing strategies.

---

## Tech Stack

- **Language:** Python
- **Libraries:** OpenCV, NumPy, Matplotlib, pandas
- **ML Models:** YOLOv8 
- **Visualization:** Matplotlib

---

## How It Works

1. **Video Input:** Load a store surveillance video from a static camera.
2. **Frame Processing:** Process the video frame-by-frame using a deep learning model.
3. **Detection & Counting:** Detect people in each frame and count them.
4. **Time Mapping:** Assign timestamps to frames and aggregate people counts.
5. **Plot Generation:** Generate and save a plot of "Number of Visitors vs. Time".
6. **Analysis:** Use the plot to observe peak hours, low-traffic times, etc.

---

## Example Output

A sample output would look like this:

![upload_page](https://drive.google.com/file/d/1A4xBZPdB5xgN7P7yklR_hiQJ1ufMUinH/view?usp=drive_link)
![sample_plot](https://drive.google.com/file/d/1HskSUyOFPqKEJMVpxqt6_BwcpyON6Xi0/view?usp=drive_link)

> The above plot shows how the number of people varies over time, helping in understanding visitor trends.

---

## Installation

1. Clone the repository:
   Use:
   git clone https://github.com/rishabhh-7/visitor_analytics.git
   cd visitor_analytics

3. Install dependencies by running the command pip install -r requirements.txt

4. Run the server using the command python manage.py runserver
