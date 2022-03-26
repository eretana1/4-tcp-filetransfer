import socket
import os


# Sends a file through the given socket
# Receives a socket, and a byte message and thread lock
def send_file(sock, filename, lock):
    lock.acquire()   # Get the current lock for thread

    try:
        # [4 bytes of file name size] [file name] [4 bytes of content size] [content]
        b_file = open(filename, 'rb')
        b_file_size = os.path.getsize(filename)
        b_file_name = filename.encode()
        b_file_name_size = len(b_file_name)

        # Create content to send to socket
        file_content = bytearray(b_file_name_size.to_bytes(4, 'big')) + bytearray(b_file_name) + bytearray(b_file_size.to_bytes(4, 'big')) + bytearray(b_file.read())
 
        b_file.close()
        sock.sendall(file_content)
        
    except FileNotFoundError:
        os.write(1, f'{filename}: File not found. Please try again.'.encode())
        sock.sendall(b'')

    lock.release() #File transfer is completed, release lock for thread
    

def recv_all(sock, msg_len) -> bytearray:
    # Read message consistently from socket
    b_msg = bytearray()

    while len(b_msg) < msg_len:
        curr_msg = sock.recv(msg_len - len(b_msg))

        b_msg.extend(curr_msg)

        # No data len obtained
        if not b_msg:
            return None

    return b_msg


def receive_file(sock):
    # Read filename from socket
    b_filename_len = recv_all(sock, 4)

    # No more content
    if b_filename_len is None:
        return ''
    
    # Convert len to int
    filename_len = int.from_bytes(b_filename_len, byteorder="big")

    # Get filename
    b_file_name = recv_all(sock, filename_len)

    # Get content len
    b_content_len = recv_all(sock, 4)

    # Convert content len to int
    content_len = int.from_bytes(b_content_len, byteorder='big')

    # Get content
    b_content = recv_all(sock, content_len)

    # Create new file in directory
    filename = b_file_name.decode().split('/')[-1]

    version = 1 
    while os.path.exists(f'client_files/{filename}'):
        filename = filename.split('.')[0].split('(')[0] + (f'({version})') + '.' + filename.split('.')[1]
        version += 1
        
        
    with open(f'client_files/{filename}', 'wb') as transferred_file:
        transferred_file.write(b_content)
    

    return b_file_name.decode()
