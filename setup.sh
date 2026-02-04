#!/usr/bin/env bash
set -e

echo "[*] MAD Linux setup starting..."

# Sanity checks
if [[ $EUID -ne 0 ]]; then
  echo "[!] Please run as root (sudo ./setup.sh)"
  exit 1
fi


# System update

echo "[*] Updating system..."
apt update -y && apt upgrade -y


# Core dependencies

echo "[*] Installing core packages..."
apt install -y \
  curl wget unzip git \
  python3 python3-pip python3-venv \
  build-essential \
  ca-certificates \
  software-properties-common \
  apt-transport-https


# Virtualization
echo "[*] Installing VirtualBox..."
apt install -y virtualbox virtualbox-ext-pack || true

# Vagrant
echo "[*] Installing Vagrant..."
if ! command -v vagrant >/dev/null 2>&1; then
  wget -q https://releases.hashicorp.com/vagrant/2.4.9/vagrant_2.4.9-1_amd64.deb
  dpkg -i vagrant_2.4.1_linux_amd64.deb || apt -f install -y
  rm vagrant_2.4.1_linux_amd64.deb
fi

# Python libraries (MAD controller)
echo "[*] Installing Python libraries..."
pip3 install --upgrade pip
pip3 install \
  pyyaml \
  wcwidth

# Optional AD interaction tools (NO exploitation)
echo "[*] Installing optional AD tooling..."
apt install -y \
  smbclient \
  ldap-utils \
  krb5-user \
  dnsutils \
  nmap

# Kerberos defaults
if [ ! -f /etc/krb5.conf ]; then
cat <<EOF >/etc/krb5.conf
[libdefaults]
  default_realm = HAWKINS.MAD
  dns_lookup_kdc = true
  dns_lookup_realm = true
  rdns = false
EOF
fi

# Vagrant plugins
echo "[*] Installing Vagrant plugins..."
vagrant plugin install vagrant-reload || true
vagrant plugin install vagrant-vbguest || true

# Done
echo "[✓] Linux setup complete"
echo "[i] You can now run: ./mad.py"
