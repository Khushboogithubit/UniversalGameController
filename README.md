# Universal Game Controller using Python and OpenCV

This project is a simple yet powerful implementation of a **game controller using Python, OpenCV, and MediaPipe**. With this controller, you can play games using **hand gestures captured by a webcam**. It’s a fun way to learn about **computer vision, gesture recognition, and game automation**.  

Let’s get started 🚀

---

## Installation

Install the required packages with pip:

```bash
pip install mediapipe
pip install opencv-python
pip install pynput

Deployment
To deploy and run this project, execute:

bash
Copy
Edit
python gesture.py
or for direct keyboard/mouse input:

bash
Copy
Edit
python direct.py
Example Code (Gesture Control)
python
Copy
Edit
import cv2
import mediapipe as mp
from pynput.keyboard import Key, Controller

cap = cv2.VideoCapture(0)
keyboard = Controller()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Example logic: all fingers closed → press LEFT, all open → press RIGHT
        # (Custom mapping can be added in gesture.py)
        # keyboard.press(Key.left) or keyboard.press(Key.right)

    cv2.imshow("Universal Game Controller", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
Output
Run the project and control your favorite games 🎮 using just your hand gestures in front of a webcam.

Demo / Screenshots
Here’s how it looks in action 👇

Gesture Detection

Game Control Example

(Place your actual GIFs or screenshots inside an assets/ folder in the repository and update the file paths.)

Follow Me
GitHub: Khushboogithubit

LinkedIn: your-link-here

Email: your-email@example.com

If you have any confusion, please feel free to contact me. Thank you 💡

License
This script is released under the MIT License.
You are free to use, modify, and distribute it.
If you find any bugs or have suggestions for improvement, please submit an issue or pull request in this repository.

