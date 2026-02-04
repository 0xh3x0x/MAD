#!/usr/bin/env bash
set -e

echo "[*] MAD KVM / VirtualBox compatibility fix"

if [[ $EUID -ne 0 ]]; then
  echo "[!] Please run as root: sudo ./fix-kvm.sh"
  exit 1
fi

# Detect CPU vendor
CPU_VENDOR=$(lscpu | grep "Vendor ID" | awk '{print $3}')

echo "[*] CPU Vendor detected: $CPU_VENDOR"

# Stop libvirt if running
if systemctl is-active --quiet libvirtd; then
  echo "[*] Stopping libvirtd service..."
  systemctl stop libvirtd
  systemctl disable libvirtd
fi

# Unload KVM modules
echo "[*] Unloading KVM kernel modules..."

modprobe -r kvm_intel 2>/dev/null || true
modprobe -r kvm_amd 2>/dev/null || true
modprobe -r kvm 2>/dev/null || true

# Blacklist KVM modules
echo "[*] Blacklisting KVM modules..."

cat <<EOF >/etc/modprobe.d/mad-disable-kvm.conf
blacklist kvm
blacklist kvm_intel
blacklist kvm_amd
EOF

# Update initramfs
echo "[*] Updating initramfs..."
update-initramfs -u

# Verify VirtualBox kernel modules
echo "[*] Rebuilding VirtualBox kernel modules..."
/sbin/vboxconfig || true

# Final status
echo
echo "[✓] KVM disabled for VirtualBox compatibility"
echo "[i] Reboot REQUIRED for changes to take effect"
echo
echo "After reboot, verify with:"
echo "  lsmod | grep kvm   # should return nothing"
echo "  VBoxManage list hostinfo | grep VT-x"
