import socket
import select
import sys
import cv2
import numpy

class Server:

    def __init__(self):
        self.running = True
        self.server = None
        self.inputs = []
        self.buffer = []
        self.header_size = 20
        data_length = 0

    # Open the Main Server Socket
    def open_socket(self, endpoint):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind(endpoint)
            self.server.listen(5)

            print('Listening {}:{}'.format(endpoint[0], endpoint[1]))

        except socket.error as error:
            self.error(error)

    # Handle a new incomming client connection
    def process_new_client(self):
        client = Client(self.server.accept())
        self.inputs.append(client)

    # Process a request from a connected client
    def process_client_request(self, client):
        # Request from a client
        while self.running:
            try:
                data = client.socket.recv(client.buffer).strip()
                # receive image header first, then cat data to the buffer
                header = data[0:self.header_size]
                # first 4 bytes encode message type
                # next 8 bytes encode image width and height
                image_type = int.from_bytes(header[0:3], byteorder='little', signed=False)
                image_width = int.from_bytes(header[4:7], byteorder='little', signed=False)
                image_height = int.from_bytes(header[8:11], byteorder='little', signed=False)
                image_bpp = int.from_bytes(header[12:15], byteorder='little', signed=False)

                image_size = (image_height, image_width, image_bpp)
                buffer_size = image_width * image_height * image_bpp

                self.buffer = bytearray(buffer_size)
                data_length = len(data) - self.header_size
                self.buffer[0:data_length] = data[self.header_size:-1]

                while data_length < buffer_size:
                    data = client.socket.recv(client.buffer)
                    self.buffer[data_length:data_length + len(data)] = data

                # display image
                image = np.frombuffer(self.buffer, np.uint8).reshape(image_size)
                cv2.imshow('image', image)
                cv2.waitKey(0)
                # not a first call
                self.sendall('Data received!'.encode())
            except socket.error as error:
                self.error(error)

    # Send a message to all connected clients
    def sendall(self, data):
        for client in self.inputs:
            if isinstance(client, Client):
                client.send(data)

    def error(self, *error):
        message, value = error
        if self.server:
            self.server.close()
        print('Could not open socket: {}, {}'.format(message, value))
        sys.exit(1)

    # Shutdown the server
    def shutdown(self):
        # Close all the connected clients
        for client in self.inputs:
            if isinstance(client, Client):
                self.inputs.remove(client)
                client.send('Server Shutting Down!\n')
                client.socket.close()
        # Now close the server socket
        if self.server:
            self.server.close()
        # And stop running
        self.running = False

    # Main Server Loop
    def run(self):
        # Input Sources
        self.inputs = [self.server]
        self.running = True

        while self.running:
            # Check client instance
            for client in self.inputs:
                if client == self.server:
                    # Process a first connection from client
                    self.process_new_client()

                elif isinstance(client, Client):
                    # Process a message from a connected client
                    self.process_client_request(client)
        # Shutdown the Server
        self.shutdown()


# Class to keep track of a connected client
class Client:

    def __init__(self, *client):
        socket, address = client[0]
        self.socket = socket
        self.address = address
        self.buffer = 65536
        self.socket.setblocking(0)

    # This lets the Client class pretend to be a socket
    def fileno(self):
        return self.socket.fileno()

    # Send message to Client
    def send(self, data):
        self.socket.send(data)
