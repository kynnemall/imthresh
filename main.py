import cv2
import numpy as np
import streamlit as st
from PIL import Image
from streamlit_toggle import st_toggle_switch

def update_slider_vals(kl, kh, new_l, new_h):
    st.session_state[kl] = new_l
    st.session_state[kh] = new_h

fnames = st.file_uploader("Upload an RGB image", type=["png", "jpg"],
                        accept_multiple_files=True)
min_val = 1 if fnames else 0
file_num = st.number_input("Image to display", min_value=min_val, max_value=len(fnames))
grid = st_toggle_switch(
    label="Grid layout?",
    default_value=False,
)
tabnames = ("R", "G", "B", "H", "S", "V")

if len(fnames) != 0:
    # load channels
    fname = fnames[file_num - 1]
    img = Image.open(fname).convert("RGB") # BGR format
    w_, h_ = img.size

    cola, colb, colc = st.columns(3)
    resize = cola.checkbox('Resize?')
    width = colb.number_input('New width in px', min_value=250, max_value=w_)
    height = colc.number_input('New height in px', min_value=250, max_value=h_)

    if resize:
        img = img.resize((width, height))

    img = np.array(img).astype(np.uint8)

    r = img[:, :, 0]
    g = img[:, :, 1]
    b = img[:, :, 2]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h = hsv[:, :, 0]
    s = hsv[:, :, 1]
    v = hsv[:, :, 2]

    # iterate channels and show with masks
    if grid:
        with st.container():
            c1, c2, c3 = st.columns(3)
            for i,im in enumerate((r, g, b, h, s, v)):
                index = i - 3 if i >= 3 else i
                col = (c1, c2, c3)[index]
                col.header(tabnames[i])
                k_low = "low_" + tabnames[i]
                k_high = "high_" + tabnames[i]
                if k_low in st.session_state:
                    low = st.session_state[k_low]
                    high = st.session_state[k_high]
                else:
                    low, high = 0, 255
                    
                k = f"{tabnames[i]}_{i}"
                l, h = col.slider("Select a values for thresholding",
                                0, 255, (low, high), step=5, key=k,
                                on_change=update_slider_vals, kwargs={"kl" : k_low,
                                "kh" : k_high, "new_l" : low, "new_h" : high}
                                )
                col.image(cv2.inRange(im, l, h))
            
    else:
        # create and display tabs
        with st.container():
            tabs = st.tabs(tabnames)
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
