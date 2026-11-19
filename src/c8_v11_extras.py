"""Topics on CCNA v1.1 (exam until Feb 2, 2027) that v2.0 no longer names. Optional."""
from h import *

S = []
G = 'v1.1 Extras (not on v2.0)'
V11 = 'Optional: this topic is on the CCNA v1.1 exam (last day February 2, 2027) but is not named in v2.0. Skip it if you are sitting v2.0. '

# ------------------------------------------------------------------ architectures + WAN + cloud
qs = [
 Q('In a three-tier campus design, which layer do end devices connect to?', 'Access', ['Distribution', 'Core', 'Spine'], 'Access: many affordable ports and edge security. Distribution: aggregation and policy. Core: fast transport between distribution blocks.'),
 Q('What is a collapsed core (two-tier) design?', 'The distribution and core layers are combined into one pair of switches', ['The access layer is removed', 'All switches are in one stack', 'Routers replace the core'],
   'Smaller campuses don\'t need a separate core. Add one when there are several distribution blocks.'),
 Q('Which layer should avoid heavy policy such as complex ACLs and QoS so it can switch as fast as possible?', 'Core', ['Access', 'Distribution', 'All layers equally'], 'The core\'s job is speed and resilience. Policy lives in distribution (and security in access).'),
 Q('In a spine-leaf data centre design, how are switches connected?', 'Every leaf connects to every spine; leaves never connect to each other and spines never connect to each other',
   ['Leaves connect in a ring', 'Spines connect only to one leaf each', 'Every switch connects to every other switch'],
   'Any server is the same number of hops from any other (leaf, spine, leaf), which suits heavy east-west traffic.'),
 Q('Which WAN topology connects every branch only to the head office?', 'Hub and spoke', ['Full mesh', 'Partial mesh', 'Point-to-point ring'],
   'Cheapest and simplest; branch-to-branch traffic goes via the hub. Full mesh connects every site to every other.'),
 Q('What does MPLS give an enterprise WAN?', 'A provider network that forwards on labels and keeps each customer\'s traffic separate, connecting all sites as one private network',
   ['Encryption of all traffic by default', 'Free internet access', 'A wireless WAN'],
   'MPLS L3VPN is private but not encrypted. Internet VPNs (IPsec) are cheaper and encrypted but have no performance guarantees.'),
 Q('What is PPPoE used for?', 'Carrying PPP sessions over Ethernet, typically for DSL or fibre internet with username/password authentication', ['Powering IP phones', 'Running OSPF over the WAN', 'Encrypting VPN traffic'],
   'On the router: a dialer interface with "encapsulation ppp", "ip address negotiated" and the ISP credentials (PAP or CHAP).'),
 Q('Which two are characteristics of a leased line?', ['A dedicated point-to-point link between two sites', 'Fixed bandwidth that is not shared with other customers'], ['It is always the cheapest WAN option', 'It connects many sites over one shared cloud'],
   'Reliable and private, but expensive and inflexible compared with MPLS or internet VPN.', card='Give two characteristics of a leased line.'),
 Q('Which cloud service model gives the customer virtual machines, storage and networks to manage from the operating system up?', 'IaaS', ['PaaS', 'SaaS', 'On-premises'],
   'IaaS: you manage the OS and above. PaaS: you deploy code onto a managed platform. SaaS: you just use the application (for example Microsoft 365).'),
 Q('A company uses Salesforce through a web browser and manages nothing underneath. Which model is this?', 'SaaS', ['IaaS', 'PaaS', 'Private cloud'], 'The provider runs the whole stack; the customer just uses it.'),
 Q('Which deployment model combines an organisation\'s private cloud or data centre with a public cloud?', 'Hybrid cloud', ['Community cloud', 'Public cloud', 'Colocation'],
   'Community clouds are shared by organisations with common needs, such as government departments.'),
 Q('Which five traits does NIST use to define cloud computing?', ['On-demand self-service', 'Broad network access', 'Resource pooling', 'Rapid elasticity', 'Measured service'], ['Fixed long-term contracts', 'Dedicated hardware per customer'],
   'If a hosting service lacks these (for example you must phone to get a server), it isn\'t really cloud.', card='List NIST\'s five essential characteristics of cloud computing.'),
 Q('What does a SOHO network usually consist of?', 'One small multifunction device acting as router, switch, wireless AP and firewall, with an internet connection', ['A three-tier campus', 'A spine-leaf fabric', 'An MPLS core'],
   'Small office/home office: a single box does everything.'),
]
L = lesson(12, V11 + 'This lesson covers network architectures (two- and three-tier campus, spine-leaf, WAN and SOHO) and cloud computing.',
 [
  ('Campus and data centre designs', [
    TB(['Layer', 'Job'], ['Access', 'Where users and devices connect; port density; edge security (port security, 802.1X)'], ['Distribution', 'Aggregates access switches; routing between VLANs; policy'],
       ['Core', 'Fast, resilient transport between distribution blocks; minimal policy']),
    UL('Collapsed core (two-tier): distribution and core combined. Fine for one building.', 'Spine-leaf: every leaf to every spine, so every server is two switch hops from any other. Built for east-west data-centre traffic.', 'SOHO: one router/switch/AP/firewall box.'),
    CK(0, 1, 2, 3, 12)]),
  ('WAN options', [
    TB(['Option', 'Notes'], ['Leased line', 'Dedicated point-to-point, fixed bandwidth, expensive'], ['MPLS', 'Provider label-switched network, private between your sites, can offer QoS'],
       ['Internet VPN', 'IPsec over broadband or fibre; cheap, encrypted, no guarantees'], ['Metro Ethernet', 'Provider Ethernet service across a city'], ['PPPoE', 'PPP over Ethernet for DSL/fibre internet with login']),
    UL('Hub and spoke: branches connect only to the hub.', 'Full mesh: every site to every other site.', 'Partial mesh: somewhere in between.', 'Single-homed / dual-homed / multihomed: one link, two links to one provider, or links to two providers.'),
    CK(4, 5, 6, 7)]),
  ('Cloud computing', [
    TB(['Model', 'You manage', 'Example'], ['IaaS', 'OS, middleware, apps, data', 'AWS EC2, Azure VMs'], ['PaaS', 'Your apps and data', 'Google App Engine'], ['SaaS', 'Just your data and users', 'Microsoft 365, Salesforce']),
    UL('Deployment: public, private, hybrid, community.', 'NIST traits: on-demand self-service, broad network access, resource pooling, rapid elasticity, measured service.',
       'Reaching the cloud: internet, internet VPN, or a private connection (for example Azure ExpressRoute or AWS Direct Connect).'),
    CK(8, 9, 10, 11)]),
 ],
 [('v1.1 1.2', 'Describe characteristics of network topology architectures (2-tier, 3-tier, spine-leaf, WAN, SOHO, on-premises and cloud)'), ('v1.1 1.2.f', 'On-premises and cloud')])
L['course'] = ['21-02 Campus Design', '21-03 Spine-Leaf Network Design', '31 WAN (overview, connectivity options, leased lines, MPLS, PPPoE, topologies)', '36 Cloud Computing']
S.append(sec('Network Architectures, WAN and Cloud', 'Architectures', G, '', L, qs))

# ------------------------------------------------------------------ security concepts
qs = [
 Q('Match the terms: a weakness in a system, something that takes advantage of it, and anything that could cause harm.', 'Vulnerability, exploit, threat', ['Threat, vulnerability, exploit', 'Exploit, threat, vulnerability', 'Risk, mitigation, threat'],
   'Mitigation reduces the chance or impact. Risk is the likelihood (and impact) of a successful attack.', card='Define threat, vulnerability, exploit and mitigation.'),
 Q('Which kind of malware spreads by itself across a network without any user action?', 'A worm', ['A virus', 'A Trojan horse', 'Adware'],
   'A virus needs a user to run something to spread. A Trojan pretends to be legitimate software. Ransomware encrypts data and demands payment.'),
 Q('An attacker phones the help desk pretending to be a manager and asks for a password reset. What kind of attack is this?', 'Social engineering', ['Denial of service', 'MAC flooding', 'Brute force'],
   'Phishing is social engineering by email; spear phishing targets specific people; whaling targets executives; vishing is by phone.'),
 Q('What is a DDoS attack?', 'Many compromised machines (a botnet) flood a target to make a service unavailable', ['A single packet that crashes a router', 'An attacker reading traffic between two hosts', 'Guessing passwords from a dictionary'],
   'A DoS comes from one source; a distributed DoS comes from many, so blocking one address doesn\'t stop it.'),
 Q('What is a man-in-the-middle attack?', 'The attacker secretly relays (and can read or change) traffic between two parties', ['The attacker floods a server', 'The attacker tricks a user by phone', 'The attacker installs ransomware'],
   'ARP spoofing on a LAN is a classic way in. DAI and encryption defend against it.'),
 Q('Which three are security program elements?', ['User awareness', 'Training', 'Physical access control'], ['Spanning tree', 'OSPF authentication', 'VLAN numbering'],
   'Awareness: regular reminders such as phishing tests. Training: formal courses. Physical access: badges, locks, cameras.', card='Name the three security program elements.'),
 Q('What does multi-factor authentication require?', 'Two or more different kinds of proof: something you know, something you have, something you are', ['Two passwords', 'A password changed every day', 'A password and a username'],
   'Two passwords are the same factor twice. A password plus a phone code or a fingerprint is MFA.'),
 Q('Which is the stronger password policy element?', 'Long passphrases, checked against breached-password lists, with MFA', ['Short complex passwords changed weekly', 'The same strong password everywhere', 'Passwords written under the keyboard'],
   'Length beats complexity. Forced frequent changes tend to produce weak, predictable passwords.'),
 Q('How does a stateful firewall differ from a simple ACL (packet filter)?', 'It tracks connections and automatically allows the return traffic for sessions started from the inside', ['It only filters by MAC address', 'It doesn\'t inspect traffic', 'It needs a separate rule for every return packet'],
   'An ACL judges every packet on its own. A stateful firewall knows a reply belongs to an existing session.'),
 Q('What is the difference between an IDS and an IPS?', 'An IDS watches a copy of the traffic and alerts; an IPS sits inline and can block attacks', ['An IPS only alerts', 'An IDS sits inline', 'They are identical'],
   'Both use signatures and anomaly detection. Next-generation firewalls build IPS, application awareness and user identity in.'),
 Q('Which statement about symmetric and asymmetric encryption is true?', 'Symmetric uses one shared key and is fast; asymmetric uses a public/private key pair and is slower, so it\'s often used to exchange the symmetric key',
   ['Asymmetric is faster', 'Symmetric uses a public key', 'Asymmetric keys must both be kept secret'],
   'AES is symmetric. RSA and elliptic-curve are asymmetric. TLS and IPsec use asymmetric methods to agree a symmetric session key.'),
 Q('In HTTPS, how does your browser know a website\'s certificate is genuine?', 'The certificate is signed by a certificate authority the browser already trusts', ['The website sends its private key', 'DNS confirms it', 'The browser asks the user every time'],
   'This is PKI. The CA vouches that the public key belongs to that site.'),
 Q('Which two are digital certificate or PKI elements?', ['A certificate authority (CA)', 'A public/private key pair'], ['A community string', 'A VLAN tag'], 'Certificates bind an identity to a public key, signed by a CA.'),
]
L = lesson(12, V11 + 'This lesson covers core security concepts: threats and attacks, security programmes, passwords and MFA, firewalls and IPS, and cryptography basics.',
 [
  ('Threats and attacks', [
    TB(['Term', 'Meaning'], ['Threat', 'Something that could cause harm'], ['Vulnerability', 'A weakness'], ['Exploit', 'A way of using the weakness'], ['Mitigation', 'Reducing likelihood or impact'], ['Risk', 'Likelihood and impact of a successful attack']),
    UL('Malware: virus (needs user action), worm (self-spreading), Trojan (disguised), ransomware (encrypts and extorts).', 'Social engineering: phishing, spear phishing, whaling, vishing, tailgating.',
       'DoS / DDoS: overwhelm a service. Man-in-the-middle: intercept and relay. Reconnaissance: ping sweeps, port scans, public searching.', 'Spoofing: faking a MAC, IP or identity. Password attacks: brute force, dictionary.'),
    CK(0, 1, 2, 3, 4)]),
  ('Security programmes and passwords', [
    UL('Security program elements: user awareness, training, physical access control.', 'Password policy: length and passphrases, no reuse, check against breached lists, lockout after failed attempts.',
       'MFA: something you know + something you have + something you are.', 'Certificates and biometrics are alternatives to passwords.'),
    CK(5, 6, 7)]),
  ('Firewalls, IPS and cryptography', [
    UL('Stateful firewall: tracks sessions; return traffic for inside-initiated sessions is allowed automatically.', 'IDS: alerts on a copy of traffic. IPS: inline, blocks.', 'Next-generation firewall: adds application control, IPS and user identity.',
       'Symmetric encryption: one shared key (AES), fast. Asymmetric: key pair (RSA, ECC), slower, used for key exchange and signatures.', 'PKI: a CA signs certificates so you can trust a site\'s public key (HTTPS/TLS).'),
    CK(8, 9, 10, 11, 12)]),
 ],
 [('v1.1 5.1', 'Define key security concepts (threats, vulnerabilities, exploits, mitigation)'), ('v1.1 5.2', 'Describe security program elements'), ('v1.1 5.4', 'Describe security password policy elements and alternatives')])
L['course'] = ['32 Security Threat Landscape (threats, common attacks, firewalls and IDS, cryptography, TLS, threat defense)']
S.append(sec('Security Concepts', 'Sec Concepts', G, '', L, qs))

# ------------------------------------------------------------------ QoS, NTP, TFTP/FTP
qs = [
 Q('Which traffic type is most sensitive to delay, jitter and loss?', 'Voice', ['Email', 'File backup', 'Software updates'],
   'Voice targets: one-way delay under 150 ms, jitter under 30 ms, loss under 1%. It also uses little bandwidth, so priority queuing suits it.'),
 Q('Which DSCP marking is normally used for voice packets?', 'EF (DSCP 46)', ['AF41 (DSCP 34)', 'CS1 (DSCP 8)', 'Default (DSCP 0)'],
   'EF = Expedited Forwarding. Video often uses AF41; scavenger traffic CS1; normal traffic DSCP 0.'),
 Q('Where is the CoS marking carried, and how big is it?', 'In the 802.1Q tag, 3 bits (values 0–7)', ['In the IP header, 6 bits', 'In the TCP header, 8 bits', 'In the Ethernet FCS'],
   'CoS (802.1p) only exists on trunks. DSCP is 6 bits in the IP header and survives across routers.'),
 Q('What is a trust boundary?', 'The point where the network starts trusting the QoS markings on incoming packets, usually the access switch port or IP phone', ['The firewall\'s outside interface', 'The DHCP server', 'The VLAN 1 SVI'],
   'Marks from untrusted devices are rewritten. Cisco IP phones are commonly trusted, with the PC behind them re-marked.'),
 Q('Which queuing method gives voice a strict priority queue while sharing the rest of the bandwidth fairly by class?', 'LLQ (low latency queuing)', ['FIFO', 'WRED', 'Round robin only'],
   'LLQ = CBWFQ plus a policed strict-priority queue, so voice goes first but can\'t starve everything else.'),
 Q('What is the difference between policing and shaping?', 'Policing drops (or re-marks) traffic over the rate immediately; shaping buffers the excess and sends it later', ['Shaping drops traffic', 'Policing buffers traffic', 'They are the same'],
   'Shaping smooths traffic to match a slower WAN rate; providers police at their edge.'),
 Q('What does WRED do?', 'Randomly drops some lower-priority TCP packets as a queue fills, before it is completely full, to avoid global synchronisation', ['Prioritises voice', 'Marks packets with DSCP', 'Encrypts queued traffic'],
   'Early drops make some TCP senders slow down gradually instead of all at once.'),
 Q('What is the NTP stratum?', 'The distance from an authoritative time source: stratum 1 is directly attached to a reference clock, and each hop adds 1', ['The NTP version', 'The accuracy in milliseconds', 'The number of NTP clients'],
   'A router using "ntp master 3" claims stratum 3. Clients prefer lower stratum sources.'),
 Q('Which command makes a router an NTP client of 10.0.0.1?', 'ntp server 10.0.0.1', ['ntp master 10.0.0.1', 'ntp peer 10.0.0.1 server', 'clock set ntp 10.0.0.1'],
   '"ntp master [stratum]" makes the router an authoritative server from its own clock. "show ntp status" and "show ntp associations" verify.'),
 Q('Which statement compares TFTP and FTP correctly?', 'TFTP uses UDP 69 with no authentication; FTP uses TCP 20/21 with a username and password (sent in clear text)', ['TFTP uses TCP and encrypts', 'FTP uses UDP 69', 'Both encrypt data'],
   'Both are insecure. Use SCP or SFTP for anything that matters.'),
 Q('In active mode FTP, which side opens the data connection?', 'The server, from its port 20 to a port the client specified', ['The client, to server port 21', 'Neither; FTP uses one connection', 'The client, to server port 20'],
   'Passive mode (common through firewalls and NAT) has the client open the data connection to a port the server specifies.'),
 Q('Which two are reasons QoS is needed on a WAN link?', ['Real-time traffic suffers when the link is congested', 'Bandwidth on WAN links is limited and costly'], ['QoS increases the link speed', 'QoS replaces routing'],
   'QoS doesn\'t create bandwidth; it decides who goes first when there isn\'t enough.'),
]
L = lesson(12, V11 + 'This lesson covers QoS (classification, marking, queuing, policing and shaping), NTP, and TFTP/FTP.',
 [
  ('Why QoS, and marking', [
    P('When a link is congested, QoS decides which traffic goes first, which waits and which is dropped. Voice and video are the sensitive ones.'),
    TB(['Marking', 'Where', 'Size', 'Typical values'], ['CoS (802.1p)', '802.1Q tag', '3 bits (0–7)', 'Voice 5'], ['DSCP', 'IP header', '6 bits (0–63)', 'Voice EF 46, video AF41 34, scavenger CS1 8, default 0']),
    UL('Classification: identify traffic (ACL, NBAR, existing marks).', 'Marking: set CoS/DSCP so later devices don\'t need to reclassify.', 'Trust boundary: where markings start being trusted, usually the access port or IP phone.'),
    CK(0, 1, 2, 3, 11)]),
  ('Queuing, policing and shaping', [
    UL('Queuing: CBWFQ gives each class a share of bandwidth; LLQ adds a strict-priority queue for voice.', 'Congestion avoidance: WRED drops some TCP early so senders back off gradually.',
       'Policing: drops or re-marks traffic above a rate, immediately.', 'Shaping: buffers the excess and sends it later, smoothing to a target rate.'),
    CK(4, 5, 6)]),
  ('NTP, TFTP and FTP', [
    UL('NTP (UDP 123) keeps clocks in sync for logs and certificates. Stratum 1 = attached to a reference clock.', 'ntp server 10.0.0.1 (client); ntp master 3 (act as server); show ntp associations / status.',
       'TFTP: UDP 69, no login, small and simple (often used for IOS images in labs).', 'FTP: TCP 21 control, TCP 20 data (active mode); username and password in clear text.'),
    CK(7, 8, 9, 10)]),
 ],
 [('v1.1 4.2', 'Configure and verify NTP operating in client and server mode'), ('v1.1 4.7', 'Explain the forwarding per-hop behaviour (PHB) for QoS'), ('v1.1 4.9', 'Describe the capabilities and functions of TFTP/FTP in the network')])
L['course'] = ['35 QoS (overview, classification and marking, congestion management, policing and shaping)', '33-10 Global Security Best Practices (NTP)', '15-06 / 15-07 Backups and upgrades (TFTP)']
S.append(sec('QoS, NTP, TFTP and FTP', 'QoS/NTP', G, '', L, qs))

# ------------------------------------------------------------------ wireless architectures
qs = [
 Q('What is the main difference between an autonomous AP and a lightweight AP?', 'An autonomous AP is configured and run on its own; a lightweight AP is managed by a wireless LAN controller through CAPWAP', ['Lightweight APs have no radios', 'Autonomous APs need a WLC', 'They are configured identically'],
   'Lightweight APs split the work ("split-MAC"): real-time radio tasks on the AP, management on the WLC.'),
 Q('Which AP mode lets a branch AP switch client traffic locally to its own VLANs while still being managed by a central WLC?', 'FlexConnect', ['Local', 'Monitor', 'Sniffer'],
   'In local mode, all client traffic is tunnelled to the WLC. FlexConnect suits branches across a WAN.'),
 Q('Which AP mode doesn\'t serve clients but scans channels for rogue APs and intrusion?', 'Monitor', ['Local', 'FlexConnect', 'Bridge'],
   'Sniffer mode captures frames for a remote analyser; rogue detector mode looks for rogues on the wired side; bridge mode builds mesh or point-to-point links; SE-Connect analyses the spectrum.'),
 Q('Which management model runs the controller as a service on the internet?', 'Cloud-based (for example Meraki)', ['Autonomous', 'Lightweight with an on-site WLC', 'Ad hoc'], 'Cloud-managed APs build a tunnel to the vendor\'s cloud dashboard.'),
 Q('How does a WLC typically connect to the switched network for its distribution system ports?', 'With an EtherChannel (LAG) trunk carrying the WLAN VLANs', ['With a single access port in VLAN 1', 'Through the service port only', 'With PAgP desirable on each AP'],
   'WLC LAG is always "on" (no LACP or PAgP negotiation). The service port is for out-of-band management only.'),
 Q('Which two can be used to manage a WLC securely?', ['HTTPS', 'SSH'], ['Telnet', 'HTTP', 'TFTP'],
   'Also console, and RADIUS/TACACS+ for admin logins. Turn off Telnet and HTTP.'),
 Q('When creating a WLAN in the WLC GUI, which settings do you set?', ['The SSID and profile name', 'The interface (VLAN) the WLAN maps to', 'Layer 2 security such as WPA2/WPA3 with PSK or 802.1X'],
   ['The OSPF area', 'The STP root bridge'],
   'Also QoS profile (Platinum for voice, Gold for video, Silver best effort, Bronze background) and advanced options such as client timeouts.'),
 Q('In the WLC QoS profiles, which is intended for voice?', 'Platinum', ['Gold', 'Silver', 'Bronze'], 'Platinum: voice. Gold: video. Silver: best effort (default). Bronze: background.'),
 Q('Which ports and protocol does CAPWAP use between AP and WLC?', 'UDP 5246 for control (encrypted) and UDP 5247 for data', ['TCP 443 for both', 'UDP 1812 and 1813', 'TCP 22 for control'],
   'The AP finds its controller by DHCP option 43, DNS (CISCO-CAPWAP-CONTROLLER), or broadcast on the local subnet.'),
]
L = lesson(10, V11 + 'This lesson covers wireless architectures, AP modes, how APs and WLCs connect, and WLAN setup in the controller GUI.',
 [
  ('Architectures and AP modes', [
    TB(['Architecture', 'How it works'], ['Autonomous', 'Each AP configured on its own; trunk port for multiple SSIDs'], ['Lightweight + WLC', 'Split-MAC; CAPWAP tunnel (UDP 5246/5247) to a controller'], ['Cloud-managed', 'Controller is a cloud dashboard (e.g. Meraki)']),
    TB(['AP mode', 'Purpose'], ['Local', 'Serve clients; tunnel all traffic to the WLC'], ['FlexConnect', 'Serve clients; switch traffic locally at the branch'], ['Monitor', 'No clients; scan for rogues and intrusion'],
       ['Sniffer', 'Capture frames for an analyser'], ['Rogue detector', 'Look for rogue devices on the wired side'], ['SE-Connect', 'Spectrum analysis'], ['Bridge / mesh', 'Wireless links between APs']),
    CK(0, 1, 2, 3, 8)]),
  ('Connections and management', [
    UL('Lightweight AP: access port. Autonomous or FlexConnect AP: trunk.', 'WLC distribution ports: LAG (always "on") as a trunk. Service port: out-of-band management.', 'Manage with HTTPS and SSH; disable Telnet and HTTP; use RADIUS/TACACS+ for admin logins.'),
    CK(4, 5)]),
  ('Creating a WLAN in the GUI', [
    UL('WLANs → Create New: profile name, SSID, WLAN ID.', 'General: map to an interface (VLAN), enable it.', 'Security: Layer 2 (WPA2/WPA3, PSK or 802.1X with RADIUS servers).', 'QoS: Platinum voice, Gold video, Silver best effort, Bronze background.', 'Advanced: timeouts, FlexConnect local switching, and so on.'),
    CK(6, 7)]),
 ],
 [('v1.1 2.6', 'Describe Cisco wireless architectures and AP modes'), ('v1.1 2.7', 'Describe physical infrastructure connections of WLAN components'), ('v1.1 2.8', 'Describe network device management access'), ('v1.1 2.9', 'Interpret the wireless LAN GUI configuration')])
L['course'] = ['37-03 Infrastructure Mode and Wireless APs', '37-04 Wireless LAN Controllers and CAPWAP', '37-05 Switch Configuration for Wireless Networks']
S.append(sec('Wireless Architectures and WLC', 'WLC', G, '', L, qs))

# ------------------------------------------------------------------ automation: REST, JSON, SDA, SD-WAN
JS = '{\n  "interface": "GigabitEthernet1",\n  "enabled": true,\n  "mtu": 1500,\n  "addresses": ["10.1.1.1", "10.1.2.1"],\n  "description": null\n}'
qs = [
 Q('Match the REST HTTP methods to CRUD actions.', 'POST = create, GET = read, PUT/PATCH = update, DELETE = delete', ['GET = create, POST = read', 'PUT = delete, DELETE = update', 'POST = read, GET = create'],
   'PUT replaces a whole resource; PATCH changes part of it.', card='Map POST, GET, PUT, PATCH and DELETE to CRUD.'),
 Q('An API call returns HTTP 401. What does that mean?', 'Unauthorized: the request lacks valid authentication', ['Success', 'Not found', 'Server error'],
   '200 OK, 201 Created, 204 No Content, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 500 Internal Server Error.'),
 Q('Which statement describes REST APIs?', 'Stateless client-server calls, usually over HTTPS, often with JSON data', ['They keep session state on the server', 'They always use XML over SOAP', 'They only work with SNMP'],
   'Stateless means every request carries everything the server needs, including authentication (often a token).'),
 Q('Look at this JSON. Which statement is true?\n' + JS, ['"addresses" is an array', '"enabled" is a Boolean'], ['"mtu" is a string', '"description" is an empty string', 'The outer braces make it an array'],
   'Curly braces = object (key/value pairs). Square brackets = array. true/false = Boolean, null = null, numbers have no quotes.', card='Identify the JSON data types in this example:\n' + JS),
 Q('Which character pairs mark a JSON object and a JSON array?', 'Object { }, array [ ]', ['Object [ ], array { }', 'Object ( ), array < >', 'Both use { }'],
   'Keys are always strings in double quotes. Whitespace doesn\'t matter.'),
 Q('Which data format relies on indentation and is used by Ansible playbooks?', 'YAML', ['JSON', 'XML', 'CSV'], 'XML uses tags; JSON uses braces and brackets; YAML uses indentation.'),
 Q('What are YANG, NETCONF and RESTCONF?', 'YANG is a data model; NETCONF (over SSH, TCP 830, XML) and RESTCONF (over HTTPS, JSON or XML) carry YANG data to and from devices', ['Three routing protocols', 'Three Cisco controllers', 'Three versions of SNMP'],
   'Model-driven programmability replaces screen-scraping the CLI with structured data.'),
 Q('In Cisco SD-Access, what are the underlay and the overlay?', 'Underlay: the physical routed network; overlay: virtual tunnels (VXLAN) built on top that carry user traffic', ['Underlay is wireless; overlay is wired', 'Underlay is the internet; overlay is MPLS', 'They are two VLANs'],
   'The fabric is the overlay plus its control plane (LISP). Policy follows the user via security group tags, set through Catalyst Center and ISE.'),
 Q('Which component in Cisco SD-WAN is the central control plane that distributes routes and policy to the edge routers?', 'vSmart controller', ['vEdge router', 'vBond orchestrator', 'vManage'],
   'vManage: management GUI. vBond: onboarding and authentication. vSmart: control. vEdge/cEdge: data plane with IPsec tunnels between sites.'),
 Q('How does controller-based networking (for example Catalyst Center) compare with traditional device-by-device management?', 'A central controller holds the intent and pushes consistent config and policy to all devices, with network-wide visibility and APIs',
   ['Every device is still configured by hand', 'Controllers remove the data plane', 'Controllers only collect syslog'],
   'Intent-based networking: you state the outcome; the controller translates it into device config and checks it stays true.'),
 Q('What does Terraform use to describe infrastructure, and what does it keep to track what exists?', 'Declarative HCL files and a state file', ['Imperative Python scripts and no state', 'YAML playbooks and an inventory', 'Ruby recipes and a cookbook'],
   '"terraform plan" shows what will change; "terraform apply" makes it so.'),
]
L = lesson(12, V11 + 'This lesson covers the automation topics v2.0 dropped: REST APIs, JSON, model-driven programmability, SD-Access, SD-WAN, and Puppet, Chef and Terraform.',
 [
  ('REST APIs', [
    TB(['HTTP method', 'CRUD'], ['POST', 'Create'], ['GET', 'Read'], ['PUT / PATCH', 'Update (replace / modify)'], ['DELETE', 'Delete']),
    TB(['Code', 'Meaning'], ['200 / 201 / 204', 'OK / Created / No content'], ['400', 'Bad request'], ['401 / 403', 'Not authenticated / not allowed'], ['404', 'Not found'], ['500', 'Server error']),
    UL('REST: client-server, stateless, cacheable, uniform interface. Usually HTTPS with JSON.', 'Authentication: basic auth, API keys, or tokens (often a token from a login call).'),
    CK(0, 1, 2, 9)]),
  ('Data formats', [
    CODE(*JS.split('\n')),
    UL('JSON: objects { }, arrays [ ], strings "in quotes", numbers, true/false, null.', 'XML: <tags>. YAML: indentation, used by Ansible.', 'YANG models the data; NETCONF (SSH, TCP 830) and RESTCONF (HTTPS) move it.'),
    CK(3, 4, 5, 6)]),
  ('SD-Access, SD-WAN and config tools', [
    UL('SD-Access: underlay (routed physical network) + overlay (VXLAN fabric, LISP control plane); ISE identity and security group tags; managed from Catalyst Center.',
       'SD-WAN: vManage (management), vBond (orchestration), vSmart (control), edge routers (data plane, IPsec between sites).', 'Puppet and Chef: agent-based, pull. Ansible: agentless, push. Terraform: declarative IaC with a state file.'),
    CK(7, 8, 10)]),
 ],
 [('v1.1 6.2-6.3', 'Controller-based and software-defined architectures (overlay, underlay, fabric)'), ('v1.1 6.5', 'Characteristics of REST-based APIs'), ('v1.1 6.6', 'Configuration management (Ansible and Terraform)'), ('v1.1 6.7', 'Recognise components of JSON-encoded data')])
L['course'] = ['38-04 Data Serialization Formats (XML, JSON, YAML)', '38-05 APIs (CRUD, REST, SOAP)', '38-06 YANG, NETCONF, RESTCONF and gRPC', '38-12 Cisco SD-Access', '38-13 Cisco SD-WAN']
S.append(sec('REST APIs, JSON and SD Architectures', 'REST/JSON', G, '', L, qs))
