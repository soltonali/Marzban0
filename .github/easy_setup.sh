#!/usr/bin/env bash

rm -rf "/opt/marzban";
rm -rf "/usr/bin/marzban-cli";
rm -rf "/var/lib/marzban";

mkdir -p /opt/marzban;
mkdir -p /var/lib/marzban/

cd /opt/marzban;
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install --beta
git clone https://github.com/soltonali/Marzban0.git;
mv ./Marzban0/* ./;
cp ./xray_config.json /var/lib/marzban/xray_config.json
rm -rf ./Marzban
rm -rf ./Marzban0
clear;
echo "marzban downloaded";
echo "install deps..."
pip install -r requirements.txt
clear;
alembic upgrade head
sudo ln -s $(pwd)/marzban-cli.py /usr/bin/marzban-cli
sudo chmod +x /usr/bin/marzban-cli
marzban-cli completion install
cp .env.example .env
#nano  m .env
cp ./marzban0.service /var/lib/marzban/marzban.service
systemctl enable /var/lib/marzban/marzban.service
systemctl start marzban
