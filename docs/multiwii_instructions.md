checked os version: cat /etc/os-release       version (of raspbian) is buster
upgrade to python3.7 (python --version gives 2.7.16)      sudo apt update
sudo apt full-upgrade          sudo apt install python3
(ssh back in) 
(for me, it said python3 was already installed)    sudo python3 get-pip.py
(gives no module named 'distutils.util')         sudo apt-get install python3-distutils
Next install MultiWii 0.0.1           pip3 install MultiWii
