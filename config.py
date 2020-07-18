### Use this file to configure access to DNAC
### Replace all values below with your production DNAC
### Provided is DNAC sandbox login

DNAC_FQDN = 'sandboxdnac.cisco.com'
DNAC_PORT = '443'
DNAC_USER = 'devnetuser'
DNAC_PASSWORD = 'Cisco123!'

### SCOPE of devices thi script is going to manipulate, this need to be the same as "Series" field of the device
SCOPE = ["Cisco Catalyst 9300 Series Switches", "Cisco Catalyst 9200 Series Switches"]

### Domain that all devices belong to, for example ".cisco.com", the hostname of the device would be "device.cisco.com"
DOMAIN = ".abc.inc"