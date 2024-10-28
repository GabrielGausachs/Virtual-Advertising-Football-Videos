import cv2
import sys
import numpy as np
import os

from Utils.config import (
    INPUT_FOLDER,
    INPUT_NAME_VIDEO,
    OUTPUT_FOLDER,
    OUTPUT_NAME_VIDEO,
)

# from Utils.line_detection import line_detection
from Utils.line_detection_ani import detect_lines


def main(input_video_file: str, output_video_file: str):
    # OpenCV video objects to work with
    cap = cv2.VideoCapture(input_video_file)
    fps = int(round(cap.get(5)))
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_video_file, fourcc, fps, (frame_width, frame_height))

    # Create a resizable window
    cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)

    # while loop where the real work happens
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            if cv2.waitKey(28) & 0xFF == ord("q"):
                break

            frame_b = detect_lines(frame)
            frame = cv2.cvtColor(frame_b, cv2.COLOR_GRAY2BGR)

            lines = cv2.HoughLinesP(frame_b, rho=1, theta=np.pi/180, threshold=50, minLineLength=80, maxLineGap=10)
            print(lines.shape)
            # Draw the detected lines on the original image
            if lines is not None:
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Perform Canny edge detection on the frame
            # blurred, edges = canny_edge_detection(frame)

            # Display the original frame and the edge-detected frame
            # cv2.imshow("Original", frame)
            # cv2.imshow("Blurred", blurred)
            # cv2.imshow("Edges", edges)

            # (optional) display the resulting frame
            cv2.imshow("Frame", frame)

            cv2.resizeWindow("Frame", frame_width, frame_height)

            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord("q"):
                break

        # Break the loop
        else:
            break

    # When everything done, release the video capture and writing object
    cap.release()
    out.release()
    # Closes all the frames
    cv2.destroyAllWindows()


if __name__ == "__main__":
    input_video = INPUT_FOLDER + "/" + INPUT_NAME_VIDEO
    output_video = OUTPUT_FOLDER + "/" + OUTPUT_NAME_VIDEO
    main(input_video, output_video)
