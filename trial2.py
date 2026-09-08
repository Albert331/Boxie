from ultralytics import YOLO
import cv2
from hands import Hands
from punch import Punch
from stamina import Stamina
from health import Health

left_hand = Hands(5, 7, 9)
right_hand = Hands(6, 8, 10)

ZONE_X, ZONE_Y, ZONE_W, ZONE_H = 100, 50, 400, 400
punch = Punch(ZONE_X, ZONE_Y, ZONE_W, ZONE_H)

model = YOLO("yolo26s-pose.pt")
cap = cv2.VideoCapture(0)

stamina = Stamina()
health = Health()


if not cap.isOpened():
    print("cant open camera")
    exit()

cv2.namedWindow("camera", cv2.WINDOW_NORMAL)
cv2.resizeWindow("camera", 1280, 720)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    if not ret:
        break

    results = model(frame, verbose=False)[0]
    keypoints = results.keypoints.xy
    for person in keypoints:
        person = person.cpu().numpy()

        elbow_anglel = left_hand.calc(person)
        elbow_angler = right_hand.calc(person)

        punched = punch.see_punch(elbow_anglel, elbow_angler, person[9], person[10])

        if punched :
            punched = stamina.punch()

        stamina.block(person)
        print(stamina.stamina)

        
        

        for points in person:

            x, y = points

            x = int(x)
            y = int(y)

            if x > 0 and y > 0:
                
                cv2.circle(frame, (x, y), 6, (0, 0, 255), -1)
                
                cv2.putText(
                    frame,
                    f"{elbow_anglel} Deg",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 0, 0),
                    2,
                )
                cv2.putText(
                    frame,
                    f"{elbow_angler} Deg",
                    (200, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 0, 0),
                    2,
                )
                cv2.rectangle(
                    frame,
                    (ZONE_X, ZONE_Y),
                    (ZONE_X + ZONE_W, ZONE_Y + ZONE_H),
                    color=(0, 255, 0), 
                    thickness=2,  
                )

        punch.reset(elbow_anglel, elbow_angler, person[9], person[10])
        stamina.regen()

    cv2.imshow("camera", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
