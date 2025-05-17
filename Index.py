import streamlit as st

st.set_page_config(page_title="Skin Care App", page_icon=":guardsman:", layout="wide")
st.title("Skin Care App")
st.write("Welcome to the Skin Care App!")

imagen = st.file_uploader("Upload an image of your skin", type=["jpg", "jpeg", "png"])
if imagen is not None:
    st.image(imagen, caption="Uploaded Image", use_column_width=True)
    st.write("Image uploaded successfully!")
else:
    st.write("Please upload an image of your skin to get started.")
    
