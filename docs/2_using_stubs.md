# 2 - Using stubs

## 2.1 - Manual configuration

the manual configuration, including sample configuration files is described in detail in the sister-repo [micropython-stubs][] section [using-the-stubs][]

---------

# 2 - Using stubs

### 2.1 - Manual configuration

## Using the stubs 

In order to use the stubs you need to do a few things:  

  1.  Download a copy of this repo , either via `git clone` or by download a zip file with it's contents
      - store this in a folder, for example 'next to' your software projects such as in `c:\develop\micropython-stubs`  
        this contains a `stubs` folder that contains all stubs

  2.  Over time you may want to periodically update this folder using `git pull`

### For each project where you want to use the stubs (Manual configuration) :   

this is not as complex as it seems,

  1.  **Create a symlink folder to `c:\develop\micropython-stubs\stubs` inside your project**  
      This will allow you to reference the same stub files from multiple projects, and limit the space needed. This a recommendation, and things work equally well if you copy the `stubs` folder into your project.  
      For details on how to create a symlink, please see : **2.3 Create a symbolic link**



 1. **Copy the [samples](doc/samples) folder to your project**  
     this contains the base files you need to improve syntax highlighting and linting.

 2. **Select which stub folders you need to reference**  

    - The order will influence results. place the 'higher quality' folders first.
    - Use forward slashes `/` rather than backslashes, also on Windows.
    - for example for micropython 1.13 on an ESP32 select:
      1. "./src/lib",

      2. "all-stubs/cpython_patch",

    3. "all-stubs/mpy_1_13-nightly_frozen/esp32/GENERIC", 

       4. "all-stubs/esp32_1_13_0-103",

          

 3. **Configure VSCode to use the selected stub folders**  
    This instructs the VSCode Pylance to consider your libs folder and the stubs for static code evaluation.
    VSCode allows this configuration to be set on **_workspace_** or _user_ level. I prefer setting it per workspace as that allows different settings for different projects, but you could do either.

    the configuration is [Pylance]([Pylance - Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)) specific, and is simplifed compared to the now depricated 'Microsoft Mython Language Server' 

    - use the [`.VSCode/settings.json` sample file](docs/samples/.VSCode/settings.json) located in the sample folder
    - you can open this file in VSCode itself, or use the settings menu 
    - add the folders to the `python.autoComplete.extraPaths` section. 
    - it can be on a single line or split across lines. 
      - make sure it is a valid json array 

    ```json
         "python.languageServer": "Pylance",
         "python.analysis.autoSearchPath": true,
         "python.autoComplete.extraPaths": [
              "src/lib", 
              "all-stubs/cpython_patch", 
              "all-stubs/mpy_1_13-nightly_frozen/esp32/GENERIC", 
              "all-stubs/esp32_1_13_0-103",
         ]
        "python.linting.enabled": true,
        "python.linting.pylintEnabled": true,
    ```

 4. **Configure pylint to use the selected stub folders**  
    This instructs pylint to insert the list of paths into `sys.path` before performing linting, thus allowing it to find the stubs and use them to better validate your code. 

    - use the [.pylintcr sample file](docs/sample/.pylintrc) located in the sample folder

    - edit the line that starts with `init-hook=`  

      ``` ini
      init-hook='import sys;sys.path[1:1] = ["src/lib", "folder1","folder2", "folder3",];'
      ```

    - replace the folders with your selection of stub folders. **In this case they MUST be on a single line**

    - the result should look like:

      ``` ini
      init-hook='import sys;sys.path[1:1] = ["src/lib", "all-stubs/cpython_patch","all-stubs/mpy_1_13-nightly_frozen/esp32/GENERIC", "all-stubs/esp32_1_13_0-103",];'
      ```

 5. **Restart VSCode**  
    VSCode must be restated for the Python language engine and Pylint to read the updated configuration.
    you can use: 

    - the `Developer: Reload Window` command.
    - or stop / start the editor

## Order of the stub folders

The stubs are used by 3 components.

  1. pylint
  2. the VSCode Pylance Language Server
   3. the VSCode Python add-in

These 3 tools work together to provide code completion/prediction, type checking and all the other good things.
For this the order in which these tools use  the stub folders is significant, and best results are when they use the same order. 

In most cases the best results are achieved by the below setup:  

![stub processing order](docs/img/stuborder.png)

  1. **Your own source files**, including any libraries you add to your project.
     This can be a single libs folder or multiple directories

  2. **The CPython common stubs**. These stubs are handcrafted to mimic MicroPython modules on a CPython system.
     there are only a limited number of these stubs. ALso for some modules this approach does not appear to work. (such as the `cg` and `sys` modules)

  3. **Firmware specific frozen stubs**. Most micropython firmwares include a number of python modules that have been included in the firmware as frozen modules in order to take up less memory.
     these modules have been extracted from the source code. where possible this is done per port and board,  or if not possible the common configuration for has been included.

  4. **Micropython-stubber Stubs**. For all other modules that are included on the board, [micropython-stubber](https://github.com/Josverl/micropython-stubber) or [micropy-cli](https://github.com/BradenM/micropy-cli) has been used to extract as much information as available, and provide that as stubs. While there is a lot of relevant and useful information for code completion, it does unfortunately not provide all details regarding parameters that the earlier  options may provide.


When using a different code editor, a similar configuration may be used. 

 _**Note:**_ While it is possible for you to configure different processing orders, this will probably lead to confusing or contradicting feedback in the code editor that you are using.

## 2.2 - Using micropy-cli

'micropy-cli' is  command line tool for managing MicroPython projects with VSCode
If you want a command line interface to setup a new project and configure the settings as described above for you, then take a look at : [micropy-cli]  

``` 
pip install micropy-cli
micropy init
```

Braden has essentially created a front-end for using micropython-stubber, and the configuration of a project folder for pymakr. 

micropy-cli  maintains its own repository of stubs. 



## 2.3 Create a symbolic link

To create the symbolic link to the `micropython-stubs/stubs` folder the instructions differ slightly for each OS/
The below examples assume that the micropython-stubs repo is cloned 'next-to' your project folder.
please adjust as needed.

### Windows 10 

Requires `Developer enabled` or elevated powershell prompt.

``` powershell
# target must be an absolute path, resolve path is used to resolve the relative path to absolute
New-Item -ItemType SymbolicLink -Path "all-stubs" -Target (Resolve-Path -Path ../micropython-stubs/stubs)
```

or use [mklink](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/mklink) in an (elevated) command prompt

``` cmd
rem target must be an absolute path
mklink /d all-stubs c:\develop\micropython-stubs\stubs
```

### Linux/Macos/Unix

``` sh
# target must be an absolute path
ln -s /path/to/micropython-stubs/stubs all-stubs
```

## 



---------------



[stubs-repo]:   https://github.com/Josverl/micropython-stubs
[stubs-repo2]:  https://github.com/BradenM/micropy-stubs
[micropython-stubber]: https://github.com/Josverl/micropython-stubber
[micropython-stubs]: https://github.com/Josverl/micropython-stubs#micropython-stubs
[micropy-cli]: https://github.com/BradenM/micropy-cli
[using-the-stubs]: https://github.com/Josverl/micropython-stubs#using-the-stubs
[demo]:         docs/img/demo.gif	"demo of writing code using the stubs"
[stub processing order]: docs/img/stuborder_pylance.png	"recommended stub processing order"
[naming-convention]: #naming-convention-and-stub-folder-structure
[all-stubs]: https://github.com/Josverl/micropython-stubs/blob/master/firmwares.md
[micropython]: https://github.com/micropython/micropython
[micropython-lib]:  https://github.com/micropython/micropython-lib
[pycopy]: https://github.com/pfalcon/pycopy
[pycopy-lib]: https://github.com/pfalcon/pycopy-lib
[createstubs-flow]: docs/img/createstubs-flow.png
[symlink]: #6.4-create-a-symbolic-link



