#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Pre/Post Processing for createstubs.py"""


import argparse
import itertools
import re
import sys
from optparse import Values
from pathlib import Path

# Pyminifier Dep
token_utils = None
minification = None
try:
    from pyminifier import token_utils, minification
except ImportError:
    pass

ROOT = Path(__file__).parent
SCRIPT = ROOT / 'createstubs.py'
PATCHES = ROOT / 'patches'


def apply_patch(s, patch, revert=False):
    """
    Apply patch to string s to recover newer string.
    If revert is True, treat s as the newer string, recover older string.

    Credits:
    Isaac Turner 2016/12/05
    https://gist.github.com/noporpoise/16e731849eb1231e86d78f9dfeca3abc
    """
    _hdr_pat = re.compile(r"@@ -(\d+),?(\d+)? \+(\d+),?(\d+)? @@")
    s = s.splitlines(True)
    p = patch.splitlines(True)
    t = ''
    i = sl = 0
    (midx, sign) = (1, '+') if not revert else (3, '-')
    while i < len(p) and not p[i].startswith("@@"):
        i += 1  # skip header lines
    while i < len(p):
        m = _hdr_pat.match(p[i])
        if not m:
            raise Exception("Bad patch -- regex mismatch [line "+str(i)+"]")
        l = int(m.group(midx))-1 + (m.group(midx+1) == '0')  # noqa
        if sl > l or l > len(s):
            raise Exception("Bad patch -- bad line num [line "+str(i)+"]")
        t += ''.join(s[sl:l])
        sl = l
        i += 1
        while i < len(p) and p[i][0] != '@':
            if i+1 < len(p) and p[i+1][0] == '\\':
                line = p[i][:-1]
                i += 2
            else:
                line = p[i]
                i += 1
            if len(line) > 0:
                if line[0] == sign or line[0] == ' ':
                    t += line[1:]
                sl += (line[0] != sign)
    t += ''.join(s[sl:])
    return t


def edit_lines(content, edits, show_diff=False):
    """Edit string by list of edits

    Args:
        content (str): content to edit
        edits ([(str, str)]): List of edits to make.
            The first string in the tuple represents
            the type of edit to make, can be either:
                comment - comment text out (removed on minify)
                rprint - replace text with print
                rpass - replace text with pass
            The second string is the matching text to replace
        show_diff (bool, optional): Prints diff of each edit. 
            Defaults to False.

    Returns:
        str: edited string
    """
    def comment(l, x): return l.replace(x, f"# {x}")

    def rprint(l, x):
        split = l.split("(")
        if len(split) > 1:
            return l.replace(split[0].strip(), "print")
        return l.replace(x, f"print")

    def rpass(l, x): return l.replace(x, f"pass")

    def get_whitespace_context(content, index):
        """Get whitespace count of lines surrounding index"""
        def count_ws(line): return sum(
            1 for _ in itertools.takewhile(str.isspace, line))
        lines = content[index - 1:index+2]
        context = (count_ws(l) for l in lines)
        return context

    def handle_multiline(content, index):
        """Handles edits that require multiline comments

        Example:
            self._log.debug("info: {} {}".format(
                1,
                2
            ))
        Here, only commenting out the first self._log line will raise
        an error. So this function returns all lines that need to
        be commented out instead.

        It also checks for situations such as this:
            if condition:
                self._log.debug('message')

        Here, since the only functionality of the conditional is the call log,
        both lines would be returned to comment out.

        """
        line = content[index]
        open_cnt = line.count("(")
        close_cnt = line.count(")")
        ahead_index = 1
        while not open_cnt == close_cnt:
            look_ahead = l_index + ahead_index
            ahead_index += 1
            next_l = content[look_ahead]
            open_cnt += next_l.count("(")
            close_cnt += next_l.count(")")
        if ahead_index > 1:
            return range(index, look_ahead + 1)
        prev = content[index - 1]
        _, line_ws, post_ws = get_whitespace_context(content, index)
        prev_words = prev.strip().strip(":").split()
        check = any(t in ('if', 'else', ) for t in prev_words)
        if check and line_ws != post_ws:
            return range(index-1, index+1)

    def handle_try_except(content, index):
        """Checks if line at index is in try/except block

        Handles situations like this:
            try:
                something()
            except:
                self._log.debug('some message')

        Simply removing the self._log call would create a syntax error,
        which is what this function checks for.

        """
        prev = content[index - 1]
        _, line_ws, post_ws = get_whitespace_context(content, index)
        if 'except' in prev and line_ws != post_ws:
            return True

    lines = []
    multilines = set()
    content = content.splitlines(keepends=True)
    for line in content:
        _line = line
        for edit, text in edits:
            if text in line:
                if edit == "comment":
                    l_index = content.index(line)
                    # Check if edit spans multiple lines
                    mline = handle_multiline(content, l_index)
                    if mline:
                        multilines.update(mline)
                        break
                    # Check if line is only statement in try/except
                    if handle_try_except(content, l_index):
                        edit = "rpass"
                        text = line.strip()
                func = eval(edit)
                line = func(line, text)
                if line != _line:
                    if show_diff:
                        print(f"\n- {_line.strip()}")
                        print(f"+ {line.strip()}")
                    break
        lines.append(line)
    for line_num in multilines:
        # Go back and comment out multilines
        line = lines[line_num]
        lines[line_num] = comment(line, line.strip())
    stripped = "".join(lines)
    return stripped


def minify_script(patches=None, keep_report=True, show_diff=False):
    """minifies createstubs.py

    Args:
        patches ([PathLike], optional): List of paths to patches to apply.
            Defaults to None.
        keep_report (bool, optional): Keeps single report line in createstubs
            Defautls to True.
        show_diff (bool, optional): Print diff from edits. Defaults to False.

    Returns:
        str: minified source text
    """
    patches = patches or []
    edits = [
        ("comment", "print"),
        ("comment", "import logging"),
        ("comment", "self._log ="),
        ("comment", "self._log.debug"),
        ("comment", "self._log.warning"),
        ("comment", "self._log.info"),
        ("comment", "self._log.error"),
    ]
    if keep_report:
        report = ('rprint', ('self._log.info("Stub module: {:<20} to file:'
                             ' {:<55} mem:{:>5}".'
                             'format(module_name, file_name, m1))'))
        edits.insert(0, report)
    minopts = Values({'tabs': False})
    with SCRIPT.open('r') as f:
        content = f.read()
        for path in patches:
            path = Path(path)
            content = apply_patch(content, path.read_text())
        content = edit_lines(content, edits, show_diff=show_diff)
        tokens = token_utils.listified_tokenizer(content)
        source = minification.minify(tokens, minopts)
    return source


def get_patches():
    """Iterate patch files"""
    for f in PATCHES.iterdir():
        yield (f.stem, f.resolve())


def resolve_patches(patch_names):
    """Validates/Provides help for patches"""
    patch_files = list(get_patches())
    patches = [next((p for p in patch_files if p[0] == n), (n, None))
               for n in patch_names]
    paths = []
    for name, path in patches:
        if path is None:
            print(f"Cannot find patch: {name}")
            print("\nAvailable Patches:")
            print("\n".join(p[0] for p in get_patches()))
            sys.exit(0)
        print(f"Applying Patch: {name}")
        paths.append(path)
    return paths


def cli_patch(**kwargs):
    """apply patch cli handler"""
    print("Patching createstubs.py...")
    out = kwargs.get("output")
    patch_names = kwargs.pop('patches')
    paths = resolve_patches(patch_names)
    with SCRIPT.open('r') as f:
        source = f.read()
        for p in paths:
            content = apply_patch(source, p.read_text())
    with out.open('w+') as o:
        o.write(content)
    print("\nDone!")
    print("Patched file written to:", out)


def cli_minify(**kwargs):
    """minify cli handler"""
    print("\nMinifying createstubs.py...")
    out = kwargs.pop("output")
    patches = kwargs.pop("patch")
    if not minification:
        print("\pyminifier is required to minify createstubs.py\n")
        print("Please install via:\n  pip install pyminifier")
        sys.exit(1)
    patch_paths = resolve_patches(patches)
    with out.open('w+') as f:
        report = kwargs.pop('no_report')
        diff = kwargs.pop('diff')
        source = minify_script(
            patches=patch_paths,
            keep_report=report,
            show_diff=diff
        )
        f.write(source)
    print("\nDone!")
    print("Minified file written to:", out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Pre/Post Processing for createstubs.py")
    parser.set_defaults(func=None)
    parser.add_argument(
        "-o", "--output",
        help="Specify file to output to. Defaults to processed.py",
        type=Path,
        default=(ROOT / 'processed.py')
    )
    subparsers = parser.add_subparsers(help="Command to execute")

    minify_parser = subparsers.add_parser("minify",
                                          help=("Create minified version of"
                                                " createstubs.py")
                                          )

    minify_parser.add_argument(
        '-p', '--patch',
        action='append',
        help="Apply patch before minification",
        default=[]
    )
    minify_parser.add_argument(
        "-d", "--diff",
        help="Print diff report from minify",
        action='store_true'
    )
    minify_parser.add_argument(
        "-n", "--no-report",
        help=("Disables all output from createstubs.py."
              " Use if your having memory related issues."),
        action="store_false"
    )
    minify_parser.set_defaults(func=cli_minify)

    patch_parser = subparsers.add_parser(
        "patch",
        help=("Apply a patch to createstubs.py"))
    patch_parser.add_argument(
        "patches",
        help="List of patches to apply, seperated by a space.",
        action='append',
    )
    patch_parser.set_defaults(func=cli_patch)

    args = parser.parse_args()
    if not args.func:
        parser.print_help()
    else:
        args.func(**vars(args))
