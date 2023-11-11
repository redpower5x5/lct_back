from ultralytics import YOLO

model = YOLO("best.pt")

#process vide_file and return the result
def process_video(video_file):
    result = model(video_file, size=1280)
    return result