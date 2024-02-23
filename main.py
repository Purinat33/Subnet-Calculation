def insertDot(bin_ip):
    # Insert after every 8th
    ip = ""
    count = 0
    for i in range(len(bin_ip)):
        ip += bin_ip[i]
        i += 1
        if i % 8 == 0:
            ip += '.'

    ip = ip.removesuffix('.')
    return ip


def convertDecimalIP(bin_ip: str) -> str:
    octets = bin_ip.split('.')
    decimal = []
    for ip in octets:
        decimal.append(str(int(ip, 2)))

    return '.'.join(decimal)


def format_dict_to_str(dictionary: dict):
    for key, val in dictionary.items():
        print(f"{key} : {val}\n")


def concatNetwork_host(network_address, calculated_host_address):
    # Append calculated host portion to the network address
    # full_network_id = network_address + network_id
    # full_network_id = insertDot(full_network_id)
    # We got full IP in binary form
    # full_network_id = convertDecimalIP(full_network_id)  # convert to decimal
    full_ip_bin = network_address + calculated_host_address
    full_ip_bin = insertDot(full_ip_bin)
    full_ip_dec = convertDecimalIP(full_ip_bin)
    return full_ip_dec


def subnet(ip: str, mask_bits: int):
    if mask_bits >= 32:
        return
    # Counts 4 octets (separated by ".")
    octets = ip.split('.')
    if len(octets) != 4:
        print(f"Incorrect amounts of subnet (required 4): {len(octets)}")
        return
    for address in octets:
        if int(address) < 0 or int(address) > 255:
            print(f'Incorrect address range ({address})')
            return

    # To bin
    # Fill the string with zeros until it is 10 characters long: str.zfill(desired_length)
    bin_octet = ""
    for address in octets:
        temp = int(address)
        bin_octet += bin(temp).removeprefix('0b').zfill(8)
        bin_octet += '.'

    bin_octet = bin_octet.removesuffix('.')
    # Split base on number of bits
    for_calculation = bin_octet.replace('.', '')
    # print(for_calculation)
    # print(len(for_calculation))
    # print(bin_octet)
    # We don't do anything with this (yet)
    network_address = for_calculation[:mask_bits]
    # print(network_address)
    host_address = for_calculation[mask_bits:]
    # From all 0 to all 1 (of host address part)
    # All 0 = IP of address (Network ID)
    # All 1 = Broadcast address
    # First usable IP = Network ID + 1
    # Last usable IP = Broadcase ID - 1
    network_id = host_address.replace('1', '0')
    broadcast_ip = host_address.replace('0', '1')
    first_usable_ip = bin(int(network_id, 2) +
                          1).removeprefix('0b').zfill(len(host_address))
    last_usable_ip = bin(int(broadcast_ip, 2) -
                         1).removeprefix('0b').zfill(len(host_address))
    ip_count = pow(2, 32-mask_bits) - 2  # Excluding Network ID and broadcast
    important_ip = {}

    full_network_id = concatNetwork_host(network_address, network_id)
    important_ip["Network ID"] = full_network_id

    full_broadcast_ip = concatNetwork_host(network_address, broadcast_ip)
    important_ip["Broadcast IP"] = full_broadcast_ip

    first_host_ip = concatNetwork_host(network_address, first_usable_ip)
    important_ip["First Usable Host"] = first_host_ip

    last_host_ip = concatNetwork_host(network_address, last_usable_ip)
    important_ip["Last Usable Host"] = last_host_ip

    important_ip["Usable Host Counts"] = ip_count
    mask_address = ('1' * mask_bits).ljust(32, '0')
    mask_address = insertDot(mask_address)
    mask_address = convertDecimalIP(mask_address)

    important_ip["Mask (Address)"] = mask_address
    important_ip["Mask (CIDR)"] = f"/{mask_bits}"

    format_dict_to_str(important_ip)


subnet('255.0.0.0', 16)
