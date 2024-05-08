import streamlit as st

# Main function to run the Streamlit application
def main():
    st.title("RecycleMate")

    # Upload image
    uploaded_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

    if uploaded_image:
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

        
if __name__ == "__main__":
    main()
