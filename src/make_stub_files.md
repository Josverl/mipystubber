
This is the readme file for `make_stub_files.py`. This file explains what
the script does, how it works and why it is important. After a brief
overview, a step-by-step section will get you started. Full source code for
the script is in its [github repository]
(https://github.com/edreamleo/make-stub-files). This script is in the
public domain.


### Overview

This script makes a stub (.pyi) file in the **output directory** for each
**source file** listed on the command line (wildcard file names are
supported). This script never creates directories automatically, nor does
it overwrite stub files unless the --overwrite command-line option is in
effect.

GvR says,
> We actually do have a [stub generator](https://github.com/JukkaL/mypy/blob/master/mypy/stubgen.py)
> as part of mypy now (it has a few options) but yours has the advantage of
> providing a way to tune the generated signatures...This allows for a nice
> iterative way of developing stubs.

The script does no type inference. Instead, the user supplies **patterns**
in a configuration file. The script matches these patterns to:

1. The names of arguments in functions and methods and

2. The text of **return expressions**. Return expressions are the actual
   text of whatever follows the "return" keyword. The script removes all
   comments in return expressions and converts all strings to "str". This
   **preprocessing** greatly simplifies pattern matching.

As a first example, given the method:

    def foo(self, i, s):
        if i:
            return "abc" # a comment
        else:
            return s
        
and the patterns:

    i: int
    s: str
    
the script produces the stub:

    def foo(i: int, s: str) --> str: ...

The `make_stub_files` script eliminates much of the drudgery of creating
[python stub (.pyi) files]
(https://www.python.org/dev/peps/pep-0484/#stub-files)
from python source files. This script should encourage more people to use mypy. Stub files can be used by people who use Python 2.x code bases.


### Quick Start

1. Put `make_stub_files.py` on your path.

2. Enter a directory containing .py files:

        cd myDirectory
    
3. Generate stubs for foo.py in foo.pyi:

        make_stub_files foo.py

4. Look at foo.pyi to see the generated stubs.

5. Regenerate foo.pyi with more verbose output:

        make_stub_files foo.py -o -v

   The -o (--overwrite) option allows the script to overwrite foo.pyi.  
   The -v (--verbose) options generates return comments for all stubs in foo.pyi.
   
6. Update foo.pyi:

        make_stub_files -o -u
        
   The -u (--update) options updates foo.pyi as follows:
   
   - adds stubs to foo.pyi for classes and defs that are new in foo.py.
   - deletes stubs in foo.pyi for classes and defs that no longer exist in foo.py.
   - leaves all other stubs in foo.pyi unchanged.
   
7. Specify a configuration file containing patterns:

        make_stub_files -c myConfigFile.cfg -o

### Command-line arguments

    Usage: make_stub_files.py [options] file1, file2, ...
    
    Options:
      -h, --help          show this help message and exit
      -c FN, --config=FN  full path to configuration file
      -d DIR, --dir=DIR   full path to the output directory
      -o, --overwrite     overwrite existing stub (.pyi) files
      -t, --test          run unit tests on startup
      --trace-matches     trace Pattern.matches
      --trace-patterns    trace pattern creation
      --trace-reduce      trace st.reduce_types
      --trace-visitors    trace visitor methods
      -u, --update        update stubs in existing stub file
      -v, --verbose       verbose output in .pyi file
      -w, --warn          warn about unannotated args

*Note*: glob.glob wildcards can be used in file1, file2, ...

### The configuration file

The --config command-line option specifies the full path to the optional
configuration file. The configuration file uses the .ini format. It has
several configuration sections, all optional.


#### Patterns

The [Def Name Patterns] and [General Patterns] configuration sections
specify patterns. All patterns have the form:

    find-string: replacement-string
    
Colons are not allowed in the find-string. This is a limitation of .ini files.

There are three kinds of patterns: balanced, regex and plain.

**Balanced patterns** are patterns whose find string that:

A: contain either `(*)`, `[*]`, or `{*}` or

B: ends with `*`.

Unlike regular expressions, `(*)`, `[*]`, or `{*}` match only
balanced brackets. A trailing `*` matches the rest of the string.

Examples:

    str(*): str
    StubTraverser.do_*
    
Balanced patterns such as:

    [*]: List[*]

work as expected. The script replaces the `*` in replacement-strings with
whatever matched `*` in the find-string.

**Regex patterns** (regular expression patterns) are denoted by a
find-string that ends with `$`. The trailing `$` does not become part of
the find-string. For example:

    ab(.*)de$: de\1\1ab

A pattern is a **plain pattern** if it is neither a balanced nor a regex
pattern.

The script matches patterns to *all parts* of return expressions.

*Important*: The script applies patterns *separately* to each return
expression. Comments never appear in return expressions, and all strings in
return values appear as str. As a result, there is no context to worry
about context in which patterns are matched. Very short patterns suffice.


#### [Global]

This configuration section specifies the files list, prefix lines and
output directory. For example:

    [Global]

    files:
        # Files to be used *only* if no files are given on the command line.
        # glob.glob wildcards are supported.
        ~/leo-editor/leo/core/*.py
        
    output_directory:
        # The output directory to be used if no --dir option is given.
        ~/stubs
        
    prefix:
        # Lines to be inserted at the start of each stub file.
        from typing import TypeVar, Iterable, Tuple
        T = TypeVar('T', int, float, complex)

#### [Def Name Patterns]

The script matches the find-strings in this section against names of
functions and methods. For methods, the script matches find-strings against
names of the form:

    class_name.method_name

When a find-string matches, the replacement-string becomes the return type
in the stub, without any further pattern matching. That is, this section
*overrides* [General Patterns].

Example 1:

    [Def Name Patterns]
    myFunction: List[str]
    
Any function named myFunction returns List[str].

Example 2:

    [Def Name Patterns]
    MyClass.myMethod: str
    
The myMethod method of the MyClass class returns str.

Example 3:

    [Def Name Patterns]
    MyClass.do_*: str
    
All methods of the MyClass class whose names start with "do_" return str.

#### [General Patterns]

For each function or method, the script matches the patterns in this
section against **all parts** of all return expressions in each function or method.

The intent of the patterns in this section should be to **reduce** return
expressions to **known types**. A known type is a either a name of a type
class, such as int, str, long, etc. or a **type hint**, as per
[Pep 484](https://www.python.org/dev/peps/pep-0484/).

The script *always* produces a syntactically correct stub, even if the
patterns do not reduce the return expression to a known type. For unknown
types, the script does the following:

1. Uses Any as the type of the function or method.

2. Follows the stub with a list of comments giving all the return
   expressions in the function or method.
   
For example, suppose that the patterns are not sufficient to resolve the
return type of:

    def foo(a):
        if a:
            return a+frungify(a)
        else:
            return defrungify(a)
         
The script will create this stub:

    def foo(a) --> Any: ...
        # return a+frungify(a)
        # return defrungify(a)
        
The comments preserve maximal information about return types, which should
help the user to supply a more specific return type. The user can do this
in two ways by altering the stub files by hand or by adding new patterns to
the config file.

### Why this script is important

The script eliminates most of the drudgery from creating stub files. The
script produces syntactically and semantically correct stub files without
any patterns at all. Patterns make it easy to make stubs more specific.

Once we create stub files, mypy will check them by doing real type
inference. This will find errors both in the stub files and in the program
under test. There is now an easy way to use mypy!

Stubs express design intentions and intuitions as well as types. Until now,
there has been no practical way of expressing and *testing* these
assumptions. Now there is.

Using mypy, we can be as specific as we like about types. We can simply
annotate that d is a dict, or we can say that d is a dict whose keys are
strings and whose values are executables with a union of possible
signatures. Stubs are the easy way to play with type inference.

Stub files clarify long-standing questions about types. To what extent *do*
we understand types? How dynamic (RPython-like) *are* our programs? mypy
will tell us where are stub files are dubious. Could we use type annotation
to convert our programs to C? Not likely, but now there is a way to know
where things get sticky.

Finally, stubs can simplify the general type inference problem. Without
type hints or annotations, the type of everything depends on the type of
everything else. Stubs could allow robust, maybe even complete, type
inference to be done locally. Stubs help mypy to work faster.

### Summary

The make-stub-files script does for type/design analysis what Leo's c2py
command did for converting C sources to python. It eliminates much of the
drudgery associated with creating stub files, leaving the programmer to
make non-trivial inferences.

Stub files allow us to explore type checking using mypy as a guide and
helper. Stub files are both a design document and an executable, checkable,
type specification. Stub files allow those with a Python 2 code base to use
mypy.

One could imagine a similar insert_annotations script that would inject
function annotations into source files using stub files as data. The
"reverse" script should be more straightforward than this script.

Edward K. Ream  
January 25 to February 15, 2016
