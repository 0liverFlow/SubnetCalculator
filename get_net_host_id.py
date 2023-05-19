import re

from rich import print as printc
from rich.table import Table


class NetHostId():
    """ 
        This class allows you to determine the following addresses:
        -network address (n_a)
        -broadcast address (b_a) 
        -first address (f_a)
        -last_address (l_a)
        ... 
    """
    
    def __init__(self, ip: str, subnet_mask: str):
        """
        Constructs all the necessary attributes for the NetHostId object.

        Parameters
        -----------
        ip (str): The IP address specified by the user
        subnet_mask (int): The subnet mask specified by the user
        """

        self.ip = ip
        self.default_subnet_mask = subnet_mask
        self.ip_cidr = self.ip + '/' + str(self.default_subnet_mask)
        self.ip_separator = ''
        self.network_address = ''
        self.first_address = ''
        self.last_address = ''
        self.broadcast_address = ''
        self.hosts = ''
    
    @staticmethod
    def double_letter_format(string: str):
        letters = "𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ"
        numbers = "𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡"
        string = string.strip().upper()
        double_string = ''
        for char in string:
            if char in [' ', '-', '°']:
                double_string += char
            else:
                char_dec = ord(char)
                if 48 <= char_dec <= 57:
                    double_string += numbers[char_dec - 48]
                elif  char_dec >= 65 and char_dec <= 90:
                   double_string += letters[char_dec - 65] + ' '
        return double_string
    
    def check_subnet_mask_validity(self) -> bool:
        """
        Check if the subnet mask specified by the user is correct.
        """
        
        # Check if subnet mask is an integer
        try:
            self.default_subnet_mask = int(self.default_subnet_mask)
            self.hosts = 2**(32-self.default_subnet_mask)-2
        except ValueError:
            printc(f"[[red1 b]-[/red1 b]] Incorrect subnet mask type! Expected an integer!")
            return False

        # Checking subnet_mask's values
        if self.default_subnet_mask < 1 or self.default_subnet_mask > 31:
            printc(f"[[red1 b]-[/red1 b]] Incorrect subnet mask's value! Expected a value between 1 and 31!")
            return False
        return True

    def check_ip_validity(self) -> bool:
        """
        Check if the ip specified by the user is correct.
        """
        
        # Check ip address format.
        ip_pattern = re.compile('^\d{1,3}([.-]\d{1,3}){3}$')
        if re.search(ip_pattern, self.ip) is None:
            print(self.ip)
            printc(f"[[red1 b]-[/red1 b]] Incorrect IP address! Expected the following formats : x.x.x.x or x-x-x-x")
            return False
        
        # Get ip address's separator.
        if self.ip.find('.') != -1:
            self.ip_separator = '.'
        else:
            self.ip_separator = '-'
        
        # Check if the ip address' values (bytes) are correct.
        ip_bytes = [int(byte) for byte in re.split("[.-]", self.ip)]
        for byte in ip_bytes:
            if byte < 0 or byte > 255:
                printc("""[[red1 b]-[/red1 b]] Incorrect IP address' value found! Each byte should be between 0 and 255.""")
                return False
        return True
    
    def display_network_info(self, header: str) -> None:
        """
        Display a table containing a summary of the information related to the network cidr specified by the user
        """

        table = Table(title=f"{self.double_letter_format(header)}", style="bold") 
        table.add_column("CIDR Notation", justify="center")
        table.add_column("Network Address", justify="center")
        table.add_column("First Address", justify="center")  
        table.add_column("Last Address", justify="center")
        table.add_column("Broadcast Address", justify="center")
        table.add_column("Hosts number", justify="center")
        table.add_row(f"{self.ip_cidr}", f"{self.network_address}", f"{self.first_address}", f"{self.last_address}", f"{self.broadcast_address}", f"{self.hosts}")
        printc(table)

    def get_ip_subnet_mask_significant_byte(self, ip_address: list, net_index) -> tuple[list]:
        bits_list = [128, 192, 224, 240, 248, 252, 254]
        network_address = list()
        broadcast_address = list()
        subnet_mask_significant_byte = None

        # Get the subnet_mask significant byte
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

        # Get the magical number
        magical_number = 256 - subnet_mask_significant_byte
        k = 0
        magical_number_multiple = magical_number * k
        ip_significant_byte = int(ip_address[net_index])
       
        while magical_number_multiple <= ip_significant_byte:
            k += 1
            magical_number_multiple = magical_number * k
        magical_number_next_multiple = magical_number_multiple
        magical_number_multiple = magical_number_next_multiple - magical_number

        # Get network and broadcast address
        for i in range(net_index+1):
            if i == net_index:
                network_address.append(magical_number_multiple)
                broadcast_address.append(magical_number_next_multiple -1 )
            else:
                network_address.append(int(ip_address[i]))
                broadcast_address.append(int(ip_address[i]))

       # Get the first and the last ip address
        for i in range(net_index+1, len(ip_address)):
            network_address.append(0)
            broadcast_address.append(255)
        first_address = network_address.copy()
        first_address[-1] += 1
        last_address = broadcast_address.copy()
        last_address[-1] -= 1
        return network_address, broadcast_address, first_address, last_address

    def get_network_broadcast_first_last_addresses(self) -> tuple[list]:
        """"
        Returns the network address, the first and last address and the broadcast address.
        """

        ip_address = re.split("[.-]", self.ip)  # ip_address is a list of bytes
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
            return self.get_ip_subnet_mask_significant_byte(ip_address, net_index)
    
    def set_network_broadcast_first_last_addresses(self, network_address: list, broadcast_address: list, first_address: list, last_address: list) -> None:
        """
        Method used to convert the arguments specified in parameters into strings.
        """

        n_a, b_a, f_a, l_a = network_address, broadcast_address, first_address, last_address
        n_a, b_a, f_a, l_a = [str(na) for na in n_a], [str(ba) for ba in b_a], [str(fa) for fa in f_a], [str(la) for la in l_a] 
        self.network_address = self.ip_separator.join(n_a)
        self.broadcast_address = self.ip_separator.join(b_a)
        self.first_address = self.ip_separator.join(f_a)
        self.last_address = self.ip_separator.join(l_a)
