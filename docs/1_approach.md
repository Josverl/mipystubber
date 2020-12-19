# 1 - Approach to collecting stub information

The stubs are used by 3 components.

  2. pylint
   3. the VSCode Pylance Language Server
   4. the VSCode Python add-in

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
 4. **Firmware Stubs**. For all other modules that are included on the board, [micropython-stubber] or [micropy-cli] has been used to extract as much information as available, and provide that as stubs. While there is a lot of relevant and useful information for code completion, it does unfortunately not provide all details regarding parameters that the above options may provide.

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
6. 

## 1.3 - Firmware naming convention 

The firmware naming conventions is most relevant to provide clear folder names when selecting which stubs to use.

for stubfiles: {**firmware**}-{port}-{version}[-{build}]

for frozen modules : {firmware}-{version}-frozen

* ***firmware***: lowercase 
  * micropython | loboris | pycopy | ...
* ***port***: lowercase , as reported by os.implementation.platform 
  * esp32 | linux | win32 | esp32_lobo
* ***version*** : digits only , dots replaced by underscore, follow version in documentation rather than semver 
  * 1_13
  * 1_9_4
* ***build***, only for nightly build, the buildnr extracted from the git tag 
  * Nothing , for released versions
  * 103 
  * N ( short notation)



--------------------------



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

