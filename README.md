# haem
A simple manager for headless Android emulators

This tool is largely intended to manage a group of headless emulators for dev services like CI.

## Troubleshooting Android Emulator
Error message:
```
emulator: ERROR: x86 emulation currently requires hardware acceleration!
Please ensure KVM is properly installed and usable.
CPU acceleration status: This user doesn't have permissions to use KVM (/dev/kvm).

---- OR ----
emulator: ERROR: x86 emulation currently requires hardware acceleration!
Please ensure KVM is properly installed and usable.
CPU acceleration status: Could not open /dev/kvm :Permission denied
```
Solution (root perm required):
```bash
groupadd kvm  # create a kvm user group
usermod -G kvm -a yourloginuser # add yourself to the group
echo 'KERNEL=="kvm",GROUP="kvm",MODE="0660"' >> /etc/udev/rules.d/androidUseKVM.rules  # tell udev to grant kvm group the access to /dev/kvm
<reboot>
```

* [more, in Chinese](http://www.cnblogs.com/howdop/p/5347729.html)
