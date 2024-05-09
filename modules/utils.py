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

    rgb_colors = ['b', 'g', 'r']
    plt.figure(figsize=[10,5])
    plt.subplot(121); plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)); plt.title("Image")
    for i, col in enumerate(rgb_colors):
        plt.subplot(122); plt.plot(cv2.calcHist([image], [i], None, [256], [0,256]), color=col)
        plt.title("Histogram")
        plt.xlabel('Pixel Intensity')  
        plt.ylabel('Pixel Count')  
        plt.xlim([0,256])
    
    hist_fig = plt.gcf()
    st.pyplot(hist_fig)

    col1, col2 = st.columns([1, 1])
    
    if colors:
        with col1:
            st.write("Detected colors and their percentages:")
            st.markdown("""
            _percentage_ variable represents the percentage of pixels in the image that fall within the specified color range for a particular color.
            """)
            color_data = {"Color": [], "Percentage": []}
            for color, percentage in colors.items():
                color_data["Color"].append(color)
                color_data["Percentage"].append(percentage)
            st.table(color_data)


        with col2:
            st.write("Pie Chart:")
            fig, ax = plt.subplots(figsize=(6, 6))
            wedges, _, autotexts = ax.pie(color_data["Percentage"], labels=color_data["Color"], startangle=140, autopct='%1.1f%%')
            for wedge, color in zip(wedges, colors.keys()):
                wedge.set_facecolor(color)
                wedge.set_edgecolor('black') 
            ax.axis('equal')
            for autotext, wedge_color in zip(autotexts, colors.values()):
                if wedge_color == 'white':
                    autotext.set_color('black')
                else:
                    autotext.set_color('white')
            st.pyplot(fig)

    
    else:
        st.write("No colors detected.")


    st.divider()



    st.markdown("""
        
                ### Histogram Computation
                
                - Histogram computation in opencv allows us to visualize the color intensities in an image with the help of histograms, which gives us a high level intuition on the pixel density in an image.
                - We can compute histograms for grayscale images and RGB images.

                For more details check out my [notebook](https://github.com/adimail/computerVisionNotes/blob/main/opencv-notes.ipynb)
                
    """)

    b, g, r = cv2.split(image)
    plt.figure(figsize=[20,5])

    plt.subplot(141); plt.imshow(r, cmap='gray'); plt.title("Red channel")
    plt.subplot(142); plt.imshow(g, cmap='gray'); plt.title("Green channel")
    plt.subplot(143); plt.imshow(b, cmap='gray'); plt.title("Blue channel")

    
    rgb_channels = plt.gcf()
    st.pyplot(rgb_channels)

    st.markdown("""### Color spaces""")

    all, rgb, bgr, gray, lab, yuv, xyz, hls = st.tabs(["all", "rgb", "bgr", "gray", "lab", "yuv", "xyz", "hls"])

    with all:
        plt.figure(figsize=[15,7])
        plt.subplots_adjust(wspace=0.5, hspace=0.5)

        plt.subplot(3,3,1); plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)); plt.title("RGB")
        plt.subplot(3,3,2); plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), cmap="gray"); plt.title("GRAY")
        plt.subplot(3,3,3); plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2HSV)); plt.title("HSV")
        plt.subplot(3,3,4); plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2LAB)); plt.title("LAB")
        plt.subplot(3,3,5); plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2YUV)); plt.title("YUV")
        plt.subplot(3,3,6); plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2XYZ)); plt.title("XYZ")
        plt.subplot(3,3,8); plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2HLS)); plt.title("HLS")

        color_space = plt.gcf()
        st.pyplot(color_space)

    with rgb:
        st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption='RGB', use_column_width=True, channels="RGB")
    with bgr:
        st.image(cv2.cvtColor(image, cv2.COLOR_RGB2BGR), caption='BGR', use_column_width=True, channels="GRAY")
    with gray:
        st.image(cv2.cvtColor(image, cv2.COLOR_RGB2GRAY), caption='BRAY', use_column_width=True, channels="LAB")
    with lab:
        st.image(cv2.cvtColor(image, cv2.COLOR_RGB2LAB), caption='LAB', use_column_width=True, channels="YCrCb")
    with yuv:
        st.image(cv2.cvtColor(image, cv2.COLOR_BGR2YUV), caption='YUV', use_column_width=True, channels="YUV")
    with xyz:
        st.image(cv2.cvtColor(image, cv2.COLOR_BGR2XYZ), caption='XYZ', use_column_width=True, channels="XYZ")
    with hls:
        st.image(cv2.cvtColor(image, cv2.COLOR_BGR2HLS), caption='HLS', use_column_width=True, channels="HLS")



      

