import math
import re
class NetHostId():
    def __init__(self, ip, subnet_mask):
        self.ip = ip
        self.default_subnet_mask = int(subnet_mask.replace('/', ''))
        self.ip_separator = ''
        self.ip_cidr = self.ip + '/' + str(self.default_subnet_mask)
        self.network_address = ''
        self.first_address = ''
        self.last_address = ''
        self. broadcast_address = ''
        self.machines = int(math.pow(2, (32 - self.default_subnet_mask)) - 2)

    @classmethod
    def warning(cls):
        print("\nBefore using this program, thanks in advance to respect the following rules:\n\
        1.This program works only for IPv4 addresses, not IPv6 so far.\n\
        2.The format of an IP address must be as follows : x.x.x.x or x-x-x-x\n\
        with x between 0 and 255.\n\
        3.The ip address's separator must be a dot(.) or a dash(-)\n\
        4.The subnet mask must be given in CIDR notation /x or in decimal(without /) with x between 1 and 31\n\
        Thank you very much for taking the information above into consideration.\n\
        Hope you're gonna enjoy subnet_calculator :)\n")

    @staticmethod
    def double_letter_converter(string):
        letters = "𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ"
        numbers = "𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡"
        string = string.strip().upper()
        double_string = ''
        for char in string:
            if char in [' ', '-', '°']:
                double_string = double_string + char
            else:
                char_dec = ord(char)
                if 48 <= char_dec <= 57:
                    double_string = double_string + numbers[char_dec - 48]
                elif char_dec < 65 or char_dec > 90:
                    continue 
                else:
                    double_string = double_string + letters[char_dec - 65] + ' '
        return double_string

    @staticmethod
    def ascii_design(char, char_length, started_char='+', ended_char='+'):
        print(started_char,end='')
        for i in range(char_length):
            print(char,end='')
        print(ended_char)
    
    @staticmethod
    def convert_int_list_to_string(*ip_addresses):
        ips_str_format_list = list()
        for ip_address in ip_addresses:
            ips_str_format_list.append([str(byte) for byte in ip_address])
        return tuple(ips_str_format_list)
    
    def check_subnet_mask_validity(self):
        if self.default_subnet_mask > 0 and self.default_subnet_mask < 32:
            return True
        else:
            print("|>The subnet mask specified is incorrect.\n\
                The subnet mask should be between 1 and 31")
            return False

    def check_ip_validity(self):
        #Check the ip address format
        ip_regex = r'^\d{,3}[.-]\d{,3}[-.]\d{,3}[.-]\d{,3}$'
        if re.search(ip_regex, self.ip) == None:
            print("|>Error : Incorrect IP address format\n\
            The format must be : x.x.x.x or x-x-x-x\n\
            Try again please.")
            return False

        #Get the ip address's separator
        self.ip_separator = '\.' if self.ip.find('.') != -1 else '-'

        #Check if the ip address' values(bytes) are correct.
        ip_bytes = [int(byte) for byte in re.split(self.ip_separator, self.ip)]
        for byte in ip_bytes:
            if byte < 0 or byte > 255:
                print("|>Incorrect IP address 0_0 :\n\
                    Knowing that a byte is a set of 8 bits, its value should be between 0 and 255.\n\
                    Please, check your ip, then try again!")
                return False
            else:
                return True
    
    def display_network_info(self, header):
        self.ascii_design('-',71)
        print("|",self.double_letter_converter(header).center(72),"\t\t\t|")
        self.ascii_design('-',71)
        print("|CIDR notation      : ", self.ip_cidr, " \t\t\t\t\t|")
        self.ascii_design('-',71)
        print("|Network address    : ", self.network_address.replace('\\', ''), " \t\t\t\t\t|")
        self.ascii_design('-',71)
        print("|First ip address   : ", self.first_address.replace('\\', ''), " \t\t\t\t\t|")
        self.ascii_design('-',71)
        print("|Last ip address    : ", self.last_address.replace('\\', ''), " \t\t\t\t\t|")
        self.ascii_design('-',71)
        print("|Broadcast address  : ", self.broadcast_address.replace('\\', ''), " \t\t\t\t\t|")
        self.ascii_design('-',71)
        print("|Number of machines : ", self.machines, "\t\t\t\t\t\t|")
        self.ascii_design('-',71)

    def get_significant_ip_subnet_mask_byte(self, ip_address, net_index):
        bits_list = [128, 192, 224, 240, 248, 252, 254]
        network_address = list()
        broadcast_address = list()
        subnet_mask_significant_byte = 0
        if self.default_subnet_mask < 8:
            subnet_mask_significant_byte = bits_list[self.default_subnet_mask-1]
        elif self.default_subnet_mask < 16: 
            subnet_mask = self.default_subnet_mask - 8
            subnet_mask_significant_byte = bits_list[subnet_mask-1]
        elif self.default_subnet_mask < 24: 
            subnet_mask = self.default_subnet_mask - 16
            subnet_mask_significant_byte = bits_list[subnet_mask-1]
        elif self.default_subnet_mask < 32: 
            subnet_mask = self.default_subnet_mask - 24
            subnet_mask_significant_byte = bits_list[subnet_mask-1]
        magical_number = 256 - subnet_mask_significant_byte
        k = 0
        magical_number_multiple = magical_number * k
        ip_significant_byte = int(ip_address[net_index])
        
        while magical_number_multiple <= ip_significant_byte:
            k = k + 1
            magical_number_multiple = magical_number * k
        magical_number_multiple_next = magical_number_multiple
        magical_number_multiple = magical_number_multiple - magical_number
       
        for i in range(0, net_index + 1):
            if(i == net_index):
                network_address.append(magical_number_multiple)
                broadcast_address.append(magical_number_multiple_next -1 )
            else:
                network_address.append(int(ip_address[i]))
                broadcast_address.append(int(ip_address[i]))
       
        for i in range(net_index + 1, len(ip_address)):
            network_address.append(0)
            broadcast_address.append(255)
        first_address = network_address.copy()
        first_address[-1] = first_address[-1] + 1
        last_address = broadcast_address.copy()
        last_address[-1] = last_address[-1] - 1
        return network_address, broadcast_address, first_address, last_address

    def get_network_broadcast_first_last_addresses(self):
        ip_address = re.split(self.ip_separator, self.ip)
        network_address = list()
        broadcast_address = list()
        net_index = self.default_subnet_mask // 8
        if self.default_subnet_mask % 8 == 0:
            network_address = [int(ip_address[i]) for i in range(0, net_index)]
            broadcast_address = network_address.copy()
            for i in range(net_index, len(ip_address)):
                network_address.append(0)
                broadcast_address.append(255)
                if i == len(ip_address) - 1:
                    first_address = network_address[:i] + [1]
                    last_address = broadcast_address[:i] + [254]
            return network_address, broadcast_address, first_address, last_address
        else:
            return self.get_significant_ip_subnet_mask_byte(ip_address, net_index)
    
    def set_network_broadcast_first_last_addresses(self, network_address, broadcast_address, first_address, last_address):
        #Here n_a, b_a, f_a, l_a stand respectively for network_address, broadcast_address, first_address,
        # and last_address
        n_a, b_a, f_a, l_a = self.convert_int_list_to_string(network_address, broadcast_address, first_address, last_address)
        self.network_address = self.ip_separator.join(n_a)
        self.broadcast_address = self.ip_separator.join(b_a)
        self.first_address = self.ip_separator.join(f_a)
        self.last_address = self.ip_separator.join(l_a)
