from django.core.management.base import BaseCommand
from honeypot_dashboard.command.base import BaseCommands
from stix.models import AttackPatternType, MalwareLabel, StixType, CourseOfAction, IdentityType


class Command(BaseCommand, BaseCommands):

    def __init__(self):
        super(Command, self).__init__()
        BaseCommands.__init__(self, database="default")

    def handle(self, *args, **options):
        try:
            # Handling Attack Pattern Type
            self.stdout.write(self.style.WARNING('Handling Attack Pattern type Table'))
            self.truncate_table(AttackPatternType._meta.db_table)
            attack_pattern_types = """Reconnaissance Attacks#These rules detect reconnaissance or information-gathering attacks being performed on the network. Reconnaissance is a type of computer attack in which an intruder engages with the targeted system to gather information about vulnerabilities.%Web Browser Attacks#These rules detect attacks that infect a web browser by taking advantage of vulnerabilities in browser security, such as, Cross Site Scripting, Browser Cache Poisoning, Drive-by-download et-etcetera%Botnet C&C Communication#These rules detect malicious botnet C&C communication occurring over the network. Command-and-control servers, also called C&C or C2, are used by attackers to maintain communications with compromised systems within a target network. Botnet�s are intended to follow specific instructions that are received from its C&C, the instructions are set of commands based on purpose and structure of the botnet.%Chat Application Attacks#These rules will detect attacks that target chatting software and messaging platforms such as, Facebook, Google Talk and Skype.%Malicious IP Communication#These rules will detect IP addresses referencing malicious server communication over the network.%Exploit Based Attacks#These rules detect attacks which target and exploit specific vulnerabilities or security flaws in an application or system  so that an attacker can use it for their benefit.%Protocol Attacks#These rules detect attacks which target a specific feature or implementation bug of a particular protocol. This type of attack consumes actual server resources, or those of intermediate communication equipment, such as firewalls and load balancers.%Game Application Attacks#These rules detect attacks that target security issues in gaming applications, servers and online platforms such as, Minecraft, Nintendo User Agent et-etcetera.%Malware Attacks#These rules detect the  presence  of malware in a host system or network. Malware is a malicious software that was intentionally developed to infiltrate or damage a computer system without consent of the owner. This includes, among others, viruses, worms, and Trojan horses.%Miscellaneous Attacks#These rules detect multiple miscellaneous file and network based attacks.%Mobile Malware Attacks#These rules detect the presence of mobile malware. A mobile malware is a malicious software that specifically targets the operating systems on mobile phones or wireless-enabled Personal digital assistants (PDA), causing the collapse of the system and loss or leakage of confidential information.%NetBIOS Attacks#These rules detect attacks targeted on NetBIOS. A network basic input output system (NetBIOS) is a system service that acts on the session layer of the OSI model and controls how applications residing in separate hosts/nodes communicate over a local area network.%Application Policy Communication#These rules detect the network traffic of certain restricted applications according to organization�s policy like Torrent, NMAP, Gaming Applications, Free Proxy Servers et-etcetera%Shellcode Attacks#These rules detect attacks based on shellcode payloads. Shellcode can be described as code executed by a target program due to a vulnerability exploit and used to open a remote shell � that is, an instance of a command line interpreter � so that an attacker could use that shell to further interact with the victim�s system.%SQL Attacks#These rules detect attacks targeting vulnerabilities in the SQL application, such as executing malicious SQL statements and  feeding unsanitized input.%User Agent Attacks#These rules detect the presence of suspicious user agents in network traffic, which are software agents acting on behalf of a user, such as web browser that retrieves, renders and facilitates end user interaction with Web content.%Web Application Attacks#These rules detect attacks that target security flaws present in web applications and web services. These flaws allow criminals to gain direct and public access to databases in order to churn sensitive data. Some such attacks include Cross Site Scripting, SQL Injection and Cross Site Request Forgery.%Application Server Attacks#These rules detect attacks targeting critical application servers such as mail servers, Samba servers and SQL servers. Servers hold crucial information which is the primary motivation behind application server attacks.%File Attacks#These rules detect the presence of suspicious files travelling over the network which may contain malicious applications or exploit codes.%Data Obfuscation#These rules detect any kind of obfuscated data travelling over the network. Data obfuscation (DO) is a form of data masking where data is purposely scrambled to prevent unauthorized access to sensitive materials. Malware attacks and exploits are obfuscated by hackers to hide the attack.%Operating System Attacks#These rules detect attacks that attempt to exploit security flaws present in operating systems such as, unpatched applications and security misconfiguration.%Potentially Unwanted Application Attacks#These rules detect the presence of potentially unwanted applications in the network or host. A Potentially Unwanted Application (PUA) has behaviours or aspects that can be considered undesirable or unwanted, depending on the user's context. Applications may be potentially unwanted if they include security vulnerabilities, are unlicensed, or are not sanctioned by the network administrator, among other reasons.%Global Recent Breakouts#These rules detect the exploit, malware and other network attacks happened in recent worldwide breakout%Network Compromise Indicators#These rules detect responses from the target systems and applications which indicate that the target has been compromised by the originated attack%Attack Responses#These rules detect responses from the target system when a suspicious attack request is sent before complete compromise%TOR Communication#These rules will detect IP addresses referencing TOR Network%Denial of Service Attacks#These rules detect DoS attacks, a type of cyber attack in which a malicious actor aims to render a computer or other device unavailable to its intended users by interrupting the device's normal functionaing. DoS attacks typically function by overwhelming or flooding a targeted machine with requests until normal traffic is unable to be processed, resulting in DoS%SCADA Attacks#These rules detect attacks targetting and network communication over SCADA Protocols and OT networks"""
            attack_pattern_types = attack_pattern_types.split("%")
            attack_pattern_model = []
            for attack_pattern_type in attack_pattern_types:
                attack_pattern_type = attack_pattern_type.split("#")
                attack_pattern_model.append(
                    AttackPatternType(name=attack_pattern_type[0], description=attack_pattern_type[1]))
            AttackPatternType.objects.bulk_create(attack_pattern_model)
            self.stdout.write(self.style.SUCCESS('Successfully created Attack Pattern Type'))

            # Handling Malware Label
            self.stdout.write(self.style.WARNING('Handling Malware Label Table'))
            self.truncate_table(MalwareLabel._meta.db_table)
            malware_labels = """adware#Any software that is funded by advertising. Adware may also gather sensitive user information from a system.%backdoor#A malicious program that allows an attacker to perform actions on a remote system, such as transferring files, acquiring passwords, or executing arbitrary commands%bot#A program that resides on an infected system, communicating with and forming part of a botnet. The bot may be implanted by a worm or Trojan, which opens a backdoor. The bot then monitors the backdoor for further instructions.%ddos#A tool used to perform a distributed denial of service attack.%dropper#A type of trojan that deposits an enclosed payload (generally, other malware) onto the target computer.%exploit-kit#A software toolkit to target common vulnerabilities.%keylogger#A type of malware that surreptitiously monitors keystrokes and either records them for later retrieval or sends them back to a central collection point.%ransomware#A type of malware that encrypts files on a victim's system, demanding payment of ransom in return for the access codes required to unlock files.%remote-access-trojan#A remote access trojan program�(or RAT), is a trojan horse capable of controlling a machine through commands issued by a remote attacker.%resource-exploitation#A type of malware that steals a system's resources (e.g., CPU cycles), such as a bitcoin miner.%rogue-security-software#A fake security product that demands money to clean phony infections.%rootkit#A type of malware that hides its files or processes from normal methods of monitoring in order to conceal its presence and activities. Rootkits can operate at a number of levels, from the application level���simply replacing or adjusting the settings of system software to prevent the display of certain information���through hooking certain functions or inserting modules or drivers into the operating system kernel, to the deeper level of firmware or virtualization rootkits, which are activated before the operating system and thus even harder to detect while the system is running.%screen-capture#A type of malware used to capture images from the target systems screen, used for exfiltration and command and control.%spyware#Software that gathers information on a user's system without their knowledge and sends it to another party. Spyware is generally used to track activities for the purpose of delivering advertising.%trojan#Any�malicious computer program which is used to hack into a computer by misleading users of its true intent.%virus#A malicious computer program�that replicates by reproducing itself or infecting other programs by modifying them.%worm#A self-replicating, self-contained program that usually executes itself without user intervention."""
            malware_labels = malware_labels.split("%")
            malware_label_model = []
            for malware_label in malware_labels:
                malware_label = malware_label.split("#")
                malware_label_model.append(
                    MalwareLabel(name=malware_label[0], description=malware_label[1])
                )
            MalwareLabel.objects.bulk_create(malware_label_model)
            self.stdout.write(self.style.SUCCESS('Successfully created Malware Label'))

            # Handling Stix Type
            self.stdout.write(self.style.WARNING('Handling Stix Type Table'))
            self.truncate_table(StixType._meta.db_table)
            stix_types = """Malware#malware%Attack Pattern#attack_pattern%Course of Action#course_of_action%Identity#idnetity%Indicator#Indicator%Observed Data#observed_data%Report#report%Threat Actors#threat_actors%Vulnerability#vulnerability"""
            stix_types = stix_types.split("%")
            stix_type_model = []
            for stix_type in stix_types:
                stix_type = stix_type.split("#")
                stix_type_model.append(StixType(name=stix_type[0], identifier=stix_type[1]))
            StixType.objects.bulk_create(stix_type_model)
            self.stdout.write(self.style.SUCCESS('Successfully created STIX Type'))

            # Handle COA Data
            self.stdout.write(self.style.WARNING('Handling COA Table'))
            self.truncate_table(CourseOfAction._meta.db_table)
            CourseOfAction.objects.create(name="Default", description="Default COA", generic_id=None,
                                          action="10.113.59.15/course_of_action/data.pdf")
            self.stdout.write(self.style.SUCCESS('Successfully created COA'))

            # Handle Identity type
            self.stdout.write(self.style.WARNING('Handling Identity Table'))
            self.truncate_table(IdentityType._meta.db_table)
            IdentityType.objects.create(name="Subex Honeypot",
                                        description="Honeypot based in Subex Bangalore India Consists of 1000 IOT devices, designed for getting IOT, OT and IT attacks.",
                                        label=None, identity_class="Organization", sectors=None,
                                        contact_information="manav.chawla@subex.com")
            self.stdout.write(self.style.SUCCESS('Successfully created Identity Type Table'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(str(e)))
