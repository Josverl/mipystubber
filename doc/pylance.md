

Pyright 

https://github.com/microsoft/pyright/blob/master/docs/getting-started.md


### https://github.com/microsoft/pyright/blob/master/docs/configuration.md

typeshedPath [path, optional]: Path to a directory that contains typeshed type stub files. Pyright ships with a bundled copy of typeshed type stubs. If you want to use a different version of typeshed stubs, you can clone the typeshed github repo to a local directory and reference the location with this path. This option is useful if you’re actively contributing updates to typeshed.

stubPath [path, optional]: Path to a directory that contains custom type stubs. Each package's type stub file(s) are expected to be in its own subdirectory. The default value of this setting is "./typings". (typingsPath is now deprecated)

executionEnvironments [array of objects, optional]: Specifies a list of execution environments (see below). Execution environments are searched from start to finish by comparing the path of a source file with the root path specified in the execution environment.

https://github.com/microsoft/pyright/blob/master/docs/configuration.md#sample-config-file 

### http://www.ianhopkinson.org.uk/2020/07/type-annotations-in-python-an-adventure-with-visual-studio-code-and-pylance/


There a number of different ways of providing typing information, depending on your preference and whether you are looking at your own code, or at a 3rd party library:

 1. Types provided at definition in the source module – this is the simplest method, you just replace the function def line in the source module file with the type annotated one;

 2. Types provided in the source module by use of *.pyi files – you can also put the type-annotated function definition in a *.pyi file alongside the original file in the source module in the manner of a C header file. The *.pyi file needs to sit in the same directory as its *.py sibling. This definition takes precedence over a definition in the *.py file. The reason for using this route is that it does not bring incompatible syntax into the *.py files – non-compliant interpreters will simply ignore *.pyi files but it does clutter up your filespace. Also there is a risk of the *.py and *pyi becoming inconsistent;

 3. Stub files added to the destination project – if you import write_dictionary into a project Pylance will highlight that it cannot find a stub file for ihutilities and will offer to create one. This creates a `typings` subdirectory alongside the file on which this fix was executed, this contains a subdirectory called `ihutilities` in which there are files mirroring those in the ihutilities package but with the *.pyi extension i.e. __init__.pyi, io_utils.py, etc which you can modify appropriately;

 4. Types provided by stub-only packages – PEP-0561 indicates a fourth route which is to load the type annotations from a separate, stub only, module.

 5. Types provided by Typeshed – Pyright uses Typeshedfor annotations for built-in and standard libraries, as well as some popular third party libraries;



