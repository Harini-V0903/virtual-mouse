import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize MediaPipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Start webcam
cap = cv2.VideoCapture(0)

# Screen size
screen_w, screen_h = pyautogui.size()

# Eye landmarks
LEFT_EYE = [33, 133, 160, 159, 158, 157, 173, 144, 145, 153]
RIGHT_EYE = [362, 263, 387, 386, 385, 384, 398, 373, 374, 380]

# Blink detection landmarks
LEFT_BLINK = [159, 145]
RIGHT_BLINK = [386, 374]

# Smoothing
prev_x, prev_y = 0, 0
smooth_factor = 5

# Click timing
last_click_time = 0

while True:
    success, frame = cap.read()
    if not success:
        break

    # Flip for natural control
    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb_frame)

    h, w, _ = frame.shape

    if result.multi_face_landmarks:
        for face_landmarks in result.multi_face_landmarks:

            # -------- LEFT EYE --------
            left_points = []
            for idx in LEFT_EYE:
                lm = face_landmarks.landmark[idx]
                x, y = int(lm.x * w), int(lm.y * h)
                left_points.append((x, y))
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            left_center_x = int(sum(p[0] for p in left_points) / len(left_points))
            left_center_y = int(sum(p[1] for p in left_points) / len(left_points))

            cv2.circle(frame, (left_center_x, left_center_y), 5, (0, 0, 255), -1)

            # -------- RIGHT EYE --------
            right_points = []
            for idx in RIGHT_EYE:
                lm = face_landmarks.landmark[idx]
                x, y = int(lm.x * w), int(lm.y * h)
                right_points.append((x, y))
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            right_center_x = int(sum(p[0] for p in right_points) / len(right_points))
            right_center_y = int(sum(p[1] for p in right_points) / len(right_points))

            cv2.circle(frame, (right_center_x, right_center_y), 5, (0, 0, 255), -1)

            # -------- FINAL CENTER --------
            center_x = int((left_center_x + right_center_x) / 2)
            center_y = int((left_center_y + right_center_y) / 2)

            cv2.circle(frame, (center_x, center_y), 6, (0, 255, 255), -1)

            # -------- SMOOTH CURSOR --------
            screen_x = screen_w * center_x / w
            screen_y = screen_h * center_y / h

            curr_x = prev_x + (screen_x - prev_x) / smooth_factor
            curr_y = prev_y + (screen_y - prev_y) / smooth_factor

            pyautogui.moveTo(curr_x, curr_y)

            prev_x, prev_y = curr_x, curr_y

            # -------- BLINK DETECTION --------
            upper_left = face_landmarks.landmark[LEFT_BLINK[0]]
            lower_left = face_landmarks.landmark[LEFT_BLINK[1]]
            left_dist = abs(int(upper_left.y * h) - int(lower_left.y * h))

            upper_right = face_landmarks.landmark[RIGHT_BLINK[0]]
            lower_right = face_landmarks.landmark[RIGHT_BLINK[1]]
            right_dist = abs(int(upper_right.y * h) - int(lower_right.y * h))

            # Draw blink points
            cv2.circle(frame, (int(upper_left.x * w), int(upper_left.y * h)), 3, (0, 0, 255), -1)
            cv2.circle(frame, (int(lower_left.x * w), int(lower_left.y * h)), 3, (0, 0, 255), -1)

            cv2.circle(frame, (int(upper_right.x * w), int(upper_right.y * h)), 3, (255, 0, 0), -1)
            cv2.circle(frame, (int(lower_right.x * w), int(lower_right.y * h)), 3, (255, 0, 0), -1)

            # -------- CLICK LOGIC --------
            current_time = time.time()

            # LEFT CLICK
            if left_dist < 4:
                if current_time - last_click_time > 1:
                    pyautogui.click()
                    last_click_time = current_time
                    print("LEFT CLICK")

            # RIGHT CLICK
            elif right_dist < 4:
                if current_time - last_click_time > 1:
                    pyautogui.rightClick()
                    last_click_time = current_time
                    print("RIGHT CLICK")

    cv2.imshow("Eye Controlled Mouse", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()