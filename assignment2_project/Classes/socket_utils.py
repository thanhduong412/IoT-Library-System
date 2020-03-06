#!/usr/bin/env python3
"""Creates SocketUtils class"""
# Documentation: https://docs.python.org/3/library/struct.html
# Provided by Matthew Bolger
import json
import struct

class SocketUtils:
    """This class handles the utilities of socket connection with json"""
    @staticmethod
    def send_json(socket, object_to_send):
        """Sends JSON data via socket"""
        json_string = json.dumps(object_to_send)
        data = json_string.encode("utf-8")
        json_length = struct.pack("!i", len(data))
        socket.sendall(json_length)
        socket.sendall(data)

    @staticmethod
    def recv_json(socket):
        """Receives JSON data via socket"""
        buffer = socket.recv(4)
        json_length = struct.unpack("!i", buffer)[0]

        # Reference: https://stackoverflow.com/a/15964489/9798310
        buffer = bytearray(json_length)
        view = memoryview(buffer)
        while json_length:
            nbytes = socket.recv_into(view, json_length)
            view = view[nbytes:]
            json_length -= nbytes

        json_string = buffer.decode("utf-8")
        return json.loads(json_string)
