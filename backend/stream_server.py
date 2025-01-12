import asyncio
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack

async def stream_to_rtp():
    pc = RTCPeerConnection()

    video = VideoStreamTrack()
    
    pc.addTrack(video)

    offer = await pc.createOffer()

    await pc.setLocalDescription(offer)

    for sender in pc.getSenders():
        if sender.track.kind == "video":
            parameters = sender.getParameters()
            await sender.setParameters(parameters)

    print(pc.localDescription.sdp)
    await asyncio.sleep(3600)

asyncio.run(stream_to_rtp())
