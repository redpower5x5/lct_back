from ultralytics import YOLO
import cv2
from ultralytics.utils.plotting import Annotator  # ultralytics.yolo.utils.plotting is deprecated
import torchvision
import datetime
import base64
from app.config import settings
from app.config import log
from app.core import crud
from app.models.models import VideoAction
from sqlalchemy.orm import Session

colors = {
    0: (255,0,0),
    1: (0,255,0),
    2: (0,0,255),
    3: (255,255,0),
    4: (255,0,255),
    5: (0,255,255),
    6: (125,0,70),
    7: (200,150,200),
    8: (40, 30, 50)
}
labels = {
    0: 'Мобильная точка продажи',
    1: 'Продавец'
}
model = YOLO('app/ai/yolov8s_custom.pt')

def run_on_file(file_path: str, db: Session, video_id: int):
    capture = cv2.VideoCapture(file_path)
    success = True
    count = 0
    while success:
        success, img = capture.read()
        if img is None:
            break
        cut_img = img.copy()
        detection = False
        frame_info = {}
        if count % 100 == 0:
            result = model(img, imgsz=1280)
            bboxes = []
            for res in result:
                for obj in res:
                    conf = obj.boxes.conf.cpu().numpy().astype('float32')[0]
                    cls = obj.boxes.cls.cpu().numpy().astype('int32')[0]
                    x1, y1, x2, y2 = obj.boxes.xyxy.cpu().numpy().astype('float32')[0]
                    if cls == 0 or cls == 1:
                        if conf > 0.75:
                            detection = True
                            detection_info = {
                                'class': cls,
                                'confidence': conf,
                            }
                    bboxes.append(((int(x1), int(y1)), (int(x2), int(y2))))
                    cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), colors[cls], 3)
            if detection:
                name = f'{settings.FRAMES_FOLDER}/DEFAULT_{count}.jpg'
                retval, buffer = cv2.imencode('.jpg', img)
                jpg_as_text = base64.b64encode(buffer)
                # cur date time to str
                time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                comment = ''
                if detection_info['class'] == 0:
                    comment = 'Обнаружена незаконная точка продаж'
                elif detection_info['class'] == 1:
                    comment = 'Обнаружен продавец'
                data = VideoAction(
                    video_id=video_id,
                    time_detected=time,
                    comment=comment,
                    detection=labels[detection_info['class']],
                    precision=detection_info['confidence'],
                    frame=jpg_as_text
                )

                log.debug(f"Detected {detection_info['class']} with precision {detection_info['confidence']}")
                crud.add_video_action(db=db, action=data)
                # cv2.imwrite(name, img)
            # for i, bbox in enumerate(bboxes):
            #     x1 = bbox[0][0]
            #     x2 = bbox[1][0]
            #     y1 = bbox[0][1]
            #     y2 = bbox[1][1]
            #     x1, x2, y1, y2 = round(x1), round(x2), round(y1), round(y2)
            #     image = cut_img[y1:y2, x1:x2]
            #     cv2.imwrite(f'CUT_DEF_{count}_{i}.PNG', image)

        count+=1
    capture.release()
    log.debug(f"File {file_path} processing finished")