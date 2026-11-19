"""Additions after cross-checking against Adam's Flackbox CCNA notes and Anki deck.
New IOS basics section, gap-fill questions for existing sections, and per-lesson
pointers to the matching Flackbox sections. Everything written in our own words."""
from h import *

CODE = lambda *lines: {'code': '\n'.join(lines)}
NOTE = lambda label, t: {'note': t, 'nl': label}

# ------------------------------------------------------------------ new section: IOS basics
qs = [
 Q('A brand-new switch has no IP address. How do you reach its CLI to do the first configuration?', 'Through the console port with a console cable (RJ45 or USB) and a terminal program',
   ['By SSH to its default IP address', 'By Telnet to 192.168.1.1', 'By browsing to its web page'],
   'Cisco devices ship with no management IP, so the console port is the way in. The console also lets you watch the boot process, which SSH can\'t.'),
 Q('What is out-of-band management?', 'Managing devices over a separate network or path that doesn\'t carry user traffic', ['Managing devices over the same links users use', 'Managing devices only by SNMP', 'Managing devices from the cloud'],
   'If the production network breaks, a separate management network (or console servers) still lets you in.'),
 Q('Match each prompt to its mode: R1>, R1#, R1(config)#, R1(config-if)#.', 'User EXEC, privileged EXEC, global configuration, interface configuration',
   ['Privileged EXEC, user EXEC, interface configuration, global configuration', 'User EXEC, global configuration, privileged EXEC, interface configuration', 'Setup mode, user EXEC, global configuration, line configuration'],
   '"enable" goes from > to #. "configure terminal" enters global config. "interface x" enters interface config.', card='Name the modes for the prompts R1>, R1#, R1(config)# and R1(config-if)#.'),
 Q('Which command returns straight to privileged EXEC mode from any configuration level?', 'end (or Ctrl-Z)', ['exit', 'disable', 'logout'],
   '"exit" goes back one level. "disable" drops from privileged to user EXEC.'),
 Q('Which command shows only the lines of the running configuration that contain "ospf"?', 'show running-config | include ospf', ['show running-config ospf', 'show ospf | begin running', 'grep ospf running-config'],
   'Pipes filter output: | include, | exclude, | begin, | section. "| section router ospf" shows a whole block.'),
 Q('Where are the running configuration, startup configuration and IOS image stored?', 'Running config in RAM, startup config in NVRAM, IOS image in flash',
   ['All three in flash', 'Running config in NVRAM, startup config in RAM, IOS in ROM', 'Running config in flash, startup config in ROM, IOS in NVRAM'],
   'RAM is lost on reload, which is why you save the running config to NVRAM.', card='Where are the running config, startup config and IOS image kept?'),
 ORD('Put the router boot sequence in order.', ['POST runs from ROM', 'The bootstrap loads from ROM', 'IOS is found in flash and loaded into RAM', 'The startup-config is loaded from NVRAM into the running-config'],
   'If no IOS image is found you land at the ROMMON prompt. If there is no startup-config, the setup wizard starts.'),
 Q('A router boots to the "rommon 1 >" prompt. What is the most likely cause?', 'It couldn\'t find a valid IOS image in flash', ['The startup-config is missing', 'The console cable is wrong', 'The enable secret was forgotten'],
   'ROM Monitor is the fallback when there is no bootable image. You can recover by loading an image from USB or TFTP.'),
 Q('You changed several settings and want them to survive a reload. Which command saves them?', 'copy running-config startup-config', ['copy startup-config running-config', 'write erase', 'reload'],
   '"write memory" (wr) does the same thing on most platforms. "write erase" deletes the startup config.'),
 Q('What happens when you copy a configuration file into the running-config?', 'It is merged with the current configuration rather than replacing it', ['It completely replaces the running config', 'It is ignored until a reload', 'It overwrites the IOS image'],
   'To replace a configuration cleanly, erase the startup config, reload, then load the new file (or use "configure replace").'),
 Q('Which configuration register value makes a router ignore the startup-config at boot, as used in password recovery?', '0x2142', ['0x2102', '0x2120', '0x2100'],
   '0x2102 is the normal boot. After recovery, set it back to 0x2102 or the router will keep ignoring its config.'),
 ORD('Put the router password recovery steps in order.', ['Break into ROMMON during boot', 'Set confreg 0x2142 and reset', 'Skip setup, enter enable mode and copy startup-config to running-config', 'Set a new enable secret', 'Set config-register 0x2102 and save with copy run start'],
   'The old config (with the forgotten secret) is still in NVRAM. You load it after you are already in enable mode, then overwrite the secret and save.'),
 Q('How do you give a Layer 2 switch a management address reachable from other subnets?', 'Put an IP address on an SVI (for example interface vlan 1), then set "ip default-gateway"',
   ['Put the IP on a physical access port', 'Use "ip route 0.0.0.0 0.0.0.0" on a Layer 2 switch with routing off', 'Layer 2 switches cannot be managed remotely'],
   'A Layer 2 switch is like a host: it needs an address and a default gateway. Use a dedicated management VLAN rather than VLAN 1 in production.'),
 Q('Why is a loopback interface often used for router management and the OSPF router ID?', 'It never goes down unless shut, so the address stays reachable over any working path', ['It is faster than physical interfaces', 'It doesn\'t need an IP address', 'It is the only interface that supports SSH'],
   'Loopbacks are virtual, usually /32, and advertised by the routing protocol. Make them passive in OSPF.'),
 Q('Which troubleshooting approach starts at the physical layer and works up the OSI model?', 'Bottom-up', ['Top-down', 'Divide and conquer', 'Follow the path'],
   'Top-down starts at the application. Divide and conquer starts in the middle (often with a ping) and goes up or down depending on the result.'),
 ORD('Put the general troubleshooting process in order.', ['Define the problem', 'Gather information', 'Analyse the information', 'Eliminate possible causes', 'Propose a hypothesis', 'Test the hypothesis', 'Solve the problem and document the fix'],
   'Documenting the fix is part of the job: it saves time next time and keeps the network records accurate.'),
 Q('What does "Ctrl-Shift-6" do on a Cisco device?', 'Interrupts a running command such as a long ping or traceroute', ['Saves the configuration', 'Logs out of the session', 'Shows command history'],
   'Useful when a traceroute is printing "* * *" for 30 hops.'),
 Q('What does "logging synchronous" on a console or VTY line do?', 'Reprints your partly typed command after a log message interrupts it', ['Sends logs to a server', 'Saves logs in NVRAM', 'Stops all log messages'],
   'It keeps log messages from scrambling what you are typing.'),
]
L = lesson(18,
 'Before routing or switching, you need to be comfortable on the Cisco command line. This lesson covers connecting to a device, moving around the modes, where configuration lives, the boot process, password recovery, basic settings, and a step-by-step way to troubleshoot.',
 [
  ('Connecting to a device', [
    P('New devices have no IP address, so the first connection is the console port: an RJ45 or USB console cable and a terminal program such as PuTTY (9600 baud by default). After that, you manage devices over the network with SSH.'),
    UL('In-band management: over the same network that carries user traffic.', 'Out-of-band management: a separate management network or console server, so you can still get in when production is broken.',
       'The console also shows the boot messages, which SSH can\'t, because the IP stack isn\'t up yet.'),
    CK(0, 1)]),
  ('Getting around the CLI', [
    TB(['Prompt', 'Mode', 'Get there with'], ['R1>', 'User EXEC (look only)', 'Log in'], ['R1#', 'Privileged EXEC', 'enable'], ['R1(config)#', 'Global configuration', 'configure terminal'],
       ['R1(config-if)#', 'Interface configuration', 'interface g0/1'], ['R1(config-line)#', 'Line configuration', 'line vty 0 15']),
    UL('exit goes back one level; end or Ctrl-Z jumps to privileged EXEC.', '? shows help: "sh?" lists commands starting with sh, "show ?" lists options.', 'Commands can be shortened if unambiguous: "conf t", "sh ip int br".',
       'Pipes filter output: show run | include ospf, | begin, | exclude, | section.', 'Ctrl-Shift-6 stops a running ping or traceroute. "do" runs an EXEC command from config mode.'),
    CODE('R1> enable', 'R1# configure terminal', 'R1(config)# interface g0/1', 'R1(config-if)# end', 'R1# show running-config | section interface'),
    CK(2, 3, 4, 16)]),
  ('Memory and the boot process', [
    TB(['Memory', 'Holds', 'Survives a reload?'], ['ROM', 'POST, bootstrap, ROMMON', 'Yes'], ['Flash', 'IOS image files', 'Yes'], ['NVRAM', 'startup-config', 'Yes'], ['RAM', 'running-config, routing tables, the running IOS', 'No']),
    UL('1. POST tests the hardware (ROM).', '2. The bootstrap looks for an IOS image in flash (or what "boot system" points to).', '3. IOS loads into RAM. No image found → ROMMON prompt.',
       '4. startup-config is loaded from NVRAM into the running-config. None found → setup wizard.'),
    TIP('On switches the VLAN database lives in vlan.dat in flash, separate from the startup-config.'),
    CK(5, 6, 7)]),
  ('Saving, backing up and resetting', [
    UL('Commands take effect at once but live only in RAM until you save: copy running-config startup-config (or write memory).', 'Copying a file into the running-config merges it; it doesn\'t replace it.',
       'Factory reset: write erase (or erase startup-config), then reload.', 'Back up images and configs to a server: use SCP or SFTP (see Device Access lesson).'),
    CK(8, 9)]),
  ('Configuration register and password recovery', [
    TB(['Value', 'Effect'], ['0x2102', 'Normal boot (default)'], ['0x2142', 'Ignore the startup-config'], ['0x2120', 'Boot into ROMMON']),
    UL('1. Break into ROMMON at power-on (Ctrl-Break; on switches, often the Mode button).', '2. confreg 0x2142, then reset.', '3. Say no to setup, type enable (no password needed: the config wasn\'t loaded).',
       '4. copy startup-config running-config to bring the old config back.', '5. Set a new enable secret.', '6. config-register 0x2102, then copy running-config startup-config.'),
    CK(10, 11)]),
  ('Basic device settings', [
    CODE('hostname SW1', 'banner motd #Authorised users only#', 'interface vlan 10', ' ip address 10.10.10.5 255.255.255.0', ' no shutdown', 'ip default-gateway 10.10.10.1',
         'interface g1/0/1', ' description Uplink to DIST1', 'line con 0', ' logging synchronous', 'interface loopback0', ' ip address 1.1.1.1 255.255.255.255'),
    UL('A Layer 2 switch gets one management IP on an SVI plus "ip default-gateway".', 'Router interfaces are shut by default; switch ports are up by default.', 'Loopbacks never go down, so they make stable management and router-ID addresses.'),
    CK(12, 13, 17)]),
  ('A troubleshooting method', [
    UL('1. Define the problem.', '2. Gather information.', '3. Analyse it.', '4. Eliminate possible causes.', '5. Propose a hypothesis.', '6. Test it.', '7. Solve the problem and document the fix.'),
    TB(['Approach', 'How'], ['Bottom-up', 'Start at Layer 1 (cable, interface) and work up'], ['Top-down', 'Start at the application and work down'], ['Divide and conquer', 'Start in the middle (ping), then go up or down'],
       ['Follow the path', 'Trace the route hop by hop'], ['Compare', 'Compare with a working device or config'], ['Swap', 'Swap a suspect cable, port or device']),
    CK(14, 15)]),
 ],
 [('2.4', 'Troubleshoot basic Layer 2/Layer 3 connectivity and device operations'), ('4.2', 'Manage device configuration and software files'), ('1.0', 'Foundation for all configuration tasks')])
L['course'] = ['04 The IOS Operating System (04-04 Navigating IOS, 04-05 Configuration Management)', '13 The Cisco Troubleshooting Methodology',
               '14 Cisco Router and Switch Basics', '15 Cisco Device Management (boot-up, password recovery, backups, upgrades)', '17-12 Loopback Interfaces', '34-03 Terminal Monitor and Logging Synchronous']
IOS_SEC = sec('Cisco IOS Basics and Device Management', 'IOS Basics', 'Foundations', '', L, qs)

# ------------------------------------------------------------------ additions to existing sections
# name -> (part heading to add to (None = new part before the last), new questions, extra blocks, Flackbox refs)
ADD = {
 'Networking Fundamentals': [
  ('Switches: delivery inside one network', [
   Q('How does a hub differ from a switch?', 'A hub repeats every bit out every port and all its ports share one half-duplex collision domain; a switch forwards frames by MAC address and each port is its own collision domain',
     ['A hub routes between subnets', 'A hub learns MAC addresses but a switch does not', 'There is no difference'],
     'Hubs work at Layer 1 only. Devices on a hub take turns using CSMA/CD (listen, send, detect collisions, back off and retry).'),
   Q('Which access method do half-duplex Ethernet devices use to handle collisions?', 'CSMA/CD', ['CSMA/CA', 'Token passing', 'TDMA'],
     'Carrier Sense Multiple Access with Collision Detection. Wi-Fi, which can\'t detect collisions while sending, uses CSMA/CA instead.'),
  ], [UL('Old hubs simply repeated bits out every port: one shared, half-duplex collision domain where devices used CSMA/CD. Switches replaced them.')]),
  ('Layers: who does what', [
   ORD('Put the encapsulation names in order from Layer 4 down to Layer 1.', ['Segment (Layer 4)', 'Packet (Layer 3)', 'Frame (Layer 2)', 'Bits (Layer 1)'],
     'Each layer adds its own header around the data from the layer above. The receiver strips them off in reverse.'),
   Q('Which statement describes the three IPv4 traffic types?', 'Unicast goes to one host, broadcast goes to every host on the subnet, multicast goes to hosts that joined a group',
     ['Unicast goes to all hosts, broadcast to one host', 'Multicast goes to every host on the internet', 'Broadcasts are forwarded by routers by default'],
     'Broadcasts stop at the router. Multicast lets one sender reach many receivers without a copy per receiver.'),
  ], []),
  ('Routers and ARP: getting to other networks', [
   Q('What does the TTL field in the IP header do?', 'Each router decreases it by 1 and drops the packet at 0, so a looping packet can\'t circulate forever', ['It sets how long a TCP session can last', 'It holds the packet\'s priority', 'It tells the switch how long to keep the MAC entry'],
     'When TTL reaches 0 the router sends back ICMP Time Exceeded, which is what traceroute uses.'),
   Q('A router receives a packet for a host on one of its connected subnets but has no ARP entry for that host. What does it do?', 'Holds the packet and sends an ARP request out that interface, then forwards once it gets the reply',
     ['Drops the packet', 'Floods the packet out all interfaces', 'Sends the packet to its default route'],
     'The same happens for a next-hop router address. After the first exchange, ARP and MAC tables are built and later packets flow without delay.'),
   Q('What is the main difference between a router and a Layer 3 switch?', 'Both route between subnets, but a Layer 3 switch has many Ethernet ports and routes in hardware, while a router supports more interface types such as WAN and cellular',
     ['A Layer 3 switch can\'t route', 'Routers can\'t use Ethernet', 'Layer 3 switches forward broadcasts between subnets'],
     'Inside a campus, Layer 3 switches usually do inter-VLAN routing. Routers sit at the WAN and internet edge.'),
  ], []),
 ],
 'IPv4 Addressing and Subnetting': [
  (None, [
   Q('What is 159 in binary?', '10011111', ['10010111', '11011111', '10011110'], '128 + 16 + 8 + 4 + 2 + 1 = 159. Work left to right through 128 64 32 16 8 4 2 1, subtracting as you go.'),
   Q('What is 11000000.10101000.00001010.00000001 in dotted decimal?', '192.168.10.1', ['192.168.10.129', '192.172.10.1', '193.168.10.1'], '11000000 = 192, 10101000 = 168, 00001010 = 10, 00000001 = 1.'),
   Q('Which address class has a first octet of 128–191 and a default mask of 255.255.0.0?', 'Class B', ['Class A', 'Class C', 'Class D'],
     'A: 1–126, /8. B: 128–191, /16. C: 192–223, /24. D: 224–239, multicast. E: 240–255, experimental. 127 is loopback.', card='Give the first-octet range and default mask for classes A, B and C, and what D and E are for.'),
   Q('What does CIDR allow?', 'Any prefix length, not just the class defaults (/8, /16, /24), for subnetting and summarisation', ['Only classful masks', 'IPv6 addressing only', 'Automatic address assignment'],
     'Classless Inter-Domain Routing is why we write /27 or /20 and why a /22 summary works.'),
   Q('When carving one block into subnets of different sizes (VLSM), what order should you allocate them in?', 'Largest subnet first, then the next largest, working down', ['Smallest first', 'Alphabetical order', 'Any order; it doesn\'t matter'],
     'Allocating the biggest blocks first keeps every subnet on a proper boundary and avoids gaps and overlaps.'),
   Q('You need subnets of 1,000 hosts from 10.0.0.0/8. What mask and block size do you use, and what is the second subnet?', '255.255.252.0 (/22), block of 4 in the third octet; second subnet is 10.0.4.0/22',
     ['255.255.255.0, block 1; second subnet 10.0.1.0', '255.255.248.0, block 8; second subnet 10.0.8.0', '255.255.252.0, block 4; second subnet 10.0.3.0'],
     '1,000 hosts need 10 host bits (1,022 usable): /22. The interesting octet is the third, 256 − 252 = 4, so 10.0.0.0, 10.0.4.0, 10.0.8.0 ...'),
  ], [P('Binary in one line: write 128 64 32 16 8 4 2 1, and put a 1 under each value you use. 159 = 128 + 16 + 8 + 4 + 2 + 1 = 10011111.'),
      TB(['Class', 'First octet', 'Default mask', 'Use'], ['A', '1–126', '/8', 'Large networks'], ['B', '128–191', '/16', 'Medium'], ['C', '192–223', '/24', 'Small'], ['D', '224–239', '—', 'Multicast'], ['E', '240–255', '—', 'Experimental']),
      P('Classes are history now (CIDR lets any prefix be used), but they still explain default masks and old documentation.'),
      TIP('The Subnetting drill (top menu) generates endless practice questions with worked answers using this same block-size method.')], 'Binary, classes and VLSM'),
 ],
 'IPv6 Addressing': [
  ('Getting an address automatically', [
   Q('What does "ipv6 enable" on a router interface do on its own?', 'Creates only a link-local address on the interface', ['Creates a global address by SLAAC', 'Turns on IPv6 routing globally', 'Starts DHCPv6'],
     'Use "ipv6 address autoconfig" to make an interface a SLAAC client, or "ipv6 address <prefix> eui-64" / a full address for a static one.'),
   Q('Why was IPv6 created?', 'IPv4\'s 32-bit address space (about 4.3 billion addresses) ran out; IPv6 has 128 bits', ['To replace Ethernet', 'Because IPv4 couldn\'t do routing', 'To remove the need for DNS'],
     'NAT and private addresses stretched IPv4, but IPv6 removes the shortage and the need for NAT.'),
  ], []),
 ],
 'DHCP Server, Client and Relay': [
  ('DHCP relay', [
   Q('Besides DHCP, what else does "ip helper-address" forward by default?', 'Several other UDP broadcast services, such as TFTP, DNS, TACACS, time and NetBIOS', ['Nothing else', 'All TCP traffic', 'OSPF hellos'],
     'IOS forwards a default set of UDP ports. "no ip forward-protocol udp <port>" removes any you don\'t want relayed.'),
  ], []),
 ],
 'Wireless Principles': [
  (None, [
   Q('What is the difference between an SSID and a BSSID?', 'The SSID is the network name users see; the BSSID is the MAC address that identifies one AP radio serving that SSID', ['They are the same thing', 'The BSSID is the password', 'The SSID is the AP\'s IP address'],
     'One AP can broadcast several SSIDs (each with its own BSSID), each mapped to its own VLAN and security settings.'),
   Q('What is an ESS?', 'Several APs sharing the same SSID so clients can roam between them', ['A single AP and its clients', 'Two laptops connected directly', 'A wired switch stack'],
     'BSS = one AP and its clients. ESS = several BSSs on the same SSID joined by the wired distribution system.'),
   Q('Two laptops connect directly to each other with no AP. What is this called?', 'An ad hoc network (IBSS)', ['Infrastructure mode', 'An ESS', 'A mesh BSS'],
     'Infrastructure mode uses an AP. Ad hoc (Independent BSS) is peer-to-peer.'),
   Q('Why is Wi-Fi described as half duplex?', 'Only one device can transmit on a channel at a time, so devices take turns', ['APs can only receive', 'Wi-Fi only works in one direction', 'Each client gets its own channel'],
     'Devices use CSMA/CA to avoid collisions. More clients on a channel means less airtime each.'),
  ], [TB(['Term', 'Meaning'], ['SSID', 'Network name, e.g. Corporate'], ['BSSID', 'MAC address of the AP radio for that SSID'], ['BSS', 'One AP and its clients'], ['ESS', 'Several APs with the same SSID; clients roam'],
         ['IBSS (ad hoc)', 'Devices connect directly, no AP'], ['Distribution system', 'The wired network joining the APs'])], 'Wireless building blocks'),
 ],
 'EtherChannel, Routed Ports and SVIs': [
  ('Rules and troubleshooting', [
   Q('How can one server or access switch run an EtherChannel to two separate upstream switches?', 'Use multi-chassis EtherChannel, where the two upstream switches act as one (StackWise, VSS or vPC)',
     ['It is impossible', 'Configure two separate port channels and let STP block one', 'Use PAgP desirable mode'],
     'Normally a port channel must end on one switch. Stacking or virtual-switch technologies make two switches look like one, so all links forward with no STP blocking.'),
  ], []),
 ],
 'Rapid PVST+ Spanning Tree': [
  ('Rapid PVST+', [
   Q('Match the standards: 802.1D, 802.1w and 802.1s.', '802.1D is the original STP, 802.1w is Rapid STP, 802.1s is Multiple STP (MST)',
     ['802.1D is RSTP, 802.1w is MST, 802.1s is STP', '802.1D is MST, 802.1w is STP, 802.1s is RSTP', 'All three are Cisco proprietary'],
     'PVST+ (Cisco) runs 802.1D per VLAN; Rapid PVST+ runs 802.1w per VLAN.', card='What are 802.1D, 802.1w and 802.1s?'),
   Q('Which spanning tree version maps groups of VLANs onto a small number of tree instances?', 'MST (802.1s)', ['PVST+', 'Rapid PVST+', '802.1D'],
     'Per-VLAN versions run one tree per VLAN, which uses more CPU on switches with hundreds of VLANs. MST groups them.'),
  ], []),
  ('PortFast and the guards', [
   Q('In "show spanning-tree vlan 10", a port shows "Altn BLK". What does it mean?', 'It is an alternate port, discarding traffic as a backup path to the root', ['It is the root port', 'It is err-disabled', 'It is a designated port forwarding traffic'],
     'Other abbreviations: Root FWD, Desg FWD, Back BLK (backup). "This bridge is the root" appears on the root switch.'),
  ], []),
 ],
 'Routing Tables and Static Routes': [
  ('How the router chooses', [
   Q('What is the difference between administrative distance and metric?', 'AD chooses between different route sources (for example OSPF vs static); metric chooses between paths learned by the same source',
     ['They are the same thing', 'Metric chooses between sources; AD between paths', 'AD only applies to static routes'],
     'An OSPF cost can\'t be compared with a RIP hop count, so AD decides which source to trust first.'),
   Q('A router has two static routes to 10.50.0.0/16 with the same AD, via two different next hops. What happens?', 'Both are installed and traffic is load-balanced across them (equal-cost multipath)', ['Only the first configured is used', 'Neither is installed', 'The command is rejected'],
     'Routing protocols do the same for equal-cost paths. A floating static uses a higher AD precisely to avoid this.'),
   Q('What is the difference between a distance vector and a link-state routing protocol?', 'Distance vector routers share their route lists with neighbours ("routing by rumour"); link-state routers share descriptions of their links so every router builds a full map',
     ['Link-state protocols use hop count only', 'Distance vector protocols flood LSAs', 'They are the same'],
     'RIP is distance vector, EIGRP is advanced distance vector, OSPF and IS-IS are link-state, BGP is path vector.'),
   Q('Which protocol is the exterior gateway protocol used between organisations on the internet?', 'BGP', ['OSPF', 'EIGRP', 'RIP'],
     'IGPs (OSPF, EIGRP, IS-IS, RIP) route inside an organisation; BGP routes between them.'),
  ], []),
 ],
 'Single-Area OSPFv2 and OSPFv3': [
  ('Neighbours and adjacencies', [
   Q('Which OSPF packet type do neighbours use to summarise the contents of their link-state databases to each other?', 'Database Description (DBD)', ['Hello', 'Link State Request (LSR)', 'Link State Acknowledgement'],
     'Hello finds neighbours; DBD summarises the database; LSR asks for missing entries; LSU carries the LSAs; LSAck confirms them.'),
   ORD('Put the five OSPF packet types in the order they are first used when two routers meet.', ['Hello', 'Database Description (DBD)', 'Link State Request (LSR)', 'Link State Update (LSU)', 'Link State Acknowledgement (LSAck)'],
     'LSAs are not a packet type of their own; they travel inside LSUs.', card='Name the five OSPF packet types and what each does.'),
   Q('At which neighbour state is the DR and BDR elected?', '2-Way', ['Init', 'ExStart', 'Full'], 'Once routers see each other in hellos (2-Way), the election happens before database exchange starts.'),
  ], []),
  ('Broadcast networks and the DR', [
   Q('On a broadcast segment, a DROTHER notices a link change. Where does it send its LSU?', 'To 224.0.0.6 (DR and BDR), and the DR then floods it to 224.0.0.5 (all OSPF routers)', ['Directly to every router on 224.0.0.5', 'By unicast to the BDR only', 'To 255.255.255.255'],
     'Funnelling updates through the DR cuts down flooding on segments with many routers.'),
  ], []),
  ('How OSPF works', [
   Q('What is OSPF area 0, and why can a small network put every router in it?', 'Area 0 is the backbone area; small networks don\'t need the extra hierarchy, so a single area 0 is fine',
     ['Area 0 is reserved for stub routers', 'Every router must be in a different area', 'Area 0 can only contain two routers'],
     'Large networks split into areas joined to area 0 to limit database size and SPF runs. The CCNA only needs single-area OSPF.'),
  ], []),
 ],
 'First Hop Redundancy: HSRP and VRRP': [
  ('Reading the status', [
   Q('Distribution switch D1 is the spanning-tree root for VLAN 10. Which switch should be HSRP active for VLAN 10, and why?', 'D1, so hosts\' traffic takes the most direct Layer 2 path to the gateway', ['D2, to spread the load', 'Either; it makes no difference', 'Neither; HSRP should be off where STP runs'],
     'If STP and HSRP disagree, traffic crosses an extra link to reach the active gateway. Align them per VLAN.'),
   Q('How can both routers forward traffic with HSRP, which only has one active router per group?', 'Use two groups (for example per VLAN), making each router active for a different one', ['Enable pre-emption on both', 'Give both routers priority 255', 'Use HSRP version 2'],
     'This splits the load. GLBP can load-balance inside a single group.'),
  ], []),
 ],
 'Device Access, AAA and Secure File Transfer': [
  ('Local users and SSH', [
   Q('A router has both "enable password" and "enable secret" configured. Which is used?', 'The enable secret; the enable password is ignored', ['The enable password', 'Whichever was configured last', 'Both must be entered'],
     'Only configure the secret. The plain enable password is shown in clear text in the config.'),
   Q('What does "service password-encryption" do, and why isn\'t it enough on its own?', 'It hides clear-text passwords in the config with type 7 encryption, which is easily reversed',
     ['It hashes all passwords with SHA-256', 'It encrypts SSH traffic', 'It encrypts the whole configuration file'],
     'It stops shoulder-surfing, nothing more. Use "secret" commands for real protection.'),
   Q('By default, what privilege level does a local user get, and which level gives full access?', 'Level 1 by default; level 15 is full access', ['Level 0 by default; level 1 is full', 'Level 15 by default', 'Level 5 by default; level 10 is full'],
     'Levels run 0–15. Use "username admin privilege 15 secret ..." for administrators.'),
   Q('What is the difference between "login" and "login local" on a line?', '"login" checks the line\'s own password; "login local" checks usernames in the local database', ['They are the same', '"login local" uses RADIUS', '"login" disables passwords'],
     'With AAA (aaa new-model) on, method lists replace both.'),
   Q('Which two hardening steps are good practice on a router?', ['Disable unused services such as the HTTP server', 'Show a legal warning with a login banner'], ['Enable Telnet on all VTY lines', 'Use the same password for every device'],
     'Also: SSH only, exec-timeout, access-class on VTY lines, NTP for accurate logs, and turning off CDP where it isn\'t needed.'),
  ], []),
 ],
 'DNS Records': [
  ('Diagnosing record problems', [
   Q('Which IOS command creates a static name-to-address entry on the router itself?', 'ip host SERVER1 10.1.1.10', ['ip name-server SERVER1 10.1.1.10', 'ip dns record SERVER1 10.1.1.10', 'hostname SERVER1 10.1.1.10'],
     '"ip name-server" points the router at a DNS server; "ip dns server" makes the router answer DNS queries itself.'),
   Q('What does "ip domain-name example.com" do on a router?', 'Sets the router\'s default domain, which is also needed to generate RSA keys for SSH', ['Makes the router a DNS server', 'Registers the router in public DNS', 'Blocks lookups for other domains'],
     'Unqualified names typed at the router are tried with this suffix added.'),
  ], []),
 ],
 'IPv4 Access Control Lists': [
  ('Verifying', [
   Q('An outbound ACL on R1\'s Gi0/1 denies all ICMP. Can you still ping out of Gi0/1 from R1 itself?', 'Yes; outbound ACLs don\'t filter traffic the router itself originates', ['No, the ping is blocked', 'Only with extended ping', 'Only if the ACL is standard'],
     'Packets generated by the router aren\'t checked against outbound interface ACLs, which can make testing misleading. Test from a host behind the router.'),
  ], []),
 ],
 'Layer 2 Security': [
  (None, [
   Q('In 802.1X port-based authentication, what are the three roles?', 'Supplicant (the client), authenticator (the switch or AP) and authentication server (usually RADIUS)', ['Client, router and DNS server', 'Supplicant, relay and DHCP server', 'Host, VLAN and controller'],
     'Until authentication succeeds, the switch port only passes authentication traffic (EAP over LAN).', card='Name the three 802.1X roles.'),
   Q('What does 802.1X add that port security can\'t?', 'It authenticates the user or device itself, not just its MAC address, so the port is useful wherever they plug in', ['It encrypts all traffic on the port', 'It stops spanning tree loops', 'It replaces DHCP'],
     'MAC addresses are easy to spoof. 802.1X ties access to credentials or certificates, and the server can assign the VLAN.'),
  ], [P('802.1X is the next step up from port security: a port passes only authentication traffic until the user or device proves who it is to a RADIUS server.'),
      UL('Supplicant: the client software on the PC.', 'Authenticator: the switch (or AP) that relays EAP messages.', 'Authentication server: RADIUS (for example Cisco ISE), which can also assign the VLAN.')], '802.1X (related)'),
 ],
 'SNMP and Syslog': [
  ('Configuring logging', [
   Q('Which SNMPv3 configuration order is correct?', 'Create a group with its security level (snmp-server group NAME v3 priv), then a user in that group with auth and priv passwords',
     ['Create a community string, then a user', 'Create a user first, then enable v2c', 'Only "snmp-server enable traps" is needed'],
     'Example: snmp-server group NMS v3 priv, then snmp-server user nms1 NMS v3 auth sha <pass> priv aes 128 <pass>.'),
   Q('What is the main difference between syslog and SNMP for monitoring?', 'Syslog sends event messages as text; SNMP lets a manager poll counters and values (and receive traps)', ['Syslog uses TCP 161', 'SNMP can\'t send alerts', 'They are the same protocol'],
     'Most networks use both: SNMP for graphs and thresholds, syslog for what happened and when.'),
  ], []),
 ],
 'Management Approaches and Ansible': [
  ('Infrastructure as code', [
   Q('What is configuration drift?', 'Device configs slowly becoming inconsistent because of one-off manual changes over time', ['Clock differences between devices', 'Routes changing during convergence', 'IP addresses moving between DHCP leases'],
     'Automation and IaC fix drift by applying the same source of truth to every device.'),
   Q('Why is Git useful for network configurations?', 'It is version control: every change is recorded with who and why, and you can compare or roll back', ['It pushes configs to devices by itself', 'It replaces SSH', 'It encrypts device passwords'],
     'Git is distributed: every copy holds the full history. GitHub and similar services host shared repositories and reviews.'),
   Q('How do Puppet and Chef traditionally differ from Ansible?', 'Puppet and Chef use agents on managed devices that pull their config from a server; Ansible is agentless and pushes over SSH', ['They are agentless', 'They use YAML playbooks', 'They only work on Cisco routers'],
     'Puppet uses its own manifest language; Chef uses Ruby recipes and cookbooks.'),
  ], []),
 ],
}

# Flackbox section pointers for every original lesson
REFS = {
 'Networking Fundamentals': ['03 Host to Host Communications (OSI model, TCP/IP stack)', '05 OSI Layer 4 - The Transport Layer', '06 OSI Layer 3 (IP header, unicast/broadcast/multicast)', '09 OSI Layer 2', '11 Cisco Device Functions', '12 The Life of a Packet (DNS, ARP, routed traffic)'],
 'Cables and Interface Problems': ['10 OSI Layer 1 - Ethernet Connection Media', '14-04 Speed and Duplex Settings', '14-06 Basic Layer 1 and Layer 2 Troubleshooting'],
 'Virtualization and Containers': ['36-05 Server Virtualization', '36-06 Virtualizing Network Devices'],
 'IPv4 Addressing and Subnetting': ['06 Decimal to binary, IPv4 addresses, subnet mask, slash notation', '07 IP Address Classes', '08 Subnetting (CIDR, VLSM, written examples, private addresses)', 'Your Subnetting.xlsx block-size sheet'],
 'IPv6 Addressing': ['30 IPv6 Addressing and Routing (format, global unicast, EUI-64, link-local, SLAAC)'],
 'DHCP Server, Client and Relay': ['23 DHCP (Cisco DHCP server, external server, Cisco DHCP client)'],
 'Client Connectivity Troubleshooting': ['12-04 ARP (host ARP commands)', '18 Connectivity Troubleshooting'],
 'Wireless Principles': ['37 Wireless Fundamentals (network types, APs, channels, security)'],
 'VLANs, Trunks and Edge Ports': ['21 VLANs (access ports, trunk ports, DTP)', '37-05 Switch Configuration for Wireless Networks'],
 'EtherChannel, Routed Ports and SVIs': ['22 Inter-VLAN Routing (router on a stick, Layer 3 switch)', '26 EtherChannel (load balancing, protocols, StackWise/VSS/vPC, Layer 3 EtherChannel)'],
 'Rapid PVST+ Spanning Tree': ['25 STP (terminology, how it works, versions, show spanning-tree, root election, PortFast/BPDU guard/root guard)'],
 'CDP, LLDP and Troubleshooting Tools': ['14-05 CDP and LLDP', '18 Connectivity Troubleshooting (ping, extended ping, traceroute)', '25-08 show mac address-table'],
 'Routing Tables and Static Routes': ['16 Routing Fundamentals (connected/local routes, static, summarisation, default)', '17 Dynamic Routing Protocols (types, metrics, ECMP, administrative distance)'],
 'Single-Area OSPFv2 and OSPFv3': ['20 OSPF (characteristics, configuration, router ID, areas, cost, adjacencies, DR/BDR)', '17-13 Adjacencies and Passive Interfaces', '30-10 IPv6 Static Routes'],
 'First Hop Redundancy: HSRP and VRRP': ['24 HSRP (FHRPs, priority, pre-emption, versions)', '25-10 Spanning Tree and HSRP Alignment'],
 'Device Access, AAA and Secure File Transfer': ['33 Cisco Device Security (line security, enable secret, privilege levels, SSH, AAA, best practices)', '15-06 Backing up the System Image', '15-07 Upgrading IOS'],
 'NAT and PAT': ['29 NAT (static, dynamic, PAT, inside/outside terms)'],
 'DNS Records': ['12-02 DNS', '12-03 DNS on Cisco Routers'],
 'IPv4 Access Control Lists': ['28 ACLs (overview, standard/extended/named, syntax, operations)'],
 'Layer 2 Security': ['27 Switch Security (DHCP snooping, DAI, 802.1X, port security)'],
 'IPsec VPNs': ['32-06 Cryptography', '32-08 Site-to-Site VPNs', '32-09 Remote Access VPNs', '31-03 VPN'],
 'SNMP and Syslog': ['34 Network Device Management (syslog, terminal monitor, SNMP, SNMPv3, syslog vs SNMP)'],
 'Management Approaches and Ansible': ['38-02 Benefits of Automation', '38-03 Python, Git, GitHub and CI/CD', '38-08 Ansible, Puppet and Chef', '38-10 SDN', '38-11 Cisco DNA Center'],
 'AI in Network Operations': [],
}


def apply(secs):
    by = {s['name']: s for s in secs}
    # insert IOS section after Networking Fundamentals
    i = [s['name'] for s in secs].index('Networking Fundamentals')
    secs.insert(i + 1, IOS_SEC)
    for name, adds in ADD.items():
        s = by[name]
        parts = s['lesson']['parts']
        for item in adds:
            ph, newq, blocks = item[0], item[1], item[2]
            start = len(s['qs'])
            s['qs'].extend(newq)
            ck = CK(*range(start, start + len(newq)))
            if ph is None:
                title = item[3]
                # new part before the final part
                parts.insert(len(parts) - 1 if len(parts) > 1 else len(parts), {'h': title, 'b': blocks + [ck]})
            else:
                p = next(p for p in parts if p['h'] == ph)
                # put new text before the part's last check block
                p['b'][-1:-1] = blocks
                p['b'].append(ck)
    for name, refs in REFS.items():
        if refs: by[name]['lesson']['course'] = refs
    return secs
