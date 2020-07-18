# DNAC-DNS-Automation
Automatically update device management from IP to DNS

This script is made for situations where DNAC users cannot rely on IP address to identify and manage devices, and need a dynamic, automated, and human friendly way to name and manage devices.

# How it works
1. DNAC generate a DNS name for the device through Day 0 template and provision/onboard the device
2. Device boots and register DNS name automatically
3. Run this script to update DNAC to manage these devices with DNS name instead of IP
This script can also be run priodically to scan for new device onboarded and update their device information automatically

# How to use
1. Configuration file
   Update "Config.py" with information of your environment. Wha'ts currently provided was DNAC Sandbox.
   You can use this for test but you wouldn't be able to make changes.
   When you run the script you will get a HTTP 403 code becuase you won't have access to make change on Sandbox.
   
   ### Use this file to configure access to DNAC
   ### Replace all values below with your production DNAC
   ### Provided is DNAC sandbox login

   DNAC_FQDN = 'sandboxdnac.cisco.com'
   DNAC_PORT = '443'
   DNAC_USER = 'devnetuser'
   DNAC_PASSWORD = 'Cisco123!'

   ### SCOPE of devices thi script is going to manipulate, this need to be the same as "Series" field of the device
   SCOPE = ["Cisco Catalyst 9300 Series Switches", "Cisco Catalyst 9200 Series Switches"]

   ### Optoinal - Domain that all devices belong to, for example ".cisco.com", the hostname of the device would be "device.cisco.com"
   DOMAIN = ".abc.inc"
   
2. Make sure you have all 3 files
   - config.py - stores configuration as described in # How to use item 1
   - util.py - functions needed to run the script
   - main.py - main script
   
3. Run "main.py"

   - Expected results
   ### If "No" is chosen update operations will be canceled
    Parsing device list...
    Found new device, collecting information...
    Found new device, collecting information...
    ================================================================================
    Parsing complete, here is a list of devices that needs updated, please confirm...       
    ================================================================================
    10.10.22.66:    Cisco Catalyst 9300 Series Switches
    10.10.22.70:    Cisco Catalyst 9300 Series Switches
    Confirm to update devices [Y/N]? n
    ================================================================================
    Task canceled, exiting...
    ================================================================================
   
   ### If "Yes" is chosen update operations proceed and devices will be updated
    Parsing device list...
    Parsing device list...
    Found new device, collecting information...
    Found new device, collecting information...
    ================================================================================
    Parsing complete, here is a list of devices that needs updated, please confirm...
    ================================================================================
    10.10.22.66:    Cisco Catalyst 9300 Series Switches
    10.10.22.70:    Cisco Catalyst 9300 Series Switches
    Confirm to update devices [Y/N]? y
    Confirmed, updating devices...
    ================================================================================
    Task completed, exiting...
    ================================================================================
   
   ### If you're using the sandbox or don't have access to make changes, the following error will be seen
    Parsing device list...
    Found new device, collecting information...
    Found new device, collecting information...
    ================================================================================
    Parsing complete, here is a list of devices that needs updated, please confirm...
    ================================================================================
    10.10.22.66:    Cisco Catalyst 9300 Series Switches
    10.10.22.70:    Cisco Catalyst 9300 Series Switches
    Confirm to update devices [Y/N]? y
    Confirmed, updating devices...
    ================================================================================
    Unauthorized to make a change! Existing...
    ================================================================================
    Operation failed, exiting...
    ================================================================================
    Unauthorized to make a change! Existing...
    ================================================================================
    Operation failed, exiting...
    ================================================================================
    Task completed, exiting...
    ================================================================================
    
Thank you. If there's any issue please feel free to contact the author.
