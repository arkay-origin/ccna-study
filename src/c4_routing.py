from h import *

S = []
G = 'IP Routing'

RT = ('Gateway of last resort is 10.0.0.2 to network 0.0.0.0\n'
      'S*  0.0.0.0/0 [1/0] via 10.0.0.2\n'
      'O   10.20.0.0/16 [110/3] via 10.0.0.6, Gi0/2\n'
      'O   10.20.5.0/24 [110/20] via 10.0.0.10, Gi0/3\n'
      'S   10.20.5.0/26 [1/0] via 10.0.0.14\n')

# ------------------------------------------------------------------ Routing table & static routes
qs = [
 Q('A router has routes to 10.20.0.0/16 and 10.20.5.0/24. A packet arrives for 10.20.5.9. Which route is used, and why?', '10.20.5.0/24, because the longest prefix match always wins first',
   ['10.20.0.0/16, because it was learned first', 'Whichever has the lower administrative distance', 'Whichever has the lower metric'],
   'Routers pick the most specific matching route first. AD and metric only decide between routes to the exact same prefix.',
   card='How does a router choose between 10.20.0.0/16 and 10.20.5.0/24 for 10.20.5.9?'),
 Q('A router learns 172.16.1.0/24 from OSPF and has a static route to 172.16.1.0/24. Which goes into the routing table?', 'The static route, because its administrative distance (1) is lower than OSPF (110)',
   ['The OSPF route, because it has a metric', 'Both, load-balanced', 'Whichever was learned most recently'],
   'Same prefix and length, so administrative distance decides. Lower is more trusted.'),
 Q('Match the default administrative distances: static, OSPF, EIGRP (internal) and eBGP.', 'Static 1, eBGP 20, EIGRP 90, OSPF 110',
   ['Static 0, eBGP 20, EIGRP 100, OSPF 110', 'Static 1, eBGP 200, EIGRP 90, OSPF 120', 'Static 5, eBGP 20, EIGRP 90, OSPF 115'],
   'Also: connected 0, IS-IS 115, RIP 120, EIGRP external 170, iBGP 200. 255 means "never use".', card='Give the default AD for connected, static, eBGP, EIGRP, OSPF, RIP and iBGP.',
   ca=['Connected 0', 'Static 1', 'eBGP 20', 'EIGRP (internal) 90', 'OSPF 110', 'IS-IS 115', 'RIP 120', 'EIGRP external 170', 'iBGP 200']),
 Q('In the route "O 10.20.0.0/16 [110/3] via 10.0.0.6, Gi0/2", what do 110 and 3 mean?', '110 is the administrative distance and 3 is the OSPF metric (cost)',
   ['110 is the metric and 3 is the hop count', '110 is the process ID and 3 is the area', '110 is the cost and 3 is the AD'],
   'The brackets are always [AD/metric]. "via" is the next hop and the interface is the exit.'),
 Q('Given this routing table, which next hop does the router use for a packet to 10.20.5.100?\n' + RT, '10.0.0.10',
   ['10.0.0.14', '10.0.0.6', '10.0.0.2'],
   '10.20.5.100 is outside the /26 (which covers .0 to .63), so that route does not match. Of the routes that do match (the /24, the /16 and the default), the /24 is the longest, so traffic goes to 10.0.0.10. A packet to 10.20.5.9 would match the /26 and go to 10.0.0.14.',
   card='In this table, which next hop is used for 10.20.5.100, and which for 10.20.5.9?\n' + RT,
   ca=['10.20.5.100 → 10.0.0.10 (the /24; it is outside the /26)', '10.20.5.9 → 10.0.0.14 (the /26 is the longest match)']),
 Q('What does "Gateway of last resort is not set" mean?', 'The router has no default route, so it drops packets that match no other route',
   ['The router has no connected networks', 'The router\'s default gateway is down', 'OSPF is not running'],
   'Without a default route, unknown destinations are dropped (and an ICMP unreachable may be sent).'),
 Q('Which command creates an IPv4 default route toward next hop 203.0.113.1?', 'ip route 0.0.0.0 0.0.0.0 203.0.113.1', ['ip default-gateway 203.0.113.1', 'ip route 255.255.255.255 0.0.0.0 203.0.113.1', 'ip default-route 203.0.113.1'],
   'Network 0.0.0.0 with mask 0.0.0.0 matches everything. "ip default-gateway" is only for switches or routers with routing turned off.'),
 Q('What is a host route?', 'A route to a single address, using a /32 mask (or /128 in IPv6)', ['A route learned from a host', 'The default route', 'A route to a directly connected network'],
   'Example: ip route 10.9.9.9 255.255.255.255 10.0.0.2. Often used to steer traffic for one server or a loopback.'),
 Q('OSPF provides the main path to 10.50.0.0/16. A backup static route should be used only if OSPF loses the route. Which command is correct?', 'ip route 10.50.0.0 255.255.0.0 10.0.0.9 130',
   ['ip route 10.50.0.0 255.255.0.0 10.0.0.9', 'ip route 10.50.0.0 255.255.0.0 10.0.0.9 100', 'ip route 10.50.0.0 255.255.0.0 10.0.0.9 1'],
   'A floating static has an AD higher than the primary route\'s. OSPF is 110, so anything above 110 works. With 100 or the default 1, the static would replace OSPF.',
   card='How do you make a floating static route behind OSPF?'),
 Q('An engineer configures a floating static with AD 5 as a backup for an OSPF route. What actually happens?', 'The static route is used all the time and OSPF\'s route is ignored',
   ['It works as a backup', 'The command is rejected', 'Both routes are load-balanced'],
   'AD 5 is lower than 110, so the static wins. For a floating route the AD must be higher than the primary.'),
 Q('R1 can ping R2\'s directly connected interface but a host behind R1 can\'t reach a host behind R2. R1 has a static route to R2\'s LAN. What is the most likely missing piece?', 'A route on R2 back to R1\'s LAN',
   ['A default route on the hosts', 'A second static route on R1', 'An ACL on R1'],
   'Routing has to work both ways. Without a return route, R2 can\'t send replies back. Extended ping sourced from R1\'s LAN interface would show this.'),
 Q('Which IPv6 static route is correct when the next hop is a link-local address?', 'ipv6 route 2001:DB8:2::/64 Gi0/0 FE80::2', ['ipv6 route 2001:DB8:2::/64 FE80::2', 'ip route 2001:DB8:2::/64 FE80::2', 'ipv6 route 2001:DB8:2:: FE80::2 Gi0/0'],
   'Every interface has its own FE80 link, so a link-local next hop is ambiguous without the exit interface.'),
 Q('Which command creates an IPv6 default route?', 'ipv6 route ::/0 2001:DB8:0:1::1', ['ipv6 route 0::0/128 2001:DB8:0:1::1', 'ipv6 default-route 2001:DB8:0:1::1', 'ip route ::/0 2001:DB8:0:1::1'],
   '::/0 is the IPv6 "match everything" prefix. "ipv6 unicast-routing" must also be enabled.'),
 Q('A static route\'s next hop is on a subnet whose interface is down. What happens to the static route?', 'It is removed from the routing table until the next hop becomes reachable again',
   ['It stays and traffic is dropped', 'It converts to a default route', 'It changes AD to 255'],
   'A static route is installed only if its next hop or exit interface is usable. That\'s also what lets a floating static take over.'),
 Q('Which code marks a local route (the router\'s own interface address as a /32) in the IPv4 routing table?', 'L', ['C', 'S', 'O'],
   'Each configured interface adds a C (connected subnet) and an L (local /32 host route for the interface address itself).'),
]
L = lesson(16,
 'Every routing question comes back to reading the routing table. This lesson shows how a router picks a route (longest match, then AD, then metric), how to read each line, and how to configure and troubleshoot every kind of static route v2.0 lists, in IPv4 and IPv6.',
 [
  ('Reading a routing table', [
    P('Each line in "show ip route" tells you how the route was learned, the prefix, how trusted it is, how good it is, and where to send traffic.'),
    TB(['Part', 'Example', 'Meaning'], ['Code', 'O', 'Learned by OSPF (S static, C connected, L local, D EIGRP, B BGP, * candidate default)'], ['Prefix/mask', '10.20.0.0/16', 'Destinations matched'],
       ['[AD/metric]', '[110/3]', 'Administrative distance / route metric'], ['Next hop', 'via 10.0.0.6', 'Router to send to'], ['Exit interface', 'Gi0/2', 'Where it leaves']),
    P('"Gateway of last resort" at the top shows the default route, if there is one.'),
    CK(3, 5, 14)]),
  ('How the router chooses', [
    UL('1. Longest prefix match: the most specific route that matches wins, whatever its source.', '2. If two sources offer the same prefix and length: lowest administrative distance wins.', '3. Same source, same prefix: lowest metric wins (equal metrics are load-shared).'),
    TB(['Source', 'Default AD'], ['Connected', '0'], ['Static', '1'], ['eBGP', '20'], ['EIGRP', '90'], ['OSPF', '110'], ['IS-IS', '115'], ['RIP', '120'], ['EIGRP external', '170'], ['iBGP', '200'], ['Unusable', '255']),
    TIP('Longest match first. Students often jump to AD. AD is only a tie-breaker between identical prefixes.'),
    CK(0, 1, 2, 4)]),
  ('Static routes in IPv4', [
    TB(['Type', 'Command']
      , ['Network route', 'ip route 10.2.0.0 255.255.0.0 10.0.0.2']
      , ['Default route', 'ip route 0.0.0.0 0.0.0.0 203.0.113.1']
      , ['Host route', 'ip route 10.9.9.9 255.255.255.255 10.0.0.2']
      , ['Floating static', 'ip route 10.2.0.0 255.255.0.0 10.0.0.6 130']),
    P('You can point at a next-hop IP, an exit interface, or both. On Ethernet, use a next-hop IP (or both), otherwise the router has to ARP for every destination.'),
    P('A floating static is a backup: give it an AD higher than the main route\'s. It stays out of the table until the main route disappears.'),
    DIA(svg(360, 120, 'Primary path learned by OSPF over the MPLS link; floating static with AD 130 over the internet VPN takes over only if OSPF loses the route',
      router(60, 60, 'R1'), router(300, 60, 'HQ'), '<path class="d-ln" d="M71 55 Q180 10 289 55"/>', '<path class="d-ln d-dash" d="M71 65 Q180 110 289 65"/>',
      txt(180, 25, 'OSPF AD 110 (in use)', 'd-s'), txt(180, 108, 'static AD 130 (floating backup)', 'd-s'))),
    CK(6, 7, 8, 9, 13)]),
  ('Static routes in IPv6', [
    UL('Turn on IPv6 routing first: ipv6 unicast-routing.', 'Network: ipv6 route 2001:DB8:2::/64 2001:DB8:0:1::2', 'Default: ipv6 route ::/0 2001:DB8:0:1::1',
       'Host: ipv6 route 2001:DB8:2::10/128 2001:DB8:0:1::2', 'Floating: add an AD at the end, e.g. ... 2001:DB8:0:2::2 130',
       'Link-local next hop: you must also name the exit interface: ipv6 route ::/0 Gi0/0 FE80::1'),
    CK(11, 12)]),
  ('Troubleshooting static routing', [
    UL('Wrong mask or prefix: the route never matches the destination.', 'Wrong next hop: the address isn\'t on a connected subnet, so the route doesn\'t install.',
       'Missing return route: traffic gets there, replies don\'t come back. Always think in both directions.', 'Floating static with too low an AD replaces the primary route.',
       'Next hop interface down: the route is withdrawn (that\'s expected).'),
    TIP('Use "show ip route 10.2.0.5" to see exactly which route a destination matches.'),
    CK(10)]),
 ],
 [('3.1', 'Interpret a routing table to identify the next hop (routing protocol, prefix/mask, administrative distance, metric, default route)'), ('3.2.a', 'Default route'), ('3.2.b', 'Network route'), ('3.2.c', 'Host route'), ('3.2.d', 'Floating static route')])
S.append(sec('Routing Tables and Static Routes', 'Static Routing', G, '', L, qs))

# ------------------------------------------------------------------ OSPF
qs = [
 Q('How does OSPF choose its router ID?', 'The manually configured router-id; otherwise the highest IP on a loopback; otherwise the highest IP on an active physical interface',
   ['The lowest IP address on any interface', 'The MAC address of the first interface', 'A random number chosen at startup'],
   'Set it manually so it never changes unexpectedly. A new router ID only takes effect after "clear ip ospf process" or a reload.',
   card='In what order does OSPF pick its router ID?'),
 Q('Which two must match for two OSPF routers to become neighbours?', ['Area ID', 'Hello and dead timers'], ['Router ID', 'Interface bandwidth', 'Process ID'],
   'Neighbours must agree on area, subnet and mask, hello/dead timers, authentication and stub flags. Router IDs must be different. The process ID is only local.',
   card='List what must match for OSPF neighbours to form.'),
 Q('R1 uses "router ospf 1" and R2 uses "router ospf 20". Will they form an adjacency?', 'Yes, the process ID only matters inside each router', ['No, process IDs must match', 'Only if both are in area 0', 'Only on point-to-point links'],
   'The process ID is locally significant. A common trick question.'),
 Q('Two OSPF neighbours are stuck in EXSTART/EXCHANGE. What is the classic cause?', 'An MTU mismatch between the two interfaces', ['Mismatched hello timers', 'Different areas', 'Duplicate process IDs'],
   'Hello/area problems stop them even seeing each other as neighbours. MTU mismatch lets them see each other but the database exchange fails.'),
 Q('On a broadcast network with four OSPF routers, two show "FULL/DROTHER" and "2WAY/DROTHER" toward each other. Is this a problem?', 'No; DROTHERs only form full adjacencies with the DR and BDR, and stay 2-WAY with each other',
   ['Yes, all routers must be FULL with each other', 'Yes, it means the hello timers don\'t match', 'Yes, the DR has failed'],
   'Keeping DROTHERs at 2-WAY is the whole point of the DR: fewer adjacencies and less flooding.'),
 Q('How is the OSPF DR elected?', 'Highest interface priority wins; if tied, highest router ID', ['Lowest priority, then lowest router ID', 'Highest IP address only', 'The first router to boot always wins'],
   'Default priority is 1. Priority 0 means the router never becomes DR or BDR. The election is not pre-emptive: a better router joining later does not take over.'),
 Q('A new router with OSPF priority 255 joins a segment that already has a DR. What happens?', 'Nothing; the current DR keeps the role until it fails or OSPF restarts',
   ['It immediately becomes the DR', 'It becomes the BDR immediately', 'It becomes DR after the dead interval'],
   'DR elections are not pre-emptive. To force a change, clear the OSPF process on the routers.'),
 Q('Which command keeps a router from ever becoming DR or BDR on an interface?', 'ip ospf priority 0', ['ip ospf priority 255', 'passive-interface', 'ip ospf network broadcast'],
   'Priority 0 opts out of the election.'),
 Q('Two routers are connected by an Ethernet link with nothing else on it. What does "ip ospf network point-to-point" on both ends do?', 'Skips the DR/BDR election so the adjacency forms faster',
   ['Disables OSPF on the link', 'Makes the link passive', 'Changes the OSPF cost to 1'],
   'Ethernet defaults to broadcast type, which elects a DR and waits. On a two-router link that\'s pointless.'),
 Q('Which wildcard mask in "network 10.1.1.0 <wildcard> area 0" matches only the interfaces in 10.1.1.0/24?', '0.0.0.255', ['255.255.255.0', '0.0.0.0', '0.0.255.255'],
   'A wildcard is the inverse of the mask. You can also enable OSPF directly on the interface: "ip ospf 1 area 0".'),
 Q('What does "passive-interface Gi0/1" do under router ospf?', 'Stops sending hellos on Gi0/1 so no neighbours form there, but still advertises its subnet',
   ['Removes Gi0/1\'s network from OSPF', 'Shuts down the interface', 'Makes Gi0/1 the DR'],
   'Use it on LAN interfaces with only hosts: the network is advertised but nobody can form an adjacency there.'),
 Q('With the default reference bandwidth of 100 Mbps, what OSPF cost do a 1 Gbps and a 10 Gbps interface get?', 'Both get a cost of 1', ['10 and 1', '4 and 2', '1 and 0.1'],
   'Cost = 100 Mbps ÷ bandwidth, minimum 1. Fix it with "auto-cost reference-bandwidth 100000" (in Mbps) on every router.'),
 Q('Which command makes an OSPF router advertise its default route to the other OSPF routers?', 'default-information originate', ['redistribute static', 'default-route ospf', 'ip ospf default'],
   'The router must have a default route itself, unless you add "always".'),
 Q('What OSPF neighbour state shows the routers have fully synchronised their databases?', 'FULL', ['2-WAY', 'EXSTART', 'LOADING'],
   'Down → Init → 2-Way → ExStart → Exchange → Loading → Full.'),
 ORD('Put these OSPF neighbour states in order.', ['Down', 'Init', '2-Way', 'ExStart', 'Exchange', 'Loading', 'Full'],
   'Init: I heard your hello. 2-Way: you heard mine. ExStart/Exchange: compare databases. Loading: request what\'s missing. Full: in sync.'),
 Q('How is OSPFv3 for IPv6 enabled on an interface?', 'ipv6 ospf 1 area 0 on the interface', ['network 2001:DB8::/64 area 0', 'ospf ipv6 area 0', 'ipv6 router ospf area 0'],
   'OSPFv3 has no network command; you enable it per interface. "ipv6 unicast-routing" must be on.'),
 Q('An IPv6-only router runs OSPFv3 but the process won\'t start. Why?', 'It has no IPv4 address to use as a router ID, so one must be configured manually',
   ['OSPFv3 needs IPv4 routing enabled', 'OSPFv3 uses a 128-bit router ID that must be set', 'Area 0 is not allowed in OSPFv3'],
   'The OSPFv3 router ID is still a 32-bit number in dotted decimal. With no IPv4 address, set it with "router-id 1.1.1.1".'),
 Q('Which two multicast addresses does OSPFv2 use?', ['224.0.0.5 for all OSPF routers', '224.0.0.6 for the DR and BDR'], ['224.0.0.10 for all OSPF routers', '224.0.0.2 for all routers', '255.255.255.255 for hellos'],
   'OSPFv3 uses FF02::5 and FF02::6 for the same jobs.', card='What multicast addresses does OSPF use, and for what?'),
 Q('Which command shows each OSPF neighbour\'s router ID, state, and the interface it is on?', 'show ip ospf neighbor', ['show ip ospf database', 'show ip protocols', 'show ip route ospf'],
   'show ip ospf interface [brief] shows area, cost, network type, DR/BDR and timers; show ip protocols shows router ID and networks.'),
]
L = lesson(20,
 'OSPF is the routing protocol on the CCNA. This lesson explains how link-state routing works, how to configure single-area OSPFv2 and OSPFv3, how neighbours and the DR election work on point-to-point and broadcast networks, and how to fix adjacencies that won\'t form.',
 [
  ('How OSPF works', [
    P('OSPF is a link-state protocol. Each router describes its own links in Link-State Advertisements (LSAs) and floods them to every router in the area. Every router ends up with the same map (the LSDB) and runs the SPF algorithm to find the best path to each network.'),
    UL('Metric: cost. Cost = reference bandwidth (default 100 Mbps) ÷ interface bandwidth, minimum 1.', 'AD 110. IP protocol 89. Multicast 224.0.0.5 (all OSPF routers) and 224.0.0.6 (DR/BDR).',
       'Single-area means everything is in area 0, the backbone. Multi-area design is beyond the CCNA.'),
    TIP('With the default reference bandwidth, 1 Gbps and 10 Gbps both cost 1. Use "auto-cost reference-bandwidth 100000" on every router.'),
    CK(11, 17)]),
  ('Configuring OSPFv2', [
    UL('router ospf 1', ' router-id 1.1.1.1', ' network 10.1.1.0 0.0.0.255 area 0', ' passive-interface Gi0/1', ' default-information originate'),
    P('Or enable it on the interface: "ip ospf 1 area 0". The process number is only local; neighbours don\'t need to match it.'),
    P('Router ID: the configured router-id, else the highest loopback IP, else the highest active interface IP. Changing it takes effect after "clear ip ospf process".'),
    P('Passive interface: the subnet is advertised, but no hellos are sent, so no neighbours form on a user LAN.'),
    CK(0, 2, 9, 10, 12)]),
  ('Neighbours and adjacencies', [
    P('Routers discover each other with hellos (every 10 s on Ethernet, dead after 40 s). To become neighbours they must match on:'),
    UL('Area ID', 'Subnet and mask', 'Hello and dead timers', 'Authentication', 'Stub area flag', 'Plus: unique router IDs, interface not passive. MTU must match to get past ExStart/Exchange.'),
    TB(['State', 'Means'], ['Init', 'I received your hello'], ['2-Way', 'We see each other in our hellos'], ['ExStart / Exchange', 'Agree who leads; swap database summaries'], ['Loading', 'Request missing LSAs'], ['Full', 'Databases match']),
    CK(1, 3, 13, 14)]),
  ('Broadcast networks and the DR', [
    P('On a shared Ethernet segment, every router forming a full adjacency with every other would be a lot of flooding. Instead they elect a Designated Router (DR) and a Backup (BDR). Others (DROTHERs) go FULL with the DR and BDR and stay 2-WAY with each other.'),
    UL('Highest interface priority wins (default 1, range 0–255).', 'Tie: highest router ID.', 'Priority 0: never DR or BDR.', 'Not pre-emptive: a better router joining later waits until the DR fails.'),
    DIA(svg(360, 160, 'Broadcast segment with DR, BDR and two DROTHERs; DROTHERs are FULL with the DR and BDR and 2-WAY with each other',
      ln(30, 70, 330, 70, 'd-ln'), router(60, 35, 'DR · pri 10', below=False), router(140, 35, 'BDR', below=False), router(220, 105, 'DROTHER'), router(300, 105, 'DROTHER'),
      ln(60, 46, 60, 70), ln(140, 46, 140, 70), ln(220, 70, 220, 94), ln(300, 70, 300, 94), txt(180, 154, 'DROTHERs: 2-WAY with each other, FULL with DR/BDR', 'd-s'))),
    CK(4, 5, 6, 7)]),
  ('Point-to-point networks', [
    P('Serial links and two-router Ethernet links set to "ip ospf network point-to-point" have no DR or BDR. The adjacency forms faster and both routers show FULL/-.'),
    P('Both ends must use the same network type. A broadcast/point-to-point mismatch can form an adjacency but leave routes missing.'),
    CK(8)]),
  ('OSPFv3 for IPv6', [
    UL('ipv6 unicast-routing', 'ipv6 router ospf 1', ' router-id 1.1.1.1  (needed if the router has no IPv4 address)', 'interface Gi0/0', ' ipv6 ospf 1 area 0'),
    P('OSPFv3 works the same way: same states, DR election and cost. It uses link-local addresses for neighbours and next hops, and multicast FF02::5 and FF02::6.'),
    CK(15, 16)]),
  ('Verify and troubleshoot', [
    TB(['Command', 'Shows'], ['show ip ospf neighbor', 'Neighbour router IDs, state, interface'], ['show ip ospf interface brief', 'Area, cost, state (DR/BDR/DROTHER/P2P), neighbour count'],
       ['show ip protocols', 'Router ID, networks, passive interfaces'], ['show ip route ospf', 'OSPF routes installed'], ['show ipv6 ospf neighbor', 'OSPFv3 neighbours']),
    UL('No neighbour at all: area, subnet/mask, timers, authentication, passive interface, ACL blocking 224.0.0.5.', 'Stuck ExStart/Exchange: MTU mismatch.', 'Neighbour up but no routes: network type mismatch, or networks not advertised.'),
    CK(18)]),
 ],
 [('3.3.a', 'Neighbor adjacencies (excluding authentication)'), ('3.3.b', 'Point-to-point networks'), ('3.3.c', 'Broadcast networks (DR/BDR selection)'), ('3.3.d', 'Router ID'), ('3.3', 'Single-area OSPFv2 (IPv4) and OSPFv3 (IPv6)')])
S.append(sec('Single-Area OSPFv2 and OSPFv3', 'OSPF', G, '', L, qs))

# ------------------------------------------------------------------ FHRP
SB = ('R1# show standby brief\n'
      'Interface  Grp  Pri P State   Active      Standby     Virtual IP\n'
      'Vl10       10   110 P Active  local       10.10.0.3   10.10.0.1\n')
qs = [
 Q('What problem do first hop redundancy protocols solve?', 'Hosts have one default gateway address; an FHRP lets two routers share a virtual gateway IP so a router failure doesn\'t cut hosts off',
   ['They route between areas', 'They stop Layer 2 loops', 'They hand out IP addresses'],
   'Hosts keep pointing at the same virtual IP. Whichever router is active answers for it.'),
 Q('Which statement compares HSRP and VRRP correctly?', 'HSRP is Cisco proprietary with active/standby roles; VRRP is an open standard with master/backup roles',
   ['Both are Cisco proprietary', 'HSRP is open standard; VRRP is Cisco', 'Both load-balance traffic across all routers by default'],
   'GLBP (also Cisco) is the one that load-balances within a single group.'),
 Q('By default, which HSRP router becomes active?', 'The one with the highest priority (default 100); if tied, the highest interface IP address',
   ['The one with the lowest priority', 'The one with the lowest IP address', 'The first one configured'],
   'Set priority with "standby 10 priority 110". Higher wins.'),
 Q('An HSRP router with higher priority reboots and comes back, but stays standby. Why?', 'Pre-emption is off by default in HSRP',
   ['Its priority reset to 0', 'HSRP never allows a new active router', 'VRRP is overriding it'],
   'Add "standby 10 preempt" so the preferred router takes back the active role. VRRP pre-empts by default.'),
 Q('Interpret this output. Which statements are true?\n' + SB, ['R1 is the active router for group 10', 'Hosts should use 10.10.0.1 as their default gateway'],
   ['10.10.0.3 is the virtual IP', 'Pre-emption is disabled', 'R1 is standby'],
   '"Active local" means this router. Priority 110 with P = pre-emption on. The standby router is 10.10.0.3 and the virtual IP is 10.10.0.1.',
   card='Read this "show standby brief": who is active, who is standby, and what do hosts use?\n' + SB),
 Q('Two routers in the same HSRP group both report the Active state. What does this usually indicate?', 'They can\'t hear each other\'s hellos, often because of a VLAN, trunk or ACL problem between them',
   ['Normal operation with load-balancing', 'Both have pre-emption enabled', 'The virtual IP is a duplicate of a host'],
   'Each thinks the other is gone, so both answer for the virtual IP. Check the link and VLAN between them.'),
 Q('What virtual MAC address does HSRP version 1 use for group 10?', '0000.0C07.AC0A', ['0000.5E00.010A', '0000.0C9F.F00A', '0100.5E00.000A'],
   'HSRPv1: 0000.0C07.ACxx (xx = group in hex, 10 = 0A). HSRPv2: 0000.0C9F.Fxxx. VRRP: 0000.5E00.01xx.'),
 Q('Which two are differences between HSRP version 1 and version 2?', ['Version 2 supports group numbers up to 4095', 'Version 2 uses multicast 224.0.0.102 instead of 224.0.0.2'],
   ['Version 2 is an open standard', 'Version 1 supports IPv6', 'Version 2 has no virtual MAC'],
   'v1: groups 0–255, 224.0.0.2. v2: groups 0–4095, 224.0.0.102, adds IPv6 support. Both use UDP 1985.', card='How does HSRPv2 differ from HSRPv1?'),
 Q('What does VRRP call the router currently forwarding for the virtual IP?', 'Master', ['Active', 'Primary', 'DR'], 'VRRP: master/backup. HSRP: active/standby.'),
 Q('Which statement about VRRP is true and differs from HSRP?', 'The virtual IP can be the real IP address of one of the routers, which then becomes the owner with priority 255',
   ['VRRP has pre-emption disabled by default', 'VRRP uses UDP port 1985', 'VRRP only works on Cisco devices'],
   'VRRP lets the gateway address be a real interface address. Pre-emption is on by default. VRRP uses IP protocol 112 and multicast 224.0.0.18.'),
 Q('What should hosts on the VLAN have as their default gateway when HSRP is used?', 'The HSRP virtual IP address', ['The active router\'s real interface IP', 'The standby router\'s real IP', 'Both routers\' real IPs'],
   'If hosts pointed at a real IP, they\'d lose their gateway when that router failed.'),
 Q('HSRP interface tracking is set to lower R1\'s priority by 20 if its WAN uplink fails. R1 has priority 110, R2 has 100 with pre-emption. What happens when R1\'s WAN fails?', 'R1 drops to 90, so R2 pre-empts and becomes active',
   ['Nothing changes; R1 stays active', 'Both routers become standby', 'R1 shuts down its LAN interface'],
   'Tracking makes the gateway role follow the working uplink. R2 needs pre-emption to take over.'),
 Q('Which command shows VRRP group status in summary form?', 'show vrrp brief', ['show standby brief', 'show glbp brief', 'show ip vrrp'],
   'Similar columns to HSRP: interface, group, priority, pre-empt, state, master address, group (virtual) address.'),
]
L = lesson(12,
 'A host has one default gateway. If that router fails, the host is cut off. First hop redundancy protocols put two routers behind one virtual gateway address. v2.0 asks you to read their status, so this lesson focuses on what the output means.',
 [
  ('The idea', [
    P('Two routers (or Layer 3 switches) on the same VLAN share a virtual IP and virtual MAC address. Hosts use the virtual IP as their gateway. One router forwards; the other watches its hellos and takes over if they stop.'),
    DIA(svg(360, 150, 'Two routers share virtual IP 10.10.0.1; R1 is active, R2 standby; hosts use 10.10.0.1',
      router(110, 35, 'R1 · Active · .2', below=False), router(250, 35, 'R2 · Standby · .3', below=False), ln(110, 46, 160, 85), ln(250, 46, 200, 85),
      switch(180, 92), host(130, 135, 'PC'), host(230, 135, 'PC'), ln(170, 101, 140, 126), ln(190, 101, 220, 126),
      txt(205, 96, 'Virtual IP 10.10.0.1', 'd-s', 'start'))),
    CK(0, 10)]),
  ('HSRP', [
    UL('Cisco proprietary. Roles: active and standby (others listen).', 'Priority 0–255, default 100. Highest wins; tie goes to highest IP.', 'Pre-emption off by default: standby 10 preempt.',
       'Hello 3 s, hold 10 s. UDP 1985.', 'v1: groups 0–255, 224.0.0.2, MAC 0000.0C07.ACxx. v2: groups 0–4095, 224.0.0.102, MAC 0000.0C9F.Fxxx, supports IPv6.'),
    UL('interface Vlan10', ' ip address 10.10.0.2 255.255.255.0', ' standby version 2', ' standby 10 ip 10.10.0.1', ' standby 10 priority 110', ' standby 10 preempt'),
    CK(2, 3, 6, 7)]),
  ('VRRP', [
    UL('Open standard (RFC 5798). Roles: master and backup.', 'Priority default 100; the router that owns the virtual IP as its real address gets 255.', 'Pre-emption on by default.',
       'IP protocol 112, multicast 224.0.0.18, MAC 0000.5E00.01xx.'),
    TB(['', 'HSRP', 'VRRP'], ['Standard', 'Cisco', 'IETF (open)'], ['Roles', 'Active / Standby', 'Master / Backup'], ['Default priority', '100', '100'],
       ['Pre-empt default', 'Off', 'On'], ['Virtual IP = real IP?', 'No', 'Allowed']),
    CK(1, 8, 9)]),
  ('Reading the status', [
    P('Interpreting operational status is the actual v2.0 objective. Here is typical output:'),
    TB(['Interface', 'Grp', 'Pri', 'P', 'State', 'Active', 'Standby', 'Virtual IP'], ['Vl10', '10', '110', 'P', 'Active', 'local', '10.10.0.3', '10.10.0.1']),
    UL('"local" in the Active column means this router is active.', 'P means pre-emption is configured.', 'Two routers both Active: they can\'t hear each other. Check the VLAN or link between them.',
       'Init or Listen on both: the virtual IP or group may not match.', 'Interface tracking lowers priority when an uplink fails, letting the other router pre-empt.'),
    CK(4, 5, 11, 12)]),
 ],
 [('3.4', 'Interpret the operational status of First Hop Redundancy Protocols (HSRP and VRRP)')])
S.append(sec('First Hop Redundancy: HSRP and VRRP', 'HSRP/VRRP', G, '', L, qs))
