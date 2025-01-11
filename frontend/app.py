import streamlit as st

# App title
st.title("Nintendo Switch Joy-Con Layout (Single)")

# Main columns for Joy-Con layout
sl_sr_col, buttons_col = st.columns([1, 4], gap="small")

# SL and SR buttons
with sl_sr_col:
    st.button("SL", key="sl_button", use_container_width=True)
    st.button("SR", key="sr_button", use_container_width=True)

# Main Buttons (ABXY or D-pad)
with buttons_col:
    col1, col2, col3 = st.columns([1, 1, 1], gap="small")
    with col1:
        st.markdown("&nbsp;")  # Spacer
        st.button("⬅️", key="left_button", use_container_width=True)
    with col2:
        st.button("⬆️", key="up_button", use_container_width=True)   
        st.button("⬇️", key="down_button", use_container_width=True)
    with col3:
        st.markdown("&nbsp;")  # Spacer
        st.button("➡️", key="right_button", use_container_width=True)

# Optional Footer
#st.markdown("<p style='text-align:center;'>Nintendo Switch Single Joy-Con Layout</p>", unsafe_allow_html=True)
