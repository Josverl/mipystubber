# Boost MicroPython productivity in VSCode

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

1. The sister-repo MicroPython-stubs**][stubs-repo] contains [all stubs][all-stubs] I have collected with the help of others, and which can be used directly.
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



Index : 

[1 Approach](docs/1_approach.md)

[2 Using the subs](docs/2_using_stubs.md)

[1 Advanced VSCode and pylint configuration](docs/3_configuraton.md)

[4 Create Fimware Stubs](docs/4_create_stubs.md)









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

----------------------------

--------------------------------



[stubs-repo]:   https://github.com/Josverl/micropython-stubs
[stubs-repo2]:  https://github.com/BradenM/micropy-stubs
[micropython-stubber]: https://github.com/Josverl/micropython-stubber
[micropython-stubs]: https://github.com/Josverl/micropython-stubs#micropython-stubs
[micropy-cli]: https://github.com/BradenM/micropy-cli
[using-the-stubs]: https://github.com/Josverl/micropython-stubs#using-the-stubs
[demo]:         /docs/img/demo.gif	"demo of writing code using the stubs"
[stub processing order]: /docs/img/stuborder_pylance.png	"recommended stub processing order"
[naming-convention]: #naming-convention-and-stub-folder-structure
[all-stubs]: https://github.com/Josverl/micropython-stubs/blob/master/firmwares.md
[micropython]: https://github.com/micropython/micropython
[micropython-lib]:  https://github.com/micropython/micropython-lib
[pycopy]: https://github.com/pfalcon/pycopy
[pycopy-lib]: https://github.com/pfalcon/pycopy-lib
[createstubs-flow]: /docs/img/createstubs-flow.png
[symlink]: #6.4-create-a-symbolic-link