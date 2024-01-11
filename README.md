# RPC-client-server

An RPC client which can interact with a synchronous RPC server to initiate function calls.

### File Description

- `rpc_*.py` 👉 contains client/server script.
- `run_*.py` 👉 contains runner code to run  corresponding client/server.
- `function_repo.py` 👉 contains functions to be called by the RPC client.
- `instance_repo.py` 👉 contains classes whose methods is to be called by RPC client.

### Installation

Write your functions and your classes in their respective `*_repo.py` files.

The `.env` file is already primed so it can be used as it is.

```sh
# activate the environment
pipenv install
pipenv shell

# run the server
python3 run_server.py

# run the client
python3 run_client.py
```

### TODOs:

- Enable functionality for instances
