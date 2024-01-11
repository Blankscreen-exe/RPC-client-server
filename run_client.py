from rpc_client import RPCClient
from dotenv import load_dotenv
import os

load_dotenv()

print("PORT = ", os.environ.get('SERVER_PORT'))
print("HOST = ", os.environ.get('CLIENT_HOST'))
# TODO: use env variables
client = RPCClient(os.environ.get('CLIENT_HOST', '0.0.0.0'), int(os.environ.get('SERVER_PORT', 8000)))

print("\033[91m\bReady to accept Remote Procedure Calls ...")
print("e.g. function_name(param_1, param_2=123)")
print("Type 'exit()' or press Ctrl+C to close the client.")
print("------------------------------------------------------", end="\033[0m\n\n")

while True:
    try:  
        client.connect()

        command = input("\033[92;1m\b> ")
        print("\033[0m\b\b")  
        if "exit()" in command:
            client.disconnect()
            exec(command)
        else:
            exec(f"client.{command}")
        
        print()

    except Exception as e:
        print (e)
        print("Connection Closed")
        client.disconnect()
        break