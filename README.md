# vmware-deploy
Script for deploying a VM from a template using VMWare pyvmomi connected to VMWare vSphere. 

The deployed VM will have the specs assigned to it, will be set up to RDP or SSH to it, and have a randomized Admin 
password (spat out by the script).

## Supports
1. Windows 2012, 2016 and CentOS 7 deploys
2. VMWare vSphere 6.5

# Requirements

Python3 virtualenv with requirements installed from the provided requirements.txt file.

You'll also need to copy the sample.secret.py file to secret.py, and fill in the connection info for your VMWare 
vSphere.

# Usage
Copy the sample.input.py file to input.py and fill in the details for the template you want to clone and the VM you want 
to create from it.

# Customising
This script is meant to be integrated into your own projects, so the input is strictly segregated from the output. 

