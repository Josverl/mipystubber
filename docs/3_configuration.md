# 3 - [VSCode and Pylint configuration](vscode-configuration)

The current configuration and section describes how to use [Microsoft Python Language Server][mpls]

There is a newer implementation [Pylance] that has better speed and functionality.

*To deliver an improved user experience, we’ve created Pylance as a brand-new language server based on Microsoft’s [Pyright](https://github.com/microsoft/pyright) static type checking tool. Pylance leverages type stubs ([.pyi files](https://www.python.org/dev/peps/pep-0561/)) and lazy type inferencing to provide a highly-performant development experience. Pylance supercharges your Python IntelliSense experience with rich type information, helping you write better code, faster. The Pylance extension is also shipped with a collection of type stubs for popular modules to provide fast and accurate auto-completions and type checking.*

## 3.1 - Recommended order of the stubs in your config:  

1. The src/libs folder(s)
2. The CPython common modules 
3. The frozen modules offer more information that can be used in code completion, and therefore should be loaded before the firmware stubs.
4. The firmware stubs generated on or for your board

[Announcing Pylance: Fast, feature-rich language support for Python in Visual Studio Code | Python (microsoft.com)](https://devblogs.microsoft.com/python/announcing-pylance-fast-feature-rich-language-support-for-python-in-visual-studio-code/)

## 3.2 - Relevant VSCode settings

| Setting                        | Default | Description                                                  | ref                                                          |
| ------------------------------ | ------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| python.autoComplete.extraPaths | []      | Specifies locations of additional packages for which to load autocomplete data. | [Autocomplete Settings](https://code.visualstudio.com/docs/python/settings-reference#_autocomplete-settings) |
| typeshedPaths                  | []      | Specifies paths to local typeshed repository clone(s) for the Python language server. | [Git](https://github.com/DonJayamanne/pythonVSCode/commit/7a90e863c1742b7c7d8a6612596bdc0a34a595d1) |
| python.linting.                |         |                                                              | [Linting Settings](https://code.visualstudio.com/docs/python/settings-reference#_linting-settings) |
| enabled                        | true    | Specifies whether to enable linting in general.              |                                                              |
| pylintEnabled                  | true    | Specifies whether to enable Pylint.                          |                                                              |



### 3.2.2 - Pylance - pyright

[Pylance]([Pylance - Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)) is replacing MPLS and provides the same and more functionality.

| Setting                        | Default   | Description                                                  |
| ------------------------------ | --------- | ------------------------------------------------------------ |
| python.analysis.stubPath       | ./typings | Used to allow a user to specify a path to a directory that contains custom type stubs. Each package's type stub file(s) are expected to be in its own subdirectory. |
| python.analysis.autoSearchPath | true      | Used to automatically add search paths based on some predefined names (like `src`). |
| python.analysis.extraPaths     | []        | Used to specify extra search paths for import resolution. This replaces the old `python.autoComplete.extraPaths` setting. |

### 3.2.3 - Sample configuration for Pylance

To update a project configuration from MPLS to Pylance is simple : 

Open your VSCode settings file :  ` .vscode/settings.json`

- change the  language server to Pylance ➡  `"python.languageServer": "Pylance",`
- remove  the section: `python.autoComplete.typeshedPaths`
- remove the section : `python.analysis.typeshedPaths`
- optionally add :  `"python.analysis.autoSearchPath": true,`



The result should be something like this :

```  json
{
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
}

```

If you notice problems :

* The paths are case sensitive (which may not be apparent for your platform)
* To allow the config to be used cross platform you can use forward slashes `/`, _note that this is also accepted on Windows_ 
* If you prefer to use a backslash :  in JSON notation the `\` (backslash) MUST be escaped as `\\` (double backslash)
* Remember to put the 'Frozen' module paths before the generated module paths. 

References : 

[Pylance - Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)

[microsoft/pyright: Static type checker for Python (github.com)](https://github.com/microsoft/pyright#static-type-checker-for-python)

possible testing / diag : 

[pyright/command-line.md at master · microsoft/pyright (github.com)](https://github.com/microsoft/pyright/blob/master/docs/command-line.md)



## 3.3 - pylint 

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



## 3.3 - Deprecated - Microsoft Python Language Server settings  [MPLS]

MPLS is being replaced by Pylance , and the below configuration is for reference only .

The language server settings apply when `python.jediEnabled` is `false`.

| Setting            | Default                              | Description                                                  | ref                                                          |
| ------------------ | ------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| python.jediEnabled | Default *true*, must be set to FALSE | Indicates whether to use Jedi as the IntelliSense engine (true) or the Microsoft Python Language Server (false). Note that the language server requires a platform that supports .NET Core 2.1 or newer. |                                                              |
| python.analysis.   |                                      |                                                              | [code analysis settings)](https://code.visualstudio.com/docs/python/settings-reference#_code-analysis-settings) |
| typeshedPaths      | []                                   | Paths to look for typeshed modules on GitHub.                |                                                              |

*The long-term plan is to transition the Microsoft Python Language Server users over to Pylance and eventually deprecate and remove the old language server as a supported option*