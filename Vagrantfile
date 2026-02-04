# Vagrantfile
require 'yaml'

# Load user configuration
config_file = File.join(File.dirname(__FILE__), "config.yml")
settings = YAML.load_file(config_file) if File.exist?(config_file)

  def apply_dns(vm, dns_ip)
    vm.vm.provision "shell", privileged: true, inline: <<-PS
      Write-Host "Setting DNS on Ethernet 2 to #{dns_ip}"
      Set-DnsClientServerAddress -InterfaceAlias "Ethernet 2" -ServerAddresses #{dns_ip}
    PS
  end


Vagrant.configure("2") do |config|

  # Global SSH Settings
  config.ssh.username = "vagrant"
  config.ssh.private_key_path = "./id_rsa"
  config.ssh.insert_key = false

  # --- CHILD DOMAIN CONTROLLER: HAWKINS-DC01 ---
  if settings['install_root_ad']
  config.vm.define "MAD-VECNA-DC01" do |vecna_dc01|
    vecna_dc01.vm.box = "MAD-AD/VECNA-DC01"

    # Communication settings
    vecna_dc01.vm.communicator = "winrm"
    vecna_dc01.vm.boot_timeout = 1200
    vecna_dc01.winrm.retry_limit = 20
    vecna_dc01.winrm.retry_delay = 10

    # Networking
    vecna_dc01.vm.network "private_network", ip: "192.168.56.110", adapter: 2
    apply_dns(vecna_dc01, "192.168.56.110,192.168.56.115")
    
    # VirtualBox provider settings
    vecna_dc01.vm.provider "virtualbox" do |vb|
      vb.name = "MAD-VECNA-DC01"
      vb.gui = true
    end
  end
    config.vm.define "MAD-ARCADE-PC01" do |arcade_pc01|
    arcade_pc01.vm.box = "MAD-AD/ARCADE-PC01"

    arcade_pc01.vm.communicator = "winrm"
    arcade_pc01.vm.boot_timeout = 1200
    arcade_pc01.winrm.retry_limit = 20
    arcade_pc01.winrm.retry_delay = 10

    arcade_pc01.vm.network "private_network", ip: "192.168.56.120", adapter: 2
    apply_dns(arcade_pc01, "192.168.56.110")

    arcade_pc01.vm.provider "virtualbox" do |vb|
      vb.name = "MAD-ARCADE-PC01"
      vb.gui = true
    end
  end
    config.vm.define "MAD-DND-SERVER" do |dnd_server|
    dnd_server.vm.box = "MAD-AD/DND-SERVER"

    dnd_server.vm.communicator = "ssh"
    dnd_server.vm.boot_timeout = 300

    dnd_server.vm.network "private_network", ip: "192.168.56.125"

    dnd_server.vm.provider "virtualbox" do |vb|
      vb.name = "MAD-DND-SERVER"
      vb.gui = true
      vb.check_guest_additions = false
    end
  end
end

  # --- ROOT DOMAIN CONTROLLER: VECNA-DC01 ---
  if settings['install_child_ad']
  config.vm.define "MAD-BRENNER-DC02" do |brenner_dc02|
    brenner_dc02.vm.box = "MAD-AD/BRENNER-DC02"

    # Communication settings
    brenner_dc02.vm.communicator = "winrm"
    brenner_dc02.vm.boot_timeout = 1200
    brenner_dc02.winrm.retry_limit = 20
    brenner_dc02.winrm.retry_delay = 10

    # Networking
    brenner_dc02.vm.network "private_network", ip: "192.168.56.115", adapter: 2
    apply_dns(brenner_dc02, "192.168.56.115,192.168.56.110")

    # VirtualBox provider settings
    brenner_dc02.vm.provider "virtualbox" do |vb|
      vb.name = "MAD-BRENNER-DC02"
      vb.gui = true
    end
  end
    config.vm.define "MAD-LAB-SYSTEM01" do |lab_sys|
    lab_sys.vm.box = "MAD-AD/LAB-SYSTEM01"

    lab_sys.vm.communicator = "winrm"
    lab_sys.vm.boot_timeout = 1200
    lab_sys.winrm.retry_limit = 20
    lab_sys.winrm.retry_delay = 10

    lab_sys.vm.network "private_network", ip: "192.168.56.130", adapter: 2
    apply_dns(lab_sys, "192.168.56.110")

    lab_sys.vm.provider "virtualbox" do |vb|
      vb.name = "MAD-LAB-SYSTEM01"
      vb.gui = true
    end
  end
      config.vm.define "MAD-BYERS-PC01" do |byers_pc01|
    byers_pc01.vm.box = "MAD-AD/BYERS-PC01"

    byers_pc01.vm.communicator = "winrm"
    byers_pc01.vm.boot_timeout = 1200
    byers_pc01.winrm.retry_limit = 20
    byers_pc01.winrm.retry_delay = 10

    byers_pc01.vm.network "private_network", ip: "192.168.56.135", adapter: 2
    apply_dns(byers_pc01, "192.168.56.115")

    byers_pc01.vm.provider "virtualbox" do |vb|
      vb.name = "MAD-BYERS-PC01"
      vb.gui = true
    end
  end
end
  if settings['install_adcs']
    config.vm.define "MAD-STARCOURT-DC" do |starcourt_dc|
    starcourt_dc.vm.box = "MAD-AD/STARCOURT-DC"

    # Communication settings
    starcourt_dc.vm.communicator = "winrm"
    starcourt_dc.vm.boot_timeout = 1200
    starcourt_dc.winrm.retry_limit = 20
    starcourt_dc.winrm.retry_delay = 10

    # Networking
    starcourt_dc.vm.network "private_network", ip: "192.168.56.155", adapter: 2
    apply_dns(starcourt_dc, "192.168.56.155,192.168.56.110")
    
    # VirtualBox provider settings
    starcourt_dc.vm.provider "virtualbox" do |vb|
      vb.name = "MAD-STARCOURT-DC"
      vb.gui = true
    end
  end
end
end