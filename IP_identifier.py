import ipaddress

def get_ip_type(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
      
        if ip_obj.version == 4: # Classifies IP address into IPv4 or IPv
            return "IPv4"
        elif ip_obj.version == 6:
            return "IPv6"
    except ValueError:
        return "Invalid IP address"

ip = input("Enter an IP address: ")
print(get_ip_type(ip))
