import streamlit as st

def main():
     
     st.title("Results")
     
     # Input image with bounding box 
     st.image(image="https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png")
     
     # Displays detected images
     st.header("Detected objects:")
     
     with st.container(height=300):
          st.write("Placeholder text")
          st.write("Placeholder text")
          st.write("Placeholder text")
          st.write("Placeholder text")
          st.write("Placeholder text")
          st.write("Placeholder text")
          st.write("Placeholder text")
        
     # Displays recommended projects
     st.header("Recommended Projects:")
     with st.container():
          for i in range(5):
              with st.container(border=True):
                    st.write("This is where the recommended projects are displayed.")

if __name__ == "__main__":
     main()