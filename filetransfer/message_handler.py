import socket


# Sends a message through the given socket
# Receives a socket, and a byte message
def send_message(sock, message):
    message = bytearray(message)
    # Create byte array that contains message size in 4 bytes
    msg_len = bytearray(len(message).to_bytes(4, "big"))

    # Append message len to current message
    message = msg_len + message
    sock.sendall(message)


def receive_message(sock) -> bytearray:
    # Read msg_len consistently from socket
    b_msg_len = bytearray()
    while len(b_msg_len) < 4:
        curr_msg_len = sock.recv(4 - len(b_msg_len))

        # No data len obtained
        if not b_msg_len:
            return None

        b_msg_len.extend(curr_msg_len)

    # Unpack data len into an int
    msg_len = int.from_bytes(b_msg_len, byteorder="big")

    # Read data of the length of data_len
    message = bytearray()
    while len(message) < msg_len:
        curr_msg = sock.recv(msg_len - len(message))

        # No data obtained/exists
        if not curr_msg:
            return None

        message.extend(curr_msg)  # Add to the array of message

    return message
