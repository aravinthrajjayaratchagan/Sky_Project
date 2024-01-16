from flask import Flask, request, jsonify
from ncclient import manager
from ncclient.operations import RPCError

app = Flask(__name__)

DEVICE_IP = 'sandbox-iosxr-1.cisco.com'
DEVICE_PORT = 830
USERNAME = 'admin'
PASSWORD = 'C1sco12345'

def configure_loopback(interface_name, ip_address):
    netconf_payload = f"""
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>{interface_name}</name>
                <description>Loopback Interface</description>
                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
                    ianaift:softwareLoopback
                </type>
                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                    <address>
                        <ip>{ip_address}</ip>
                        <netmask>255.255.255.255</netmask>
                    </address>
                </ipv4>
            </interface>
        </interfaces>
    </config>
    """
    return netconf_payload

def delete_loopback(interface_name):
    netconf_payload = f"""
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface operation="delete">
                <name>{interface_name}</name>
            </interface>
        </interfaces>
    </config>
    """
    return netconf_payload

@app.route('/configure-loopback', methods=['POST'])
def configure_loopback_endpoint():
    data = request.get_json()
    interface_name = data.get('interface_name')
    ip_address = data.get('ip_address')

    with manager.connect(
        host=DEVICE_IP,
        port=DEVICE_PORT,
        username=USERNAME,
        password=PASSWORD,
        hostkey_verify=False,
        device_params={'name': 'iosxe'}
    ) as m:
        try:
            payload = configure_loopback(interface_name, ip_address)
            m.edit_config(target='running', config=payload)
            response = {'message': 'Loopback configured successfully'}
        except RPCError as e:
            response = {'error': f'Failed to configure loopback. RPCError: {str(e)}'}

    return jsonify(response)

@app.route('/delete-loopback', methods=['DELETE'])
def delete_loopback_endpoint():
    data = request.get_json()
    interface_name = data.get('interface_name')

    with manager.connect(
        host=DEVICE_IP,
        port=DEVICE_PORT,
        username=USERNAME,
        password=PASSWORD,
        hostkey_verify=False,
        device_params={'name': 'iosxe'}
    ) as m:
        try:
            payload = delete_loopback(interface_name)
            m.edit_config(target='running', config=payload)
            response = {'message': 'Loopback deleted successfully'}
        except RPCError as e:
            response = {'error': f'Failed to delete loopback. RPCError: {str(e)}'}

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
