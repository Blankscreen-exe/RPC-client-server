
import json
import socket
import os
from dotenv import load_dotenv

load_dotenv()

SIZE=1024

class RPCClient:
    def __init__(self, host:str=os.environ.get('SERVER_HOST', 'localhost'), port:int=os.environ.get('SERVER_PORT', 8080)) -> None:
        self.__sock = None
        self.__address = (host, port)

    def connect(self):
        try:
            self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__sock.connect(self.__address)
        except EOFError as e:
            print(e)
            raise Exception('Client was not able to connect.')
    
    def disconnect(self):
        try:
            self.__sock.close()
        except:
            pass

    def __getattr__(self, __name: str):
        def execute(*args, **kwargs):
            self.__sock.sendall(json.dumps((__name, args, kwargs)).encode())

            response = json.loads(self.__sock.recv(SIZE).decode())
            print(response)
            return response
        
        return execute
    
    # TODO: add method to show available method names
    def get_method_names(self) -> list:
        try:
            # Send a special request to the server to get method names
            self.__sock.sendall(json.dumps(("__get_method_names__", [], {})).encode())
            
            # Receive the response containing the method names
            response = json.loads(self.__sock.recv(SIZE).decode())
            
            if isinstance(response, list):
                print(response)
            else:
                print(response)
                print("Unexpected response format for method names.")
                return []
        except Exception as e:
            print(f"Error retrieving method names: {e}")
            return []
