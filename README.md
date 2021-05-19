# AwB Tech Change Management System 
The change management system originally created for OeP Company and adpapted to be used with any company as a IT Change Management System.

## Requirements
 - Ubuntu Server 18.04 - 20.04
 - 35 GB Storage Space
 - 2-4 GB RAM

## Installation

```bash
sudo -i
apt-get update && apt-get upgrade -y
apt-get install python3-pip python3-dev nginx git unixodbc-dev
apt-get update
pip3 install virtualenv
git clone https://github.com/andrewixl/oepcm.git

cd reverseproxy
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
sudo ufw allow 8000
bash install.sh
```

## Usage
Change Management GUI is Accessable at SERVER_IP.

#### Troubleshooting Commands:
- sudo service nginx restart
- sudo reboot

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
