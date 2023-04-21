import sys

from get_net_host_id import NetHostId


class VariableLengthSubnetMask(NetHostId):
    def __init__(self, ip_address, default_subnet_mask, number_of_users_list):
        super().__init__(ip_address, default_subnet_mask)
        self.default_network_address = ''
        self.number_of_users_list = number_of_users_list
        self.subnet_significant_byte = None
        #self.total_number_of_hosts_required = 0
    
    def get_new_subnet_mask(self, subnet):
        x = 1
        while 2 ** x < (self.number_of_users_list[subnet]):
            x = x + 1
        self.default_subnet_mask = 32 - x
        if subnet == 0:
            self.ip_cidr = self.ip + '/' + str(self.default_subnet_mask)
    
    def get_new_default_network_address(self):
        broadcast_address_significant_byte = int(self.broadcast_address.split(self.ip_separator)[self.subnet_significant_byte])
        network_address = self.network_address.split(self.ip_separator)
        
        if self.subnet_significant_byte <= 3 and broadcast_address_significant_byte < 255:
            network_address[self.subnet_significant_byte] = str(broadcast_address_significant_byte + 1)
            network_address_significant_byte = -1
            while network_address_significant_byte < broadcast_address_significant_byte:
                network_address[self.subnet_significant_byte] = str(broadcast_address_significant_byte + 1)
                self.ip = self.ip_separator.join(network_address)
                n_a, *_ = self.get_network_broadcast_first_last_addresses()
                network_address_significant_byte = n_a[self.subnet_significant_byte]

        elif self.subnet_significant_byte == 3 and broadcast_address_significant_byte == 255:
            network_address[self.subnet_significant_byte-1] = str(int(network_address[self.subnet_significant_byte-1]) + 1)
            self.ip = self.ip_separator.join(network_address)
        self.ip_cidr = self.ip + '/' + str(self.default_subnet_mask)
        self.machines = 2 ** (32 - self.default_subnet_mask) - 2

    def check_number_of_available_hosts(self):
        # Check if the subnet can be divided between the number of hosts specified by the user
        specified_hosts = 0
        x = 1
        for users in self.number_of_users_list:
            while x * 2 < users:
                x *= 2
            specified_hosts += x*2
            x = 1
        if specified_hosts > self.hosts:
            #self.total_number_of_hosts_required = specified_hosts
            return True
        
    def get_vlsm(self, number_of_subnets):
        number_of_subnets
        for subnet_number in range(number_of_subnets):
            display_header = "SUBNET - " + str(self.number_of_users_list[subnet_number])
            if subnet_number == 0:
                self.get_new_subnet_mask(subnet_number)
            self.subnet_significant_byte = self.default_subnet_mask // 8
            n_a, b_a, f_a, l_a = self.get_network_broadcast_first_last_addresses()
            self.set_network_broadcast_first_last_addresses(n_a, b_a, f_a, l_a)
            self.hosts = 2**(32-self.default_subnet_mask)-2
            self.display_network_info(display_header)
            if subnet_number < number_of_subnets-1:
                self.get_new_subnet_mask(subnet_number + 1)
                self.get_new_default_network_address()
