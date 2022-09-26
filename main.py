import os
import time
from menu import *
from FixedLengthSubnetMaskCalculator import *

if __name__ == '__main__':
    NetHostId.warning()
    user_choice = menu()

    match user_choice:
        case 1:
            ip_address = input("|>Enter an IPv4(eg : x.x.x.x or x-x-x-x) : ")
            subnet_mask = input("|>Enter the subnet mask in CIDR notation(eg : /24, /18) : ")
            print('|========================================================================\n')
            net_host_id = NetHostId(ip_address, subnet_mask)
            while not(net_host_id.check_subnet_mask_validity() and net_host_id.check_ip_validity()):
                time.sleep(4)
                os.system("cls")
                ip_address = input("|>Enter an IPv4(eg : x.x.x.x or x-x-x-x) : ")
                subnet_mask = input("|>Enter the subnet mask in CIDR notation(eg : /24, /18) : ")
            n_a, b_a, f_a, l_a = net_host_id.get_network_broadcast_first_last_addresses()
            net_host_id. set_network_broadcast_first_last_addresses(n_a, b_a, f_a, l_a)
            net_host_id.display_network_info('Subnet Calculator')
        case 2:
            ip_address = input("|>Enter an IPv4(eg : x.x.x.x or x-x-x-x) : ")
            subnet_mask = input("|>Enter the subnet mask in CIDR notation(eg : /24, /18) : ")
            number_of_subnets = int(input("|Enter the number of subnets please : "))
            print('|========================================================================\n')
            if number_of_subnets == 1:
                net_host_id = NetHostId(ip_address, subnet_mask)
                n_a, b_a, f_a, l_a = net_host_id.get_network_broadcast_first_last_addresses()
                net_host_id.set_network_broadcast_first_last_addresses(n_a, b_a, f_a, l_a)
                net_host_id.display_network_info('Subnet Calculator')
            else:
                flsm = FixedLengthSubnetMask(ip_address, subnet_mask, number_of_subnets)
                while not(flsm.check_subnet_mask_validity() and flsm.check_ip_validity()):
                    time.sleep(4)
                    #os.system("cls")
                    ip_address = input("|>Enter an IPv4(eg : x.x.x.x or x-x-x-x) : ")
                    subnet_mask = input("|>Enter the subnet mask in CIDR notation(eg : /24, /18) : ")
                #print("Default network that will be divided into : ",flsm.subnets, "subnets")
                n_a, b_a, f_a, l_a = flsm.get_network_broadcast_first_last_addresses()
                flsm.set_network_broadcast_first_last_addresses(n_a, b_a, f_a, l_a)
                print('flsm network address is : ', flsm.network_address, 'type na is : ',type(flsm.network_address))
                flsm.default_network_address = flsm.network_address.split('\.') if bool(re.search('\.', flsm.network_address)) else flsm.network_address.split('-') # Check the separator used by using regex
                flsm.display_network_info('Default Network')
                flsm.set_new_subnet_mask()
                flsm.set_net_id_combinations()
                for subnet_number in range(flsm.number_of_subnets):
                    display_subnet_header = "SUBNET N° " + str(subnet_number +1 )
                    n_a, b_a, f_a, l_a = flsm.set_subnet_network_broadcast_address(subnet_number)
                    flsm.set_network_broadcast_first_last_addresses(n_a, b_a, f_a, l_a)
                    flsm.display_network_info(display_subnet_header)
                    print("\n", end='')
        case 3:
                pass
       
                
    