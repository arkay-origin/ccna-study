_T = [
 ('Subnetting quick table', [
   ['/24 · 255.255.255.0', '256 addresses, 254 hosts'], ['/25 · .128', 'Block 128, 126 hosts'], ['/26 · .192', 'Block 64, 62 hosts'], ['/27 · .224', 'Block 32, 30 hosts'],
   ['/28 · .240', 'Block 16, 14 hosts'], ['/29 · .248', 'Block 8, 6 hosts'], ['/30 · .252', 'Block 4, 2 hosts (point-to-point)'], ['/31', '2 addresses, both usable on point-to-point links'],
   ['/23 · 255.255.254.0', '510 hosts'], ['/22 · 255.255.252.0', '1,022 hosts'], ['/20 · 255.255.240.0', 'Third-octet block 16, 4,094 hosts'],
   ['Hosts', '2^host bits − 2'], ['Block size', '256 − mask value in the interesting octet'], ['Wildcard', '255.255.255.255 − mask']],
  'Count in block sizes to find the network; one less than the next block is the broadcast.'),
 ('Special IPv4 ranges', [
   ['10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16', 'Private (RFC 1918)'], ['169.254.0.0/16', 'APIPA / link-local: DHCP failed'], ['127.0.0.0/8', 'Loopback'],
   ['100.64.0.0/10', 'Carrier-grade NAT'], ['224.0.0.0/4', 'Multicast'], ['255.255.255.255', 'Limited broadcast']], ''),
 ('IPv6 at a glance', [
   ['2000::/3', 'Global unicast'], ['FC00::/7 (FD..)', 'Unique local'], ['FE80::/10', 'Link-local'], ['FF00::/8', 'Multicast'], ['FF02::1 / FF02::2', 'All nodes / all routers'],
   ['FF02::5 / FF02::6', 'OSPFv3 routers / DRs'], ['::1 / ::', 'Loopback / unspecified'], ['/64', 'Every LAN subnet'], ['/48 → /64s', '65,536 subnets; /56 → 256'],
   ['EUI-64', 'Split MAC, insert FFFE, flip 7th bit (00→02)'], ['SLAAC', 'Host builds address from the RA prefix'], ['NDP', 'ICMPv6 NS/NA (replaces ARP), RS/RA, DAD'],
   ['ipv6 unicast-routing', 'Needed to route and send RAs']], 'Only one "::" per address.'),
 ('Ports to know', [
   ['TCP 20/21', 'FTP'], ['TCP 22', 'SSH, SCP, SFTP'], ['TCP 23', 'Telnet'], ['TCP 25', 'SMTP'], ['TCP/UDP 53', 'DNS'], ['UDP 67/68', 'DHCP server/client'], ['UDP 69', 'TFTP'],
   ['TCP 80 / 443', 'HTTP / HTTPS'], ['UDP 123', 'NTP'], ['UDP 161 / 162', 'SNMP / traps & informs'], ['UDP 514', 'Syslog'], ['TCP 49', 'TACACS+'], ['UDP 1812/1813', 'RADIUS'],
   ['UDP 500 / 4500', 'IKE / IPsec NAT-T'], ['IP 50 / 51', 'ESP / AH'], ['IP 89', 'OSPF'], ['UDP 1985', 'HSRP'], ['IP 112', 'VRRP'], ['UDP 5246/5247', 'CAPWAP control/data']], ''),
 ('Interfaces and cables', [
   ['Speed mismatch', 'Link does not come up'], ['Duplex mismatch', 'Link up; half side: collisions, late collisions; full side: CRC, runts'],
   ['Auto + fixed 100/full', 'Auto side picks half duplex → mismatch'], ['CRC', 'Damaged frame: cable, interference, duplex'], ['Runt / giant', '< 64 bytes / > max size'],
   ['admin down', 'shutdown configured'], ['down/down', 'Layer 1: cable, far end, speed'], ['up/down', 'Layer 2: encapsulation, keepalives'],
   ['Copper BASE-T', '100 m max'], ['MMF / SMF', 'Hundreds of metres / kilometres'], ['1000BASE-T', 'All four pairs'], ['Auto-MDIX', 'Fixes straight-through vs crossover']],
  'Low fibre receive light: dirty connector, bends, run too long. show interfaces transceiver.'),
 ('Wireless', [
   ['2.4 GHz', 'Channels 1, 6, 11; longest range; most interference'], ['5 GHz', '~25 channels; DFS on some'], ['6 GHz', 'Wi-Fi 6E/7; WPA3 required'],
   ['Wi-Fi 4 / 5 / 6 / 7', '802.11n / ac / ax / be'], ['RSSI', '−67 dBm good for voice; closer to 0 is stronger'], ['SNR', 'Signal − noise; ≥ 25 dB healthy'],
   ['Co-channel', 'Same channel, shared airtime'], ['Adjacent-channel', 'Overlapping channels; worse'], ['Non-Wi-Fi', 'Microwave, Bluetooth, cordless phones'],
   ['WEP / WPA', 'Broken / deprecated (RC4, TKIP)'], ['WPA2', 'AES-CCMP'], ['WPA3', 'SAE (Personal), PMF required, 192-bit Enterprise'], ['Enterprise', '802.1X + RADIUS'], ['OWE', 'Encrypted open network']], ''),
 ('Client troubleshooting', [
   ['Windows', 'ipconfig /all · /release · /renew · /flushdns · tracert · arp -a'], ['macOS', 'ifconfig · networksetup -getinfo Wi-Fi · traceroute'],
   ['Linux', 'ip addr · ip route · ip neigh · traceroute · dig'], ['All', 'ping · nslookup'], ['169.254.x.x', 'No DHCP reply'],
   ['IP works, name fails', 'DNS'], ['Local works, remote fails', 'Default gateway'], ['Fails at password', 'Wrong PSK or security mismatch']], ''),
 ('DHCP', [
   ['DORA', 'Discover, Offer, Request, ACK'], ['Pool', 'ip dhcp pool · network · default-router · dns-server'], ['Exclude', 'ip dhcp excluded-address (global)'],
   ['Relay', 'ip helper-address on the client-facing SVI'], ['giaddr', 'Relay\'s interface IP; server picks the matching pool'], ['Client', 'ip address dhcp · show dhcp lease'],
   ['Verify', 'show ip dhcp binding · pool · conflict']], ''),
 ('VLANs, trunks, EtherChannel', [
   ['Access', 'switchport mode access · switchport access vlan 10'], ['Phone', 'switchport voice vlan 20'], ['Trunk', 'switchport mode trunk · allowed vlan · native vlan · nonegotiate'],
   ['Add a VLAN', 'switchport trunk allowed vlan add 30'], ['Native mismatch', 'Traffic leaks; CDP warns'], ['DTP', 'auto+auto = access; desirable+auto = trunk'],
   ['LACP', 'active/passive; one side active'], ['PAgP', 'desirable/auto (Cisco)'], ['Members must match', 'Speed, duplex, mode, VLANs, native VLAN'],
   ['Flags', 'P bundled · s suspended · SU L2 in use · RU L3 in use'], ['SVI up needs', 'VLAN exists, not shut, one forwarding port in VLAN'], ['Inter-VLAN', 'ip routing; or router-on-a-stick with dot1Q subinterfaces'],
   ['PoE', 'af 15.4 W · at 30 W · bt 60/90 W'], ['Lightweight AP', 'Access port (CAPWAP to WLC)'], ['Autonomous / FlexConnect AP', 'Trunk']], ''),
 ('Rapid PVST+', [
   ['Root bridge', 'Lowest priority + MAC'], ['Default priority', '32768 + VLAN ID'], ['root primary / secondary', '24576 / 28672'], ['Steps', 'Multiples of 4096'],
   ['Cost', '10M 100 · 100M 19 · 1G 4 · 10G 2'], ['Roles', 'Root, designated, alternate, backup'], ['States', 'Discarding, learning, forwarding'],
   ['PortFast', 'Edge ports forward immediately'], ['BPDU guard', 'BPDU on edge → err-disabled'], ['Root guard', 'Superior BPDU → root-inconsistent'], ['Loop guard', 'BPDUs stop → loop-inconsistent']], ''),
 ('Routing table', [
   ['Choose', '1 longest prefix · 2 lowest AD · 3 lowest metric'], ['[110/3]', '[AD/metric]'], ['Codes', 'C connected · L local · S static · O OSPF · D EIGRP · B BGP · * default'],
   ['AD', 'Connected 0 · static 1 · eBGP 20 · EIGRP 90 · OSPF 110 · IS-IS 115 · RIP 120 · EIGRP ext 170 · iBGP 200'],
   ['Default', 'ip route 0.0.0.0 0.0.0.0 x · ipv6 route ::/0 x'], ['Host', '/32 or /128'], ['Floating', 'AD above the primary, e.g. 130 over OSPF'],
   ['IPv6 link-local next hop', 'Needs the exit interface too']], ''),
 ('OSPF', [
   ['Router ID', 'Configured > highest loopback > highest active interface'], ['Must match', 'Area, subnet/mask, hello/dead, auth, stub flag (and MTU for Full)'],
   ['Process ID', 'Local only'], ['Hello/dead', '10/40 on Ethernet'], ['DR election', 'Highest priority (default 1), then highest RID; 0 = never; not pre-emptive'],
   ['States', 'Down, Init, 2-Way, ExStart, Exchange, Loading, Full'], ['Stuck ExStart', 'MTU mismatch'], ['DROTHER ↔ DROTHER', '2-WAY is normal'],
   ['Point-to-point', 'ip ospf network point-to-point: no DR'], ['Cost', '100 Mbps ÷ bandwidth; raise reference bandwidth'], ['Default route', 'default-information originate'],
   ['OSPFv3', 'ipv6 ospf 1 area 0 on interface; set router-id if no IPv4'], ['Verify', 'show ip ospf neighbor · interface brief · show ip protocols']], ''),
 ('HSRP and VRRP', [
   ['HSRP', 'Cisco · active/standby · pri 100 · pre-empt off · UDP 1985'], ['HSRPv1 / v2', '224.0.0.2, 0000.0C07.ACxx / 224.0.0.102, 0000.0C9F.Fxxx'],
   ['VRRP', 'Open · master/backup · pri 100 · pre-empt on · IP 112 · 224.0.0.18 · 0000.5E00.01xx'], ['Both Active', 'Hellos not received: VLAN or link problem'],
   ['Hosts use', 'The virtual IP'], ['Tracking', 'Lowers priority when an uplink fails']], ''),
 ('AAA, SSH, file transfer', [
   ['SSH', 'hostname · ip domain-name · crypto key generate rsa · username/secret · login local · transport input ssh'],
   ['TACACS+', 'TCP 49 · whole body encrypted · separate AAA · admin access'], ['RADIUS', 'UDP 1812/1813 · password only encrypted · network access'],
   ['Fallback', '"local" only when servers don\'t respond'], ['SCP server', 'ip scp server enable'], ['Copy', 'copy sftp://user@host/file flash:'], ['Verify image', 'verify /md5 flash:file']], ''),
 ('NAT', [
   ['Inside local', 'Real private address'], ['Inside global', 'Public address it becomes'], ['Static', 'ip nat inside source static 10.1.1.10 203.0.113.10'],
   ['Dynamic', 'ip nat pool … + ip nat inside source list 1 pool NAME'], ['PAT', 'ip nat inside source list 1 interface Gi0/1 overload'],
   ['Interfaces', 'ip nat inside · ip nat outside'], ['Verify', 'show ip nat translations · statistics']], 'Empty translation table: check the ACL and inside/outside.'),
 ('DNS records', [
   ['A / AAAA', 'Name → IPv4 / IPv6'], ['CNAME', 'Alias → another name; no other records at that name'], ['MX', 'Mail server name + preference (lower first)'],
   ['NS', 'Authoritative servers'], ['PTR', 'IP → name (reverse)'], ['TTL', 'Cache lifetime; old answers persist after changes']], ''),
 ('ACLs', [
   ['Standard', '1–99, 1300–1999 · source only · near destination'], ['Extended', '100–199, 2000–2699 · protocol, src, dst, ports · near source'],
   ['Processing', 'Top-down, first match, implicit deny any'], ['Apply', 'ip access-group NAME in|out (interface) · access-class (VTY)'],
   ['Limit', 'One per interface per direction per protocol'], ['Named', 'Sequence numbers: insert/delete lines'], ['Keywords', 'host x = x 0.0.0.0 · any · eq gt lt neq range']], ''),
 ('Layer 2 security', [
   ['DHCP snooping', 'Untrusted ports drop server messages; trust uplinks; binding table'], ['DAI', 'Checks ARP against bindings; ARP ACL for static hosts'],
   ['Port security', 'Default max 1, violation shutdown; protect/restrict/shutdown; sticky'], ['Storm control', 'Limits broadcast/multicast/unicast; trap or shutdown'],
   ['RA guard', 'Blocks IPv6 RAs on host ports']], ''),
 ('IPsec', [
   ['Site-to-site', 'Gateway to gateway; transparent to hosts'], ['Remote access', 'Client software (IPsec IKEv2 or TLS)'], ['IKE', 'UDP 500 / 4500'],
   ['ESP', 'IP 50, encrypts'], ['AH', 'IP 51, no encryption, breaks with NAT'], ['Tunnel mode', 'New IP header; whole packet encrypted'], ['Transport mode', 'Original header; payload encrypted'],
   ['GRE over IPsec', 'Carries multicast/routing protocols']], ''),
 ('SNMP and syslog', [
   ['SNMP', 'Get/Set UDP 161 · trap/inform UDP 162 · MIB, OIDs'], ['v2c / v3', 'Community strings / authPriv with users'],
   ['Severities', '0 Emerg · 1 Alert · 2 Crit · 3 Err · 4 Warn · 5 Notif · 6 Info · 7 Debug'], ['Format', '%FACILITY-SEVERITY-MNEMONIC: text'],
   ['logging trap 4', 'Sends levels 0–4'], ['Server facility', 'local7 by default'], ['SSH sessions', 'terminal monitor']], 'Every Awesome Cisco Engineer Will Need Ice-cream Daily.'),
 ('Automation and AI', [
   ['Approaches', 'Device · cloud · controller · automation · IaC'], ['Northbound / southbound', 'REST APIs to apps / NETCONF, CLI, SNMP to devices'],
   ['Ansible', 'Agentless, SSH, push, YAML playbooks, inventory, idempotent'], ['Modules', 'cisco.ios.ios_command (show) · ios_config (config)'], ['Run', 'ansible-playbook site.yml -i inventory'],
   ['Terraform', 'Declarative IaC, HCL, state file'], ['Agentic AI', 'Goal → observe, reason, act with tools, repeat'],
   ['Guardrails', 'Least privilege, human approval, audit logs'], ['Prompt', 'Persona · instructions · context · output format · data classification']],
  'If AI output disagrees with the device output, trust the device.'),
]
CHEAT = [{'n': i + 1, 'title': t, 'rows': r, 'tip': tip, 'qs': [], 'key': [], 'pri': []} for i, (t, r, tip) in enumerate(_T)]
CHEAT[-1]['foot'] = 'Based on the Cisco CCNA 200-301 v2.0 exam topics (exam available from February 3, 2027). Check Cisco\'s current topic list before you book.'
