import argparse
import sys

from rich import print as printc

from get_net_host_id import NetHostId
from flsm import FixedLengthSubnetMask
from vlsm import VariableLengthSubnetMask


if __name__ == '__main__':
    """
    Main function responsible for performing FLSM and VLSM.
    """
    # Warning message
    NetHostId.warning()
    # The banner
    print("""
 ___   _      ___   _      ___   _      ___   _      ___   _
[(_)] |=|    [(_)] |=|    [(_)] |=|    [(_)] |=|    [(_)] |=|
 '-`  |_|     '-`  |_|     '-`  |_|     '-`  |_|     '-`  |_|
    /PC1/        /PC2/       /PC3/       /PC4/       /PC5/     Author/0LI\/ERFL0W
    |____________|__________|___________|___________|_______________|______________Subnet/Calculator
                        |            |            |                 |
                    ___  \_      ___  \_      ___  \_           version 1.0  
                   [(_)] |=|    [(_)] |=|    [(_)] |=|
                    '-`  |_|     '-`  |_|     '-`  |_|
                    /PC6/        /PC7/        /PC8/
    """)
    parser = argparse.ArgumentParser(prog='SubnetCalculator.py', description='Subnetting program coded with <3 by 0liverFlow', epilog='Ping me: 0liverFlow@proton.me')
    parser.add_argument('--network', metavar="CIDR", help='network address in CIDR notation (e.g. 192.168.1.0/24)', required=True)
    parser.add_argument('--flsm', type=int, metavar="N",  help='perform Fixed Length Subnetting with N subnets', nargs=1)
    parser.add_argument('--vlsm', metavar="N", help='perform a Variable Length Subnet Masking using a list of N hosts per subnet', nargs="+")
    args = parser.parse_args()
    
    # Check python version is acceptable
    user_python_version = '.'.join(sys.version.split()[0].split('.')[:2])
    if float(user_python_version) <  3.9:
        sys.exit(printc(f"[yellow1 b][!][/yellow1 b] This script must be executed at least with python 3.9\nYou are using python {user_python_version}"))
    try:
        ip_address, subnet_mask = args.network.split('/')
    except ValueError:
        printc(f"[[red1 b]-[/red1 b]] Incorrect Network CIDR specified! Expected Network/Subnet (e.g. 192.168.1.0/24)")
        sys.exit(1)

    # Perform the subnetting type specified by the user
    if args.flsm:
        flsm = FixedLengthSubnetMask(ip_address, subnet_mask, args.flsm[0])
        if not(flsm.check_subnet_mask_validity() and flsm.check_ip_validity()):
            printc(f"[green b][+][/green b] Please, try again!\n")
            sys.exit(parser.print_help())
        else:
            n_a, *_ = flsm.get_network_broadcast_first_last_addresses()
            n_a = [str(na) for na in n_a]
            flsm.default_network_address = n_a
            flsm.set_new_subnet_mask()
            flsm.set_net_id_combinations()
            for subnet_number in range(flsm.number_of_subnets):
                display_header = "SUBNET N° " + str(subnet_number + 1)
                n_a, b_a, f_a, l_a = flsm.set_subnet_network_broadcast_address(subnet_number)
                flsm.set_network_broadcast_first_last_addresses(n_a, b_a, f_a, l_a)
                flsm.display_network_info(display_header)
                print("\n", end='')
    elif args.vlsm:
        number_of_subnets = len(args.vlsm)
        try:
            vlsm_args = [int(vlsm_arg) for vlsm_arg in args.vlsm]
            vlsm = VariableLengthSubnetMask(ip_address, subnet_mask, sorted(vlsm_args, reverse=True))
        except ValueError:
            sys.exit(printc(f"[red1 b][-][/red1 b] Please, make sure to separate the host list with a space"))
        if not(vlsm.check_subnet_mask_validity() and vlsm.check_ip_validity()):
            printc(f"[green b][+][/green b] Please, try again!\n")
            sys.exit(parser.print_help())
        if vlsm.check_number_of_available_hosts():
            sys.exit(printc(f"[red1 b][-][/red1 b] The HostID is too small for the number of hosts specified {sum(vlsm.number_of_users_list)}. Reduce the NetID bits, then retry!"))
        n_a, *_ = vlsm.get_network_broadcast_first_last_addresses()
        n_a = [str(na) for na in n_a] 
        vlsm.default_network_address = vlsm.ip_separator.join(n_a)
        vlsm.get_vlsm(number_of_subnets)
    else:
        net_host_id = NetHostId(ip_address, subnet_mask)
        if not(net_host_id.check_subnet_mask_validity() and net_host_id.check_ip_validity()):
            printc(f"[green b][+][/green b] Please, try again!\n")
            sys.exit(parser.print_help())
        n_a, b_a, f_a, l_a = net_host_id.get_network_broadcast_first_last_addresses()
        net_host_id.set_network_broadcast_first_last_addresses(n_a, b_a, f_a, l_a)
        net_host_id.display_network_info('Subnet Calculator')
