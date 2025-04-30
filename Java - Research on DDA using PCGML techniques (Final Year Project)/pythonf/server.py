import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import socket
import tensorflow as tf
import numpy as np



def get_diff(input):
    model = tf.keras.models.load_model("./src/model/py_model.keras")
    #print(np.array(input).reshape((1,4)))
    out = model.predict(np.array(input).reshape((1,4)))
    #print(out)
    
    out_str = ",".join([str(i) for i in out[0]])

    #print(out_str)
    return out_str

def clean_input(input):
    input  = input.strip("\nr")
    out = input.split(",")
    for i in range(len(out)):
        out[i] = float(out[i])
    return out

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get the local machine name and port
host = socket.gethostname()
port = 8000

# Bind to the port
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(5)

print(f"Server listening on {host}:{port}")

while True:
    # Establish connection with client
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")

    # Receive data from the client
    data = client_socket.recv(1024).decode()
    print(f"Received from client: {data}")
    diff = get_diff(clean_input(data))

    # Send a response back to the client
    #response = "Hello from server!"
    #client_socket.send(response.encode())
    print(f"Sent to client: {diff}")
    client_socket.send(diff.encode())

    # Close the connection
    client_socket.close()
    #break

server_socket.close()