import socket


def validate_ip(ip: str) -> bool:
    """Validate IPv4 address."""

    try:
        socket.inet_aton(ip)
        return True

    except OSError:
        return False


def validate_port(port: str) -> bool:
    """Validate TCP port number."""

    if not port.isdigit():
        return False

    port_number = int(port)

    return 1 <= port_number <= 65535