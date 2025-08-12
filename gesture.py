import cv2
import mediapipe as mp
import time
import keyboard  # For detecting manual keypress
from direct import PressKey, ReleaseKey, W, A, S, D

mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands

tipIds = [4, 8, 12, 16, 20]
current_key_pressed = set()

video = cv2.VideoCapture(0)
time.sleep(2.0)

with mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while True:
        ret, image = video.read()
        if not ret:
            break

        # image = cv2.flip(image, 1)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

        lmList = []
        hand_detected = False
        key_pressed = None
        action_text = ""
        direction = "CENTER"

        if results.multi_hand_landmarks:
            hand_detected = True
            for hand_landmark in results.multi_hand_landmarks:
                for id, lm in enumerate(hand_landmark.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                mp_draw.draw_landmarks(image, hand_landmark, mp_hand.HAND_CONNECTIONS)

        if hand_detected and len(lmList) != 0:
            fingers = []
            fingers.append(1 if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1] else 0)
            for id in range(1, 5):
                fingers.append(1 if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2] else 0)

            totalFingers = fingers.count(1)

            x_positions = [lm[1] for lm in lmList]
            cx = sum(x_positions) // len(x_positions)

            if cx <200:
                direction = "LEFT"
                key_pressed = A
            elif cx >400:
                direction = "RIGHT"
                key_pressed = D
            else:
                direction = "CENTER"

            if totalFingers == 5:
                action_text = "ACCELERATE"
                key_pressed = W
            elif totalFingers == 0:
                action_text = "BRAKE"
                key_pressed = S

        else:
            # Manual fallback using keyboard keys (WASD)
            if keyboard.is_pressed('w'):
                action_text = "ACCELERATE (Manual)"
                key_pressed = W
            elif keyboard.is_pressed('s'):
                action_text = "BRAKE (Manual)"
                key_pressed = S
            elif keyboard.is_pressed('a'):
                direction = "LEFT (Manual)"
                key_pressed = A
            elif keyboard.is_pressed('d'):
                direction = "RIGHT (Manual)"
                key_pressed = D
            else:
                key_pressed = None

        # UI Display
        cv2.rectangle(image, (0, 0), (640, 60), (0, 0, 0), -1)
        cv2.putText(image, f"Gesture: {action_text}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 3)
        cv2.putText(image, f"Move: {direction}", (350, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 255, 0), 3)

        # Handle key press/release
        if key_pressed:
            if key_pressed not in current_key_pressed:
                for key in current_key_pressed:
                    ReleaseKey(key)
                PressKey(key_pressed)
                current_key_pressed = {key_pressed}
        else:
            for key in current_key_pressed:
                ReleaseKey(key)
            current_key_pressed = set()

        cv2.imshow("Game Control (Gesture or Keyboard)", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

video.release()
cv2.destroyAllWindows()
for key in current_key_pressed:
    ReleaseKey(key)