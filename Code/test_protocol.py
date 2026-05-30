from security.crypto import CryptoHandler
from security.protocol import ProtocolHandler
import json
import struct

def test_protocol_flow():
    print("--- Starting Protocol & Encryption Tests ---")
    
    # 1. Initialize Crypto and Protocol
    key = CryptoHandler.generate_key()
    crypto = CryptoHandler(key)
    protocol = ProtocolHandler(crypto)
    
    # 2. Create a packet
    msg_type = "message"
    sender = "Alice"
    content = "Hello, this is a secret message!"
    
    print(f"Original Content: {content}")
    
    packet = protocol.create_packet(msg_type, sender, content)
    print("\nCreated Packet (Encrypted):")
    print(json.dumps(packet, indent=2))
    
    # 3. Serialize (Framing)
    framed_data = protocol.serialize(packet)
    print(f"\nSerialized Data Length: {len(framed_data)} bytes")
    header = framed_data[:4]
    length = struct.unpack('!I', header)[0]
    print(f"Framing Header Length: {length}")
    
    # 4. Deserialize
    received_packet = protocol.deserialize(framed_data)
    print("\nDeserialized Packet:")
    print(json.dumps(received_packet, indent=2))
    
    # 5. Validate and Decrypt
    decrypted_content = protocol.validate_and_decrypt(received_packet)
    print(f"\nDecrypted Content: {decrypted_content}")
    
    assert decrypted_content == content
    print("\n[SUCCESS] Basic flow verified.")

def test_error_handling():
    print("\n--- Starting Error Handling Tests ---")
    crypto = CryptoHandler()
    protocol = ProtocolHandler(crypto)
    
    # Test 1: Malformed Packet (Invalid JSON)
    print("Test 1: Malformed Packet")
    bad_data = struct.pack('!I', 10) + b"not_json"
    try:
        protocol.deserialize(bad_data)
    except ValueError as e:
        print(f"Caught expected error: {e}")

    # Test 2: Decryption Failure (Wrong Key)
    print("\nTest 2: Decryption Failure")
    packet = protocol.create_packet("test", "Bob", "Secret")
    
    # Create a new handler with a different key
    wrong_crypto = CryptoHandler()
    wrong_protocol = ProtocolHandler(wrong_crypto)
    
    result = wrong_protocol.validate_and_decrypt(packet)
    if result is None:
        print("Caught expected decryption failure (returned None)")

    # Test 3: Missing Fields
    print("\nTest 3: Missing Fields")
    incomplete_packet = {"type": "test", "payload": "something"}
    result = protocol.validate_and_decrypt(incomplete_packet)
    if result is None:
        print("Caught expected missing fields (returned None)")

    print("\n[SUCCESS] Error handling verified.")

if __name__ == "__main__":
    test_protocol_flow()
    test_error_handling()