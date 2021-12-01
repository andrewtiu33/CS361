import socket
import csv

#creates the socket object, AF_INET is for ipv4, sock_stream is for tcp
microServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#binds the socket server to port 1443 (localhost means it will only accept connections on same computer)
microServer.bind(('localhost', 1443))

#put server into listen mode with buffer of 6
microServer.listen(6)


#dict1 will import all current hints from the csv storage
dict1 = {}
with open('microStorage.csv', mode='r', newline="") as file1:

    csv_reader = csv.reader(file1)
    next(csv_reader)

    for row in csv_reader:
        character = row[0]
        hint = row[1]
        dict1[character] = hint


#while loop so that will keep allowing new connections to form
while True:
    #accepts new connection, returns the client object and address of the connection
    clientRequestor, address = microServer.accept()

    #receives message from the client and decodes it
    message = clientRequestor.recv(400)
    decodedMessage = message.decode()

    #gets the corresponding hint associated with the character in the decoded message
    responseMessage = dict1[decodedMessage]

    #encodes the hint and sends it to the client
    clientRequestor.sendall(responseMessage.encode())

    #closes the client connection once the hint is sent
    clientRequestor.close()
