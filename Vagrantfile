$script = <<SCRIPT
echo I am provisioning...

export DEBIAN_FRONTEND=noninteractive
apt-get -y -q update
apt-get -y -q upgrade

apt-get install -yq wget curl unzip

apt-get install -yq debhelper iptables-dev libavcodec-dev libavfilter-dev libavformat-dev libavresample-dev libavutil-dev libcurl4-openssl-dev libevent-dev libglib2.0-dev libhiredis-dev libpcap-dev libpcre3-dev libssl-dev markdown zlib1g-dev libxmlrpc-core-c3-dev
apt-get install -yq dkms linux-headers-`uname -r`

apt-get -y -q autoremove
apt-get -y -q clean

cd /usr/src/
curl -L -o rtpengine.zip https://github.com/sipwise/rtpengine/archive/master.zip
unzip -q rtpengine.zip

cd rtpengine-master/
./debian/flavors/no_ngcp
dpkg-buildpackage

cd ..
dpkg -i ngcp-rtpengine*.deb

echo ...Provisioning complete

SCRIPT



Vagrant.configure(2) do |config|

  config.vm.box = "ubuntu/xenial64"

  config.vm.hostname = "rtpengine"
  config.vm.provision "shell", inline: $script

  config.vm.provider "virtualbox" do |v|
    v.name = "rtpengine"
    v.memory = 512
  end
end