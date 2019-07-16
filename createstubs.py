"""
Create stubs for (all) modules on a MicroPython board
Copyright (c) 2019 Jos Verlinde
"""
import errno
import gc
import logging
import os
import sys
from utime import sleep_us
from ujson import dumps

stubber_version = '1.2.0'
# deal with firmware specific implementations
try:
    from machine import resetWDT
except:
    def resetWDT():
        pass

class Stubber():
    "Generate stubs for modules in firmware"
    def __init__(self, path: str = None):
        self._log = logging.getLogger('stubber')
        self._report = []
        u = os.uname()
        # use sys.implementation for consistency
        v = ".".join([str(i) for i in sys.implementation.version])
        self._report_fwi = {'firmware': {'sysname': u.sysname, 'nodename': u.nodename, 'release': u.release, 'version': v, 'machine': u.machine, 'firmware': self.firmware_ID()}}
        self._report_stb = {'stubber':{'version': stubber_version}}
        del u
        del v
        if path:
            #get rid of trailing slash
            if path.endswith('/'):
                path = path[:-1]
        else:
            #determine path for stubs
            path = "{}/stubs/{}".format(
                self.get_root(),
                self.firmware_ID(asfile=True)
                ).replace('//', '/')

        self.path = path
        try:
            self.ensure_folder(path + "/")
        except:
            self._log.error("error creating stub folder {}".format(path))
        self.problematic = ["upysh", "webrepl_setup", "http_client", "http_client_ssl", "http_server", "http_server_ssl"]
        self.excluded = ["webrepl", "_webrepl", "webrepl_setup"]
        # there is no option to discover modules from upython, need to hardcode
        # below contains the combines modules from  Micropython ESP8622, ESP32 and Loboris Modules
        self.modules = ['_boot', '_onewire', '_thread', '_webrepl', 'ak8963', 'apa102', 'apa106', 'array', 'binascii', 'btree', 'builtins', 'upip', #do upip early
                        'cmath', 'collections', 'curl', 'dht', 'display', 'ds18x20', 'errno', 'esp', 'esp32', 'example_pub_button', 'example_sub_led',
                        'flashbdev', 'framebuf', 'freesans20', 'functools', 'gc', 'gsm', 'hashlib', 'heapq', 'http_client', 'http_client_ssl', 'http_server',
                        'http_server_ssl', 'inisetup', 'io', 'json', 'logging', 'lwip', 'machine', 'math', 'microWebSocket', 'microWebSrv', 'microWebTemplate',
                        'micropython', 'mpu6500', 'mpu9250', 'neopixel', 'network', 'ntptime', 'onewire', 'os', 'port_diag', 'pye', 'random', 're', 'requests',
                        'select', 'socket', 'socketupip', 'ssd1306', 'ssh', 'ssl', 'struct', 'sys', 'time', 'tpcalib', 'uasyncio', 'uasyncio/core', 'ubinascii',
                        'ucollections', 'ucryptolib', 'uctypes', 'uerrno', 'uhashlib', 'uheapq', 'uio', 'ujson', 'umqtt/robust', 'umqtt/simple', 'uos', 'upip_utarfile',
                        'upysh', 'urandom', 'ure', 'urequests', 'urllib/urequest', 'uselect', 'usocket', 'ussl', 'ustruct', 'utime', 'utimeq', 'uwebsocket', 'uzlib', 'webrepl',
                        'webrepl_setup', 'websocket', 'websocket_helper', 'writer', 'ymodem', 'zlib']

        #try to avoid running out of memory with nested mods
        self.include_nested = gc.mem_free() > 3200

    def get_obj_attributes(self, obj: object):
        "extract information of the objects members and attributes"
        result = []
        errors = []
        #self._log.info('get attributes {} {}'.format(repr(obj),obj ))
        for name in dir(obj):
            try:
                val = getattr(obj, name)
                # name , value , type
                result.append((name, repr(val), repr(type(val)), val))
                #self._log.info( result[-1])
            except BaseException as e:
                errors.append("Couldn't get attribute '{}' from object '{}', Err: {}".format(name, obj, e))
        gc.collect()
        return result, errors

    def add_modules(self, modules: list):
        "Add additional modules to be exported"
        self.modules = sorted(set(self.modules) | set(modules))

    def create_all_stubs(self):
        "Create stubs for all configured modules"
        self._log.info("Start micropython-stubber v{} on {}".format(stubber_version, self.firmware_ID()))
        # start with the (more complex) modules with a / first to reduce memory problems
        self.modules = [m for m in self.modules if '/' in m] + [m for m in self.modules if '/' not in m]
        gc.collect()
        for module_name in self.modules:
            #re-evaluate
            if self.include_nested:
                self.include_nested = gc.mem_free() > 3200

            if module_name.startswith("_") and module_name != '_thread':
                self._log.warning("Skip module: {:<20}        : internal ".format(module_name))
                continue
            if module_name in self.problematic:
                self._log.warning("Skip module: {:<20}        : Known problematic".format(module_name))
                continue
            if module_name in self.excluded:
                self._log.warning("Skip module: {:<20}        : Excluded".format(module_name))
                continue

            file_name = "{}/{}.py".format(
                self.path,
                module_name.replace(".", "/")
            )
            gc.collect()
            m1 = gc.mem_free()
            self._log.info("Stub module: {:<20} to file: {:<55} mem:{:>5}".format(module_name, file_name, m1))
            try:
                self.create_module_stub(module_name, file_name)
            except:
                pass
            gc.collect()
            m2 = gc.mem_free()
            self._log.debug("Memory     : {:>20} {:>6}".format(m1, m1-m2))
        self._log.info('Finally done')

    def create_module_stub(self, module_name: str, file_name: str = None):
        "Create a Stub of a single python module"
        if module_name.startswith("_") and module_name != '_thread':
            self._log.warning("SKIPPING internal module:{}".format(module_name))
            return

        if module_name in self.problematic:
            self._log.warning("SKIPPING problematic module:{}".format(module_name))
            return
        if '/' in module_name:
            #for nested modules
            self.ensure_folder(file_name)
            module_name = module_name.replace('/', '.')
            if not self.include_nested:
                self._log.warning("SKIPPING nested module:{}".format(module_name))
                return

        if file_name is None:
            file_name = module_name.replace('.', '_') + ".py"

        #import the module (as new_module) to examine it
        try:
            new_module = __import__(module_name)
        except ImportError as e:
            self._log.debug("Unable to import module: {} : {}".format(module_name, e))
            return
        except e:
            self._log.error("Failed to import module: {}".format(module_name))
            return

        # Start a new file
        with open(file_name, "w") as fp:
            s = "\"\"\"\nModule: '{0}' on {1}\n\"\"\"\n# MCU: {2}\n# Stubber: {3}\n".format(module_name, self.firmware_ID(), os.uname(), stubber_version)
            fp.write(s)
            self.write_object_stub(fp, new_module, module_name, "")
            self._report.append({"module":module_name, "file": file_name})

        if not module_name in ["os", "sys", "logging", "gc"]:
            #try to unload the module unless we use it
            try:
                del new_module
            except BaseException:
                self._log.warning("could not del new_module")
            try:
                del sys.modules[module_name]
            except BaseException:
                self._log.debug("could not del modules[{}]".format(module_name))
            gc.collect()

    def write_object_stub(self, fp, object_expr: object, obj_name: str, indent: str):
        "Write an object stub to an open file. Can call recursive."
        if object_expr in self.problematic:
            self._log.warning("SKIPPING problematic module:{}".format(object_expr))
            return

        self._log.debug("DUMPING : {}".format(object_expr))
        items, errors = self.get_obj_attributes(object_expr)
        if errors:
            self._log.error(errors)

        for name, rep, typ, obj in sorted(items, key=lambda x: x[0]):
            if name.startswith("__"):
                #skip internals
                continue
            # allow the scheduler to run
            resetWDT()
            sleep_us(1)

            self._log.debug("DUMPING {}{}{}:{}".format(indent, object_expr, name, typ))

            if typ in ["<class 'function'>", "<class 'bound_method'>"]:
                s = indent + "def " + name + "():\n"
                s += indent + "    pass\n\n"
                fp.write(s)
                self._log.debug(s)

            elif typ in ["<class 'str'>", "<class 'int'>", "<class 'float'>"]:
                s = indent + name + " = " + rep + "\n"
                fp.write(s)
                self._log.debug(s)
            #new class
            elif typ == "<class 'type'>" and indent == "":
                # full expansion only on toplevel
                # stub style : Empty comment ... + hardcoded 4 spaces
                s = "\n" + indent + "class " + name + ":\n"  # What about superclass?
                s += indent + "    ''\n"

                fp.write(s)
                self._log.debug(s)

                self._log.debug("#recursion !!")
                self.write_object_stub(fp, obj, "{0}.{1}".format(obj_name, name), indent + "    ")
            else:
                # keep only the name
                fp.write(indent + name + " = None\n")
        del items
        del errors
        try:
            del name, rep, typ, obj # pylint: disable=undefined-loop-variable
        except:
            pass

    @staticmethod
    def firmware_ID(asfile: bool = False):
        "Get a sensible firmware ID"
        if os.uname().sysname in 'esp32_LoBo':
            #version in release
            ver = os.uname().release
        else:
            # version before '-' in version
            ver = os.uname().version.split('-')[0]
        fid = "{} {}".format(os.uname().sysname, ver)
        if asfile:
            # path name restrictions
            chars = " .()/\\:$"
            for c in chars:
                fid = fid.replace(c, "_")
        return fid

    def clean(self):
        "Remove all files from the stub folder"
        self._log.info("Clean/remove files in stubfolder: {}".format(self.path))
        for fn in os.listdir(self.path):
            try:
                os.remove("{}/{}".format(self.path, fn))
            except:
                pass

    def report(self, filename: str = "modules.json"):
        "create json with list of exported modules"
        self._log.info("Created stubs for {} modules on board {}\nPath: {}".format(
            len(self._report),
            self.firmware_ID(),
            self.path
            ))
        f_name = "{}/{}".format(self.path, filename)
        gc.collect()
        try:
            # write json by node to reduce memory requirements
            with open(f_name, 'w') as f:
                f.write('{')
                f.write(dumps(self._report_fwi)[1:-1])
                f.write(',')
                f.write(dumps(self._report_stb)[1:-1])
                f.write(',')
                f.write('"modules" :[')
                start = True
                for n in self._report:
                    if start:
                        start = False
                    else:
                        f.write(',')
                    f.write(dumps(n))
                f.write(']}')
        except:
            self._log.error("Failed to create the report.")

    def ensure_folder(self, path: str):
        "Create nested folders if needed"
        i = start = 0
        while i != -1:
            i = path.find('/', start)
            if i != -1:
                if i == 0:
                    p = path[0]
                else:
                    p = path[0:i]
                # p = partial folder
                try:
                    _ = os.stat(p)
                except OSError as e:
                    # folder does not exist
                    if e.args[0] == errno.ENOENT:
                        try:
                            os.mkdir(p)
                        except OSError as e2:
                            self._log.error('failed to create folder {}'.format(p))
                            raise e2
                    else:
                        self._log.error('failed to create folder {}'.format(p))
                        raise e
            #next level deep
            start = i+1

    @staticmethod
    def get_root():
        "Determine the root folder of the device"
        try:
            r = "/flash"
            _ = os.stat(r)
        except OSError as e:
            if e.args[0] == errno.ENOENT:
                r = os.getcwd()
            else:
                r = '/'
        return r


def main():
    global stubber
    try:
        logging.basicConfig(level=logging.INFO)
    except:
        pass
    # Now clean up and get to work
    stubber = Stubber()
    stubber.clean()
    # limit for debugging
    # stubber.modules = ['machine']
    # stubber.add_modules(['xyz'])
    stubber.create_all_stubs()
    stubber.report()

main()
