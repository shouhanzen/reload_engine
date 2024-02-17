import socket
import sys

def send_to_socket(message):
    """Function to send a message to the server."""
    # Create a socket object
    s = socket.socket()

    # Define the port on which you want to connect
    port = 12345

    # Exception handling for socket connection
    try:
        # Connect to the server on local computer
        s.connect(('127.0.0.1', port))

        # Send a message to the server
        s.send(message.encode())
        
        response = s.recv(1024).decode()
        print(f"Received response: {response}")

    except ConnectionRefusedError:
        print("Failed to connect to the server. Make sure the server is running and listening on the correct port.")
    finally:
        # Close the connection
        s.close()

valid_commands = ["go", "back", "left", "right", "frame", "reset"]

def repl():
    """Function to start a REPL that accepts commands."""
    print("Starting the command REPL. Type 'stop' to exit.")
    while True:
        # Take input from the user
        command = input("Enter command: ").strip().lower()

        # Check for the stop command to exit the REPL
        if command == "stop":
            print("Stopping the REPL.")
            break

        # You can add more conditions here to handle different commands like 'go', 'back', etc.
        elif command in valid_commands:
            # Send the command to the server
            send_to_socket(command)
            print(f"Sent '{command}' command to the server.")
        else:
            print(f"Unknown command. Available commands are: {valid_commands}.")

if __name__ == "__main__":
    repl()
