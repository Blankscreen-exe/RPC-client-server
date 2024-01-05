import function_repo as fr
import instance_repo as ir
from rpc_server import RPCServer
from functools import reduce
import inspect

server = RPCServer()

list_of_functions = inspect.getmembers(fr, inspect.isfunction)
for func in list_of_functions:
    server.register_method(func[1])

# TODO: enable this once FIXME(001) gets completed
list_of_classes = inspect.getmembers(ir, inspect.isclass)
# print(list_of_classes)
# for cls in list_of_classes:
    # print(cls)
    # server.register_instance(cls[1])

print("\033[94m", "\b=== Available Methods ===")
print(reduce(lambda a, x: a + " 🔷 " + f"{x}", server.get_method_names()))
print("=========================", end="\033[0m\n\n")

server.run()