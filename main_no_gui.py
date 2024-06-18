from models.GestureDetectionModel import GestureDetectionModel
import cv2
import queue
import threading

capture_thread = None

def capture_frames(cap):
    try:
        while cap.isOpened():
            
            ret, frame = cap.read()
            if not ret:
                break
            if frame_queue.full():
                frame_queue.get_nowait()
            frame_queue.put(frame)
            
    except Exception as e:
        print(f'Capture thread error: {e}')
        
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print('Capture thread released the camera')

def on_model_loaded():
    global capture_thread
    capture_thread = threading.Thread(target=capture_frames, args=(cap,))
    capture_thread.start()   
    print("\nAll dependencies loaded\n") 

cap = cv2.VideoCapture(0)
print("\nLoading dependencies..\nThis might take a few minutes..\nThank you for your patience :)\n\n")
model = GestureDetectionModel(on_load=on_model_loaded, use_thread = False)

action_types = model.action_types

last_action_index = None
last_prediction = None

frame_queue = queue.Queue(maxsize = 3)

def handle_input(prediction, frame):
    
    global last_action_index, last_prediction
    
    if prediction is None:
            return frame
        
    frame = model.highlight_gesture(frame, prediction)
    action_name, action_index = model.get_action(prediction)

    if last_action_index is None:
        last_action_index = action_index
            
    elif prediction != last_prediction:
        last_prediction = prediction
        
        print(f'Gesture {prediction} --> Action: {action_name}')

    if action_index != last_action_index:
        last_action_index = action_index
        model.reset_kalman_filter()

    elif action_index == action_types['TOGGLE_RELATIVE_MOUSE']:
        return frame
    
    model.execute_action(action_index, frame)
        
    return frame

while True:
    if frame_queue.empty():
        continue
    
    frame = frame_queue.get_nowait()
        
    frame, landmarks = model.process_frame(frame, draw_connections=True)
    
    if landmarks:
        is_left_hand = model.get_hand_orientation() == "Left"
        prediction = model.predict(landmarks, is_left_hand = is_left_hand)   
        frame = handle_input(prediction, frame)
    
    cv2.imshow('Virtual Mouse', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cv2.destroyAllWindows()
cap.release()
capture_thread.join()