from GetNetHost import *
class FixedLengthSubnetMask(NetHostId):
    def __init__(self, ip_address, subnet_mask, number_of_subnets):
        super().__init__(ip_address, subnet_mask)
        self.number_of_subnets = number_of_subnets
        self.new_subnet_mask = 0
        self.bits_borrowed_from_host_id = 0
        self.net_id_combinations_list = list()
        self.default_network_address = ''

    def set_new_subnet_mask(self):
        x = 1
        while 2 ** x <= (2 + self.number_of_subnets):
            x = x + 1
        self.bits_borrowed_from_host_id = x
        self.new_subnet_mask = self.default_subnet_mask + self.bits_borrowed_from_host_id
        if self.new_subnet_mask > 32 :
            raise Exception('|>The network specified cannot be divided into ', self.number_of_subnets, 'sub networks.\n\
            This error occured because the subnet is small!\nModify it and retry!')
        print("|>The new mask is : ", self.new_subnet_mask)
    
    def set_net_id_combinations(self):
        bits_list = [128, 64, 32, 16, 8, 4, 2 , 1]
        net_id_combo_list = list()
        bits_set_combination = list()
        bits_set_length = self.bits_borrowed_from_host_id 
        combo = 0
        total_number_of_combinations = 2 ** self.bits_borrowed_from_host_id

        if self.new_subnet_mask % 8 == 0 :
            net_id_bits = bits_list[-self.bits_borrowed_from_host_id:]
        else:
            net_id_bits = bits_list[:self.bits_borrowed_from_host_id]

        for combo in range(total_number_of_combinations):
            combo_binary_format = bin(combo)[2:]
            while len(combo_binary_format) < self.bits_borrowed_from_host_id:
                combo_binary_format = '0' + combo_binary_format 
            bits_set_combination.append(combo_binary_format)
        
        for bit_set in bits_set_combination:
            combo_value = bit_set_index = 0
            while bit_set_index < bits_set_length:
                combo_value += int(bit_set[bit_set_index]) * net_id_bits[bit_set_index]
                bit_set_index += 1
            net_id_combo_list.append(combo_value)
                    
        self.net_id_combo_list = net_id_combo_list.copy()
        print("|>The net_id_combo_list is : ", self.net_id_combo_list)
    
    def set_subnet_network_broadcast_address(self, net_combo_id): 
        net_index = self.new_subnet_mask // 8
        if self.new_subnet_mask % 8  == 0:
            sub_network_address = [self.default_network_address[i] for i in range(0, net_index-1)]
            #broadcast_address = network_address.copy()
            net_id = str(int(self.default_network_address[net_index-1]) + self.net_id_combo_list[net_combo_id])
        else:
            sub_network_address = [self.default_network_address[i] for i in range(0, net_index)]
            net_id = str(int(self.default_network_address[net_index]) + self.net_id_combo_list[net_combo_id])
            net_index = net_index + 1
        sub_network_address.append(net_id)
        for i in range(net_index, len(self.default_network_address)):
            sub_network_address.append('0')
        self.ip = '.'.join(sub_network_address) if self.ip_separator == '\.' else '-'.join(sub_network_address)
        self.default_subnet_mask = self.new_subnet_mask
        self.ip_cidr = self.ip + '/' + str(self.default_subnet_mask)
        return self.get_network_broadcast_first_last_addresses()
