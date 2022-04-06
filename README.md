# GroupChat-GRPC
A multi client, single server chatting application using RPC calls.

```sh
python -m <env-name> venv
```
```sh
python pip install -r requirements.txt
 ```
```sh
python .\GroupChat\server.py –-port <port> --clientIds <clientids> 
 ```
----Open Separate Terminal-------

```sh
python .\GroupChat\client.py –c <clientId> -i <server_ip> -p <server_port> 
```

FOR DOCKER:
```sh
docker build -t proj-1-karandeep . -f DockerFileServer.txt
```
``` sh
docker run -t -i proj-1-karandeep
```
Default values for all arguments are set, except “clientId” for client.py file. It should be numeric. Unless that id is in server.py’s clientIds, no message will reach or be received. Default value for clientIds = 1,2,3
