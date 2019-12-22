# BackburnerPy

BackburnerPy is an unofficial Python API for Autodesk Backburner. It provides a programming interface with the Autodesk Backburner ecosphere. This can for example be utilised to create a dashboard webpage displaying the status of your renders and your renderfarm. 

## Installation

### Requirements

  * Python 3.7+

To install this to your project, download this repository and add the path of the BackburnerPy folder to your Python Path.

In the future, this project might be available on PyPi.

## Usage

Import BackburnerPy and create a Monitor instance. This class emulates Backburner Monitor's behaviour. Open a connection to the Backburner Manager and send commands to establish communications and when finished, close the connection:

`get_manager_information.py` provides an example of the process:

```Python
import sys
import os

sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'BackburnerPy'))

from Monitor import Monitor

# Assign IP and Port from command line arguments
MANAGER_IP = str(sys.argv[1])
MANAGER_PORT = int(sys.argv[2])

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
```

## Documentation

Documentation is available here: https://fragrag.github.io/BackburnerPy/

## Disclaimer

This project is not affiliated with Autodesk. BackburnerPy is provided "as is" without warranty of any kind, either express or implied. Use at your own risk.
