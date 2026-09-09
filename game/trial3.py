
import cv2
import asyncio
import threading
import queue
import json
from websockets.asyncio.client import connect
from game.hands import Hands
from game.punch import Punch
from game.stamina import Stamina
from game.health import Health
from models.onnx_model import run_inference,run_inference_timed

outgoing = queue.Queue()
incoming = queue.Queue()

def cv_loop():
    left_hand = Hands(5, 7, 9)
    right_hand = Hands(6, 8, 10)
    was_blocking = False 

    ZONE_X, ZONE_Y, ZONE_W, ZONE_H = 100, 50, 400, 400
    punch = Punch(ZONE_X, ZONE_Y, ZONE_W, ZONE_H)

    
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
        if not ret:
            break
        frame = cv2.flip(frame, 1)

        people = run_inference_timed(frame)
        
        for person in people:
            person = person[:, :2]

            elbow_anglel = left_hand.calc(person)
            elbow_angler = right_hand.calc(person)

            punched = punch.see_punch(elbow_anglel, elbow_angler, person[9], person[10])

            if punched :
                stamina.punch()
                outgoing.put({"type": "punch"})


            stamina.block(person)
            is_blocking = stamina.is_blocking
            if is_blocking != was_blocking:
                outgoing.put({"type": "block_start" if is_blocking else "block_end"})
            was_blocking = is_blocking

            while not incoming.empty():
                opp_event = incoming.get()
                print(f"Opponent did: {opp_event}")
                if opp_event['type'] == 'punch' and not stamina.is_blocking:
                    health.take_damage()
            
            print(f"\rhealth {health.health:<3} stamina {stamina.stamina:<3} stance {'blocking' if stamina.is_blocking else 'normal'}", end="", flush=True)
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

SERVER_IP = "localhost" 
inp = input('enter the game url or press enter if none')
if inp:
    SERVER_IP = inp
   
async def send_loop(ws):
    while True:
        if not outgoing.empty():
            event = outgoing.get()
            await ws.send(json.dumps(event))
        await asyncio.sleep(0.01)

async def receive_loop(ws):
    async for message in ws:
        incoming.put(json.loads(message))        

async def network_main():
    async with connect(SERVER_IP) as ws:
        await asyncio.gather(send_loop(ws), receive_loop(ws))
        

if __name__ == "__main__":
    threading.Thread(target=cv_loop, daemon=True).start()
    asyncio.run(network_main())        