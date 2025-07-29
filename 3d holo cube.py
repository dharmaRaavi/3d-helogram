import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Define the cube vertices and edges
vertices = [
    [1, 1, -1], [1, -1, -1], [-1, -1, -1], [-1, 1, -1],
    [1, 1, 1], [1, -1, 1], [-1, -1, 1], [-1, 1, 1]
]

edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]


def draw_hologram_cube(color):
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glColor3fv(color)  # Set cube color
            glVertex3fv(vertices[vertex])
    glEnd()


def detect_hand_rotation(image):
    # Flip the image horizontally for a later selfie-view display
    image = cv2.flip(image, 1)
    # Convert the BGR image to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Process the image and detect hands
    results = hands.process(image_rgb)

    rotation_x, rotation_y, rotation_z = 0, 0, 0
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks on the image
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the landmarks for wrist, thumb, and index finger
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            # Calculate rotation angles based on hand position
            rotation_x = (wrist.y - 0.5) * 180  # Tilt hand up/down for X rotation
            rotation_y = (wrist.x - 0.5) * 180  # Tilt hand left/right for Y rotation
            rotation_z = ((thumb_tip.x - index_tip.x) ** 2 + (
                        thumb_tip.y - index_tip.y) ** 2) ** 0.5 * 100  # Pinch for Z rotation

    return rotation_x, rotation_y, rotation_z, image


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Initialize webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    clock = pygame.time.Clock()

    rotation_x, rotation_y, rotation_z = 0, 0, 0
    color = (0.0, 1.0, 1.0)  # Initial color (Neon blue)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Capture frame from webcam
        ret, frame = cap.read()
        if not ret:
            break

        # Detect hand rotation
        rot_x, rot_y, rot_z, frame = detect_hand_rotation(frame)

        # Smoothly update rotation angles
        rotation_x = 0.9 * rotation_x + 0.1 * rot_x
        rotation_y = 0.9 * rotation_y + 0.1 * rot_y
        rotation_z = 0.9 * rotation_z + 0.1 * rot_z

        # Clear the screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Apply transformations
        glPushMatrix()
        glRotatef(rotation_x, 1, 0, 0)  # Rotate around X-axis
        glRotatef(rotation_y, 0, 1, 0)  # Rotate around Y-axis
        glRotatef(rotation_z, 0, 0, 1)  # Rotate around Z-axis
        draw_hologram_cube(color)  # Draw the cube with the current color
        glPopMatrix()

        # Display the webcam feed with gestures
        cv2.imshow('Hand Rotation Control', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False

        pygame.display.flip()
        clock.tick(60)

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()


if __name__ == "__main__":
    main()