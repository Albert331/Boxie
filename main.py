from ultralytics import YOLO
import cv2
import math

def calc_angle(shoulder, elbow, wrist):
    """
    Calculates the relative angle at the elbow joint using the forearm as the baseline.
    Input parameters are tuples or lists of coordinates: [x, y]
    """
    # 1. Unpack coordinates
    sx, sy = shoulder[0], shoulder[1]
    ex, ey = elbow[0], elbow[1]
    wx, wy = wrist[0], wrist[1]
    
    # 2. Create vectors relative to the elbow as the origin (0,0)
    # Forearm Vector (Elbow -> Wrist)
    fx, fy = wx - ex, wy - ey
    # Upper Arm Vector (Elbow -> Shoulder)
    ux, uy = sx - ex, sy - ey
    
    # 3. Calculate dot product and 2D cross product manually
    dot_product = (fx * ux) + (fy * uy)
    cross_product = (fx * uy) - (fy * ux)
    
    # 4. Use math.atan2 to safely get the angle between them
    angle_radians = math.atan2(cross_product, dot_product)
    angle_degrees = abs(math.degrees(angle_radians))
    
    # 5. Enforce interior angle constraint
    if angle_degrees > 180:
        angle_degrees = 360 - angle_degrees
        
    return int(angle_degrees)

model = YOLO("yolo26s-pose.pt")
cap = cv2.VideoCapture(0)

sl_idx, el_idx, wl_idx = 5, 7, 9
sr_idx, er_idx, wr_idx = 6, 8, 10

ZONE_X, ZONE_Y, ZONE_W, ZONE_H = 10, 100, 400, 400

if not cap.isOpened():
    print("cant open camera")
    exit()

while True:
    ret, frame = cap.read()
    frame =cv2.flip(frame, 1)
    if not ret:
        break

    results = model(frame,verbose=False)[0]
    keypoints = results.keypoints.xy
    for person in keypoints:
        person_np = person.cpu().numpy()
        
        shoulderl = person[sl_idx]
        elbowl = person[el_idx]
        wristl = person[wl_idx]

        shoulderr = person[sr_idx]
        elbowr = person[er_idx]
        wristr = person[wr_idx]

        elbow_anglel = calc_angle(shoulderl, elbowl, wristl)
        elbow_angler = calc_angle(shoulderr, elbowr, wristr)

        
        if 150>elbow_anglel>100:
            x_left,y_left = wristl
            if (ZONE_X <= x_left <= ZONE_X + ZONE_W) and (ZONE_Y <= y_left <= ZONE_Y + ZONE_H):
                print('PUNCHEDDD!!!')

        if 150>elbow_angler>100:
                    x_right,y_right = wristr
                    if (ZONE_X <= x_right <= ZONE_X + ZONE_W) and (ZONE_Y <= y_right <= ZONE_Y + ZONE_H):
                        print('PUNCHEDDD!!!')


        for points in person:
            x, y = points


            
            x=int(x.item())
            y=int(y.item())

            if x > 0 and y > 0:
                # c = f"{float(c):.2f}"
                cv2.circle(frame, (x, y), 6, (0, 0, 255), -1)
                # cv2.putText(frame, c, (x, y - 20),cv2.FONT_HERSHEY_COMPLEX,0.4,(0,255,0),1)
                cv2.putText(
                    frame, 
                    f"{elbow_anglel} Deg", 
                    (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.6, 
                    (255, 0, 0), 
                    2
                )
                cv2.putText(
                    frame, 
                    f"{elbow_angler} Deg", 
                    (200, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.6, 
                    (255, 0, 0), 
                    2
                )
                cv2.rectangle(
                    frame, 
                    (ZONE_X, ZONE_Y), 
                    (ZONE_X + ZONE_W, ZONE_Y + ZONE_H), 
                    color=(0, 255, 0),  # Green color in BGR format
                    thickness=2         # 2 pixels wide border
                )
    cv2.imshow("camera",frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
