import socket
import ssl

HOST = 'www.google.com'  # Server hostname or IP address
PORT = 443               # HTTPS port
TIMEOUT = 10             # Set timeout in seconds

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.settimeout(TIMEOUT)  # Set the timeout

# Create an SSL context
context = ssl.create_default_context()

# Wrap the socket with SSL using the context
ssl_socket = context.wrap_socket(client_socket, server_hostname=HOST)

# Connect to the server
server_address = (HOST, PORT)
ssl_socket.connect(server_address)

# Send an HTTP GET request
request_header = b'GET / HTTP/1.0\r\nHost: www.google.com\r\n\r\n'
ssl_socket.sendall(request_header)

# Receive the response
response = ''
while True:
    try:
        recv = ssl_socket.recv(1024)
        if not recv:
            break
        # Decode with 'ignore' to handle non-UTF-8 bytes
        response += recv.decode('utf-8', errors='ignore')
    except socket.timeout:
        print("Socket connection timed out.")
        break

# Print the response
print(response)

# Close the connection
ssl_socket.close()
