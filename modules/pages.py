import cv2
import numpy as np
import streamlit as st
from modules.utils import process_image
from modules.utils import adjust_threshold

def model_page():
    st.title("Color Detection")

    upload, cam = st.tabs(["Upload Image File", "Camera Input"])

    threshold = adjust_threshold()

    with cam:
        img_file_buffer = st.camera_input("Indradhanu image input", key="camera", label_visibility="hidden")

        if img_file_buffer is not None:
            img_bytes = np.asarray(bytearray(img_file_buffer.read()), dtype=np.uint8)
            image = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)
            process_image(image, threshold)


    with upload:
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            # st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            process_image(image, threshold)

def home_page():

    st.title("Indra Dhanu")
    st.subheader(
        "A python application for colour detection and analysis")
    st.divider()

    with st.container():
        st.header('How to use the site:')
        st.markdown(
            """
            1. ALlow camera access
            1. get the analysis of the image data in the _model_ page
            1. Tou can take images from camera as well as you can upload images directly
            """
        )

    st.divider()

    st.image("assets/indra-dhanu-sequencediagram.png", caption='Indra Dhanu Backend', use_column_width=True)

    st.divider()

    st.markdown("""
    #### Color detection in OpenCV is typically performed using the HSV (Hue, Saturation, Value) color space. Here's a detailed explanation of the process:

    - Color Space Conversion: The first step is to convert the input image from the RGB color space to the HSV color space. This conversion is done because the HSV color space separates color information from brightness information, making it easier to work with for color-based tasks.
    - Define Color Ranges: Once the image is in the HSV color space, you define the ranges of colors you want to detect. This is done by specifying lower and upper bounds for each color in the HSV color space. For example, to detect the color red, you might specify a range of hue values from 0 to 10, a range of saturation values from 70 to 255, and a range of value (brightness) values from 50 to 255.

    ```python
    color_ranges = {
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
    ```
    - Create Masks: After defining the color ranges, you use the cv2.inRange() function to create binary masks for each color. These masks have a value of 1 (white) where the color is present in the image and 0 (black) everywhere else.
    - Apply Masks: Once the masks are created, you apply them to the original HSV image using bitwise operations. This effectively isolates the regions of the image that contain the desired colors.
    - Calculate Color Percentage: After applying the masks, you can calculate the percentage of each color present in the image. This is done by counting the number of non-zero pixels in each mask (i.e., the pixels where the color is present) and dividing by the total number of pixels in the image.
    - Return Detected Colors: Finally, the detected colors and their respective percentages are typically returned, often as a dictionary or another data structure. This allows you to easily determine the presence and relative abundance of different colors in the image.
    """)
        
    st.image("assets/indradhanu.png", caption='Indra Dhanu Backend', use_column_width=True)
    st.divider()
    st.markdown("""
    You can read more about the fundamentals of image processing with openCV, [here](https://github.com/adimail/computerVisionNotes) is [my](https://adimail.github.io) github repo 
    
    9 May 2024
                
    Indradhanu was made as a term work project for EDA and AI course.""")

def program_code():
    st.title("Python program for Indra Dhanu")
    st.divider()

    st.image("assets/indra-dhanu-sequencediagram.png", caption='Indra Dhanu Backend', use_column_width=True)

    st.markdown("""
    ## Color channels
    In computer vision and image processing, an image is typically represented in terms of color channels. These channels are the fundamental building blocks that represent different aspects of color information within an image.

    - RGB (Red, Green, Blue): This is the most common color space, where each pixel in an image is represented as a combination of red, green, and blue intensity values. RGB is additive, meaning colors are created by adding different intensities of red, green, and blue light together.
    - HSV (Hue, Saturation, Value): Unlike RGB, HSV separates color information (hue), saturation, and brightness (value) into three distinct channels. This makes it more intuitive for certain color-based tasks, such as color detection and segmentation.
    """)

    st.markdown("""
    ```python
    def detect_colors(image, threshold):
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        detected_colors = {}

        for color_name, (lower, upper) in default_color_ranges.items():
            mask = cv2.inRange(hsv_image, np.array(lower), np.array(upper))
            percentage = cv2.countNonZero(mask) / (image.size / 3) * 100
            if percentage > threshold:
                detected_colors[color_name] = percentage

        return detected_colors
    ```
    The detect_colors function takes an image and a threshold as input and returns a dictionary containing the detected colors along with their respective percentages in the image. Here's what the output dictionary looks like:
    ```
    {
        "red": 32.68,
        "black": 68.32,
        ...
    }

    ```         
    ---
    
    ### Util Functions
    
    
    ```python
    def adjust_threshold():
        threshold = st.sidebar.slider("Adjust Color Detection threshold", 0.0, 10.0, 2.0, 0.1)
        return threshold
    ```
                
    ```python
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
    ```
    """)
