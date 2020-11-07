
# Boost MicroPython in VSCode and other modern editors

The intellisense and code linting that is so prevalent in modern editors, does not work out-of-the-gate for MicroPython projects.
While the language is Python, the modules used are different from CPython , and also different ports have different modules and classes , or the same class with different parameters.

Writing MicroPython code in a modern editor should not need to involve keeping a browser open to check for the exact parameters to read a sensor, light-up a led or send a network request.

Fortunately with some additional configuration and data, it is possible to make the editors understand your flavor of MicroPython. even if you run a on-off custom firmware version.

In order to achieve this a few things are needed:
1) Stub files for the native / enabled modules in the firmware using PEP 484 Type Hints
2) Specific configuration of the VSCode Python extensions 
3) Specific configuration of Pylint
4) Suppression of warnings that collide with the MicroPython principals or code optimization.

With that in place, VSCode will understand MicroPython for the most part, and help you to write code, and catch more errors before deploying it to your board. 

![demo][]]

Note that the above is not limited to VSCode and pylint, but it happens to be the combination that I use. 

A lot of subs have already been generated and are shared on github or other means,  so it is quite likely that you can just grab a copy be be productive in a few minutes.

For now you will need to [configure this by hand](#manual-configuration), or use the [micropy cli` tool](#using-micropy-cli)

1. The sister-repo MicroPython-stubs**][stubs-repo] contains all stubs I have collected with the help of others, and which can be used directly.
That repo also contains examples configuration files that can be easily adopted to your setup.

2. A second repo [micropy-stubs repo][stubs-repo2] maintained by BradenM,  also contains stubs but in a structure used and distributed by the [micropy-cli](#using-micropy-cli) tool.
you should use micropy-cli to consume stubs in this repo.

The (stretch) goal is to create a VSCode add-in to simplify the configuration, and allow easy switching between different firmwares and versions.

## Licensing 

MicroPython-Stubber is licensed under the MIT license, and all contributions should follow this [LICENSE](LICENSE).


## Contributions
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-17-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END --> 

---
## Index 

[TOC]


-----------------------------





# 1 - Approach to providing stub information

The stubs are used by 3 components.

  2. Pylint
  3. the VSCode Autocompletion service 
  4. the VSCode Analysis server ( MPLS / Lancelot)

These 3 tools work together to provide code completion/prediction, type checking and all the other good things.
For this the order in which these tools use, the stub folders is significant, and best results are when all use the same order. 

In most cases the best results are achieved by the below setup:  

![stub processing order][]

 1. **Your own source files**, including any libraries you add to your project.
 This can be a single libs folder or multiple directories.
 There is no need to run stubber on your source or libraries.
 2. **The CPython common stubs**. These stubs are handcrafted to allow MicroPython script to run on a CPython system.
 There are only a limited number of these stubs and while they are not intended to be used to provide type hints, they do provide valuable information. 
Note that for some modules (such as the  `gc`, `time`  and `sys` modules) this approach does not work. 
 3. **Frozen stubs**. Most micropython firmwares include a number of python modules that have been included in the firmware as frozen modules in order to take up less memory.
 These modules have been extracted from the source code. 
 4. **Firmware Stubs**. For all other modules that are included on the board, [micropython-stubber] or [micropy-cli] has been used to extract as much information as available, and provide that as stubs. While there is a lot of relevant and useful information for code completion, it does unfortunately not provide all details regarding parameters that the earlier  options may provide.

## 1.1 - Stub collection process 

* The **CPython common stubs** are periodically collected from the [micropython-lib][] or the [pycopy-lib][].
* The **Frozen stubs** are collected from the repos of [micropython][] + [micropython-lib][] and from the [loboris][] repo
  the methods to gather these differs per firmware family , and there are differences between versions how these are stored , and retrieved.
  where possible this is done per port and board,  or if not possible the common configuration for has been included.
* the **Firmware stubs** are generated directly on a MicroPython board.



## 1.2 - Firmware Stubs format and limitations 

1. No function parameters are generated 
2. No return types are generated 
3. Instances of imported classes have no type (due to 2)
4. The stubs use the .py extension rather than .pyi (for autocomplete to work) 
5. Due to the method of generation nested modules are included, rather than referenced. While this leads to somewhat larger stubs, this should not be limiting for using the stubs on a PC.  

## 1.3 - Firmware naming convention 

for stubfiles: {firmware}-{port}-{version}[-{build}]

for frozen modules : {firmware}-{version}-frozen

* Firmware: lowercase 
  * micropython | loboris | pycopy | ...
* port: lowercase , as reported by os.implementation.platform 
  * esp32 | linux | win32 | esp32_lobo
* version : digits only , dots replaced by underscore, follow version in documentation rather than semver 
  * 1_13
  * 1_9_4
* build, only for nightly build, the buildnr extracted from the git tag 
  * Nothing , for released versions
  * 103 
  * N ( short notation)


---------
# 2 - Using stubs
### 2.1 - Manual configuration

the manual configuration, including sample configuration files is described in detail in the sister-repo [micropython-stubs][] section [using-the-stubs][]


### 2.2 - Using micropy-cli

'micropy-cli' is  command line tool for managing MicroPython projects with VSCode
If you want a command line interface to setup a new project and configure the settings as described above for you, then take a look at : [micropy-cli]  

``` 
pip install micropy-cli
micropy init
```

Braden has essentially created a front-end for using micropython-stubber, and the configuration of a project folder for pymakr. 

micropy-cli  maintains its own repository of stubs. 

---------
# 3 - [VSCode and Pylint configuration](vscode-configuration)

The current configuration and section describes how to use [Microsoft Python Language Server][mpls]

There is a newer implementation [Pylance] that has better speed and functionality.

*To deliver an improved user experience, we’ve created Pylance as a brand-new language server based on Microsoft’s [Pyright](https://github.com/microsoft/pyright) static type checking tool. Pylance leverages type stubs ([.pyi files](https://www.python.org/dev/peps/pep-0561/)) and lazy type inferencing to provide a highly-performant development experience. Pylance supercharges your Python IntelliSense experience with rich type information, helping you write better code, faster. The Pylance extension is also shipped with a collection of type stubs for popular modules to provide fast and accurate auto-completions and type checking.*



[Announcing Pylance: Fast, feature-rich language support for Python in Visual Studio Code | Python (microsoft.com)](https://devblogs.microsoft.com/python/announcing-pylance-fast-feature-rich-language-support-for-python-in-visual-studio-code/)

#### 3.1 - Relevant VSCode settings

Setting | Default   | Description  | ref  
--------|-----------|--------------|--- 
python.autoComplete.extraPaths | []	| Specifies locations of additional packages for which to load autocomplete data.| [Autocomplete Settings](https://code.visualstudio.com/docs/python/settings-reference#_autocomplete-settings)
typeshedPaths | [] | Specifies paths to local typeshed repository clone(s) for the Python language server. | [Git](https://github.com/DonJayamanne/pythonVSCode/commit/7a90e863c1742b7c7d8a6612596bdc0a34a595d1)
python.linting. ||| [Linting Settings](https://code.visualstudio.com/docs/python/settings-reference#_linting-settings)
enabled | true   | Specifies whether to enable linting in general.|
pylintEnabled | true | Specifies whether to enable Pylint.|

#### 3.1.1 - Microsoft Python Language Server settings  [MPLS]


The language server settings apply when python.jediEnabled is false.

Setting | Default   | Description | ref 
--------|-----------|--------------|--
python.jediEnabled | Default *true*, must be set to FALSE | Indicates whether to use Jedi as the IntelliSense engine (true) or the Microsoft Python Language Server (false). Note that the language server requires a platform that supports .NET Core 2.1 or newer. |
python.analysis. ||| [code analysis settings)](https://code.visualstudio.com/docs/python/settings-reference#_code-analysis-settings)
typeshedPaths | [] | Paths to look for typeshed modules on GitHub.|

*Our  long-term plan is to transition our Microsoft Python Language Server users over to Pylance and eventually deprecate and remove the old language server as a supported option*

#### 3.1.1 - Pylance - pyright

The intent is to adjust the configuration to support Lancelot to work in the same way as MPLS, but this currently runs into some issues where pylance cannot resolve builtins and other symbols 

| Setting                        | Default   | Description                                                  |
| ------------------------------ | --------- | ------------------------------------------------------------ |
| python.analysis.stubPath       | ./typings | Used to allow a user to specify a path to a directory that contains custom type stubs. Each package's type stub file(s) are expected to be in its own subdirectory. |
| python.analysis.autoSearchPath | true      | Used to automatically add search paths based on some predefined names (like `src`). |
| python.analysis.extraPaths     | []        | Used to specify extra search paths for import resolution. This replaces the old `python.autoComplete.extraPaths` setting. |



references : 

[Pylance - Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)

[microsoft/pyright: Static type checker for Python (github.com)](https://github.com/microsoft/pyright#static-type-checker-for-python)

possible testing / diag : 

[pyright/command-line.md at master · microsoft/pyright (github.com)](https://github.com/microsoft/pyright/blob/master/docs/command-line.md)



### 3.1.2 - Recommended order of the stubs in your config:  

1. The src/libs folder(s)
2. The CPython common modules 
3. The frozen modules offer more information that can be used in code completion, and therefore should be loaded before the firmware stubs.
4. The firmware stubs generated on or for your board


### 3.1.3 - Sample configuration VSCode settings
Note: the below settings include the paths to multiple folders, containing stubs for different firmware. 
you can remove ( or //comment ) the lines of firmwares that you to not use.

File: .vscode/settings.json

<TODO: update paths to naming convention>

```  json
{
    "python.linting.enabled": true,

    "python.autoComplete.extraPaths": [
        "stubs/esp32_LoBo_3_2_24_Frozen",
        "stubs/esp32_LoBo_3_2_24",
        "stubs/esp32_1_10_0_Frozen",
        "stubs/esp32_1_10_0",
    ],
    "python.autoComplete.typeshedPaths": [
        "stubs/esp32_LoBo_3_2_24_Frozen",
        "stubs/esp32_LoBo_3_2_24",
        "stubs/esp32_1_10_0_Frozen",
        "stubs/esp32_1_10_0",
    ],
    "python.analysis.typeshedPaths": [
        "stubs/esp32_LoBo_3_2_24_Frozen",
        "stubs/esp32_LoBo_3_2_24",
        "stubs/esp32_1_10_0_Frozen",
        "stubs/esp32_1_10_0",
    ],

    "python.linting.pylintEnabled": true,
}

```

If you notice problems :

* The paths are case sensitive (which may not be apparent for your platform)

* To allow the config to be used cross platform you can use forward slashes `/`, _note that this is also accepted on Windows_ 
* If you prefer to use a backslash :  in JSON notation the `\` (backslash) MUST be escaped as `\\` (double backslash)
* Remember to put the 'Frozen' module paths before the generated module paths. 

### 3.2 - pylint 

Pylint needs 2 settings :
1. Specify **init-hook** to inform pylint where the stubs are stored.
   note that the `src` folder is already automagically included, so you do not need to add that. 
2. disable some pesky warnings that make no sense for MicroPython, and that are caused by the stubs that have only limited information

File: .pylintrc
``` ini
[MASTER]
# Loaded Stubs:  esp32-micropython-1.11.0 
init-hook='import sys;sys.path[1:1] = ["src/lib", "all-stubs/cpython-core", "all-stubs/mpy_1_12/frozen/esp32/GENERIC", "all-stubs/esp32_1_13_0-103",]'

disable = missing-docstring, line-too-long, trailing-newlines, broad-except, logging-format-interpolation, invalid-name, 
        no-method-argument, assignment-from-no-return, too-many-function-args, unexpected-keyword-arg
        # the 2nd  line deals with the limited information in the generated stubs.

```




---------
# 4 - Create Firmware Stubs

It is possible to create MicroPython stubs using the `createstubs.py` MicroPython script.  

the script goes though the following stages

1. it determines the firmware family, the version and the port of the device, 
   and based on that information it creates a firmware identifier (fwid) in the format : {family}-{port}-{version}
   the fwid is used to name the folder that stores the subs for that device.

   - micropython-pyboard-1_10

   - micropython-esp32-1_12

   - loboris-esp32_LoBo-3_2_4
2. it cleans the stub folder 
3. it generates stubs, using a predetermined list of module names.
   for each found module or submodule a stub file is written to the device and progress is output to the console/repl.
4. a module manifest (`modules.json`) is created that contains the pertinent information determined from the board, the version of createstubs.py and a list of the successful generated stubs 

**Module duplication** 

Due to the module naming convention in micropython some modules will be duplicated , ie `uos` and `os` will both be included 

## 4.1 - running the script

the createstubs.py script can either be run as a script or imported as a module depending on your preferences.

running as a script may be needed on the linux or win32 platforms in order to pass parameters to the script.

The steps are : 

1. connect to your board 
2. upload the script to your board [optional]
3. run/import the `createsubs.py` script 
4. download the generated stubs to a folder on your PC
5. run the post-processor [optional, but recommended]

![createstubs-flow][]





## 4.2 - Generating Stubs for a specific Firmware 

The stub files are generated on a MicroPython board by running the script `createstubs.py`, this will generate the stubs on the board and store them, either on flash or on the SD card.

**Normal and minified versions**

The  script is available in 2 versions : 
1) The [normal version](tree/master/board), which includes logging, but also requires to logging module to be avaialble.
2) A [minified version](tree/master/minified),  which requires less memory and only  very basic logging. this is specially suited for low memory devices such as the esp8622 
Both versions have the exact same functionality.

if your firmware does not include the `logging` module, you will need to upload this to your board, or use the minified version.

``` python
import createstubs
```

The generation will take a few minutes ( 2-5 minutes) depending on the speed of the board and the number of included modules.

As the stubs are generated on the board, and as MicroPython is highly optimized to deal with the scarce resources, this unfortunately does mean that the stubs lacks parameters details. So for these you must still use the documentation provided for that firmware.

## 4.3 - Downloading the files

After the sub files have been generated , you will need to download the generated stubs from the micropython board and most likely you will want to copy and  save them on a folder on your computer. 
if you work with multiple firmwares, ports or version it is simple to keep the stub files in a common folder as the firmware id is used to generate unique names

- ./stubs

  - /micropython-pyboard-1_10

  - /micropython-esp32-1_12

  - /micropython-linux-1_11

  - /loboris-esp32_LoBo-3_1_20

  - /loboris-esp32_LoBo-3_2_24

    Note: I found, that you need to be mindful of the maximum path and filename limitations on the filesystem if your firmware uses IFSS as a filesystem.
    therefore 

## 4.4 - Custom firmware 

The script tries to determine a firmware ID and version from the information provided in `sys.implementation `,  `  sys.uname()` and the existence of specific modules..

This firmware ID is used in the stubs , and in the folder name to store the subs.

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

after this , upload the file and import it to generate the stubs using your custom firmware id.



# 5 - CPython and Frozen modules 



## 5.1 - Frozen Modules 

It is common for Firmwares to include a few (or many) python modules as 'frozen' modules. 
'Freezing' modules is a way to pre-process .py modules so they're 'baked-in' to MicroPython' s firmware and use less memory. Once the code is frozen it can be quickly loaded and interpreted by MicroPython without as much memory and processing time.

Most OSS firmwares store these frozen modules as part of their repository, which allows us to: 

1. Download the *.py from the (github) repo using `git clone` or a direct download 

2. Extract and store the 'unfrozen' modules (ie the *.py files) in a <Firmware>_Frozen folder.
   if there are different port / boards or releases defined , there may be multiple folders such as: 

   * stubs/micropython_1_12_frozen

     * /esp32

       * /GENERIC
       * /RELEASE
       * /TINYPICO

     * /stm32

       * /GENERIC
       * /PYBD_SF2

       

3. generate typeshed stubs of these files. (the .pyi files will be stored alongside the .py files)

4. Include/use them in the configuration 

ref: https://learn.adafruit.com/micropython-basics-loading-modules/frozen-modules




## 5.2 - TODO: Collect Frozen Stubs 

< todo:  how to run >

- repos used 
- run .../py TODO:
- copy to sister-repo 



## 5.3 - TODO: postprocessing 

< todo:  how to 

run postprocessing for firmware stubs 

run postprocessing for all stubs 



# 6 - Repo structure 

- [This and sister repos](#this-and-sister-repos) 
- [Structure of this repo](#structure-of-this-repo)
- [Naming Convention and Stub folder structure][naming-convention]
- 2 python versions 


## 6.1 - This and sister repos
| What                 | Why                      | Where                             |
|----------------------|--------------------------|-----------------------------------|
| stubber project      | needed to make stubs     | develop/micropython-stubber|
| stubs sister repo    | stores collected stubs   | develop/micropython-stubs|
| micropython          | to collect frozen modules| develop/micropython|
| micropython-lib      | to collect frozen modules| develop/micropython-lib|


## 6.2 - Structure of this repo 

The file structure is based on my personal windows environment, but you should be able to adapt that without much hardship to you own preference and OS.

| What                 | Details                      | Where                             |
|----------------------|--------------------------|-----------------------------------|
| stub root            | symlink to connect the 2 sister-repos | all_stubs|
| firmware stubber     | MicroPython              | board/createstubs.py|
| minified firmware stubber | MicroPython         | minified/createstubs.py|
| PC based scripts     | CPython                  | src/*|
| PC based scripts     | CPython                  | process.py|
| pytest tests         |                          | test/*|
|                           |                                       |                         |

## 6.3 - Naming Convention and Stub folder structure

| What                 | Why                      | Where                             |
|----------------------|--------------------------|-----------------------------------|
| stub root            | connect the 2 repos                         | all_stubs|
| cpython stubs for micropython core | adapt for differences between CPython and MicroPython | stubs/cpython-core |
| generated stub files | needed to use stubs      | stubs/{firmware}-{port}-{version}-frozen |
| Frozen stub files    | better code intellisense | stubs/{firmware}-{version}-frozen |




Note: I found that, for me, using submodules caused more problems than it solved. So instead I link the two repo's using a symlink.

**< TODO: Check folder name>**  
Note: I have used the folder `TESTREPO-micropython` to avoid conflicts with any development that you might be doing on the `micropython` repo at the potential cost of a little diskspace.

``` powershell
cd /develop 

git clone  https://github.com/josverl/micropython-stubber.git 
git clone  https://github.com/josverl/micropython-stubs.git 
git clone  https://github.com/micropython/micropython.git 
git clone  https://github.com/micropython/micropython.git 
```






## 6.4 - Create a symbolic link

To create the symbolic link to the `../micropython-stubs/stubs` folder the instructions differ slightly for each OS/
The below examples assume that the micropython-stubs repo is cloned 'next-to' your project folder.
please adjust as needed.

### 6.4.1 - Windows 10 

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

### 6.4.2 - Linux/Unix/Mac OS

``` sh
# target must be an absolute path
ln -s /path/to/micropython-stubs/stubs all-stubs
```

------------

# 7 - Developing
I use Windows 10  and use WSL2 to run the linux based parts. 
if you develop on other platform, it is quite likely that you may need to change some details. if that is needed , please update/add to the documentation and send a documentation PR.

* clone 
* create python virtual environment (optional) 
* install requirements-dev 
* setup sister repos
* run test to verify setup 

# 7.1 - wresting with two pythons 

This project combines CPython and MicroPython in one project.  As a result you may/will need to switch the configuration of pylint and VSCode to match the section of code that you are working on.  This is caused by the fact that pylint does not support per-folder configuration 

to help switching there are 2 different .pylintrc files stored in the root of the project to simplify switching.

Similar changes will need to be done to the .vscode/settings.json 

If / when we can get pylance  to work with the micropython stubs , this may become simpler as 
Pylance natively supports [multi-root workspaces](https://code.visualstudio.com/docs/editor/multi-root-workspaces), meaning that you can open multiple folders in the same Visual Studio Code session and have Pylance functionality in each folder.

## 7.2 Minification 

if you make changes to the createstubs.py script , you should also update the minified version by running `python process.py minify` at some point.

if you forget to do this there is a github action that should do this for you and create a PR for your branch.

## 7.3 Testing 

MicroPython-Stubber has a number of tests written in Pytest

see below overview

| folder        | what                                               | how                                                          | used where              |
| ------------- | -------------------------------------------------- | ------------------------------------------------------------ | ----------------------- |
| board         | createsubs.py<br />normal & minified               | runs createstubs.py on micropython-linux ports               | WSL2 and github actions |
| checkout_repo | simple_git module<br />retrieval of frozen modules | does not use mocking but actually retrieves different firmware versions locally using git or dowNloads modules for online | local windows           |
| common        | all other tests                                    | common                                                       | local + github action   |



**Testing on linux port**

in order to be able to test `createstubs.py`  it has been updated to run on linux, and accept a --path parameter to indicate tha pathe where the stubs should be stored.



## 7.4 github actions



### pytests.yml 

This workflow will :

- test the workstation scripts 

- test the createstubs.py script on multiple micropython linux versions 

- test the minified createstubs.py script on multiple micropython linux versions 



### run minify-pr.yml

This workflow will :

- create a minified version of createstubs.py 

- run a quick test on that 

- and submit a PR to the branch <branch>-minify



# 8 - Stubs 



## 8.1 Firmware and libraries 

### 8.1.1 MicroPython firmware and frozen modules _[MIT]_

https://github.com/micropython/micropython

https://github.com/micropython/micropython-lib

### 8.1.2 - Pycopy firmware and frozen modules _[MIT]_

https://github.com/pfalcon/pycopy

https://github.com/pfalcon/pycopy-lib

### 8.1.3 - LoBoris ESP32 firmware and frozen modules _[MIT, Apache 2]_

https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo




## 8.2 - Included custom stubs 

| Github repo                | Contributions                                                           | License |
|----------------------------|-------------------------------------------------------------------------|---------|
| pfalcon/micropython-lib    | CPython backports                                            | MIT |
| dastultz/micropython-pyb   | a pyb.py file for use with IDEs in developing a project for the Pyboard | Apache 2|



### Stub source: MicroPython-lib > CPython backports _[MIT, Python]_

While micropython-lib focuses on MicroPython, sometimes it may be beneficial to run MicroPython code using CPython, e.g. to use code coverage, debugging, etc. tools available for it. To facilitate such usage, micropython-lib also provides re-implementations ("backports") of MicroPython modules which run on CPython. 
https://github.com/pfalcon/micropython-lib#cpython-backports

### micropython_pyb _[Apache 2]_

This project provides a pyb.py file for use with IDEs in developing a project for the Pyboard.
https://github.com/dastultz/micropython-pyb

---------


# 9 - References 

## 9.1 - Inspiration 

### Thonny - MicroPython _cmd_dump_api_info  _[MIT License]_

The `createstubs.py` script to create the stubs is based on the work of Aivar Annamaa and the Thonny crew.
It is somewhere deep in the code and is apparently only used during the development cycle but it showed a way how to extract/generate a representation of the MicroPython modules written in C

While the concepts remain,  the code has been rewritten to run on a micropython board, rather than on a connected PC running CPython.
Please refer to :  
https://github.com/thonny/thonny/blob/786f63ff4460abe84f28c14dad2f9e78fe42cc49/thonny/plugins/micropython/__init__.py#L608

### make_stub_files _[Public Domain]_

https://github.com/edreamleo/make-stub-files

This script makes a stub (.pyi) file in the output directory for each source file listed on the command line (wildcard file names are supported). 

The script does no type inference. Instead, the user supplies patterns in a configuration file. The script matches these patterns to:
The names of arguments in functions and methods and
The text of return expressions. Return expressions are the actual text of whatever follows the "return" keyword. The script removes all comments in return expressions and converts all strings to "str". This preprocessing greatly simplifies pattern matching.



# 10 - Related 

[Type hints cheat sheet](https://github.com/python/mypy/blob/master/docs/source/cheat_sheet_py3.rst#type-hints-cheat-sheet-python-3)

### 10.1 - References

PEP 3107 -- Function Annotations
https://www.python.org/dev/peps/pep-3107/

PEP 484 -- Type Hints
https://www.python.org/dev/peps/pep-0484/

### 10.2 - Stub generators

https://stackoverflow.com/questions/35602541/create-pyi-files-automatically

### 10.3 - Mypy

[Optional Static Typing for Python](https://github.com/python/mypy#mypy-optional-static-typing-for-python)

### 10.4 - Typeshed 

https://github.com/python/typeshed/

### 10.5 - stubgen , runs on host and extracts information from the source 

https://github.com/python/mypy/blob/master/mypy/stubgen.py



----------------

# 11 - contributions 

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->

<table>
  <tr>
    <td align="center"><a href="https://github.com/Josverl"><img src="https://avatars2.githubusercontent.com/u/981654?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Jos Verlinde</b></sub></a><br /><a href="https://github.com/Josverl/micropython-stubbber/commits?author=josverl" title="Code">💻</a> <a href="#research-josverl" title="Research">🔬</a> <a href="#ideas-josverl" title="Ideas, Planning, & Feedback">🤔</a> <a href="#content-josverl" title="Content">🖋</a> <a href="#stubs-josverl" title="MicroPython stubs">📚</a> <a href="#test-josverl" title="Test">✔</a></td>
    <td align="center"><a href="https://thonny.org/"><img src="https://avatars1.githubusercontent.com/u/46202078?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Thonny, Python IDE for beginners</b></sub></a><br /><a href="#ideas-thonny" title="Ideas, Planning, & Feedback">🤔</a> <a href="#research-thonny" title="Research">🔬</a></td>
    <td align="center"><a href="https://micropython.org/"><img src="https://avatars1.githubusercontent.com/u/6298560?v=4?s=100" width="100px;" alt=""/><br /><sub><b>MicroPython</b></sub></a><br /><a href="#data-micropython" title="Data">🔣</a> <a href="#stubs-micropython" title="MicroPython stubs">📚</a></td>
    <td align="center"><a href="https://github.com/loboris"><img src="https://avatars3.githubusercontent.com/u/6280349?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Boris Lovosevic</b></sub></a><br /><a href="#data-loboris" title="Data">🔣</a> <a href="#stubs-loboris" title="MicroPython stubs">📚</a></td>
    <td align="center"><a href="https://github.com/pfalcon"><img src="https://avatars3.githubusercontent.com/u/500451?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Paul Sokolovsky</b></sub></a><br /><a href="#data-pfalcon" title="Data">🔣</a> <a href="#stubs-pfalcon" title="MicroPython stubs">📚</a></td>
    <td align="center"><a href="https://github.com/pycopy"><img src="https://avatars0.githubusercontent.com/u/67273174?v=4?s=100" width="100px;" alt=""/><br /><sub><b>pycopy</b></sub></a><br /><a href="#data-pycopy" title="Data">🔣</a> <a href="#stubs-pycopy" title="MicroPython stubs">📚</a></td>
    <td align="center"><a href="https://github.com/pycom"><img src="https://avatars2.githubusercontent.com/u/16415153?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Pycom</b></sub></a><br /><a href="#infra-pycom" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/BradenM"><img src="https://avatars1.githubusercontent.com/u/5913808?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Braden Mars</b></sub></a><br /><a href="https://github.com/Josverl/micropython-stubbber/issues?q=author%3ABradenM" title="Bug reports">🐛</a> <a href="https://github.com/Josverl/micropython-stubbber/commits?author=BradenM" title="Code">💻</a> <a href="#stubs-BradenM" title="MicroPython stubs">📚</a> <a href="#platform-BradenM" title="Packaging/porting to new platform">📦</a></td>
    <td align="center"><a href="https://binary.com.au/"><img src="https://avatars2.githubusercontent.com/u/175909?v=4?s=100" width="100px;" alt=""/><br /><sub><b>James Manners</b></sub></a><br /><a href="https://github.com/Josverl/micropython-stubbber/commits?author=jmannau" title="Code">💻</a></td>
    <td align="center"><a href="http://patrickwalters.us/"><img src="https://avatars0.githubusercontent.com/u/4002194?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Patrick</b></sub></a><br /><a href="https://github.com/Josverl/micropython-stubbber/issues?q=author%3Aaskpatrickw" title="Bug reports">🐛</a> <a href="https://github.com/Josverl/micropython-stubbber/commits?author=askpatrickw" title="Code">💻</a> <a href="#stubs-askpatrickw" title="MicroPython stubs">📚</a></td>
    <td align="center"><a href="https://opencollective.com/pythonseverywhere"><img src="https://avatars3.githubusercontent.com/u/16009100?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Paul m. p. P.</b></sub></a><br /><a href="#ideas-pmp-p" title="Ideas, Planning, & Feedback">🤔</a> <a href="#research-pmp-p" title="Research">🔬</a></td>
    <td align="center"><a href="https://github.com/edreamleo"><img src="https://avatars0.githubusercontent.com/u/592928?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Edward K. Ream</b></sub></a><br /><a href="#plugin-edreamleo" title="Plugin/utility libraries">🔌</a></td>
    <td align="center"><a href="https://github.com/dastultz"><img src="https://avatars3.githubusercontent.com/u/4334042?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Daryl Stultz</b></sub></a><br /><a href="#stubs-dastultz" title="MicroPython stubs">📚</a></td>
    <td align="center"><a href="https://github.com/cabletie"><img src="https://avatars1.githubusercontent.com/u/2356734?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Keeping things together</b></sub></a><br /><a href="https://github.com/Josverl/micropython-stubbber/issues?q=author%3Acabletie" title="Bug reports">🐛</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/vbolshakov"><img src="https://avatars2.githubusercontent.com/u/2453324?v=4?s=100" width="100px;" alt=""/><br /><sub><b>vbolshakov</b></sub></a><br /><a href="https://github.com/Josverl/micropython-stubbber/issues?q=author%3Avbolshakov" title="Bug reports">🐛</a> <a href="#stubs-vbolshakov" title="MicroPython stubs">📚</a></td>
    <td align="center"><a href="https://lemariva.com/"><img src="https://avatars2.githubusercontent.com/u/15173329?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Mauro Riva</b></sub></a><br /><a href="#blog-lemariva" title="Blogposts">📝</a> <a href="https://github.com/Josverl/micropython-stubbber/issues?q=author%3Alemariva" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://github.com/MathijsNL"><img src="https://avatars0.githubusercontent.com/u/1612886?v=4?s=100" width="100px;" alt=""/><br /><sub><b>MathijsNL</b></sub></a><br /><a href="https://github.com/Josverl/micropython-stubbber/issues?q=author%3AMathijsNL" title="Bug reports">🐛</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
------------------------------

[stubs-repo]:   https://github.com/Josverl/micropython-stubs
[stubs-repo2]:  https://github.com/BradenM/micropy-stubs
[micropython-stubber]: https://github.com/Josverl/micropython-stubber
[micropython-stubs]: https://github.com/Josverl/micropython-stubs#micropython-stubs
[micropy-cli]: https://github.com/BradenM/micropy-cli
[using-the-stubs]: https://github.com/Josverl/micropython-stubs#using-the-stubs
[demo]:         docs/img/demo.gif	"demo of writing code using the stubs"
[stub processing order]: docs/img/stuborder.png	"recommended stub processing order"
[naming-convention]: #naming-convention-and-stub-folder-structure
[firmwares]: https://github.com/Josverl/micropython-stubs/blob/master/firmwares.md
[micropython]: https://github.com/micropython/micropython
[micropython-lib]:  https://github.com/micropython/micropython-lib
[pycopy]: https://github.com/pfalcon/pycopy
[pycopy-lib]: https://github.com/pfalcon/pycopy-lib
[createstubs-flow]: docs/img/createstubs-flow.png


