from app.utils.server import Server

class Estimation():

    def __init__(self, name):
        self.name = name
        self.config = object
        self.db = object

    def run(self, host, port):
        '''
        Create GazeEstimationServer instance,
        open socket and serve forever
        '''
        server = Server()
        server.open_socket((host, port))
        server.run()
