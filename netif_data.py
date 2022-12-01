import netifaces as ni
import scapy.all as sc
import contextlib
import io
import re
from tabulate import tabulate

def get_netifaces_data():
    with contextlib.redirect_stdout(io.StringIO()) as f:
        sc.show_interfaces()
    s = f.getvalue()
    ifacesData = s.split('\n')
    ifaces = list()
    for ifaceData in ifacesData:
        iface = re.split(r'\s{2,}', ifaceData)[2:]
        iface = [i for i in iface if i != '']
        ifaces.append(iface)
    print(tabulate(ifaces[1:], headers=ifaces[0]))

if __name__ == '__main__':
    get_netifaces_data()
        

