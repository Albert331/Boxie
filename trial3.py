
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
from ui import render

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

    

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)

        people = run_inference(frame)
        
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
            

            xl, yl = person[9]
            xr, yr = person[10]
            xl *= 1280 / 640
            yl *= 720 / 480
            xr *= 1280 / 640
            yr *= 720 / 480

            xl,xr = int(xl),int(xr)
            yl,yr = int(yl),int(yr)

            if xl > 0 and yl > 0 and xr >0 and yr >0:
                render(xl,yl,elbow_anglel,xr,yr,elbow_angler)
                    
                    

        punch.reset(elbow_anglel, elbow_angler, person[9], person[10])
        stamina.regen()

        


    cap.release()
    cv2.destroyAllWindows()

# SERVER_IP = "localhost" 
# inp = input('enter the game url or press enter if none')
# if inp:
#     SERVER_IP = inp
   
# async def send_loop(ws):
#     while True:
#         if not outgoing.empty():
#             event = outgoing.get()
#             await ws.send(json.dumps(event))
#         await asyncio.sleep(0.01)

# async def receive_loop(ws):
#     async for message in ws:
#         incoming.put(json.loads(message))        

# async def network_main():
#     async with connect(SERVER_IP) as ws:
#         await asyncio.gather(send_loop(ws), receive_loop(ws))
        

if __name__ == "__main__":
    threading.Thread(target=cv_loop, daemon=True).start()
    # asyncio.run(network_main())   
    while True:
        pass     