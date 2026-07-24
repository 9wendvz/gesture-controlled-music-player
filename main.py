from pynput.keyboard import Key, Controller
import cv2 #handles webcam 
import mediapipe as mp #google's hand tracking library
import time 
import os

# setting up hand detector 
mpHands = mp.solutions.hands #for hands tool
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7) #detecting hands
mpDraw = mp.solutions.drawing_utils #drawing skeletons/dots on screen
keyboard = Controller () #creates a virtual keyboard 

#turning on webcam
cap = cv2.VideoCapture(0)

wasPinching = False
lastVolume = 0

lastActionTime = 0
cooldownSeconds = 1

wasPointingRight = False
wasPointingLeft = False


#while loop for camera
while True:
    success, frame = cap.read()
    if not success:
        break
    frame = cv2.flip(frame, 1) #flips image horizontally 
    rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #converts color format
    results = hands.process(rgbFrame) #returns us the hand tracking data

    #for pausing/playing (pinching)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)
            landmarks = handLms.landmark
            thumbTip = landmarks[4]
            indexTip = landmarks [8]
            distance = ((thumbTip.x - indexTip.x)**2 + (thumbTip.y - indexTip.y)**2)**0.5
            print(distance)
            isPinching = distance < 0.05

       

            if isPinching and not wasPinching:
                keyboard.press(Key.media_play_pause)
                keyboard.release(Key.media_play_pause)

            wasPinching = isPinching



            #volume
            wristY = landmarks[0].y
            minHeight = 0.2
            maxHeight = 0.8

            volume = (maxHeight - wristY) / (maxHeight - minHeight) * 100
            volume = max(0, min(100, volume))

            if abs(volume - lastVolume) > 2:
                os.system(f"osascript -e 'set volume output volume {volume}'")
                lastVolume = volume

            
            indexX = landmarks[8].x
            wristX = landmarks[0].x
            pointDirection = indexX - wristX

            isPointingRight = pointDirection > 0.15
            isPointingLeft = pointDirection < -0.15

            currentTime = time.time()
            timeSinceLastAction = currentTime - lastActionTime

            if isPointingRight and not wasPointingRight and timeSinceLastAction > cooldownSeconds:
                keyboard.press(Key.media_next)
                keyboard.release(Key.media_next)
                lastActionTime = currentTime

            if isPointingLeft and not wasPointingLeft and timeSinceLastAction > cooldownSeconds:
                keyboard.press(Key.media_previous)
                keyboard.release(Key.media_previous)
                lastActionTime = currentTime

            wasPointingRight = isPointingRight
            wasPointingLeft = isPointingLeft


    cv2.imshow("Gesture Control", frame) #shows the window with tracking      
    if cv2.waitKey(1) & 0xFF == ord ('q'): #press q to quit
        break

cap.release() #turns off webcam 
cv2.destroyAllWindows() #closes the window


