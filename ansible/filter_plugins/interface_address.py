try:
    from jinja2 import pass_context
except ImportError:
    from jinja2.filters import contextfilter as pass_context

from ansible.errors import AnsibleFilterError


ANY_ADDRESS_MAPPING = {
    '4': '0.0.0.0',
    '6': '::1'
}


@pass_context
def interface_address(context,
                      interface,
                      ip_version='4',
                      hostname=None,
                      *args,
                      **kwargs):
    address = ''

    ip_version = str(ip_version)

    if interface == 'any':
        return ANY_ADDRESS_MAPPING[ip_version]

    if hostname is None:
        hostname = context.get('inventory_hostname')

    vars_ = context.get('hostvars').get(hostname)

    interfaces = vars_['ansible_interfaces']

    if interface not in interfaces:
        raise AnsibleFilterError("Can not found interface: %s" % interface)

    if ip_version == '4':
        address = vars_['ansible_' + interface]['ipv4']['address']
    elif ip_version == '6':
        addresses = vars_['ansible_'+interface]['ipv6']
        global_addresses = [address for address in addresses
                            if address['scope'] == 'global'
                            and address['prefix'] != '128']
        if global_addresses:
            address = global_addresses[0]['address']
    else:
        raise AnsibleFilterError('Unknow ip_version parameter: %s' %
                                 ip_version)
    if not address:
        raise AnsibleFilterError(
            "Can not found ipv%s address for interface: %s" %
            (ip_version, interface))

    return address


class FilterModule(object):
    def filters(self):
        return {
            'address': interface_address
        }
