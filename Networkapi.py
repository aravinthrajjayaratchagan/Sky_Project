from ncclient import manager

netconf_params = {
    'host': 'sandbox-iosxr-1.cisco.com',
    'port': 830,
    'username': 'admin',
    'password': 'C1sco12345',
    'hostkey_verify': False,
    'device_params': {'name': 'csr'}
}


with manager.connect(**netconf_params) as rtr_mgr:
    schema = rtr_mgr.get_schema('ietf-interfaces')
    print(schema)


