import json
import socket
import inspect
from threading import Thread
import os
from dotenv import load_dotenv

load_dotenv()

SIZE=1024

class RPCServer:

    def __init__(self, host:str="0.0.0.0", port:int=int(os.environ.get('SERVER_PORT', 8080))) -> None:
        self.host = host
        self.port = port
        self.address = host, port
        self._methods = {}

    def register_method(self, function) -> None:
        try:
            print(function.__code__.co_varnames)
            self._methods.update({function.__name__: function})
        except:
            raise Exception('A non function object has been passed into RPCServer.registerMethod(self, function)')
        
    # FIXME(001): class not getting registered
    # def register_instance(self, instance=None) -> None:
    #     try:
    #         for function_name, function in inspect.getmembers(instance, predicate=inspect.ismethod):
    #             if not function_name.startswith('__'):
    #                 self._methods.update({function_name, function})
    #     except:
    #         raise Exception('A non class object has been passed into RPCServer.registerInstance(self, instance)')
        
    def __handle__(self, client:socket.socket, address:tuple) -> None:
        print(f"managing requests from address {address}.")
        while True:
            try:
                function_name, args, kwargs = json.loads(client.recv(SIZE).decode())

                if function_name == "__get_method_names__":
                    print("SPECIAL REQUEST")
                    # Respond with the list of method names
                    client.sendall(json.dumps(self.get_method_names()).encode())
                    continue
            except:
                print(f'! Client {address} disconnected.')
                break

            print(f'> {address} : {function_name}({args})')

            try:
                response = self._methods[function_name](*args, **kwargs)
            except Exception as e:
                client.sendall(json.dumps(str(e)).encode())
            else:
                client.sendall(json.dumps(response).encode())

        print(f'Completed request from {address}')
        client.close()

    def run(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(self.address)
            sock.listen()

            print(f'+ Server {self.address} running')

            while True:
                try:
                    client, address = sock.accept()
                    Thread(target=self.__handle__, args=[client, address]).start()
                except KeyboardInterrupt:
                    print(f'- Server {self.address} interrupted')
                    break

    def get_method_names(self) -> list:
        return list(self._methods.keys())
