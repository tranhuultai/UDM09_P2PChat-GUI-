import socket
import threading


class P2PNode:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port

        self.server_socket: socket.socket | None = None
        self.peers: list[socket.socket] = []
        self.is_running = False

    def start_server(self) -> None:
        """Start the TCP server."""

        self.server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

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

                self.peers.append(client_socket)
                receive_thread = threading.Thread(
                    target=self.receive_messages,
                    args=(client_socket,),
                    daemon=True
                )   

                receive_thread.start()  
                client_socket.close()

            except OSError:
                break

    def connect_to_peer(
        self,
        host: str,
        port: int
    ) -> None:
        """Connect to another peer."""

        try:
            peer_socket = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            peer_socket.connect((host, port))

            print(
                f"[INFO] Connected to peer {host}:{port}"
            )

            self.peers.append(peer_socket)

            receive_thread = threading.Thread(
                target=self.receive_messages,
                args=(peer_socket,),
                daemon=True
            )   

            receive_thread.start()  

        except OSError as error:
            print(
                f"[ERROR] Failed to connect: {error}"
            )
    
    def receive_messages(
        self,
        peer_socket: socket.socket
    ) -> None:
        """Receive messages from a peer."""

        while self.is_running:
            try:
                data = peer_socket.recv(1024)

                if not data:
                    break

                message = data.decode()

                print(
                    f"[MESSAGE] {message}"
                )

            except OSError:
                break

    def stop_server(self) -> None:
        """Stop the TCP server."""

        self.is_running = False

        if self.server_socket is not None:
            self.server_socket.close()

            print("[INFO] Server stopped.")