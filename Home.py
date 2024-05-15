import streamlit as st
import time
import os
import sys
from ultralytics import YOLO
import numpy as np
from PIL import Image
import torch
from datetime import datetime
import supervision as sv

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

import Results 

#configurations
modelPath = "models/model.pt"
model = YOLO('models/model.pt')
st.session_state.classes = model.names

def detect(image):
     img = Image.open(image)
     ts = datetime.timestamp(datetime.now())
     imgpath = os.path.join('data/uploads', str(ts)+image.name)
     outputpath = os.path.join(
          'data/outputs', os.path.basename(imgpath))
     with open(imgpath, mode="wb") as f:
          f.write(image.getbuffer())
          results = model(imgpath)
          
     return results

def main():
    icon = "./RecycleMateLogo.ico"

    st.set_page_config(
        page_title="Home",
        page_icon=icon,
    )

    if 'page' not in st.session_state:
        st.session_state.page = 'home'

    if st.session_state.page == 'home':
        with st.sidebar:
            col1, mid, col2 = st.columns([4, 1, 20])
            with col1:
                st.image(icon, width=60)
            with col2:
                st.title("RecycleMate")

        st.title("Welcome to RecycleMate!")

        st.markdown(
            """
            RecycleMate is a web application designed to assist you in practicing recycling and contributing to environmental sustainability.

            ### Instructions
            1. **Upload or Capture an Image**: Upload an image of the recycling material from your device or capture an image using 
            your device's camera.
            2. **Generate Recommendations**: After uploading or capturing the image, click on the "Generate" button to initiate 
            the analysis process.
            3. **Explore Recycling Projects**: Once the analysis is complete, RecycleMate will display a list of recommended recycling 
            projects based on the identified materials in the image. Explore the list to find initiatives that interest you and 
            contribute to a greener planet!
            """
        )

        tab1, tab2 = st.tabs(["Upload Image", "Capture Image"])

        with tab1:
            upload_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
            if upload_image:
                st.image(upload_image, caption="Uploaded Image", use_column_width=True)
                st.session_state.uploaded_image = upload_image
        with tab2:
            capture_image = st.camera_input("Capture Image")
            if capture_image:
                st.session_state.captured_image = capture_image

        if upload_image or capture_image:
            if st.button("Generate Recommendations"):
                with st.spinner('Generating Recommendations...'):
                    time.sleep(3)
                    
                    if upload_image:
                         img_files = upload_image
                    else:
                         img_files = capture_image
                    
                    st.session_state.detection = detect(img_files)
                    
                    detections = sv.Detections.from_ultralytics(st.session_state.detection[0])
    
                    # Generate dictionary of predictions
                    labels = [
                         f"{st.session_state.classes[class_id]}"
                         for _, _, _, class_id, _, _
                         in detections
                    ]
                    
                                        
                    st.session_state.recommendations = labels
                    st.session_state.page = 'results'
                    st.experimental_rerun()

    elif st.session_state.page == 'results':
        Results.main()

if __name__ == "__main__":
    main()
