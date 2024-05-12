import streamlit as st
import time

# Main function to run the Streamlit application
def main():
    st.set_page_config(
        page_title="Home",
        page_icon=":recycle:",
    )

    with st.sidebar:
        st.title("RecycleMate :recycle:")

    st.title("Welcome to RecycleMate! :recycle:")

    st.markdown(
        """
        RecycleMate is a web application designed to assist you in practicing recycling and contributing to environmental sustainability.

        ### Instructions
        1. **Upload or Capture an Image**: Upload an image of the recycling material from your device or capture an image using 
        your device's camera.
        2.  **Generate Recommendations**: After uploading or capturing the image, click on the "Generate" button to initiate 
        the analysis process.
        3. **Explore Recycling Projects**: Once the analysis is complete, RecycleMate will display a list of recommended recycling 
        projects based on the identified materials in the image. Explore the list to find initiatives that interest you and 
        contribute to a greener planet!
    """
    )

    # Create tabs for uploading image and capturing image
    tab1, tab2, = st.tabs(["Upload Image", "Capture Image"])

    with tab1:
        # Upload image option
        upload_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
        if upload_image:
            st.image(upload_image, caption="Uploaded Image", use_column_width=True)
    with tab2:
        # Capture image option
        capture_image = st.camera_input("Capture Image")
        if capture_image:
            st.image(capture_image)

    # Generate recommendations button
    if upload_image or capture_image:
        st.write("The item in the image is a: *insert item*")
        if st.button("Generate Recommendations"):
            with st.spinner('Generating Recommendations...'):
                time.sleep(3)
                st.text("*insert recommendations*")
    

        
if __name__ == "__main__":
    main()
