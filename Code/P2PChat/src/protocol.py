HEADER_SIZE = 4

import json
import struct
import socket


def encode_message(
    message: str | dict
) -> bytes:
    """Encode message with length header."""

    if isinstance(message, dict):
        message = json.dumps(message)

    message_bytes = message.encode()

    message_length = len(message_bytes)

    header = struct.pack(
        "!I",
        message_length
    )

    return header + message_bytes


def receive_exact(
    peer_socket: socket.socket,
    size: int
) -> bytes:
    """Receive an exact number of bytes."""

    buffer = b""

    while len(buffer) < size:
        data = peer_socket.recv(
            size - len(buffer)
        )

        if not data:
            return b""

        buffer += data

    return buffer


def decode_message(
    peer_socket: socket.socket
) -> str | dict | None:
    """Decode message from socket."""

    try:
        header = receive_exact(
            peer_socket,
            HEADER_SIZE
        )

        if not header:
            return None

        message_length = struct.unpack(
            "!I",
            header
        )[0]

        data = b""

        data = receive_exact(
            peer_socket,
            message_length
        )

        if not data:
            return None 


        message = data.decode()

        try:
            parsed_message = json.loads(message)

            if isinstance(parsed_message, dict):
                return parsed_message
            
            return message

        except json.JSONDecodeError:
            return message

    except OSError:
        return None