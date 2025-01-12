import streamlit as st
import streamlit.components.v1 as components
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import requests

# RTC Configuration for RTMP stream
RTC_CONFIGURATION = RTCConfiguration({
    "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
})

# Title and divider
st.title("RemoteSwitch")
st.divider()

# WebRTC streamer
webrtc_streamer(
    key="example",
    mode=WebRtcMode.RECVONLY,
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={
        "video": True,
        "audio": False
    },
    video_html_attrs={
        "controls": True,
        "autoPlay": True,
        "style": {"width": "100%"}
    }
)
# Initialize character position
if 'position' not in st.session_state:
    st.session_state.position = {'x': 0, 'y': 0}

# Display the character position
st.write(f"Character position: {st.session_state.position}")

# Add a placeholder for the JavaScript code
st.markdown("""
    <script>
    document.addEventListener('keydown', function(event) {
        var key = event.key;
        var position = {x: 0, y: 0};
        if (key === 'w') {
            position.y -= 1;
        } else if (key === 'a') {
            position.x -= 1;
        } else if (key === 's') {
            position.y += 1;
        } else if (key === 'd') {
            position.x += 1;
        }
        // Update the position in Streamlit
        window.parent.postMessage({type: 'update_position', position: position}, '*');
    });
    </script>
""", unsafe_allow_html=True)

# Handle the position update from JavaScript
query_params = st.query_params
if 'update_position' in query_params:
    position = query_params['update_position'][0]
    st.session_state.position['x'] += int(position['x'])
    st.session_state.position['y'] += int(position['y'])
    st.experimental_rerun()