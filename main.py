import cv2
import numpy as np
import streamlit as st
from PIL import Image

def update_slider_vals(kl, kh, new_l, new_h):
    st.session_state[kl] = new_l
    st.session_state[kh] = new_h

fnames = st.file_uploader("Upload an RGB image", type=["png", "jpg"],
                        accept_multiple_files=True)
file_num = st.number_input("Image to display", min_value=1, max_value=len(fnames))

if len(fnames) != 0:
    # create and display tabs
    tabnames = ("R", "G", "B", "H", "S", "V")
    tabs = st.tabs(tabnames)
    
    # load channels
    fname = fnames[file_num - 1]
    img = Image.open(fname).convert("RGB") # BGR format
    img = np.array(img).astype(np.uint8)
    r = img[:, :, 0]
    g = img[:, :, 1]
    b = img[:, :, 2]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h = hsv[:, :, 0]
    s = hsv[:, :, 1]
    v = hsv[:, :, 2]
        
    # iterate channels and show with masks
    for i,im in enumerate((r, g, b, h, s, v)):
        with tabs[i]:
            st.header(tabnames[i])
            k_low = "low_" + tabnames[i]
            k_high = "high_" + tabnames[i]
            if k_low in st.session_state:
                low = st.session_state[k_low]
                high = st.session_state[k_high]
            else:
                low, high = 0, 255
                
            k = f"{tabnames[i]}_{i}"
            l, h = st.slider("Select a values for thresholding",
                            0, 255, (low, high), step=5, key=k,
                            on_change=update_slider_vals, kwargs={"kl" : k_low,
                            "kh" : k_high, "new_l" : low, "new_h" : high}
                            )
            c1, c2 = st.columns(2)
            c1.image(im)
            c2.image(cv2.inRange(im, l, h))
