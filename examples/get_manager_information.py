import sys
import os

sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'BackburnerPy'))

from Monitor import Monitor

# Assign IP and Port from command line arguments
try:
    MANAGER_IP = str(sys.argv[1])
    MANAGER_PORT = int(sys.argv[2])
except:
    print("Incorrect arguments.")

# Initialise Monitor object
monitor = Monitor(MANAGER_IP, MANAGER_PORT)

# Open connection to the Manager
monitor.open_connection()

# Request Manager info. This returns a `BackburnerPy.BackburnerDataClasses.BackburnerManagerInfo` object
manager_info = monitor.get_manager_info()

# Print the Manager's computer name
print(manager_info.system_info.computer_name)

# Close connection
monitor.close_connection()