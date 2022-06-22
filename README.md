<!-- ABOUT THE PROJECT -->

## About The Project

The project implements a simple n clients/1-server configuration. The server maintains a message stream that is open to only clients that are part of the group. Further, server keeps track of the text messages being exchanged and logs them to serverLogs.log file. The client is responsible to send a message and take the incoming input stream from the server.

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

- [Python](https://www.python.org/)
- [GRPC](https://grpc.io/docs/languages/python/)
- [Protocol Buffers](https://developers.google.com/protocol-buffers)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

These are the instructions on setting up your project locally.

### Prerequisites

Following are the prerequisites for running the project:

- Python

### Installation

_For running the project please follow the following commands._

1. Clone the repo
   ```sh
   git clone https://github.com/karandeepParashar/GroupChat-GRPC.git
   ```
2. Enter the project directory.
   ```sh
   cd GroupChat-GRPC/GroupChat
   ```
3. Install all dependencies
   ```sh
   python pip install -r requirements.txt
   ```
4. run the server

   ```js
   python .\GroupChat\server.py –-port <port> --clientIds <clientids> 
   ```

5. Open seperate terminal for each client and run

  ```js
  python .\GroupChat\client.py –c <clientId> -i <server_ip> -p <server_port>
  ```
#### DOCKER:

_For running the project in docker please follow the following commands._

1. Build the project
```sh
docker build -t projectName . -f DockerFileServer.txt
```
2. Run the project in container
``` sh
docker run -t -i projectName
```

Default values for all arguments are set, except “clientId” for client.py file. It should be numeric. Unless that id is in server.py’s clientIds, no message will reach or be received. Default value for clientIds = 1,2,3

<p align="right">(<a href="#top">back to top</a>)</p>
