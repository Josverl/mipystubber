"""
Create stubs for (all) modules on a MicroPython board
Copyright (c) 2019-2020 Jos Verlinde
"""
import sys
import gc
import uos as os
from utime import sleep_us
from ujson import dumps
ENOENT=2
stubber_version='1.3.7'
try:
 from machine import resetWDT 
except ImportError:
 def resetWDT():
  pass
class Stubber():
 def __init__(self,path:str=None,firmware_id:str=None):
  try:
   if os.uname().release=='1.13.0' and os.uname().version<'v1.13-103':
    raise NotImplementedError("MicroPyton 1.13.0 cannot be stubbed")
  except AttributeError:
   pass
  self._report=[]
  self.info=self._info()
  self._fwid=str(firmware_id).lower()or "{family}-{port}-{ver}".format(**self.info).lower()
  self._start_free=gc.mem_free()
  if path:
   if path.endswith('/'):
    path=path[:-1]
  else:
   path=self.get_root()
  self.path="{}/stubs/{}".format(path,self.flat_fwid).replace('//','/')
  try:
   self.ensure_folder(path+"/")
  except OSError:
   pass
  self.problematic=["upysh","webrepl_setup","http_client","http_client_ssl","http_server","http_server_ssl"]
  self.excluded=["webrepl","_webrepl","port_diag","example_sub_led.py","example_pub_button.py"]
  self.modules=['_thread','ak8963','apa102','apa106','array','binascii','btree','bluetooth','builtins','cmath','collections','crypto','curl','dht','display','ds18x20','errno','esp','esp32','flashbdev','framebuf','freesans20','functools','gc','gsm','hashlib','heapq','inisetup','io','json','logging','lwip','machine','math','microWebSocket','microWebSrv','microWebTemplate','micropython','mpu6500','mpu9250','neopixel','network','ntptime','onewire','os','port_diag','pycom','pye','random','re','requests','select','socket','ssd1306','ssh','ssl','struct','sys','time','tpcalib','ubinascii','ucollections','ucryptolib','uctypes','uerrno','uhashlib','uheapq','uio','ujson','umqtt/robust','umqtt/simple','uos','upip','upip_utarfile','urandom','ure','urequests','urllib/urequest','uselect','usocket','ussl','ustruct','utime','utimeq','uwebsocket','uzlib','websocket','websocket_helper','writer','ymodem','zlib','pycom','crypto']
  self.modules+=['pyb','stm','pycopy']
  self.modules+=['uasyncio/lock','uasyncio/stream','uasyncio/__init__','uasyncio/core','uasyncio/event','uasyncio/funcs']
  self.include_nested=gc.mem_free()>3200 
 @staticmethod
 def _info():
  info={'name':sys.implementation.name,'release':'0.0.0','version':'0.0.0','build':'','sysname':'unknown','nodename':'unknown','machine':'unknown','family':sys.implementation.name,'platform':sys.platform,'port':sys.platform,'ver':''}
  try:
   info['release']=".".join([str(i)for i in sys.implementation.version])
   info['version']=info['release']
   info['name']=sys.implementation.name
   info['mpy']=sys.implementation.mpy
  except AttributeError:
   pass
  if sys.platform not in('unix','win32'):
   try:
    u=os.uname()
    info['sysname']=u.sysname
    info['nodename']=u.nodename
    info['release']=u.release
    info['machine']=u.machine
    if ' on ' in u.version:
     s=u.version.split('on ')[0]
     try:
      info['build']=s.split('-')[1]
     except IndexError:
      pass
   except(IndexError,AttributeError):
    pass
  try:
   from pycopy import const
   info['family']='pycopy'
   del const
  except(ImportError,KeyError):
   pass
  if info['platform']=='esp32_LoBo':
   info['family']='loboris'
   info['port']='esp32'
  info['ver']='v'+info['release']
  if info['family']!='loboris':
   if info['release']>='1.10.0' and info['release'].endswith('.0'):
    info['ver']=info['release'][:-2]
   else:
    info['ver']=info['release']
   if info['build']!='':
    info['ver']+='-'+info['build']
  if 'mpy' in info: 
   sys_mpy=info['mpy']
   arch=[None,'x86','x64','armv6','armv6m','armv7m','armv7em','armv7emsp','armv7emdp','xtensa','xtensawin'][sys_mpy>>10]
   if arch:
    info['arch']=arch
  return info
 def get_obj_attributes(self,obj:object):
  result=[]
  errors=[]
  name=None
  try:
   for name in dir(obj):
    try:
     val=getattr(obj,name)
     result.append((name,repr(val),repr(type(val)),val))
    except AttributeError as e:
     errors.append("Couldn't get attribute '{}' from object '{}', Err: {}".format(name,obj,e))
  except AttributeError as e:
   errors.append("Couldn't get attribute '{}' from object '{}', Err: {}".format(name,obj,e))
  gc.collect()
  return result,errors
 def add_modules(self,modules:list):
  self.modules=sorted(set(self.modules)|set(modules))
 def create_all_stubs(self):
  self.modules=[m for m in self.modules if '/' in m]+[m for m in self.modules if '/' not in m]
  gc.collect()
  for module_name in self.modules:
   if self.include_nested:
    self.include_nested=gc.mem_free()>3200 
   if module_name.startswith("_")and module_name!='_thread':
    continue
   if module_name in self.problematic:
    continue
   if module_name in self.excluded:
    continue
   file_name="{}/{}.py".format(self.path,module_name.replace(".","/"))
   gc.collect()
   m1=gc.mem_free()
   print("Stub module: {:<20} to file: {:<55} mem:{:>5}".format(module_name,file_name,m1))
   try:
    self.create_module_stub(module_name,file_name)
   except OSError:
    pass
   gc.collect()
 def create_module_stub(self,module_name:str,file_name:str=None):
  if module_name.startswith("_")and module_name!='_thread':
   return
  if module_name in self.problematic:
   return
  if '/' in module_name:
   self.ensure_folder(file_name)
   module_name=module_name.replace('/','.')
   if not self.include_nested:
    return
  if file_name is None:
   file_name=module_name.replace('.','_')+".py"
  failed=False
  new_module=None
  try:
   new_module=__import__(module_name,None,None,('*'))
  except ImportError:
   failed=True
   if not '.' in module_name:
    return
  if failed and '.' in module_name:
   levels=module_name.split('.')
   for n in range(1,len(levels)):
    parent_name=".".join(levels[0:n])
    try:
     parent=__import__(parent_name)
     del parent
    except(ImportError,KeyError):
     pass
   try:
    new_module=__import__(module_name,None,None,('*'))
   except ImportError:
    return
  with open(file_name,"w")as fp:
   s="\"\"\"\nModule: '{0}' on {1}\n\"\"\"\n# MCU: {2}\n# Stubber: {3}\n".format(module_name,self._fwid,self.info,stubber_version)
   fp.write(s)
   self.write_object_stub(fp,new_module,module_name,"")
   self._report.append({"module":module_name,"file":file_name})
  if not module_name in["os","sys","logging","gc"]:
   try:
    del new_module
   except(OSError,KeyError):
    pass
   try:
    del sys.modules[module_name]
   except KeyError:
    pass
   gc.collect()
 def write_object_stub(self,fp,object_expr:object,obj_name:str,indent:str):
  if object_expr in self.problematic:
   return
  items,errors=self.get_obj_attributes(object_expr)
  for name,rep,typ,obj in sorted(items,key=lambda x:x[0]):
   if name.startswith("__"):
    continue
   resetWDT()
   sleep_us(1)
   if typ in["<class 'function'>","<class 'bound_method'>"]:
    s=indent+"def "+name+"():\n" 
    s+=indent+"    pass\n\n"
    fp.write(s)
   elif typ in["<class 'str'>","<class 'int'>","<class 'float'>"]:
    s=indent+name+" = "+rep+"\n"
    fp.write(s)
   elif typ=="<class 'type'>" and indent=="":
    s="\n"+indent+"class "+name+":\n" 
    s+=indent+"    ''\n"
    fp.write(s)
    self.write_object_stub(fp,obj,"{0}.{1}".format(obj_name,name),indent+"    ")
   else:
    fp.write(indent+name+" = None\n")
  del items
  del errors
  try:
   del name,rep,typ,obj 
  except(OSError,KeyError):
   pass
 @property
 def flat_fwid(self):
  s=self._fwid
  chars=" .()/\\:$"
  for c in chars:
   s=s.replace(c,"_")
  return s
 def clean(self,path:str=None):
  if path is None:
   path=self.path
  print("Clean/remove files in folder: {}".format(path))
  try:
   items=os.listdir(path)
  except(OSError,AttributeError):
   return
  for fn in items:
   try:
    item="{}/{}".format(path,fn)
    os.remove(item)
   except OSError:
    try:
     self.clean(item)
     os.rmdir(item)
    except OSError:
     pass
 def report(self,filename:str="modules.json"):
  f_name="{}/{}".format(self.path,filename)
  gc.collect()
  try:
   with open(f_name,'w')as f:
    f.write('{')
    f.write(dumps({'firmware':self.info})[1:-1])
    f.write(',')
    f.write(dumps({'stubber':{'version':stubber_version}})[1:-1])
    f.write(',')
    f.write('"modules" :[')
    start=True
    for n in self._report:
     if start:
      start=False
     else:
      f.write(',')
     f.write(dumps(n))
    f.write(']}')
   used=self._start_free-gc.mem_free()
  except OSError:
   pass
 def ensure_folder(self,path:str):
  i=start=0
  while i!=-1:
   i=path.find('/',start)
   if i!=-1:
    if i==0:
     p=path[0]
    else:
     p=path[0:i]
    try:
     _=os.stat(p)
    except OSError as e:
     if e.args[0]==ENOENT:
      try:
       os.mkdir(p)
      except OSError as e2:
       raise e2
     else:
      raise e
   start=i+1
 @staticmethod
 def get_root()->str:
  try:
   r="/flash"
   _=os.stat(r)
  except OSError as e:
   if e.args[0]==ENOENT:
    try:
     r=os.getcwd()
    except:
     r='.'
   else:
    r='/'
  return r
def show_help():
 sys.exit(1)
def read_path()->str:
 path=None
 if len(sys.argv)==3:
  cmd=(sys.argv[1]).lower()
  if cmd in('--path','-p'):
   path =sys.argv[2]
  else:
   show_help()
 elif len(sys.argv)>=2:
  show_help()
 return path
def main():
 try:
  logging.basicConfig(level=logging.INFO)
 except NameError:
  pass
 stubber=Stubber(path=read_path())
 stubber.clean()
 stubber.create_all_stubs()
 stubber.report()
main()
