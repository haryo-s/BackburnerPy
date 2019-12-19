import socket
import xml.etree.ElementTree as ET

class Manager:
    def __init__(self, _manager_ip, _manager_port):
        self.MANAGER_IP = _manager_ip
        self.MANAGER_PORT = _manager_port
        self.BUFFER_SIZE = 1024 #TODO: Default buffer size, might need to be larger

    def open_connection(self):
        self.session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.session.connect((self.MANAGER_IP, self.MANAGER_PORT))
        # On opening connection, if received message is incorrect, close connection
        data = self.session.recv(29)
        print(data.decode("utf-8"))
        if(data.decode("utf-8") != "250 backburner 1.0 Ready.\r\n"):
            self.close_connection()

    def close_connection(self):
        print('Connection to manager closed')
        self.session.close()

    def send_message(self, command):
        self.session.send(command)
        # This first response is 'backburner>'   
        first_response = self.session.recv(128)
        print(first_response)

        # The second response is the response code 251 followed by message length
        second_response = self.session.recv(128)
        print(second_response)

        # Split the response message and get the message_length 
        msg_length = second_response.decode("utf-8").split()[1]
        print(msg_length)

        final_response = self.session.recv(int(msg_length))
        print(final_response)

        return final_response


if __name__ == "__main__":
    manager = Manager('192.168.178.11', 3234)
    manager.open_connection()
    print('sending message')
    print(' ')

    print("get manager info")
    manager.send_message(b'get mgrinfo\r\n')
    print(' ')

    print("get client_list")
    manager.send_message(b'get clientlist\r\n')
    manager.session.close()
    # data = manager.session.recv(1024)
    # print(data)
    # manager.session.send(b'get mgrinfo\r\n')
    # data = manager.session.recv(1024)
    # print(data)
    # data = manager.session.recv(1024)
    # print(data)
    # data = manager.session.recv(843)
    # print(len(data))

    # print('Parsing xml')
    # tree = ET.fromstring(data.decode("utf-8")[:-1]) #[:-1] is to remove last character
    # print(str(tree[0].text))
    # print(str(tree[1].text))
    # print(str(tree[2].text))
    # print(str(tree[3][3].text))



    # manager.session.close()
