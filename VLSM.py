from GetNetHost import NetHostId

class VariableLengthSubnetMask(NetHostId):
    def __init__(self, ip_address, default_subnet_mask, number_of_users_list):
        super().__init__(ip_address, default_subnet_mask)
        #self.ip = ip_address
        self.default_network_address = ''
        self.number_of_users_list = number_of_users_list
        #self.default_subnet_mask = default_subnet_mask
        self.subnet_significant_byte = None
    
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
