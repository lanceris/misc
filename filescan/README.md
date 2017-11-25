This program recursively scans a specific folder on hard drive every N seconds and transfer path and size of changed files (+creation/deletion) via TCP to server. Also includes sample server to receive TCP connections.

Arguments:
--loop - time between folder scans in seconds (default: 2)
--ip – Receiver PC/server IP-address (default: localhost)
--port - Receiver PC/server port (default: 9812)
path to folder for scan (required)
Example: python scanner.py /test --loop 60 --port 8000
