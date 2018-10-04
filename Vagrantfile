$script = <<-SCRIPT
echo I am provisioning

export DEBIAN_FRONTEND=noninteractive


apt-get -yq update
apt-get -yq upgrade

apt-get install -yq wget curl unzip devscripts equivs dpkg-dev

if [ $(lsb_release -c -s) == xenial ]; then apt-get -t xenial-backports install -yq debhelper; fi




cd /usr/src/
curl -L -o rtpengine.zip https://github.com/sipwise/rtpengine/archive/master.zip
unzip -q rtpengine.zip

cd rtpengine-master/
export DEB_BUILD_PROFILES="pkg.ngcp-rtpengine.nobcg729"

yes | mk-build-deps -i

dpkg-buildpackage

cd ..
dpkg -i ngcp-rtpengine-daemon*.deb

#apt-get -yq remove ngcp-rtpengine-build-deps
apt-get -yq autoremove
apt-get -yq clean


echo "[rtpengine]
table = -1
interface = $(hostname -i)
listen-ng = 2223" > /etc/rtpengine/rtpengine.conf


echo ...Provisioning complete




SCRIPT




servers=[
    {
        :hostname => "rtpengine-u18",
        :box => "ubuntu/bionic64",
        :ram => 512,
        :cpu => 1,
        :port => 16222
    },
    {
        :hostname => "rtpengine-u16",
        :box => "ubuntu/xenial64",
        :ram => 512,
        :cpu => 1,
        :port => 16222
    }
]


Vagrant.configure(2) do |config|

    servers.each do |machine|
        config.vm.provision "shell", inline: $script
        config.vm.define machine[:hostname] do |node|
        config.vm.network "forwarded_port", guest: 2223, host: machine[:port], protocol: "udp"
            node.vm.box = machine[:box]
            node.vm.hostname = machine[:hostname]
            node.vm.provider "virtualbox" do |vb|
                vb.name = machine[:hostname]
                vb.memory = machine[:ram]
            end
        end
    end
end

