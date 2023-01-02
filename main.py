import os
import time
from GetNetHost import NetHostId
from FLSM import FixedLengthSubnetMask
from VLSM import VariableLengthSubnetMask
from menu import menu

if __name__ == '__main__':
    NetHostId.warning()
    menu()
    user_choice = False
    while not(user_choice > 0 and user_choice < 4):
        user_choice = int(input("|Thanks to elucidate your choice: "))
    match user_choice:
        case 1:
            ip_address = input("|Enter an IPv4(eg: x.x.x.x or x-x-x-x): ")
            subnet_mask = input("|Enter the subnet mask in CIDR notation(eg: /24, /18) : ")
            print('|========================================================================\n')
            net_host_id = NetHostId(ip_address, subnet_mask)
            while not(net_host_id.check_subnet_mask_validity() and net_host_id.check_ip_validity()):
                time.sleep(4)
                ip_address = input("|Enter an IPv4(eg: x.x.x.x or x-x-x-x) : ")
                subnet_mask = input("|Enter the subnet mask in CIDR notation(eg: /24, /18) : ")
                net_host_id = NetHostId(ip_address, subnet_mask)
            n_a, b_a, f_a, l_a = net_host_id.get_network_broadcast_first_last_addresses()
            net_host_id.set_network_broadcast_first_last_addresses(n_a, b_a, f_a, l_a)
            net_host_id.display_network_info('Subnet Calculator')
        case 2:
            ip_address = input("|Enter an IPv4(eg : x.x.x.x or x-x-x-x): ")
            subnet_mask = input("|Enter the subnet mask in CIDR notation(eg: /24, /18) : ")
            number_of_subnets = int(input("|Enter the number of subnets please: "))
            print('|========================================================================\n')
            flsm = FixedLengthSubnetMask(ip_address, subnet_mask, number_of_subnets)
            while not(flsm.check_subnet_mask_validity() and flsm.check_ip_validity()):
                time.sleep(4)
                #os.system("cls")
                ip_address = input("|Enter an IPv4(eg: x.x.x.x or x-x-x-x) : ")
                default_subnet_mask = input("|Enter the subnet mask in CIDR notation(eg: /24, /18) : ")
                flsm = FixedLengthSubnetMask(ip_address, subnet_mask, number_of_subnets)
            n_a, *_ = flsm.get_network_broadcast_first_last_addresses()
            n_a = [str(na) for na in n_a]
            flsm.default_network_address = n_a #string
            #print("Default address is : ", flsm.ip_separator.join(flsm.default_network_address))
            #flsm.display_network_info('Default Network')
            flsm.set_new_subnet_mask()
            flsm.set_net_id_combinations()
            for subnet_number in range(flsm.number_of_subnets):
                display_header = "SUBNET N° " + str(subnet_number + 1)
                n_a, b_a, f_a, l_a = flsm.set_subnet_network_broadcast_address(subnet_number)
                flsm.set_network_broadcast_first_last_addresses(n_a, b_a, f_a, l_a)
                flsm.display_network_info(display_header)
                print("\n", end='')
        case 3:
            ip_address = input("|Enter an IPv4(eg: x.x.x.x or x-x-x-x): ")
            subnet_mask = input("|Enter the subnet mask in CIDR notation(eg: /24, /18): ")
            check_number_of_subnets_validity = True
            try:
                number_of_subnets = int(input("|Enter the number of subnets : "))
            except ValueError:
                check_number_of_subnets_validity = False
            print('|========================================================================')
            vlsm = VariableLengthSubnetMask(ip_address, subnet_mask, number_of_subnets)
            while not(vlsm.check_subnet_mask_validity() and vlsm.check_ip_validity() and check_number_of_subnets_validity):
                time.sleep(4)
                ip_address = input("|Enter an IPv4(eg: x.x.x.x or x-x-x-x) : ")
                default_subnet_mask = input("|Enter the subnet mask in CIDR notation(eg: /24, /18) : ")
                try:
                    number_of_subnets = int(input("|Enter the number of subnets: "))
                except ValueError:
                    pass
                else:
                    check_number_of_subnets_validity = True
                vlsm = VariableLengthSubnetMask(ip_address, subnet_mask, number_of_subnets) 
            subnet_counter = 0
            hosts_per_subnet = list()
            
            while subnet_counter < number_of_subnets:
                try:
                    hosts_number = int(input(f'|Enter the number of hosts in subnet n°{subnet_counter+1} : '))
                except ValueError:
                    print('|Whoops, it seems like you entered a other value different from an integer.')
                    continue
                hosts_per_subnet.append(hosts_number)
                subnet_counter += 1
            print('|========================================================================\n')
            vlsm.number_of_users_list = sorted(hosts_per_subnet, reverse=True)
            number_of_hosts = 2**(32-vlsm.default_subnet_mask)-2
            if sum(vlsm.number_of_users_list) > number_of_hosts:
                raise Exception(f"""
                |The network specified cannot be divided into {len(vlsm.number_of_users_list)} subnets.\n
                |This error occured because the subnet is too small!\nChange it, then retry!""")
            n_a, *_ = vlsm.get_network_broadcast_first_last_addresses()
            n_a = [str(na) for na in n_a] 
            vlsm.default_network_address = vlsm.ip_separator.join(n_a)
            for subnet_number in range(number_of_subnets):
                display_header = "SUBNET - " + str(vlsm.number_of_users_list[subnet_number])
                if subnet_number == 0:
                    vlsm.get_new_subnet_mask(subnet_number)
                vlsm.subnet_significant_byte = vlsm.default_subnet_mask // 8
                n_a, b_a, f_a, l_a = vlsm.get_network_broadcast_first_last_addresses()
                vlsm.set_network_broadcast_first_last_addresses(n_a, b_a, f_a, l_a)
                vlsm.hosts = 2**(32-vlsm.default_subnet_mask)-2
                vlsm.display_network_info(display_header)
                if subnet_number < number_of_subnets-1:
                    vlsm.get_new_subnet_mask(subnet_number + 1)
                    vlsm.get_new_default_network_address()
