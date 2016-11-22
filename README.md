UltraSafeBerry : RPi USB checker
===========================

The idea :
----------
Evaluate USB-keys dangerosity to avoid work-related computers to get infected.
It would ensure every **file** on the key isn't mallicious, nor **the usb-key itself**.

The (planned) build :
----------
A simple **Rasberry Pi**, powered by a computer or directly by a battery / power source.
It could be wired to the ( DMZed ) network to update its viral bases or its software, send samples to more advanced anti-virus platforms, send reports to CISOs....

Reminder
-----------
**BadUSB** : The USB key makes itself an HID device such as a keyboard or a network adaptator. It can then perform keystrokes or system attaks.

**USB-Kill** : A modified USB key aiming to destroy victim's computer with frequents over-powered charges.


Doability :
----------------
| Need  | Doable ?  | Source |
| ------------ | ------------ | ------------ |
| **File scan**  |   | ClamAV  |
| * Linux  | Oui  |   |
| * Windows  | Oui  |   |
| * Macros  | ?  | ?  |
| * Misc  | ?  | ?  |
| **BadUSB**   |  seems like it  | > sources |
| **USBKill**  | ?  | https://www.usbkill.com/usb-killer/9-usb-killer-tester.html  |



| Option  | Doable ?  | Source |
| ------------ | ------------ | ------------ |
| Send sample to cuckoo  |   |   |
| Virustotal or similar  |   | http://irma.quarkslab.com/  |


Sources
-----------
* https://github.com/dkopecek/usbguard
* https://github.com/trpt/usbdeath

* https://pyudev.readthedocs.io/en/latest/
* https://doc.ubuntu-fr.org/udev
* https://security.stackexchange.com/questions/64524/how-to-prevent-badusb-attacks-on-linux-desktop

* https://github.com/maliceio/malice
