# vmware-deploy (WIP)
Script for deploying a VM from a template using VMWare pyvmomi connected to VMWare vSphere. 

The deployed VM will have the specs assigned to it, will be set up to RDP or SSH to it, and have a randomized Admin 
password (spat out by the script).

## TODO:

1. ~~block out basic structure~~
1. ~~vsphere connectivity~~
1. ~~template cloning~~
1. ~~vm configuration~~
1. ~~vm power on~~
1. console connection to the guest OS (WIP) 
1. guest OS configuration

## Supports
1. Windows 2012, 2016 and CentOS 7 deploys
1. VMWare vSphere 6.5

# Requirements

Python3 virtualenv with requirements installed from the provided requirements.txt file.

You'll also need to copy the sample.secret.py file to secret.py, and fill in the connection info for your VMWare 
vSphere.

# Usage
Copy the sample.input.py file to input.py and fill in the details for the template you want to clone and the VM you want 
to create from it.

# Customising
This script is meant to be integrated into your own projects, so the input is strictly segregated from the output. 

# Credits
Much of the code for interacting with VMWare is borrowed and modified from snippets in the pyvmomi community samples: 
https://github.com/vmware/pyvmomi-community-samples

Additionally, this is based on some work undertaken by myself and a former colleague: https://github.com/inuwashi
