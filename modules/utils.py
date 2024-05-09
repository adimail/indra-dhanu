import cv2
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

default_color_ranges = {
    "red": ([0, 100, 100], [10, 255, 255]),
    "orange": ([10, 100, 100], [25, 255, 255]),
    "yellow": ([25, 100, 100], [35, 255, 255]),
    "green": ([35, 50, 50], [80, 255, 255]),
    "blue": ([90, 100, 100], [130, 255, 255]),
    "purple": ([130, 100, 100], [170, 255, 255]),
    "pink": ([170, 100, 100], [180, 255, 255]),
    "brown": ([10, 50, 50], [30, 200, 200]),
    "gray": ([0, 0, 50], [180, 50, 200]),
    "black": ([0, 0, 0], [180, 255, 30]),
    "white": ([0, 0, 200], [180, 20, 255]),
    "cyan": ([80, 100, 100], [100, 255, 255]),
    "magenta": ([170, 100, 100], [180, 255, 255]),
    "lime": ([25, 100, 100], [60, 255, 255]),
    "maroon": ([0, 100, 50], [10, 255, 150]),
    "olive": ([20, 50, 50], [40, 255, 255])
}

def detect_colors(image, threshold):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    detected_colors = {}

    for color_name, (lower, upper) in default_color_ranges.items():
        mask = cv2.inRange(hsv_image, np.array(lower), np.array(upper))
        percentage = cv2.countNonZero(mask) / (image.size / 3) * 100
        if percentage > threshold:
            detected_colors[color_name] = percentage

    return detected_colors

def adjust_threshold():
    threshold = st.sidebar.slider("Adjust Color Detection threshold", 0.0, 10.0, 2.0, 0.1)
    return threshold

def process_image(image, threshold):
    colors = detect_colors(image, threshold)

    if colors:
        col1, col2 = st.columns([1, 1])

        with col1:
            st.write("Detected colors and their percentages:")
            color_data = {"Color": [], "Percentage": []}
            for color, percentage in colors.items():
                color_data["Color"].append(color)
                color_data["Percentage"].append(percentage)
            st.table(color_data)

            st.markdown("""
            _percentage_ variable represents the percentage of pixels in the image that fall within the specified color range for a particular color.
            """)

        with col2:
            st.write("Pie Chart:")
            fig, ax = plt.subplots(figsize=(6, 6))
            wedges, _ = ax.pie(color_data["Percentage"], labels=color_data["Color"], startangle=140)
            for wedge, color in zip(wedges, colors.keys()):
                wedge.set_facecolor(color)
            ax.axis('equal')
            st.pyplot(fig)


    else:
        st.write("No colors detected.")