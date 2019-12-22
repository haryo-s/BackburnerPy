# BackburnerPy

BackburnerPy is an unofficial Python API for Autodesk Backburner. It provides a programming interface with the Autodesk Backburner ecosphere. This can for example be utilised to create a dashboard webpage displaying the status of your renders and your renderfarm. 

## Installation

### Requirements

  * Python 3.7+

To install this to your project, download this repository and add the path of the BackburnerPy folder to your Python Path.

In the future, this project might be available on PyPi.

## Usage

Import BackburnerPy and create a Monitor instance. This class emulates Backburner Monitor's behaviour. Open a connection to the Backburner Manager and send commands to establish communications and when finished, close the connection, as illustrated in the following example:

The example `get_manager_information.py` illustrates the process well:


```> python3 get_manager_information.py localhost 3234```

```Python
import sys

import BackburnerPy

# Assign IP and Port from command line arguments
MANAGER_IP = sys.argv[1]
MANAGER_PORT = sys.argv[2]

# Initialise Monitor object
monitor = BackburnerPy.Monitor(MANAGER_IP, MANAGER_PORT)

# Open connection to the Manager
monitor.open_connection()

# Request Manager info. This returns a BackburnerDataClasses.BackburnerManagerInfo object
manager_info = monitor.get_manager_info()

# Print the Manager's computer name
print(manager_info.system_info.computer_name)

# Close connection
monitor.close_connection()
```

## Documentation

Documentation is available here: https://fragrag.github.io/BackburnerPy/