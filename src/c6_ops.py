from h import *

S = []
G = 'AI and Operations'

LOG = '*Nov 13 14:02:11.381: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet0/1, changed state to down'

# ------------------------------------------------------------------ SNMP + syslog
qs = [
 Q('Which UDP ports does SNMP use?', 'UDP 161 for polling the agent, UDP 162 for traps and informs to the manager', ['UDP 514 for both', 'TCP 161 and TCP 162', 'UDP 162 for polling, UDP 161 for traps'],
   'The manager polls the device (agent) on 161. The device sends unsolicited alerts to the manager on 162.'),
 Q('What is the difference between an SNMP trap and an inform?', 'An inform is acknowledged by the manager, so the agent resends it if lost; a trap is not acknowledged',
   ['A trap is encrypted; an inform is not', 'Traps go from manager to agent', 'Informs are only in SNMPv1'],
   'Informs arrived in SNMPv2c. They are more reliable but use more resources.'),
 Q('Which SNMP version adds authentication and encryption?', 'SNMPv3', ['SNMPv1', 'SNMPv2c', 'All versions with a community string'],
   'v1 and v2c use community strings sent in clear text. v3 adds users with authentication (SHA) and privacy (AES): security level authPriv.'),
 Q('What does the MIB contain?', 'The structured set of variables (OIDs) an SNMP agent can report or change', ['The device\'s routing table', 'A list of syslog messages', 'The manager\'s user accounts'],
   'Each value, such as an interface counter, has an Object Identifier (OID) in the MIB tree.'),
 Q('Which SNMP operation does a manager use to change a value on a device?', 'Set', ['Get', 'GetNext', 'Trap'],
   'Get / GetNext / GetBulk read; Set writes. A read-write community string or v3 user is needed for Set.'),
 Q('Which syslog severity level is "warnings"?', '4', ['3', '5', '6'],
   '0 Emergencies, 1 Alerts, 2 Critical, 3 Errors, 4 Warnings, 5 Notifications, 6 Informational, 7 Debugging.'),
 Q('List syslog severities 0 to 7 in order.', '0 Emergencies, 1 Alerts, 2 Critical, 3 Errors, 4 Warnings, 5 Notifications, 6 Informational, 7 Debugging',
   ['0 Debugging, 1 Informational, 2 Notifications, 3 Warnings, 4 Errors, 5 Critical, 6 Alerts, 7 Emergencies', '0 Emergencies, 1 Critical, 2 Alerts, 3 Errors, 4 Warnings, 5 Informational, 6 Notifications, 7 Debugging', '0 Alerts, 1 Emergencies, 2 Errors, 3 Critical, 4 Warnings, 5 Notifications, 6 Debugging, 7 Informational'],
   'Memory aid: Every Awesome Cisco Engineer Will Need Ice-cream Daily. Lower number = more severe.'),
 Q('In this message, what are the facility, severity and mnemonic?\n' + LOG, 'Facility LINEPROTO, severity 5 (notifications), mnemonic UPDOWN',
   ['Facility UPDOWN, severity 5, mnemonic LINEPROTO', 'Facility LINEPROTO, severity 5 (warnings), mnemonic GigabitEthernet', 'Facility Interface, severity 0, mnemonic down'],
   'Format: %FACILITY-SEVERITY-MNEMONIC: description. Here the facility names the IOS feature that produced it.', card='Break this syslog message into facility, severity and mnemonic:\n' + LOG),
 Q('With "logging trap warnings", which severity levels are sent to the syslog server?', '0 through 4', ['Only level 4', '4 through 7', 'All levels'],
   'The configured level and everything more severe (lower numbers) are sent.'),
 Q('Which command sends syslog messages to a server at 10.0.0.50?', 'logging host 10.0.0.50', ['snmp-server host 10.0.0.50', 'logging buffered 10.0.0.50', 'syslog server 10.0.0.50'],
   'Then set the level with "logging trap <level>". Syslog uses UDP 514.'),
 Q('Why should NTP be configured along with syslog?', 'So timestamps on every device are accurate and in sync, making events possible to correlate',
   ['Syslog needs NTP to send messages', 'NTP encrypts syslog', 'NTP sets the severity level'],
   'Add "service timestamps log datetime msec" so messages carry the date and time, not uptime.'),
 Q('Which syslog facility value do Cisco devices use by default when sending to a server?', 'local7', ['local0', 'kern', 'auth'],
   'The server uses the facility (local0–local7) to sort messages into files. Change it with "logging facility local3".'),
 Q('An engineer is connected by SSH and sees no log messages appear while testing. Which command fixes this for the session?', 'terminal monitor', ['logging console', 'logging buffered', 'show logging'],
   'Log messages go to the console by default; VTY sessions need terminal monitor.'),
 Q('Which SNMPv3 security level provides both authentication and encryption?', 'authPriv', ['noAuthNoPriv', 'authNoPriv', 'privNoAuth'], 'authNoPriv authenticates but sends in clear text.'),
]
L = lesson(14,
 'To run a network you need to know what it is doing. This lesson covers the two classic monitoring tools: SNMP for polling and alerts, and syslog for event messages, including reading syslog content and severities.',
 [
  ('SNMP', [
    P('An SNMP manager (the monitoring system) talks to the SNMP agent on each device. The agent exposes values in the MIB, each with an OID.'),
    TB(['Message', 'Direction', 'Port'], ['Get / GetNext / GetBulk', 'Manager → agent, read', 'UDP 161'], ['Set', 'Manager → agent, write', 'UDP 161'],
       ['Trap', 'Agent → manager, unacknowledged', 'UDP 162'], ['Inform', 'Agent → manager, acknowledged', 'UDP 162']),
    TB(['Version', 'Security'], ['v1, v2c', 'Community string (read-only or read-write), sent in clear text'], ['v3', 'Users with authentication and encryption: noAuthNoPriv, authNoPriv, authPriv']),
    TIP('Use SNMPv3 authPriv in production. If you must use v2c, use read-only communities and an ACL.'),
    CK(0, 1, 2, 3, 4, 13)]),
  ('Syslog severity', [
    TB(['Level', 'Name', 'Example'], ['0', 'Emergencies', 'System unusable'], ['1', 'Alerts', 'Immediate action needed'], ['2', 'Critical', 'Hardware failure'], ['3', 'Errors', 'Interface down (%LINK-3)'],
       ['4', 'Warnings', 'Config issue, threshold'], ['5', 'Notifications', 'Line protocol up/down, OSPF neighbour change'], ['6', 'Informational', 'ACL match logged'], ['7', 'Debugging', 'debug output']),
    P('Memory aid: Every Awesome Cisco Engineer Will Need Ice-cream Daily. Choosing a level includes everything more severe: "logging trap warnings" sends 0–4.'),
    CK(5, 6, 8)]),
  ('Reading a syslog message', [
    P('Example: ' + LOG),
    UL('Sequence number and timestamp (if enabled).', '%LINEPROTO: the facility, meaning which part of IOS reported it.', '5: severity (notifications).', 'UPDOWN: the mnemonic, a short name for the event.', 'Then a plain-English description.'),
    P('The server-side facility (local0–local7, default local7) is a different thing: it tells the syslog server how to file the messages.'),
    CK(7, 11)]),
  ('Configuring logging', [
    UL('logging host 10.0.0.50  (UDP 514)', 'logging trap informational', 'logging buffered 16384 warnings', 'service timestamps log datetime msec', 'ntp server 10.0.0.1', 'terminal monitor  (see logs in an SSH session)'),
    CK(9, 10, 12)]),
 ],
 [('5.4', 'Describe the function of SNMP in network operations'), ('5.6', 'Interpret syslog message content, severity levels and facilities')])
S.append(sec('SNMP and Syslog', 'SNMP/Syslog', G, '', L, qs))

# ------------------------------------------------------------------ Management approaches + Ansible + IaC
qs = [
 Q('Which network management approach configures each device individually through its own CLI or GUI?', 'Device-based', ['Controller-based', 'Cloud-based', 'Infrastructure as code'],
   'Simple for a few devices, but slow and error-prone at scale.'),
 Q('Meraki devices are configured through a web dashboard hosted by the vendor on the internet. Which approach is this?', 'Cloud-based management', ['Device-based', 'Controller-based on-premises', 'Agent-based'],
   'The devices connect out to the cloud dashboard. No local controller to run, but you depend on the cloud service.'),
 Q('In a controller-based (SDN) architecture, what are the northbound and southbound interfaces?', 'Northbound: APIs (usually REST) between the controller and applications. Southbound: protocols between the controller and the network devices.',
   ['Northbound: controller to devices. Southbound: controller to apps.', 'Both connect switches to each other', 'Northbound is the internet link; southbound is the LAN'],
   'Catalyst Center (formerly DNA Center) is a controller: apps use its REST API northbound; it uses NETCONF, SSH/CLI or SNMP southbound.', card='What are the northbound and southbound interfaces of an SDN controller?'),
 Q('Which plane of a network device forwards user traffic?', 'Data plane', ['Control plane', 'Management plane', 'Application plane'],
   'Control plane builds tables (routing protocols, STP). Management plane is how admins and tools reach the device (SSH, SNMP).'),
 Q('What is infrastructure as code (IaC)?', 'Defining network and system configuration in version-controlled files that tools apply automatically',
   ['Writing device firmware', 'Configuring devices by hand from a printed runbook', 'Running code on a router\'s CPU'],
   'Files live in Git, changes are reviewed, and the same definition builds the same result every time. Terraform and Ansible are common tools.'),
 Q('Which statement about Ansible is true?', 'It is agentless and connects to network devices over SSH (or APIs)', ['It needs an agent installed on every switch', 'It is written as Ruby recipes', 'It only works with Linux servers'],
   'No agent needed on the device, which suits network gear. Puppet and Chef traditionally use agents.'),
 Q('In what format are Ansible playbooks written?', 'YAML', ['JSON only', 'XML', 'Python classes'],
   'Playbooks are YAML files containing plays and tasks. Templates use Jinja2.'),
 Q('What is the Ansible inventory?', 'The file listing the devices (hosts) and groups Ansible manages, plus their connection variables', ['The list of installed modules', 'The output of a playbook run', 'The device\'s running configuration'],
   'Example group [ios] with ansible_network_os=cisco.ios.ios and ansible_connection=network_cli.'),
 Q('Which command runs an Ansible playbook?', 'ansible-playbook site.yml -i inventory', ['ansible run site.yml', 'python site.yml', 'terraform apply site.yml'],
   'A single command against a host or group, without a playbook, is an ad-hoc command: ansible ios -m cisco.ios.ios_command -a "commands=\'show version\'".'),
 Q('Which Ansible module runs show commands on Cisco IOS devices and returns the output?', 'cisco.ios.ios_command', ['cisco.ios.ios_config', 'ansible.builtin.copy', 'cisco.ios.ios_facts only'],
   'ios_command runs exec commands. ios_config pushes configuration lines. ios_facts gathers device facts.'),
 Q('What does "idempotent" mean for an automation task?', 'Running it again makes no further changes if the device is already in the desired state', ['It runs only once and then deletes itself', 'It always overwrites the full configuration', 'It runs in parallel on all devices'],
   'Good Ansible modules check the current state first, so a playbook can be rerun safely.'),
 Q('Which model does Ansible use to apply configuration?', 'Push: the control node connects out to devices and pushes changes', ['Pull: devices poll a server for changes', 'Broadcast: changes are flooded to all devices', 'Manual: an admin copies output'],
   'Puppet and Chef agents classically pull from a master server.'),
 Q('Which tool is mainly declarative IaC, describing the desired end state in HCL files and keeping a state file?', 'Terraform', ['Ansible', 'SNMP', 'Syslog'],
   'You describe what should exist; Terraform works out what to create, change or delete. Ansible playbooks list tasks in order (more procedural).'),
]
PB = ('- name: Collect versions\n  hosts: ios\n  gather_facts: no\n  tasks:\n    - name: Run show version\n      cisco.ios.ios_command:\n        commands: show version\n      register: out\n    - debug: var=out.stdout_lines')
L = lesson(14,
 'Managing hundreds of devices one CLI at a time doesn\'t scale. This lesson compares the five management approaches v2.0 lists and shows how Ansible runs commands across many devices.',
 [
  ('Five ways to manage a network', [
    TB(['Approach', 'How', 'Example']
      , ['Device-based', 'Log in to each box: CLI, web GUI', 'SSH to each switch']
      , ['Cloud-based', 'Vendor-hosted dashboard; devices connect out to it', 'Meraki Dashboard']
      , ['Controller-based', 'A controller on your network configures devices and exposes APIs', 'Catalyst Center, WLC']
      , ['Automation-based', 'Scripts and tools push changes to many devices', 'Ansible, Python']
      , ['Infrastructure as code', 'Desired state stored as files in Git and applied by tools', 'Terraform, Ansible + Git']),
    CK(0, 1, 4)]),
  ('Planes and controllers', [
    UL('Data plane: forwards user packets.', 'Control plane: builds the tables (OSPF, STP, ARP).', 'Management plane: how people and tools manage the device (SSH, SNMP, APIs).'),
    P('A controller centralises management and some control decisions. Applications talk to it through northbound APIs (usually REST with JSON). It talks to devices through southbound protocols (NETCONF, RESTCONF, SSH/CLI, SNMP, OpenFlow).'),
    CK(2, 3)]),
  ('Ansible basics', [
    UL('Agentless: uses SSH (network_cli) or APIs. Nothing to install on the switch.', 'Push model: the control node (Linux, Python) connects out.', 'Inventory: which devices, in which groups, with connection variables.',
       'Playbook: YAML file of plays and tasks.', 'Modules: do the work, e.g. cisco.ios.ios_command (show commands), cisco.ios.ios_config (config lines).', 'Idempotent modules make reruns safe.'),
    P('A minimal playbook that runs a command on every device in the "ios" group:'),
    TB(['site.yml'], [PB]),
    UL('Run it: ansible-playbook site.yml -i inventory', 'Ad-hoc: ansible ios -i inventory -m cisco.ios.ios_command -a "commands=\'show ip int brief\'"'),
    CK(5, 6, 7, 8, 9, 10, 11)]),
  ('Infrastructure as code', [
    P('IaC treats configuration like software: written in files, kept in Git, reviewed through pull requests, tested, then applied automatically. Benefits: consistency, history of every change, quick rollback.'),
    UL('Declarative (Terraform): describe the end state; the tool works out the steps.', 'Procedural (Ansible tasks, Python scripts): list the steps in order.'),
    CK(12)]),
 ],
 [('5.3', 'Describe network management approaches (device-based, cloud-based, controller-based, automation-based, infrastructure as code)'), ('5.5', 'Use configuration management mechanisms, such as Ansible, to execute commands')])
S.append(sec('Management Approaches and Ansible', 'Mgmt/Ansible', G, '', L, qs))

# ------------------------------------------------------------------ AI
qs = [
 Q('What distinguishes agentic AI from a simple generative AI chatbot?', 'An agent pursues a goal over several steps, choosing and using tools (such as running show commands or calling APIs) and acting on the results',
   ['It only answers single questions with text', 'It cannot access any data', 'It replaces the need for monitoring'],
   'A chatbot answers. An agent observes, reasons, plans and acts, often in a loop until the goal is met.'),
 Q('Which loop best describes how an AI agent troubleshoots a network issue?', 'Observe (collect data), reason, plan, act (run a tool), then check the result and repeat', ['Guess, apply a change, reload', 'Read one log line and stop', 'Wait for a human to type each command'],
   'Each tool result feeds the next step, the way an engineer works through a problem.'),
 Q('An AI agent proposes changing the OSPF area on a core router to fix a missing route. What is the best practice before the change is applied?', 'A human reviews the proposed change against real device output and approves it',
   ['Apply it automatically, since the agent is confident', 'Reload the router first', 'Let the agent disable logging to avoid noise'],
   'Human-in-the-loop approval for changes, with read-only access by default, keeps a wrong (hallucinated) suggestion from causing an outage.'),
 Q('An AI assistant reports that "the neighbour is stuck in EXSTART due to an MTU mismatch", but the show output you have shows the neighbour in INIT. What should you do?', 'Trust the device output; INIT means one side isn\'t receiving hellos, so investigate that and treat the AI\'s claim as wrong',
   ['Accept the AI\'s answer, since it has more data', 'Change the MTU anyway', 'Restart the AI agent'],
   'v2.0 says you may need to evaluate AI output. Always check claims against the real data; AI can be confidently wrong.'),
 Q('Which two are sensible guardrails for an AI agent with access to network devices?', ['Least privilege, such as read-only credentials unless a change is approved', 'Logging and auditing of every action the agent takes'],
   ['Giving it enable-level access to every device by default', 'Turning off change approval to save time', 'Letting it edit its own permissions'],
   'Treat an agent like a new team member: limited access, everything recorded, approval for risky actions.', card='Name two guardrails for an AI agent that can reach network devices.'),
 Q('Which task is a good fit for agentic AI in network operations today?', 'Gathering show output from many devices, correlating it with logs and suggesting a likely root cause for an engineer to verify',
   ['Making unreviewed changes to production firewalls', 'Replacing all monitoring tools', 'Choosing the company\'s IP address plan with no review'],
   'Agents are strongest at collecting and correlating data quickly. Decisions with large blast radius still need people.'),
 Q('Which elements make a strong generative AI prompt for network operations?', ['A persona or role', 'Clear instructions and the task', 'The required output format', 'Appropriate data classification of what is shared'],
   ['A request to "be creative" with no details', 'All device passwords so it can log in', 'As little context as possible'],
   'v2.0 lists exactly these components: data classification, output format, persona and instructions. Context (the relevant output) helps too.', card='What four components does v2.0 list for a good network-operations prompt?'),
 Q('Before pasting a router configuration into a public AI chatbot, what should you do?', 'Remove or mask secrets and sensitive data such as passwords, keys, SNMP communities and public IP addresses, and follow your data classification policy',
   ['Nothing; AI tools never store data', 'Paste it with the passwords so the AI can check them', 'Convert it to PDF first'],
   'Data classification decides what may be shared with which tool. Confidential data should only go to approved, internal AI services.'),
 Q('Which prompt is the best one for getting a usable answer?', '"You are a senior Cisco network engineer. Here is the output of show ip ospf neighbor and show ip ospf interface brief from R1 (sanitised). Explain why R1 has no neighbour on Gi0/1, list the likely causes in order, and give the IOS commands to verify each. Reply as a numbered list."',
   ['"Fix my OSPF."', '"Here are all our router passwords and configs. What is wrong?"', '"Write a poem about routing."'],
   'It has a persona, context data (sanitised), clear instructions, and an output format.'),
 Q('Why specify an output format such as "return a table with columns Interface, Status, Issue" or "return valid JSON"?', 'So the answer is consistent and easy to read or feed into other tools and automation',
   ['It makes the AI more accurate about facts', 'It is required by every AI tool', 'It encrypts the answer'],
   'Structured output (tables, JSON, config snippets) can be compared, scripted, or pasted into tickets.'),
 Q('What is an AI "hallucination"?', 'A confident answer that is false or invented, such as a nonexistent IOS command', ['An AI refusing to answer', 'A slow response', 'An answer that cites its sources'],
   'That\'s why every command or claim from an AI must be checked against documentation or a lab before use in production.'),
 Q('What does assigning a persona in a prompt (for example "You are a CCNP-level network engineer") do?', 'Sets the expertise level, vocabulary and perspective of the answer', ['Gives the AI access to Cisco\'s systems', 'Guarantees the answer is correct', 'Changes the AI\'s data classification'],
   'It shapes the response. It doesn\'t add knowledge or make it reliable.'),
]
L = lesson(14,
 'AI is new to the CCNA in v2.0, and some exam items show you AI output to judge. This lesson explains what agentic AI is, where it helps in network operations, the risks, and how to write a good prompt.',
 [
  ('From chatbots to agents', [
    P('Generative AI (a large language model) produces text, code or configuration from a prompt. On its own it answers and stops.'),
    P('Agentic AI wraps a model in a loop with tools and a goal. The agent decides what information it needs, uses tools to get it (run show commands, query a controller API, read logs), reasons about the result, and takes the next step, until the goal is met or it hands back to a person.'),
    DIA(svg(360, 110, 'Agent loop: observe, reason and plan, act, check the result, and repeat',
      box(4, 20, 78, 34, 'd-rt'), txt(43, 35, 'Observe', 'd-t'), txt(43, 48, 'logs, output', 'd-s'),
      box(96, 20, 78, 34, 'd-rt'), txt(135, 35, 'Reason', 'd-t'), txt(135, 48, 'and plan', 'd-s'),
      box(188, 20, 78, 34, 'd-rt'), txt(227, 35, 'Act', 'd-t'), txt(227, 48, 'run a tool', 'd-s'),
      box(280, 20, 76, 34, 'd-rt'), txt(318, 35, 'Check', 'd-t'), txt(318, 48, 'the result', 'd-s'),
      ln(82, 37, 94, 37, 'd-ln', True), ln(174, 37, 186, 37, 'd-ln', True), ln(266, 37, 278, 37, 'd-ln', True),
      '<path class="d-ln" d="M318 54V78H43V58" marker-end="url(#ar)"/>', txt(180, 92, 'repeat until the goal is met or a person takes over', 'd-s'))),
    CK(0, 1)]),
  ('Where agents help, and the risks', [
    UL('Troubleshooting: collect output from many devices, correlate with logs, suggest root causes.', 'Change preparation: draft configs, check them against standards, summarise the impact.',
       'Operations: summarise alerts, open tickets, answer "what changed?" questions.'),
    UL('Hallucination: confident but wrong answers or invented commands.', 'Blast radius: an agent with write access can break things quickly.', 'Data exposure: sending confidential configs to the wrong service.'),
    P('Guardrails: least privilege (read-only by default), human approval for changes, logging of every action, and testing in a lab first.'),
    TIP('On the exam, if AI output conflicts with the device output in front of you, the device output wins.'),
    CK(2, 3, 4, 5, 10)]),
  ('Writing a good prompt', [
    TB(['Component', 'Example'], ['Persona', 'You are a senior Cisco network engineer.'], ['Instructions / task', 'Explain why R1 has no OSPF neighbour on Gi0/1 and list the checks in order.'],
       ['Context / data', 'Sanitised output of show ip ospf interface brief and show ip ospf neighbor.'], ['Output format', 'A numbered list, each with the IOS command to verify it.'],
       ['Data classification', 'Mask passwords, keys, communities, public IPs; only use approved tools for confidential data.']),
    P('"Fix my OSPF" will get a generic answer. The more precise the role, task, data and format, the more useful the result.'),
    CK(6, 7, 8, 9, 11)]),
 ],
 [('5.1', 'Describe the role of agentic AI in network operations'), ('5.2', 'Select a generative AI prompt for network operations, considering components such as data classification, output format, persona and instructions')])
S.append(sec('AI in Network Operations', 'AI', G, '', L, qs))
