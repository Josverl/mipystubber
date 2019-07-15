# Build Micropython on win10 

## Prepare 

### Install ubuntu on Windows Subsystem for Linux (WSL1) 
1. Enable the Windows Subsystem for Linux 
``` Powershell
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
#for WSL v2 also enable
Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform
```
2. Reboot
3. install ubuntu from the microsoft store 
4. start ubunto for the first time `ubuntu`
Installing, this may take a few minutes...
5. create a user / password

6. enable Windows developermode in order to enable git clone to use symlinks 


ref:
- https://docs.microsoft.com/en-us/windows/wsl/install-win10
- https://docs.microsoft.com/en-us/windows/wsl/wsl2-install



### Install buildtools and dependencies on linux/ubunto  

See: https://github.com/micropython/micropython/blob/master/README.md#external-dependencies

For Unix port, libffi library and pkg-config tool are required. On Debian/Ubuntu/Mint derivative Linux distros, install build-essential (includes toolchain and make), libffi-dev, and pkg-config packages.

``` bash
sudo apt update && sudo apt upgrade
sudo apt install build-essential
sudo apt install libffi-dev pkg-config
```

### C. using the micropython git repro from win & ubuntu 
1. @windows : clone the micropython repo to c:\develop\micropython

https://github.com/git-for-windows/git/wiki/Symbolic-Links 

```
git clone -c core.symlinks=true https://github.com/micropython/micropython.git
``` 


the Windows file system is located at `/mnt/c` in the ubuntu/Bash shell environment.
get the git submodules (can be done either from windows or ubuntu)
2. @ubunto : 
``` bash
cd /mnt/c/develop/micropython/
git submodule update --init`
``` 


### D. Build the MicroPython cross-compiler, mpy-cross
Most ports require the MicroPython cross-compiler to be built first. This program, called mpy-cross, is used to pre-compile Python scripts to .mpy files which can then be included (frozen) into the firmware/executable for a port. To build mpy-cross use:
``` bash
cd /mnt/c/develop/micropython/
cd mpy-cross
make
```


## II Build a specific port 
1. unix 
@ubunto : 
``` bash
cd /mnt/c/develop/micropython/
cd ports/unix/
make 
``` 

2. ESP32 
---------
1. linux toolchain and prereqs
see : https://docs.espressif.com/projects/esp-idf/en/stable/get-started/linux-setup.html


edit .profile 

Set up PATH and IDF_PATH by adding the following line to ~/.profile file:

edit the standard profile using `nano ~/.profile`  
and add the following lines to the end of the .profile 
```
export PATH="$HOME/esp/xtensa-esp32-elf/bin:$PATH"
export IDF_PATH=~/esp/esp-idf
```
Log off and log in back to make this change effective.

@ubunto : 
``` bash
sudo apt-get install gcc git wget make libncurses-dev flex bison gperf python python-pip python-setuptools python-serial python-cryptography python-future

#download and extract espressif tools
cd ~
mkdir -p ~/Downloads
cd ~/Downloads
wget https://dl.espressif.com/dl/xtensa-esp32-elf-linux64-1.22.0-80-g6c4433a-5.2.0.tar.gz

mkdir -p ~/esp
cd ~/esp
tar -xzf ~/Downloads/xtensa-esp32-elf-linux64-1.22.0-80-g6c4433a-5.2.0.tar.gz

#Add to Path 

cd ~/esp
git clone -b v3.2.2 --recursive https://github.com/espressif/esp-idf.git

# install espressif python prereqs 
pip install --user -r $IDF_PATH/requirements.txt

# install micropython prereqs 
pip install pyserial pyparsing




