import streamlit as st

# Main function to run the Streamlit application
def main():
    st.title("Welcome to RecycleMate!")

    st.markdown(
        """
        RecycleMate is a web application designed to assist you in practicing recycling and contributing to environmental sustainability.

        ### Instructions
        1. **Upload or Take a Picture**: Use the provided option to upload an image of recycling materials from your device, 
        or click on the camera icon to capture an image using your device's camera.
        2.  **Generate Recommendations**: After uploading or capturing the image, click on the "Generate" button to initiate 
        the analysis process.
        3. **Explore Recycling Projects**: Once the analysis is complete, RecycleMate will display a list of recommended recycling 
        projects based on the identified materials in the image. Explore the list to find initiatives that interest you and 
        contribute to a greener planet!
    """
    )

    # Upload image
    uploaded_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

    if uploaded_image:
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

        
if __name__ == "__main__":
    main()
