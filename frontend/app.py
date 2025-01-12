import streamlit as st
import streamlit.components.v1 as components
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import websocket
import threading
import json

# RTC Configuration for RTMP stream
RTC_CONFIGURATION = RTCConfiguration({
    "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
})

# Title and divider
st.title("RTMP Stream in Streamlit")
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

col1, col2, col3 = st.columns([1, 1, 1], gap="small")

with col1: 
    st.markdown("""
        <style>
        .full-width-button {
            width: 100%;
            height: 100px;  /* Adjust height as needed */
            font-size: 24px;  /* Adjust font size as needed */
            background-color: #000000;
            color: white;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .full-width-button:hover {
            background-color: #45a049;
        }
        </style>
        """, unsafe_allow_html=True)
    st.markdown('<button class="full-width-button">SL</button>', unsafe_allow_html=True)
    st.markdown("&nbsp;")  # Spacer
    html_code = """
    <!DOCTYPE html>
    <html>
    <body style="position: fixed; font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif; color:rgb(128, 128, 128); font-size: xx-large;">
        <canvas id="canvas" name="game"></canvas>
        <script>
            var connection = new WebSocket('ws://' + "192.168.4.1" + ':81/', ['arduino']);
            connection.onopen = function () {
                connection.send('Connect ' + new Date());
            };
            connection.onerror = function (error) {
                console.log('WebSocket Error ', error);
                alert('WebSocket Error ', error);
            };
            connection.onmessage = function (e) {
                console.log('Server: ', e.data);
            };

            function send(x, y, speed, angle) {
                var data = {"x": x, "y": y, "speed": speed, "angle": angle};
                data = JSON.stringify(data);
                console.log(data);
                connection.send(data);
            }

            var canvas, ctx;

            window.addEventListener('load', () => {
                canvas = document.getElementById('canvas');
                ctx = canvas.getContext('2d');
                resize();

                document.addEventListener('mousedown', startDrawing);
                document.addEventListener('mouseup', stopDrawing);
                document.addEventListener('mousemove', Draw);

                document.addEventListener('touchstart', startDrawing);
                document.addEventListener('touchend', stopDrawing);
                document.addEventListener('touchcancel', stopDrawing);
                document.addEventListener('touchmove', Draw);
                window.addEventListener('resize', resize);

                document.getElementById("x_coordinate").innerText = 0;
                document.getElementById("y_coordinate").innerText = 0;
                document.getElementById("speed").innerText = 0;
                document.getElementById("angle").innerText = 0;
            });

            var width, height, radius, x_orig, y_orig;
            function resize() {
                width = window.innerWidth;
                radius = 50;  // Adjusted radius to make the joystick smaller
                height = radius * 6.5;
                ctx.canvas.width = width;
                ctx.canvas.height = height;
                background();
                joystick(width / 2, height / 3);
            }

            function background() {
                x_orig = width / 2;
                y_orig = height / 3;

                ctx.beginPath();
                ctx.arc(x_orig, y_orig, radius + 20, 0, Math.PI * 2, true);
                ctx.fillStyle = '#ECE5E5';
                ctx.fill();
            }

            function joystick(width, height) {
                ctx.beginPath();
                ctx.arc(width, height, radius, 0, Math.PI * 2, true);
                ctx.fillStyle = '#F08080';
                ctx.fill();
                ctx.strokeStyle = '#F6ABAB';
                ctx.lineWidth = 8;
                ctx.stroke();
            }

            let coord = { x: 0, y: 0 };
            let paint = false;

            function getPosition(event) {
                var mouse_x = event.clientX || event.touches[0].clientX;
                var mouse_y = event.clientY || event.touches[0].clientY;
                coord.x = mouse_x - canvas.offsetLeft;
                coord.y = mouse_y - canvas.offsetTop;
            }

            function is_it_in_the_circle() {
                var current_radius = Math.sqrt(Math.pow(coord.x - x_orig, 2) + Math.pow(coord.y - y_orig, 2));
                return radius >= current_radius;
            }

            function startDrawing(event) {
                paint = true;
                getPosition(event);
                if (is_it_in_the_circle()) {
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    background();
                    joystick(coord.x, coord.y);
                    Draw();
                }
            }

            function stopDrawing() {
                paint = false;
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                background();
                joystick(width / 2, height / 3);
                document.getElementById("x_coordinate").innerText = 0;
                document.getElementById("y_coordinate").innerText = 0;
                document.getElementById("speed").innerText = 0;
                document.getElementById("angle").innerText = 0;
            }

            function Draw(event) {
                if (paint) {
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    background();
                    var angle_in_degrees, x, y, speed;
                    var angle = Math.atan2((coord.y - y_orig), (coord.x - x_orig));

                    if (Math.sign(angle) == -1) {
                        angle_in_degrees = Math.round(-angle * 180 / Math.PI);
                    } else {
                        angle_in_degrees = Math.round(360 - angle * 180 / Math.PI);
                    }

                    if (is_it_in_the_circle()) {
                        joystick(coord.x, coord.y);
                        x = coord.x;
                        y = coord.y;
                    } else {
                        x = radius * Math.cos(angle) + x_orig;
                        y = radius * Math.sin(angle) + y_orig;
                        joystick(x, y);
                    }

                    getPosition(event);

                    speed = Math.round(100 * Math.sqrt(Math.pow(x - x_orig, 2) + Math.pow(y - y_orig, 2)) / radius);

                    var x_relative = Math.round(x - x_orig);
                    var y_relative = Math.round(y - y_orig);

                    document.getElementById("x_coordinate").innerText = x_relative;
                    document.getElementById("y_coordinate").innerText = y_relative;
                    document.getElementById("speed").innerText = speed;
                    document.getElementById("angle").innerText = angle_in_degrees;

                    send(x_relative, y_relative, speed, angle_in_degrees);
                }
            }
        </script>
    </body>
    </html>
    """

    # Embed the HTML and JavaScript code in Streamlit
    components.html(html_code, height=600)

# Custom CSS for circular button layout with closer left and right buttons
with col2:
    st.markdown("""
        <style>
        .full-width-button {
            width: 100%;
            height: 100px;  /* Adjust height as needed */
            font-size: 24px;  /* Adjust font size as needed */
            background-color: #000000;
            color: white;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .full-width-button:hover {
            background-color: #45a049;
        }
        </style>
        """, unsafe_allow_html=True)
    st.markdown('<button class="full-width-button">SR</button>', unsafe_allow_html=True)
    st.markdown("&nbsp;")  # Spacer
    st.markdown("""
        <style>
        .remote-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 300px;
            position: relative;
        }
        .remote-button {
            position: absolute;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background-color: #000000;
            color: white;
            text-align: center;
            line-height: 60px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .remote-button:hover {
            background-color: #45a049;
        }
        .top-button {
            top: 15%;
            left: 50%;
            transform: translateX(-50%);
        }
        .bottom-button {
            bottom: 15%;
            left: 50%;
            transform: translateX(-50%);
        }
        .left-button {
            top: 50%;
            left: 3%;  /* Adjusted to bring the button closer */
            transform: translateY(-50%);
        }
        .right-button {
            top: 50%;
            right: 3%;  /* Adjusted to bring the button closer */
            transform: translateY(-50%);
        }
        </style>
        """, unsafe_allow_html=True)

    # HTML for the remote buttons
    st.markdown("""
        <div class="remote-container">
            <div class="remote-button top-button">↑</div>
            <div class="remote-button bottom-button">↓</div>
            <div class="remote-button left-button">←</div>
            <div class="remote-button right-button">→</div>
        </div>
        """, unsafe_allow_html=True)
with col3:
    st.markdown("""
        <style>
        .remote-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 300px;
            position: relative;
        }
        .remote-button {
            position: absolute;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background-color: #000000;
            color: white;
            text-align: center;
            line-height: 60px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .remote-button:hover {
            background-color: #45a049;
        }
        .capture-button {
            top: 10%;
            left: 50%;
            transform: translateX(-50%);
        }
        </style>
        """, unsafe_allow_html=True)

    # HTML for the remote buttons
    st.markdown("""
        <div class="remote-container">
            <div class="remote-button capture-button">📸</div>
        </div>
        """, unsafe_allow_html=True)