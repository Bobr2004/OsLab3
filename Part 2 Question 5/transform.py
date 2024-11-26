#! /usr/bin/env python3

# Open the input file in read mode and the output file in write mode
traceFile = open('./ls-trace.txt', 'r')
vpnFile = open('./vpn.txt', 'w')

for line in traceFile:
    # Skip lines starting with '='
    if not line.startswith('='):
        # Extract, convert, and process the hexadecimal address to get the VPN
        vpn = (int("0x" + line[3:11], 16) & 0xfffff000) >> 12
        vpnFile.write(str(vpn) + "\n")

# Close the files
traceFile.close()
vpnFile.close()
