import logging
import socket
import xml.etree.ElementTree as ET

import BackburnerDataClasses as BDC

class Monitor:
    """API class that emulates Backburner Monitor behaviour

    This class contains the API to interact with Backburner Manager instances by 
    establishing a connection and sending requests via TCP.

    Attributes:
        MANAGER_IP (str): Manager IP address
        MANAGER_PORT (int): Manager TCP port
        logging_level (int): Verbosity log level. Defaults to `logging.INFO`. Other options include `logging.DEBUG`. See documentation of Python module `logging` for more information. 

    """

    def __init__(self, _manager_ip, _manager_port, _debug = logging.INFO):
        """Creates an instance of the Manager class

        This class contains the API to interact with Backburner Manager instances by 
        establishing a connection and sending requests via TCP.

        Args:
            _manager_ip (str): Backburner Manager IP address
            _manager_port (:obj:`int`): Backburner Manager TCP port

        """
        self.MANAGER_IP = _manager_ip
        self.MANAGER_PORT = _manager_port
        self.logging_level = _debug

        logging.basicConfig(level = self.logging_level)

    def open_connection(self):
        """Open a connection with the Backburner Manager"""
        self.session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.session.connect((self.MANAGER_IP, self.MANAGER_PORT))

        # On opening connection, if received message is incorrect, close connection
        data = self.session.recv(29)
        logging.info(data.decode("utf-8"))
        if(data.decode("utf-8") != "250 backburner 1.0 Ready.\r\n"):
            self.close_connection()
        else:
            data = self.session.recv(11)
            logging.info(data.decode("utf-8"))

            if(data.decode("utf-8") != "backburner>"):
                self.close_connection()

    def close_connection(self):
        """Close connection with the Backburner Manager"""
        logging.info('Connection to manager closed')
        self.session.close()

    def _send_message(self, message):
        """Send a message to the Backburner Manager

        Args:
            message (str): Content of the message.

        Returns:
            Returns a three element tuple containing the response code (int), response message (str) and the requested data (bytes).

        """
        self.session.send(message)
 
        first_response = self.session.recv(32)

        logging.debug('First response:')
        logging.debug(str(first_response))

        # If the response code is 251, split the response message and get the message_length
        # TODO: Else does not seem tp work
        response_code = int(first_response.decode("utf-8").split(' ', 1)[0]) # Get the response code
        response_message = first_response.decode("utf-8").split(' ', 1)[1] # Get the response message 

        if int(response_code) == 251:
            msg_length = first_response.decode("utf-8").split()[1]

            requested_data = self.session.recv(int(msg_length))
            logging.debug('Requested data:')
            logging.debug(str(requested_data))
            # After all is sent, Manager will send one last packet containing 'backburner>'
            data = self.session.recv(11)
            logging.debug(data.decode("utf-8"))

            return (response_code, response_message, requested_data)
        else:
            # After all is sent, Manager will send one last packet containing 'backburner>'
            data = self.session.recv(11)
            logging.debug(data.decode("utf-8"))
            return (response_code, response_message, None)

    def _get_parsed_message(self, message):
        """Sends a message and parses the returned XML reply from Backburner Manager

        Args:
            message (str): Content of the message.

        Returns:
            Parsed XML reply as an XML Element Tree

        """
        raw_message = self._send_message(message)[2]
        logging.debug(str(raw_message.decode("utf-8")[:-1]))
        return ET.fromstring(raw_message.decode("utf-8")[:-1])

    def get_manager_info(self):
        """Retrieve information on the Backburner Manager

        Returns:
            A :obj:`BackburnerManagerInfo` data class object containing the Backburner Manager information

        """
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

    def get_client_list(self):
        """Retrieve the client list

        Returns:
            A :obj:`list` of :obj:`Client` data class objects for each client

        """
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
        """Retrieve the plug-in list

        Returns:
            A :obj:`list` of :obj:`Plugin` data class objects for each client

        """
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
        """Retrieve the server list

        Returns:
            A :obj:`list` of :obj:`ServerListItem` data class objects for each client

        """
        parsed = self._get_parsed_message(b'get srvlist\r\n')

        server_list = []

        for server in parsed:
            handle = str(server[0].text)
            state = int(server[1].text)
            name = str(server[2].text)

            server_data = BDC.ServerListItem(handle, state, name)
            server_list.append(server_data)
        
        return server_list

    def get_server(self, server_handle):
        """Retrieve information on a particular server

        Args:
            server_handle (str): The handle of the server. 

        Returns:
            A :obj:`Server` data class object containing information on the requested server

        """
        command = bytearray(b'get jobinfo ')
        command.extend(server_handle.encode('utf-8'))
        command.extend(b'\r\n')
        parsed = self._get_parsed_message(command)

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
            version = int(plugin[1].text)
            name = str(plugin[0].text)
            description = str(plugin[2].text)

            plugin_data = BDC.Plugin(version, name, description)
            plugin_list.append(plugin_data)
        
        server = BDC.Server(version, name, user_name, total_task, total_time, perf_index, ip_address, current_status, hw_info, net_status, server_schedule, att_priority, una_priority, current_job, current_task, task_started, plugin_list)

        return server

    def get_job_list(self):
        """Retrieve the server list

        Returns:
            A :obj:`list` of :obj:`JobListItem` data class objects for each client

        """
        parsed = self._get_parsed_message(b'get jobhlist\r\n')

        job_list = []

        for job in parsed:
            handle = int(job[0].text)
            state = int(job[1].text)

            job_data = BDC.JobListItem(handle, state)
            job_list.append(job_data)
        
        return job_list

    def get_job(self, job_handle):
        """Retrieve information on a particular job

        Args:
            job_handle (str): The handle of the server. You might find a hex value for this, convert this first to decimal value!

        Returns:
            A :obj:`Job` data class object containing information on the requested server

        """
        command = bytearray(b'get jobinfo ')
        command.extend(job_handle.encode('utf-8'))
        command.extend(b'\r\n')
        parsed = self._get_parsed_message(command)

        version = int(parsed[0][0].text)
        job_handle = int(parsed[0][1].text)
        name = str(parsed[0][2].text)
        description = str(parsed[0][3].text)
        job_priority = int(parsed[0][4].text)
        user = str(parsed[0][5].text)
        computer = str(parsed[0][6].text)
        last_updated = str(parsed[0][7].text)
        submitted = str(parsed[0][8].text)
        started = str(parsed[0][9].text)
        ended = str(parsed[0][10].text)
        number_tasks = int(parsed[0][11].text)
        tasks_completed = int(parsed[0][12].text)
        encoding = str(parsed[0][13].text)
        job_info = BDC.JobInfo(version, job_handle, name, description, job_priority, user, computer, last_updated, submitted, started, ended, number_tasks, tasks_completed, encoding)

        active = False
        if str(parsed[1][0].text) == 'Yes':
            active == True
        complete = False
        if str(parsed[1][1].text) == 'Yes':
            complete == True
        nonconcurrent = False
        if str(parsed[1][2].text) == 'Yes':
            nonconcurrent == True
        nonstoppable = False
        if str(parsed[1][3].text) == 'Yes':
            nonstoppable == True
        ignore_job_share = False
        if str(parsed[1][4].text) == 'Yes':
            ignore_job_share == True
        job_has_dependencies = False
        if str(parsed[1][5].text) == 'Yes':
            job_has_dependencies == True
        zip_archive = False
        if str(parsed[1][6].text) == 'Yes':
            zip_archive == True
        leave_in_queue = False
        if str(parsed[1][7].text) == 'Yes':
            leave_in_queue == True
        archive_when_done = False
        if str(parsed[1][8].text) == 'Yes':
            archive_when_done == True
        delete_when_done = False
        if str(parsed[1][9].text) == 'Yes':
            delete_when_done == True
        override_blocking_tasks = False
        if str(parsed[1][10].text) == 'Yes':
            override_blocking_tasks == True
        enable_blocking_tasks = False
        if str(parsed[1][11].text) == 'Yes':
            enable_blocking_tasks == True
        job_flags = BDC.JobFlags(active, complete, nonconcurrent, nonstoppable, ignore_job_share, job_has_dependencies, zip_archive, leave_in_queue, archive_when_done, delete_when_done, override_blocking_tasks, enable_blocking_tasks)

        plugin_name = str(parsed[3][0].text)
        plugin_version = int(parsed[3][1].text)
        job_plugin = BDC.JobPlugin(plugin_name, plugin_version)

        enabled = False
        if int(parsed[4][0].text) == 1:
            enable_blocking_tasks == True
        failure = False
        if str(parsed[4][1].text) == 'Yes':
            failure == True
        progress = False
        if str(parsed[4][2].text) == 'Yes':
            progress == True
        completion = False
        if str(parsed[4][3].text) == 'Yes':
            completion == True
        nth_task = int(parsed[4][4].text)
        send_email = False
        if str(parsed[4][5].text) == 'Yes':
            send_email == True
        include_summary = False
        if str(parsed[4][6].text) == 'Yes':
            include_summary == True
        email_from = str(parsed[4][7].text)
        email_to = str(parsed[4][8].text)
        email_server = str(parsed[4][9].text)
        job_alerts = BDC.JobAlerts(enabled, failure, progress, completion, nth_task, send_email, include_summary, email_from, email_to, email_server)

        job_server_list = []
        for server in parsed[5]:
            handle = str(server[0].text)
            active = False
            if str(server[1].text) == 'Yes':
                active == True
            task_time = float(server[2].text)
            task_total = int(server[3].text)
            context_switch = int(server[4].text)
            rt_failed = False
            if str(server[5].text) == "Yes":
                rt_failed = True
            job_server = BDC.JobServer(handle, active, task_time, task_total, context_switch, rt_failed)
            job_server_list.append(job_server)

        job = BDC.Job(job_info, job_flags, job_plugin, job_alerts, job_server_list)
        return job    
