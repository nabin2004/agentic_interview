# notes on implementation
1. Authenticate with OAuth
2. Create a WebRTC PeerConnection
3. Create SDP offer
4. Send offer to Meet Media API
5. Recieve SDP answer
6. ICE negotiation
7. Open:
    a. Audio transceivers
    b. Data Channels (participants, metadata)
8. Receive RTP audio packets
9. Decode -> PCM
10. Pipe to ASR / Storage