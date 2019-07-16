# Build Micropython on win10 

## Prepare 

### A) Install ubuntu on Windows Subsystem for Linux (WSL1) 
1. Enable the Windows Subsystem for Linux 
from an elevated PowerShell window run
``` Powershell
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
#for WSL v2 also enable
Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform
```
2. Reboot (may not be needed depending on the features enabled)
3. Install ubuntu from the Microsoft store 
4. start ubuntu for the first time: `ubuntu` or `wsl`
Installing, this may take a few minutes...
5. create a user / password


ref:
- https://docs.microsoft.com/en-us/windows/wsl/install-win10
- https://docs.microsoft.com/en-us/windows/wsl/wsl2-install


### B) Install build tools and dependencies on Ubuntu/Linux

See: https://github.com/micropython/micropython/blob/master/README.md#external-dependencies

For Unix port, libffi library and pkg-config tool are required. On Debian/Ubuntu/Mint derivative Linux distros, install build-essential (includes toolchain and make), libffi-dev, and pkg-config packages.

``` bash
sudo apt update && sudo apt upgrade
sudo apt install build-essential
sudo apt install libffi-dev pkg-config
```
Note: you will need to conform installation and restart of services several times during the installation

### C) Clone the MicroPython git repro  
The assumption is that you have a c:\develop folder where the micropython repo will be cloned into.  
Adjust this path as per your preference.

#### Clone from Windows:
As the MicroPython repo uses symbolic links, make sure that  you have enabled the use of symlinks in Windows by enabling the windows developer mode
git for windows does support symbolic links 
https://github.com/git-for-windows/git/wiki/Symbolic-Links 

1. Enable Windows developer mode in order to enable git clone to use symlinks  
    Windows > Settings > Developer Mode > Enable/select 
2. Clone the micropython repo to c:\develop\micropython
3. Update/Get the git submodules
``` powershell
cd \develop
git clone -c core.symlinks=true https://github.com/micropython/micropython.git
cd micropython
git submodule update --init
``` 

#### Clone from Ubuntu: 
The Windows file system is located at `/mnt/c` in the ubuntu/Bash shell environment.

2. Clone the micropython repo to /mnt/c/develop/micropython
3. Update/Get the git submodules
``` bash
cd /mnt/c/develop/
git clone -c core.symlinks=true https://github.com/micropython/micropython.git
cd micropython/
sudo git submodule update --init
``` 

### D) Build the MicroPython cross-compiler, mpy-cross
Most ports require the MicroPython cross-compiler to be built first. This program, called mpy-cross, is used to pre-compile Python scripts to .mpy files which can then be included (frozen) into the firmware/executable for a port. To build mpy-cross use:
``` bash
cd /mnt/c/develop/micropython/
cd mpy-cross
make
```


## II Build a specific port 
### A) Unix 
No additional toolchain is required 
1. Build MicroPython for Unix 
@Ubuntu : 
``` bash
cd /mnt/c/develop/micropython/
cd ports/unix/
make 
``` 

### ESP32 
2. ESP32 
---------
#### A) Linux toolchain and prereqs
see : https://docs.espressif.com/projects/esp-idf/en/stable/get-started/linux-setup.html


#### B) edit .profile 

Set up PATH and IDF_PATH by adding the following line to ~/.profile file:

edit the standard profile using `nano ~/.profile`  
and add the following lines to the end of the .profile 
```
export PATH="$HOME/esp/xtensa-esp32-elf/bin:$PATH"
export IDF_PATH=~/esp/esp-idf
```
Log off and log in back to make this change effective.

#### B) Install prereqs and download xtensa tools
@Ubuntu : 
``` bash
#Install prereqs 
sudo apt-get install gcc git wget make libncurses-dev flex bison gperf python python-pip python-setuptools python-serial python-cryptography python-future

#download and extract espressif tools
cd ~
mkdir -p ~/Downloads
cd ~/Downloads
wget https://dl.espressif.com/dl/xtensa-esp32-elf-linux64-1.22.0-80-g6c4433a-5.2.0.tar.gz

mkdir -p ~/esp
cd ~/esp
tar -xzf ~/Downloads/xtensa-esp32-elf-linux64-1.22.0-80-g6c4433a-5.2.0.tar.gz
```

#### C) Get ESP-IDF
Do make sure you checkout the ESP-IDF version that matches the micropython build you are working with.  
to verify the supported build, run : 

@Ubuntu : 
``` bash
cd /mnt/c/develop/micropython/
cd ports/esp32/
make idf-version
```
`ESP IDF supported hash: 6b3da6b1882f3b72e904cc90be67e9c4e3f369a9`

@Ubuntu : 
``` bash
cd ~/esp
git clone -b v3.2.2 --recursive https://github.com/espressif/esp-idf.git
cd ~/esp/esp-idf
# git checkout <Supported Git hash from make>
git checkout 6b3da6b1882f3b72e904cc90be67e9c4e3f369a9
git submodule update --init --recursive
``` 

#### D) install ESP-IDF python (2.7)  prereqs 
@Ubuntu : 
``` bash
# install espressif python (2.7)  prereqs 
pip install --user -r $IDF_PATH/requirements.txt
# or 
pip install --user -r ~/esp/esp-idf/requirements.txt
```

#### E) install micropython prereqs 

Needs to be available to python 2.x that is still used by the ESP-IDF

@Ubuntu : 
``` bash
python2 -m pip install pyserial pyparsing
#python -m pip install pyserial pyparsing

```

#### F) Build MicroPython for ESP32
@Ubuntu : 
``` bash
cd /mnt/c/develop/micropython/
cd ports/esp32/
#use multiple tasks to speed up 
make -j 4 PYTHON=python2
``` 

#### G) Resulting files: 

This will produce binary firmware images in the build/ subdirectory (three of them: bootloader.bin, partitions.bin and application.bin).
The file `build/firmware.bin` is the combined firmware image
```
user@machine:/mnt/c/develop/micropython/ports/esp32$ ll build/*.bin
-rwxrwxrwx 1 root root 1097472 Jul 15 23:24 build/application.bin*
-rwxrwxrwx 1 root root   20640 Jul 15 23:23 build/bootloader.bin*
-rwxrwxrwx 1 root root    3072 Jul 15 23:22 build/partitions.bin*
-rwxrwxrwx 1 root root 1158912 Jul 15 23:24 build/firmware.bin*
```

Note: 
while testing it was not possible to connect to the micropython board from ubuntu running in WSL1
access worked from windows , but not from wsl. 
``` bash
esptool.py --port $PORT chip_id
#> OSError: [Errno 5] Input/output error: '/dev/ttyS1'
```
( permissions on the port and group were set correctly )
even forcing permissions this did not work
```
sudo chgrp dialout /dev/ttyS1
sudo chmod 666 /dev/ttyS1
```

#### H) Flash firmware to board 

##### From Windows 
``` powershell
$PORT = "COM1"
$BAUD = 460800
$FLASH_MODE = "dio"
$FLASH_FREQ = "40m"
$FILE = "C:\develop\micropython\ports\esp32\build\firmware.bin"

esptool.py --chip esp32 --port $PORT --baud $BAUD write_flash -z --flash_mode $FLASH_MODE --flash_freq $FLASH_FREQ 0x1000 $FILE
```
