# GazeControl: Eye Controlled Virtual Mouse


## Description

  Eye Controlled Virtual Mouse is a computer vision-based project that allows users to control the mouse cursor using eye movements and blinking gestures. 
  It uses real-time webcam input to detect facial landmarks, tracks eye positions to move the cursor smoothly across the screen, and performs mouse clicks based on blink detection. This system demonstrates hands-free human-computer interaction and can be extended for assistive technologies.

## Features

   Cursor movement using eye tracking
   
   Left click using left eye blink
   
   Right click using right eye blink
   
   Smooth cursor movement using interpolation
   
   Real-time face and eye tracking
   
   Lightweight and responsive system
   
## Tech Stack

  Python
  
  OpenCV
  
  MediaPipe
  
  PyAutoGUI
  
  NumPy
  
## Controls

  Move eyes → Move cursor
  
  Blink left eye → Left click
  
  Blink right eye → Right click
  
  Press 'q' → Exit application
  
## Output

  The system opens the webcam and tracks the user’s eye movements in real time. A cursor on the screen moves smoothly based on eye position, and mouse actions like left click and right click are performed using blink gestures.
