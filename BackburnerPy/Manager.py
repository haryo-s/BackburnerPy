import BackburnerDataClasses as BDC
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
        else:
            # Slight bodge so all commands work by requesting manager_info on connection
            self.get_manager_info()

    def close_connection(self):
        print('Connection to manager closed')
        self.session.close()

    def _send_message(self, command):
        self.session.send(command)

        # This first response is 'backburner>'   
        first_response = self.session.recv(128)

        # Get the second response which includes a response code
        second_response = self.session.recv(128)

        # If the response code is 251, split the response message and get the message_length
        # TODO: Else does not work
        if int(second_response.decode("utf-8").split()[0]) == 251:
            msg_length = second_response.decode("utf-8").split()[1]

            final_response = self.session.recv(int(msg_length))
            return final_response
        else:
            return second_response

    def get_manager_info(self):
        raw_message = self._send_message(b'get mgrinfo\r\n')
        # print(raw_message)
        parsed = ET.fromstring(raw_message.decode("utf-8")[:-1])

        version = int(parsed[0].text)
        servers = int(parsed[1].text)
        jobs = int(parsed[2].text)

        total_memory = int(parsed[3][0].text)
        total_memory_f = float(parsed[3][1].text)
        num_cpus = int(parsed[3][2].text)
        platform = str(parsed[3][3].text)
        user = str(parsed[3][4].text)
        computer_name = str(parsed[3][5].text)
        mac = str(parsed[3][6].text)
        workdisk_space = int(parsed[3][7].text)
        ip_address = str(parsed[3][8].text)
        sysinfo = BDC.SystemInfo(total_memory, total_memory_f, num_cpus, platform, user, computer_name, mac, workdisk_space, ip_address)

        dropped_packets = int(parsed[4][0].text)
        bad_packets = int(parsed[4][1].text)
        tcp_requests = int(parsed[4][2].text)
        udp_requests = int(parsed[4][3].text)
        boot_time = str(parsed[4][4].text)
        net_status = BDC.NetworkStatus(dropped_packets, bad_packets, tcp_requests, udp_requests, boot_time)

        manager_info = BDC.BackburnerManagerInfo(version, servers, jobs, sysinfo, net_status)

        return manager_info

    # TODO: get_client_list has an issue where if it's the first command sent, the message length response also includes a portion of the xml data
    def get_client_list(self):
        raw_message = self._send_message(b'get clientlist\r\n')
        # print(raw_message)
        parsed = ET.fromstring(raw_message.decode("utf-8")[:-1])
        client_list = []
        for client in parsed:
            version = int(client[0].text)
            udp_port = int(client[1].text)
            controller = False
            if int(client[2].text) == 1:
                controller == True

            total_memory = int(client[3][0].text)
            total_memory_f = float(client[3][1].text)
            num_cpus = int(client[3][2].text)
            platform = str(client[3][3].text)
            user = str(client[3][4].text)
            computer_name = str(client[3][5].text)
            mac = str(client[3][6].text)
            workdisk_space = int(client[3][7].text)
            ip_address = str(client[3][8].text)
            sysinfo = BDC.SystemInfo(total_memory, total_memory_f, num_cpus, platform, user, computer_name, mac, workdisk_space, ip_address)

            client_data = BDC.Client(version, udp_port, controller, sysinfo)
            client_list.append(client_data)
        
        return client_list


if __name__ == "__main__":
    manager = Manager('192.168.178.11', 3234)
    manager.open_connection()
    # manager_info = manager.get_manager_info()
    print("")
    manager_info = manager.get_client_list()
    print("")
    manager.close_connection()

    print('')
    
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
