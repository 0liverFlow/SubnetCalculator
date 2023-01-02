from GetNetHost import NetHostId
class FixedLengthSubnetMask(NetHostId):
    def __init__(self, ip_address, default_subnet_mask, number_of_subnets):
        super().__init__(ip_address, default_subnet_mask)
        self.number_of_subnets = number_of_subnets
        self.new_subnet_mask = 0
        self.bits_borrowed_from_host_id = 0
        self.net_id_combinations_list = list()
        self.default_network_address = ''
        self.default_subnet_mask_significant_byte = 0
        self.new_subnet_mask_significant_byte = 0


    def set_new_subnet_mask(self) -> None:
        x = 1
        #while 2 ** x < (2+self.number_of_subnets)
        while 2 ** x < (self.number_of_subnets):
            x = x + 1
        self.bits_borrowed_from_host_id = x
        self.new_subnet_mask = self.default_subnet_mask + self.bits_borrowed_from_host_id
        if self.new_subnet_mask > 30 :
            raise Exception(f"""|The network specified cannot be divided into {self.number_of_subnets} sub networks.
            This error occured because the subnet is too small!\nChange it, then retry!""")
        self.hosts = 2**(32-self.new_subnet_mask)-2
    
    def set_net_id_combinations(self):
        bits_list = [128, 64, 32, 16, 8, 4, 2 , 1]
        ip_bytes = [8, 16, 24, 32]
        found_default_subnet_significant_byte = found_new_subnet_mask_significant_byte = False
        bits_set_combination = list()
        combination = index = 0
        total_number_of_combinations = 2**self.bits_borrowed_from_host_id
        #Get default_subnet_mask and new_subnet_mask significant byte
        while not(found_default_subnet_significant_byte and found_new_subnet_mask_significant_byte):
            if (ip_bytes[index] - self.default_subnet_mask) >= 0:
                if not found_default_subnet_significant_byte:
                    self.default_subnet_mask_significant_byte = index
                    found_default_subnet_significant_byte = True
                if (ip_bytes[index] - self.new_subnet_mask) >= 0 and not found_new_subnet_mask_significant_byte:
                    self.new_subnet_mask_significant_byte = index
                    found_new_subnet_mask_significant_byte = True
            index += 1
        #Get the network combinations list
        #for combination in range(1, total_number_of_combinations-1): #remove first and last address 'cause they are reserved
        for combination in range(total_number_of_combinations):
            combination_binary_format = bin(combination)[2:] #remove 0b
            while len(combination_binary_format) < self.bits_borrowed_from_host_id:
                combination_binary_format = combination_binary_format.zfill(self.bits_borrowed_from_host_id)
                #combination_binary_format = '0' + combination_binary_format
            bits_set_combination.append(combination_binary_format) #bits_set_combination --> '0001' '0111' '0010' '1111'
        
        if self.new_subnet_mask_significant_byte == self.default_subnet_mask_significant_byte:
            network_host_significant_bits = 8 - ((self.default_subnet_mask_significant_byte + 1) * 8 - self.default_subnet_mask)
            net_id_bits = bits_list[network_host_significant_bits : network_host_significant_bits + self.bits_borrowed_from_host_id] #[8,4,2,1]
            for bits_set in bits_set_combination:
                combo_value = bit_index = 0
                while bit_index < self.bits_borrowed_from_host_id:
                    combo_value += int(bits_set[bit_index]) * net_id_bits[bit_index]
                    bit_index += 1
                self.net_id_combinations_list.append(combo_value)
        else:
            first_network_host_significant_bits = 8 - ((self.default_subnet_mask_significant_byte + 1) * 8 - self.default_subnet_mask)
            second_network_host_significant_bits = 8 - ((self.new_subnet_mask_significant_byte + 1) * 8 - self.new_subnet_mask)
            first_net_id_bits = bits_list[first_network_host_significant_bits:8]
            last_net_id_bits = bits_list[:second_network_host_significant_bits]
            match self.new_subnet_mask_significant_byte - self.default_subnet_mask_significant_byte:
                case 1:
                    for bits_set in bits_set_combination:
                        combo_value1 = combo_value2 = bit_index = bit_index2 = 0
                        while bit_index < self.bits_borrowed_from_host_id:
                            if bit_index < len(first_net_id_bits):
                                combo_value1 += int(bits_set[bit_index]) * first_net_id_bits[bit_index]
                            else:
                                combo_value2 += int(bits_set[bit_index]) * last_net_id_bits[bit_index2]
                                bit_index2 += 1
                            bit_index += 1
                        self.net_id_combinations_list.append((combo_value1, combo_value2))
                case 2:
                    for bits_set in bits_set_combination:
                        combo_value1 = combo_value2 = combo_value3 = bit_index = bit_index2 = bit_index3 = 0
                        while bit_index < self.bits_borrowed_from_host_id:
                            if bit_index < len(first_net_id_bits):
                                combo_value1 += int(bits_set[bit_index]) * first_net_id_bits[bit_index]
                            elif bit_index < self.bits_borrowed_from_host_id - len(last_net_id_bits):
                                    combo_value2 += int(bits_set[bit_index]) * bits_list[bit_index2]
                                    bit_index2 += 1
                            else: 
                                combo_value3 += int(bits_set[bit_index]) * last_net_id_bits[bit_index3]
                                bit_index3 += 1
                            bit_index += 1
                        self.net_id_combinations_list.append((combo_value1, combo_value2, combo_value3))
                case 3:
                    for bits_set in bits_set_combination:
                        combo_value1 = combo_value2 = combo_value3 = combo_value4 = bit_index = bit_index2 = bit_index3 = bit_index4 = 0
                        while bit_index < self.bits_borrowed_from_host_id:
                            if bit_index < len(first_net_id_bits):
                                combo_value1 += int(bits_set[bit_index]) * first_net_id_bits[bit_index]
                            elif bit_index <= 16:
                                    combo_value2 += int(bits_set[bit_index]) * bits_list[bit_index2]
                                    bit_index2 += 1
                            elif bit_index <= 24:
                                combo_value3 += int(bits_set[bit_index]) * bits_list[bit_index3]
                                bit_index3 += 1                                
                            else: 
                                combo_value4 += int(bits_set[bit_index]) * last_net_id_bits[bit_index4]
                                bit_index4 += 1
                            bit_index += 1
                        self.net_id_combinations_list.append((combo_value1, combo_value2, combo_value3, combo_value4))

    def set_subnet_network_broadcast_address(self, net_combo_id):
        sub_network = [self.default_network_address[i] for i in range(0, self.default_subnet_mask_significant_byte)]
        if self.default_subnet_mask_significant_byte == self.new_subnet_mask_significant_byte:
            sub_network.append(str(int(self.default_network_address[self.default_subnet_mask_significant_byte]) + self.net_id_combinations_list[net_combo_id]))
        else:
            match self.new_subnet_mask_significant_byte - self.default_subnet_mask_significant_byte:
                case 1:
                    sub_network.append(str(int(self.default_network_address[self.default_subnet_mask_significant_byte]) + self.net_id_combinations_list[net_combo_id][0]))
                    sub_network.append(str(int(self.default_network_address[self.new_subnet_mask_significant_byte]) + self.net_id_combinations_list[net_combo_id][-1]))
                case 2:
                    sub_network.append(str(int(self.default_network_address[self.default_subnet_mask_significant_byte]) + self.net_id_combinations_list[net_combo_id][0]))
                    sub_network.append(str(int(self.default_network_address[self.default_subnet_mask_significant_byte + 1]) + self.net_id_combinations_list[net_combo_id][1]))
                    sub_network.append(str(int(self.default_network_address[self.new_subnet_mask_significant_byte]) + self.net_id_combinations_list[net_combo_id][-1]))
                case 3:
                    sub_network.append(str(int(self.default_network_address[self.default_subnet_mask_significant_byte]) + self.net_id_combinations_list[net_combo_id][0]))
                    sub_network.append(str(int(self.default_network_address[self.default_subnet_mask_significant_byte + 1]) + self.net_id_combinations_list[net_combo_id][1]))
                    sub_network.append(str(int(self.default_network_address[self.default_subnet_mask_significant_byte + 2]) + self.net_id_combinations_list[net_combo_id][2]))
                    sub_network.append(str(int(self.default_network_address[self.new_subnet_mask_significant_byte]) + self.net_id_combinations_list[net_combo_id][-1]))
        
        index = self.new_subnet_mask_significant_byte + 1
        while index < 4:
            sub_network.append('0')
            index += 1 
        self.ip = self.ip_separator.join(sub_network)
        self.default_subnet_mask = self.new_subnet_mask
        self.ip_cidr = self.ip + '/' + str(self.default_subnet_mask)
        return self.get_network_broadcast_first_last_addresses()
