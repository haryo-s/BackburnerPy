import BackburnerDataClasses as BDC
import socket
import xml.etree.ElementTree as ET
import time

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
            # Briefly wait for correct data transmission
            time.sleep(1)

    def close_connection(self):
        print('Connection to manager closed')
        self.session.close()

    def _send_message(self, command):
        self.session.send(command)

        # This first response is 'backburner>'   
        first_response = self.session.recv(128)

        # Get the second response which includes a response code
        second_response = self.session.recv(128)

        # print('First response:')
        # print(str(first_response))
        # print('Second response')
        # print(str(second_response))

        # If the response code is 251, split the response message and get the message_length
        # TODO: Else does not work
        if int(second_response.decode("utf-8").split()[0]) == 251:
            msg_length = second_response.decode("utf-8").split()[1]

            final_response = self.session.recv(int(msg_length))
            # print('Final response')
            # print(str(final_response))
            return final_response
        else:
            return second_response

    def _get_parsed_message(self, command):
        time.sleep(1) # Briefly wait to stabilise the data
        raw_message = self._send_message(command)
        return ET.fromstring(raw_message.decode("utf-8")[:-1])

    def get_manager_info(self):
        parsed = self._get_parsed_message(b'get mgrinfo\r\n')

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
        parsed = self._get_parsed_message(b'get clientlist\r\n')

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

    def get_plugin_list(self):
        parsed = self._get_parsed_message(b'get pluglist\r\n')

        plugin_list = []

        for plugin in parsed:
            version = int(plugin[0].text)
            name = str(plugin[1].text)
            description = str(plugin[2].text)

            plugin_data = BDC.Plugin(version, name, description)
            plugin_list.append(plugin_data)
        
        return plugin_list

    def get_server_list(self):
        parsed = self._get_parsed_message(b'get srvlist\r\n')

        server_list = []

        for server in parsed:
            handle = str(server[0].text)
            state = int(server[1].text)
            name: str(server[2].text)
        
        return server_list

    def get_server(self, handle):
        parsed = self._get_parsed_message(b'get pluglist 002590A4C7A60000\r\n' )

        version = int(parsed[0][0].text)
        name = str(parsed[0][1].text)
        user_name = str(parsed[0][2].text)
        total_task = int(parsed[0][3].text)
        total_time = float(parsed[0][4].text)
        perf_index = float(parsed[0][5].text)
        ip_address = str(parsed[0][6].text)
        current_status = int(parsed[0][7].text)

        total_memory = int(parsed[1][0].text)
        total_memory_f = float(parsed[1][1].text)
        num_cpus = int(parsed[1][2].text)
        platform = str(parsed[1][3].text)
        workdisk_space = int(parsed[1][4].text)
        mac = str(parsed[1][5].text)
        hw_info = BDC.HardwareInfo(total_memory, total_memory_f, num_cpus, platform, workdisk_space, mac)

        dropped_packets = int(parsed[2][0].text)
        bad_packets = int(parsed[2][1].text)
        tcp_requests = int(parsed[2][2].text)
        udp_requests = int(parsed[2][3].text)
        boot_time = str(parsed[2][4].text)
        net_status = BDC.NetworkStatus(dropped_packets, bad_packets, tcp_requests, udp_requests, boot_time)

        sunday = int(parsed[3][0].text)
        monday = int(parsed[3][1].text)
        tuesday = int(parsed[3][2].text)
        wednesday = int(parsed[3][3].text)
        thursday = int(parsed[3][4].text)
        friday = int(parsed[3][5].text)
        saturday = int(parsed[3][6].text)
        server_schedule = BDC.ServerSchedule(sunday, monday, tuesday, wednesday, thursday, friday, saturday)

        att_priority = False
        if int(parsed[4][0].text) == 1:
            att_priority == True
        una_priority = False
        if int(parsed[4][1].text) == 1:
            att_priority == True

        current_job = int(parsed[5][0].text)
        current_task = int(parsed[5][1].text)
        task_started = str(parsed[5][2].text)

        plugin_list = []
        for plugin in parsed[6]:
            version = int(plugin[0].text)
            name = str(plugin[1].text)
            description = str(plugin[2].text)

            plugin_data = BDC.Plugin(version, name, description)
            plugin_list.append(plugin_data)
        
        server = BDC.Server(version, name, user_name, total_task, total_time, perf_index, ip_address, current_status, hw_info, net_status, server_schedule, att_priority, una_priority, current_job, current_task, task_started, plugin_list)

        return server
if __name__ == "__main__":
    manager = Manager('192.168.0.111', 3234)
    manager.open_connection()
    print("")
    # manager_info = manager.get_manager_info()
    # client_list = manager.get_client_list()
    # plugin_list = manager.get_plugin_list()
    # server_list = manager.get_server_list()
    server = manager.get_server('002590A4C7A60000')
    print("")
    manager.close_connection()

    print('')
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
