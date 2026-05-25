import socket
import threading
from protocol import (
    encode_message, 
    decode_message
)   

class P2PNode:
    def __init__(
        self,
        host: str,
        port: int,
        on_message=None,
        on_disconnect=None
    ) -> None:
        self.host = host
        self.port = port

        self.on_message = on_message
        self.on_disconnect = on_disconnect

        self.server_socket: socket.socket | None = None
        self.peers: dict[str, socket.socket] = {}
        self.is_running = False

    def start_server(self) -> None:
        """Start the TCP server."""

        self.server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self.server_socket.settimeout(1)

        self.server_socket.bind(
            (self.host, self.port)
        )

        self.server_socket.listen()

        self.is_running = True

        print(
            f"[INFO] Listening on {self.host}:{self.port}"
        )

        accept_thread = threading.Thread(
            target=self.accept_connections,
            daemon=True
        )

        accept_thread.start()

    def accept_connections(self) -> None:
        """Accept incoming peer connections."""

        if self.server_socket is None:
            return

        while self.is_running:
            try:
                client_socket, address = (
                    self.server_socket.accept()
                )

                print(
                    f"[INFO] Peer connected: {address}"
                )

                peer_address = f"{address[0]}:{address[1]}"

                if peer_address in self.peers:
                    print(
                        f"[INFO] Peer already connected: {peer_address}"
                    )
                    client_socket.close()
                    continue

                self.peers[peer_address] = client_socket

                print(
                    f"[INFO] Active peers: {len(self.peers)}"
                )

                receive_thread = threading.Thread(
                    target=self.receive_messages,
                    args=(client_socket,),
                    daemon=True
                )   

                receive_thread.start()  

            except socket.timeout:
                continue

            except OSError:

                if self.is_running:
                    print(
                        "[ERROR] Accept connection failed"
                    )

                break

    # Networking interface
    # Used by GUI layer
    def connect_to_peer(self, host: str, port: int) -> bool:
        """Connect to another peer."""

        try:
            peer_socket = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            peer_socket.settimeout(10)

            peer_socket.connect((host, port))

            print(
                f"[INFO] Connected to peer {host}:{port}"
            )

            peer_address = f"{host}:{port}" 

            if peer_address in self.peers:

                print(
                    f"[INFO] Already connected to {peer_address}"
                )

                peer_socket.close()

                return False

            self.peers[peer_address] = peer_socket

            print(
                f"[INFO] Active peers: {len(self.peers)}"
            )
            
            handshake_message = (
                f"HELLO {self.host}:{self.port}"
            )

            message_data = encode_message(
                handshake_message
            )

            peer_socket.sendall(message_data)

            receive_thread = threading.Thread(
                target=self.receive_messages,
                args=(peer_socket,),
                daemon=True
            )   

            receive_thread.start()  
            return True
        
        except OSError as error:
            print(
                f"[ERROR] Failed to connect: {error}"
            )
            return False   

    # Networking receive loop
    # Handles incoming peer messages
    def receive_messages(
        self,
        peer_socket: socket.socket
    ) -> None:
        """Receive messages from a peer."""

        while self.is_running:
            try:
                message = decode_message(peer_socket)

                if message is None:
                    self.remove_peer(peer_socket)
                    break

                if message.startswith("HELLO"):
                    print(
                        f"[HANDSHAKE] {message}"
                    )

                elif self.on_message is not None:
                    self.on_message(message)

                else:
                    print(
                        f"[MESSAGE] {message}"
                    )

            except ConnectionResetError:
                print("[INFO] Connection reset by peer")
                self.remove_peer(peer_socket)
                break   

            except OSError as error:
                if self.is_running:
                    print(f"[ERROR] Receive failed: {error}")
                self.remove_peer(peer_socket)
                break

    # Connection lifecycle cleanup
    def remove_peer(
        self,
        peer_socket: socket.socket
    ) -> None:
        """Remove a peer from the list."""

        peer_address = None

        for address, socket_object in list(
            self.peers.items()
        ):
            if socket_object == peer_socket:
                peer_address = address
                break

        if peer_address is not None:
            del self.peers[peer_address]

            print(
                f"[INFO] Peer removed: {peer_address}"
            )
        try:
            peer_socket.close()
        except OSError:
            pass

        if peer_address is not None:
            print(
                f"[INFO] Peer disconnected: {peer_address}"
            )

            print(
                f"[INFO] Remaining peers: {len(self.peers)}"
            )

            if self.on_disconnect is not None:
                self.on_disconnect(peer_address) 

    # Networking interface
    # Used by GUI layer
    def send_message(
        self,
        message: str,
        peer_address: str
    ) -> None:
        """Send a message to connected peers."""

        peer_socket = self.peers.get(peer_address)
        
        if peer_socket is not None:
            try:
                message_data = encode_message(message)
                peer_socket.sendall(message_data)

            except BrokenPipeError:
                print("[INFO] Peer disconnected")
                self.remove_peer(peer_socket)

            except OSError as error:
                print(f"[ERROR] Send failed: {error}")
                self.remove_peer(peer_socket)

    def stop_server(self) -> None:
        """Stop the TCP server."""

        self.is_running = False

        for peer_socket in list(
            self.peers.values()
        ):

            try:
                peer_socket.close()

            except OSError:
                pass

        self.peers.clear()

        if self.server_socket is not None:
            self.server_socket.close()

            print("[INFO] Server stopped.")