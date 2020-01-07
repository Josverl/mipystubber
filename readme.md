# simplify and improve the writing of micropython code in Visual Studio code and other modern editors

In order to do this (I suggest) a few things are needed:
- Stub files for the native / enabled modules in the firmware using PEP 484 Type Hints
- Autocompletion / intellisense capabilities for python source files, using VSCode and the Python extension 
- Static syntax checks, or linting, using Pylint.
- Suppression of warnings that collide with the micropython principals or code optimization.

Not that the above is not limited to VSCode and Pylint, but it happens to be the combination that I use.
Please feel free to suggest and add other combinations and the relevant steps to configure these. 

The (stretch) goal is to create a vscode add-in to simplify the configuration, and allow easy switching between different firmwares and versions.
For now you will need to use the `microcli` tool, or configure this by hand as shown in the below sections.

## 'micropy' A command line tool for managing MicroPython projects with VSCode
If you want a command line interface to setup a new project and configure the settings as described above for you then take a look at :  
    https://github.com/BradenM/micropy-cli
    `pip install micropy-cl`
    then run `micropy init`

## File Structure 
The file structure is based on my personal windows environment, but you should be able to adapt that without much hardship to you own preference and OS.

| What                 | Why                      | Where                             |
|----------------------|--------------------------|-----------------------------------|
| stubber project      | needed to make stubs     | C:\develop\MyPython\Stubber\
| stub root            |                          | C:\develop\MyPython\Stubber\stubs
| generated stub files | needed to use stubs      | C:\develop\MyPython\Stubber\<firmware>
| Frozen stub files    | better code intellisense | C:\develop\MyPython\Stubber\<firmware>_Frozen
| vscode config        | configure vscode         | in project or global config
| pylint config        | pylint has own config    | .pylintrc in project folder 

## Configuring Visual Studio Code 

you will need to configure 2 modules 
- the VSCode Python extension , which stores its configuration in the VSCode settings files
- pylint, which stores its configuration in a .pylintrc file

### vscode workspace settings 
For simplicity in documentation I have configured most settings at workspace project level.
The same settings could be configured at User level, where they would become defaults for all your projects, and can be overridden per workspace/project.

#### Relevant VSCode settings
Setting | Default   | Description  | ref  
--------|-----------|--------------|--- 
python.autoComplete.|||[Autocomplete Settings](https://code.visualstudio.com/docs/python/settings-reference#_autocomplete-settings)
extraPaths | []	| Specifies locations of additional packages for which to load autocomplete data.| 
typeshedPaths | [] | Specifies paths to local typeshed repository clone(s) for the Python language server. | [Git](https://github.com/DonJayamanne/pythonVSCode/commit/7a90e863c1742b7c7d8a6612596bdc0a34a595d1)
python.linting. ||| [Linting Settings](https://code.visualstudio.com/docs/python/settings-reference#_linting-settings)
enabled | true   | Specifies whether to enable linting in general.|
pylintEnabled | true | Specifies whether to enable Pylint.|

#### Python Language Server settings  
The language server settings apply when python.jediEnabled is false.
Setting | Default   | Description | ref 
--------|-----------|--------------|--
python.jediEnabled | Default *true*, must be set to FALSE | Indicates whether to use Jedi as the IntelliSense engine (true) or the Microsoft Python Language Server (false). Note that the language server requires a platform that supports .NET Core 2.1 or newer. |
python.analysis. ||| [code analysis settings)](https://code.visualstudio.com/docs/python/settings-reference#_code-analysis-settings)
typeshedPaths | [] | Paths to look for typeshed modules on GitHub.|

Note: the below settings include the paths to multiple folders, containing stubs for different firmware. 
you should remove ( or //comment ) the lines of firmwares that you to not use.

File: .vscode\\settings.json

```  json
{
    "python.linting.enabled": true,
    "python.pythonPath": "C:\\Program Files (x86)\\Microsoft Visual Studio\\Shared\\Python36_64\\python.exe",

    "python.autoComplete.extraPaths": [
        "C:\\develop\\MyPython\\Stubber\\stubs\\esp32_LoBo_3_2_24_Frozen",
        "C:\\develop\\MyPython\\Stubber\\stubs\\esp32_LoBo_3_2_24",
        "C:\\develop\\MyPython\\Stubber\\stubs\\esp32_1_10_0_Frozen",
        "C:\\develop\\MyPython\\Stubber\\stubs\\esp32_1_10_0",
    ],
    "python.autoComplete.typeshedPaths": [
        "C:\\develop\\MyPython\\Stubber\\stubs\\esp32_LoBo_3_2_24_Frozen",
        "C:\\develop\\MyPython\\Stubber\\stubs\\esp32_LoBo_3_2_24",
        "C:\\develop\\MyPython\\Stubber\\stubs\\esp32_1_10_0_Frozen",
        "C:\\develop\\MyPython\\Stubber\\stubs\\esp32_1_10_0",
    ],
    "python.analysis.typeshedPaths": [
        "C:\\develop\\MyPython\\Stubber\\stubs\\esp32_LoBo_3_2_24_Frozen",
        "C:\\develop\\MyPython\\Stubber\\stubs\\esp32_LoBo_3_2_24",
        "C:\\develop\\MyPython\\Stubber\\stubs\\esp32_1_10_0_Frozen",
        "C:\\develop\\MyPython\\Stubber\\stubs\\esp32_1_10_0",
    ],

    "python.linting.pylintEnabled": true,
}

```
Note:  if you notice  problems 
* The paths appear to be case sensitive(which may not be apparent for your platform)
* in JSON notation the `\` (backslash) should be escaped as `\\` (double backslash)
* Put the 'Frozen' module paths before the generated module paths. 
The frozen modules offer more code completion, and vscode-python needs to load them first to make use of that.

### vscode User Settings

file: ~\.vscode\settings.json
``` json
{
    // ...
    "python.pythonPath": "C:\\Program Files (x86)\\Microsoft Visual Studio\\Shared\\Python36_64\\python.exe",
}
```

### pylint - workspace settings 

Pylint needs 2 settings :
1. init-hook to inform it where the stubs are stored
2. disable some pesky warnings that make no sense for micropython, and that are caused by the stubs that have only limited information

file: .pylintrc
``` ini
[MASTER]
# LoBo ESP 32 3.2.24
init-hook='import sys; sys.path.insert(1,"C:\\develop\\MyPython\\Stubber\\stubs\\esp32_LoBo_3_2_24_Frozen");sys.path.insert(1,"C:\\develop\\MyPython\\Stubber\\stubs\\esp32_LoBo_3_2_24");sys.path.insert(1,"./lib")'

# MicroPython ESP 32
# init-hook='import sys; sys.path.insert(1,"C:\\develop\\MyPython\\Stubber\\stubs\\core_1_10_0");sys.path.insert(1,"C:\\develop\\MyPython\\Stubber\\stubs\\esp32_1_10_0");sys.path.insert(1,"./lib")'

disable = missing-docstring, line-too-long, trailing-newlines, broad-except, logging-format-interpolation, invalid-name, 
        no-method-argument, assignment-from-no-return, too-many-function-args, unexpected-keyword-arg
        # the 2nd  line deals with the limited information in the generated stubs.

```



## Downloading the Stubs from GIThub 

This is not complete at this point.
You will find stubs as part of this project located in the stubs folder , but I have not settled on a way to distribute them yet.

## Generating Stubs for a specific Firmware 

The stub files are generated on a MicroPython board by running the script `createstubs.py`, 
this will generate the stubs on the board, either on flash or on the SD card.

if your firmware does not include the `logging` module, you will need to upload this to your board as well.

``` python
import createstubs
```
The generation will take a few minutes ( 2-5 minutes) depending on the speed of the board and the number of included modules.

As the stubs are generated on the board, and as MicroPython is highly optimized to deal with the scarce resources, this unfortunately does mean that the stubs lack parameters details. So for these you must still use the documentation provided for that firmware.

## Custom firmware 
the script tries to determine a firmware ID and version from the information provided in `sys.uname()`
this firmware ID is used in the stubs , and in the foldername to store the subs.

If you need, or prefer, to specify a firmware ID you can do so by setting the firmware_id variable before importing createstubs
For this you will need to edit the createstubs.py file.  

The recommendation is to keep the firmware id short, and add a version as in the below example.

``` python
# almost at the end of the file
def main():
    stubber = Stubber(firmware_id='HoverBot v1.2.1')
    # Add specific additional modules to be stubbed
    stubber.add_modules(['hover','rudder'])

```
after this , upload the file and import it to generate the stubs using your custom name.

## Downloading the files

After this is completed, you will need to download the generated stubs from the micropython board, and save them on a folder on your computer. 
if you work with multiple firmwares or versions it is recommended to use a folder name combining the firmware name and version
- /stubs
    - /ESP32_LoBo_v3_1_20
    - /ESP32_LoBo_v3_2_24
    - /ESP32_LoBo_v3_2_24_Frozen
    - /ESP32_1_10_0
    - /ESP32_1_10_0_Frozen

Note: I found, that you need to be mindful of the maximum path and filename limitations on the filesystem if you use IFSS.

## Frozen Modules 
It is common for Firmwares to include a few (or many) modules as 'frozen' modules. This a way to pre-process .py modules so they're 'baked-in' to MicroPython's firmware and use less memory. Once the code is frozen it can be quickly loaded and interpreted by MicroPython without as much memory and processing time.

Most OSS firmwares store these frozen modules as part of their repository, which allows us to: 
1. Download the *.py from the (github) repo using `git clone` or a direct download 
2. Extract and store the 'unfrozen' modules (ie the *.py files) in a <Firmware>_Frozen folder.
   if there are different port / boards or releses defined , there may be multiple folders such as: 
   mstubs/mpy_1_12_frozen
            /esp32
                /GENERIC
                /RELEASE
                /TINYPICO
            /stm32
                /GENERIC
                /PYBD_SF2
            
3. generate typeshed stubs of these files. (the .pyi files will be stored alongside the .py files)
4. Include/use them in the configuration 



ref: https://learn.adafruit.com/micropython-basics-loading-modules/frozen-modules

### Tested Firmwares :
| Firmware              | Release  | Version                          | Comments        |
|-----------------------|----------|----------------------------------|-----------------|
| MicroPython ESP32     | 1.10.0   | v1.10-247-g0fb15fc3f             | 
| MicroPython ESP32     | 1.11.0   |                                  | 
| MicroPython ESP8266   | 1.9.4    |                                  | 
| MicroPython ESP8266   | 1.9.4    |                                  | 
| MicroPython ESP8266   | 1.10.0   |                                  | 
| MicroPython ESP8266   | 1.11.0   |                                  | 
| Loboris ESP32         | 3.2.24   | ESP32_LoBo_v3.2.24 on 2018-09-06 | includes _threads module 
| M5Stack Flow          | 1.2.1    | based on ESP32_LoBo_v3.2.24      | 
| M5Stack Flow          | 1.4.0-beta| based on MicroPython ESP32 1.11.0| 



## Auto generated Stub format and limitations 

1. No function parameters are generated 
2. No return types are generated 
3. Instances of imported classes have no type (due to 2)
4. The stubs use the .py extension rather than .pyi (for autocomplete to work) 
5. Due to the method of generation nested modules are included, rather than referenced. While this leads to somewhat larger stubs, this should not be limiting for using the stubs on a PC.  

### Module Duplication 
Due to the naming convention in micropython some modules will be duplicated , ie `uos` and `os` will both be included 



# Licenses and contributions
MicroPython-Stubber is licensed under the MIT license, and all contributions should follow this [LICENSE](LICENSE).

## Inspiration : Thonny - MicroPython _cmd_dump_api_info  _[MIT License]_
The `createstubs.py` script to create the stubs is based on the work of Aivar Annamaa and the Thonny crew.
It is somewhere deep in the code and is apparently only used during the development cycle but it showed a way how to extract/generate a representation of the MicroPython modules written in C
While the concepts remain  the code has been rewritten to run on a micropython board, rather than on a connected PC running CPython.
Please refer to :  
https://github.com/thonny/thonny/blob/786f63ff4460abe84f28c14dad2f9e78fe42cc49/thonny/plugins/micropython/__init__.py#L608

## make_stub_files _[Public Domain]_
https://github.com/edreamleo/make-stub-files

This script makes a stub (.pyi) file in the output directory for each source file listed on the command line (wildcard file names are supported). 

The script does no type inference. Instead, the user supplies patterns in a configuration file. The script matches these patterns to:
The names of arguments in functions and methods and
The text of return expressions. Return expressions are the actual text of whatever follows the "return" keyword. The script removes all comments in return expressions and converts all strings to "str". This preprocessing greatly simplifies pattern matching.

## Stub sources

### LoBoris ESP32 firmware and frozen modules _[MIT, Apache 2]_
https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo

### Micropython firmware and frozen modules _[MIT, Python]_
https://github.com/micropython/micropython


## Included custom stubs 

| Github repo                | Contributions                                                           | License
|----------------------------|-------------------------------------------------------------------------|---------
| pfalcon/micropython-lib    | CPython backports                                                       | MIT, Python
| dastultz/micropython-pyb   | a pyb.py file for use with IDEs in developing a project for the Pyboard | Apache 2


### Stub source: Micropython-lib > CPython backports _[MIT, Python]_
While micropython-lib focuses on MicroPython, sometimes it may be beneficial to run MicroPython code using CPython, e.g. to use code coverage, debugging, etc. tools available for it. To facilitate such usage, micropython-lib also provides re-implementations ("backports") of MicroPython modules which run on CPython. 
https://github.com/pfalcon/micropython-lib#cpython-backports

### micropython_pyb _[Apache 2]_
This project provides a pyb.py file for use with IDEs in developing a project for the Pyboard.
https://github.com/dastultz/micropython-pyb

## Related 

[Type hints cheat sheet](https://github.com/python/mypy/blob/master/docs/source/cheat_sheet_py3.rst#type-hints-cheat-sheet-python-3)

### References
PEP 3107 -- Function Annotations
https://www.python.org/dev/peps/pep-3107/

PEP 484 -- Type Hints
https://www.python.org/dev/peps/pep-0484/

### Stub generators
https://stackoverflow.com/questions/35602541/create-pyi-files-automatically


### Mypy
[Optional Static Typing for Python](https://github.com/python/mypy#mypy-optional-static-typing-for-python)

### Typeshed 
https://github.com/python/typeshed/

### stubgen , runs on host and extracts information from the source 
https://github.com/python/mypy/blob/master/mypy/stubgen.py

