HEADER_SIZE = 4


def encode_message(message: str) -> bytes:
    """Encode a message using length-prefixed framing."""

    message_bytes = message.encode()

    message_length = len(message_bytes)

    header = message_length.to_bytes(
        HEADER_SIZE,
        byteorder="big"
    )

    return header + message_bytes


def receive_exact(
    peer_socket,
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


def decode_message(peer_socket) -> str | None:
    """Decode a framed message from a socket."""

    header = receive_exact(
        peer_socket,
        HEADER_SIZE
    )

    if not header:
        return None

    message_length = int.from_bytes(
        header,
        byteorder="big"
    )

    message_data = receive_exact(
        peer_socket,
        message_length
    )

    if not message_data:
        return None

    return message_data.decode()