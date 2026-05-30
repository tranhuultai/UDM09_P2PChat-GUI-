import json
import struct
import datetime
from typing import Dict, Any, Optional
from security.crypto import CryptoHandler
from cryptography.fernet import InvalidToken

class ProtocolHandler:
    """
    Handles packet creation, serialization, framing, and validation.
    """
    HEADER_SIZE = 4  # 4-byte length header

    def __init__(self, crypto_handler: CryptoHandler):
        self.crypto_handler = crypto_handler

    def create_packet(self, msg_type: str, sender: str, payload_content: str) -> Dict[str, str]:
        """
        Creates a packet dictionary with an encrypted payload.
        """
        encrypted_payload = self.crypto_handler.encrypt(payload_content)
        
        packet = {
            "type": msg_type,
            "sender": sender,
            "payload": encrypted_payload,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        return packet

    def serialize(self, packet: Dict[str, Any]) -> bytes:
        """
        Serializes a packet dictionary into a framed byte stream.
        Format: [4-byte length header][json_payload]
        """
        json_data = json.dumps(packet).encode('utf-8')
        # Length header includes its own size + the data size
        total_length = self.HEADER_SIZE + len(json_data)
        header = struct.pack('!I', total_length)
        return header + json_data

    def deserialize(self, framed_data: bytes) -> Dict[str, Any]:
        """
        Deserializes a framed byte stream into a packet dictionary.
        """
        if len(framed_data) < self.HEADER_SIZE:
            raise ValueError("Data too short to contain a header.")
            
        header = framed_data[:self.HEADER_SIZE]
        total_length = struct.unpack('!I', header)[0]
        
        if len(framed_data) < total_length:
            raise ValueError(f"Incomplete packet. Expected {total_length} bytes, got {len(framed_data)}.")
            
        json_data = framed_data[self.HEADER_SIZE:total_length]
        try:
            return json.loads(json_data.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            raise ValueError(f"Malformed packet: {str(e)}")

    def validate_and_decrypt(self, packet: Dict[str, Any]) -> Optional[str]:
        """
        Validates the packet structure and attempts to decrypt the payload.
        Returns the decrypted payload string if successful, or None if validation/decryption fails.
        """
        required_fields = ["type", "sender", "payload", "timestamp"]
        
        # Check for missing fields
        for field in required_fields:
            if field not in packet:
                print(f"Validation Error: Missing field '{field}'")
                return None
        
        # Attempt decryption
        try:
            decrypted_payload = self.crypto_handler.decrypt(packet["payload"])
            return decrypted_payload
        except (InvalidToken, ValueError) as e:
            print(f"Decryption/Validation Error: {str(e)}")
            return None

    def handle_incoming_data(self, data: bytes) -> Optional[Dict[str, Any]]:
        """
        A helper method to process incoming raw bytes, deserialize, and return the packet.
        """
        try:
            packet = self.deserialize(data)
            return packet
        except ValueError as e:
            print(f"Incoming data error: {str(e)}")
            return None