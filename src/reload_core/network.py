import socket 
import select

sockets_list = []
def start_dev_server():
    global sockets_list
    
    try:
        # Create a server socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Bind the socket to a public host, and a well-known port
        server_socket.bind(('localhost', 12345))
        
        # Become a server socket
        server_socket.listen(5)
        
        print("Server started at localhost on port 12345")
        sockets_list.append(server_socket)
        
        return server_socket
    except Exception as e:
        print("Error starting dev server")
        print(e)
        return None

def update_socket(server_socket, cmds):
    # client_socket, addr = server_socket.accept()
    # print(f"Got connection from {addr}")
    
    try:
        # Use select to wait for socket to be ready to read
        readable, writable, errored = select.select(sockets_list, [], [], 0.001)
        for s in readable:
            if s is server_socket:
                # Accept new connection
                client_socket, client_address = server_socket.accept()
                print(f"Accepted new connection from {client_address}")
                client_socket.setblocking(0)
                sockets_list.append(client_socket)
            else:
                # Read data from a client socket
                data = s.recv(1024)
                if data:
                    print(f"Received data: {data} from {s.getpeername()}")
                    
                    # Execute command
                    cmd = data.decode().strip().lower()
                    if cmd in cmds:
                        cmds[cmd](s)
                    
                    
                else:
                    # Remove socket that's closed
                    print(f"Closing connection to {s.getpeername()}")
                    sockets_list.remove(s)
                    s.close()
    
    except Exception as e:
        print("Error receiving message")
        print(e)
        return None
    

def send_dev_message(dev_socket, message):
    dev_socket.sendall(message.encode())

def recv_dev_message(dev_socket):
    return dev_socket.recv(1024).decode()