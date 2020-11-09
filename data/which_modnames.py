#pylint:disable= trailing-whitespace, line-too-long
#######################################################################
# the exceptions 
#######################################################################
mods_problematic = set(["upysh", "webrepl_setup", "http_client", "http_client_ssl", "http_server", "http_server_ssl"])
mods_excluded = set(['__main__', '_boot', '_webrepl' ,'uasyncio/__init__', "webrepl", "webrepl_setup","uasyncio.__init__","_onewire",'example_pub_button', 'example_sub_led'])
remove = set( mods_excluded | mods_problematic  )

#######################################################################
# LoBo ESP32 3.2.24  
#######################################################################
lobo_esp32 = set([ ##Loboris
            '_thread', 'ak8963', 'array', 'binascii', 'btree', 'builtins',
            'cmath', 'collections', 'curl', 'display', 'errno', 'framebuf',
            'freesans20', 'functools', 'gc', 'gsm', 'hashlib', 'heapq', 'io',
            'json', 'logging', 'machine', 'math', 'microWebSocket', 'microWebSrv',
            'microWebTemplate', 'micropython', 'mpu6500', 'mpu9250', 'network', 'os',
            'pye', 'random', 're', 'requests', 'select', 'socket', 'ssd1306', 'ssh',
            'ssl', 'struct', 'sys', 'time', 'tpcalib', 'ubinascii', 'ucollections',
            'uctypes', 'uerrno', 'uhashlib', 'uheapq', 'uio', 'ujson', 'uos', 'upip',
            'upip_utarfile', 'upysh', 'urandom', 'ure', 'urequests', 'uselect', 'usocket',
            'ussl', 'ustruct', 'utime', 'utimeq', 'uzlib', 'websocket', 'writer', 'ymodem', 'zlib'])

#######################################################################
# ESP32 v1.10?
#######################################################################

mpy_esp32 =set([ #standard ESP32 micropython        
        'framebuf',          'socket',            'upip',
        '_boot',             'gc',                'ssl',               'upip_utarfile',
        '_onewire',          'hashlib',           'struct',            'upysh',
        '_thread',           'heapq',             'sys',               'urandom',
        '_webrepl',          'inisetup',          'time',              'ure',
        'apa106',            'io',                'ubinascii',         'urequests',
        'array',             'json',              'ucollections',      'uselect',
        'binascii',          'machine',           'ucryptolib',        'usocket',
        'btree',             'math',              'uctypes',           'ussl',
        'builtins',          'micropython',       'uerrno',            'ustruct',
        'cmath',             'neopixel',          'uhashlib',          'utime',
        'collections',       'network',           'uhashlib',          'utimeq',
        'dht',               'ntptime',           'uheapq',            'uwebsocket',
        'ds18x20',           'onewire',           'uio',               'uzlib',
        'errno',             'os',                'ujson',             'webrepl',
        'esp',               'random',            'umqtt/robust',      'webrepl_setup',
        'esp32',             're',                'umqtt/simple',      'websocket_helper',
        'flashbdev',         'select',            'uos',               'zlib'
        ])
#######################################################################
# ESP8622 1.11
#######################################################################

#(sysname='esp8266', nodename='esp8266', release='2.2.0-dev(9422289)', version='v1.11-8-g48dcbbe60 on 2019-05-29', machine='ESP module with ESP8266')
mpy_esp8622 = set([
        'http_client',       'socket',            'upip',
        '_boot',             'http_client_ssl',   'ssd1306',           'upip_utarfile',
        '_onewire',          'http_server',       'ssl',               'upysh',
        '_webrepl',          'http_server_ssl',   'struct',            'urandom',
        'apa102',            'inisetup',          'sys',               'ure',
        'array',             'io',                'time',              'urequests',
        'binascii',          'json',              'uasyncio/__init__', 'urllib/urequest',
        'btree',             'lwip',              'uasyncio/core',      'uselect',
        'builtins',          'machine',           'ubinascii',         'usocket',
        'collections',       'math',              'ucollections',      'ussl',
        'dht',               'micropython',       'ucryptolib',        'ustruct',
        'ds18x20',           'neopixel',          'uctypes',           'utime',
        'errno',             'network',           'uerrno',            'utimeq',
        'esp',               'ntptime',           'uhashlib',          'uwebsocket',
        'example_pub_button','onewire',           'uheapq',            'uzlib',
        'example_sub_led',   'os',                'uio',               'webrepl',
        'flashbdev',         'port_diag',         'ujson',             'webrepl_setup',
        'framebuf',          'random',            'umqtt/robust',      'websocket_helper',
        'gc',                're',                'umqtt/simple',       'zlib',
        'hashlib',           'select',            'uos'
        ])

#######################################################################
# M5Flow UI 1.2.1
#######################################################################

# 1.2.1 (sysname='esp32', nodename='esp32', release='1.11.0', version='v1.10-272-g6fdd9e277 on 2019-06-06', machine='ESP32 module with ESP32')
mods_m5_flow = set( [
    '_thread','ak8963','array','binascii','btree','builtins','cmath','collections','display','errno',
    'freesans20','functools','gc','hashlib','heapq','io','json','logging','m5base','m5flow/app_manage',
    'm5flow/i2c_bus','m5flow/m5cloud','m5flow/m5mqtt','m5flow/m5stack','m5flow/m5ucloud',
    'm5flow/peripheral','m5flow/remote','m5flow/simple','m5flow/ubutton','m5flow/unit/_adc',
    'm5flow/unit/_button','m5flow/unit/_color','m5flow/unit/_dac','m5flow/unit/_dual_button',
    'm5flow/unit/_ext_io','m5flow/unit/_finger','m5flow/unit/_ir','m5flow/unit/_ncir',
    'm5flow/unit/_relay','m5flow/unit/_rfid','m5flow/unit/_rgb','m5flow/unit/_tof','m5flow/units',
    'm5flow/utils','m5flow/wifichoose','m5flow/wificonfig','m5flow/wifisetup','m5uart','m5ui',
    'machine','math','micropython','microWebSocket','microWebSrv','microWebTemplate','mpu6500',
    'mpu9250','network','os','pye','random','re','select','socket','ssd1306','ssl','struct',
    'sys','tpcalib','ubinascii','ucollections','uctypes','uerrno','uhashlib','uheapq','uio',
    'ujson','uos','upip','upip_utarfile','upysh','urandom','ure','urequests','uselect','usocket',
    'ussl','ustruct','utime','utimeq','uzlib','websocket','writer','ymodem','zlib'
])

#######################################################################
# M5 FlowUI 1.4.0-beta
#######################################################################

raw = """
__main__          flowlib/lib/speak flowlib/units/_ext_io               neopixel
_onewire          flowlib/lib/time_ex                 flowlib/units/_finger               network
_thread           flowlib/lib/urequests               flowlib/units/_gps                  os
array             flowlib/lib/wave  flowlib/units/_ir random
binascii          flowlib/lib/wavplayer               flowlib/units/_joystick             re
btree             flowlib/lib/wifiCardKB              flowlib/units/_light                select
builtins          flowlib/lib/wifiCfg                 flowlib/units/_makey                socket
cmath             flowlib/lib/wifiWebCfg              flowlib/units/_mlx90640             ssl
collections       flowlib/m5cloud   flowlib/units/_ncir                 struct
display           flowlib/m5mqtt    flowlib/units/_pahub                sys
errno             flowlib/m5stack   flowlib/units/_pbhub                time
esp               flowlib/m5ucloud  flowlib/units/_pir                  ubinascii
esp32             flowlib/module    flowlib/units/_relay                ucollections
espnow            flowlib/modules/_cellular           flowlib/units/_rfid                 ucryptolib
flowlib/app_manage                  flowlib/modules/_lego               flowlib/units/_rgb                  uctypes
flowlib/button    flowlib/modules/_legoBoard          flowlib/units/_rgb_multi            uerrno
flowlib/face      flowlib/modules/_lidarBot           flowlib/units/_servo                uhashlib
flowlib/faces/_calc                 flowlib/modules/_lorawan            flowlib/units/_tof                  uhashlib
flowlib/faces/_encode               flowlib/modules/_m5bala             flowlib/units/_tracker              uheapq
flowlib/faces/_joystick             flowlib/modules/_stepMotor          gc                uos
flowlib/faces/_keyboard             flowlib/peripheral                  hashlib           upip
flowlib/faces/_rfid                 flowlib/power     heapq             upip_utarfile
flowlib/flowSetup flowlib/remote    io                urandom
flowlib/i2c_bus   flowlib/simple    json              ure
flowlib/lib/bmm150                  flowlib/timeSchedule                lidar             uselect
flowlib/lib/bmp280                  flowlib/uiflow    logging           usocket
flowlib/lib/chunk flowlib/unit      m5base            ussl
flowlib/lib/dht12 flowlib/units/_adc                  m5uart            ustruct
flowlib/lib/easyIO                  flowlib/units/_angle                m5ui              utime
flowlib/lib/emoji flowlib/units/_button               machine           utimeq
flowlib/lib/imu   flowlib/units/_cardKB               math              uwebsocket
flowlib/lib/mpu6050                 flowlib/units/_color                microWebSocket    uzlib
flowlib/lib/mstate                  flowlib/units/_dac                  microWebSrv       zlib
flowlib/lib/numbers                 flowlib/units/_dual_button          microWebTemplate
flowlib/lib/pid   flowlib/units/_earth                micropython
flowlib/lib/sh200q                  flowlib/units/_env                  mlx90640
"""

M5flowui = set(raw.split())

#######################################################################
# Lego EV3 MicroPython
#######################################################################

raw = """
main parameters_c pybricks/uev3dev/messaging umachine
_thread pybricks/init pybricks/uev3dev/sound uos
array pybricks/display pybricks/uev3dev/util urandom
boot pybricks/ev3brick sys ure
btree pybricks/ev3devices termios uselect
builtins pybricks/ev3devio tools usocket
cmath pybricks/parameters ubinascii ussl
ev3brick_c pybricks/robotics ucollections ustruct
ev3devices_c pybricks/speaker ucryptolib utime
ffi pybricks/tools uctypes utimeq
framebuf pybricks/uev3dev/init uerrno uzlib
gc pybricks/uev3dev/_alsa uhashlib websocket
math pybricks/uev3dev/_wand uheapq
micropython pybricks/uev3dev/display uio
mmap pybricks/uev3dev/i2c ujson
"""

Lego_EV3 = set(raw.split())

print("\nstubber.add_modules({})".format(sorted( Lego_EV3 - remove) ))


#######################################################################
# 
#######################################################################

pycom = set(['pycom', 'crypto'])

#######################################################################
# 
#######################################################################


print('Known firmwares ========================')
print( "mpy  esp8622  :", len(mpy_esp8622))
print( "mpy  esp32    :", len(mpy_esp32) ) 
print( "lobo esp32    :", len(lobo_esp32 )) 
print( "LEGO EV3      :", len(Lego_EV3)) 
print( "pycom         :", len(pycom)) 

print( "\nm5 flow 1.2   :", len(mods_m5_flow )) 
print( "m5 flowui 1.4 :", len(M5flowui)) 

# print("\m5flow1.4.0_only = ",end='')
# print( sorted( (M5flowui - mpy_esp32) -set( mods_excluded | mods_problematic  ) ))



all = sorted(( mpy_esp32 | lobo_esp32 | mpy_esp8622 | pycom
                    )-set( mods_excluded | mods_problematic  ) )

# Adjust order 
# [m for m in all if '/' in m] + [m for m in all if '/' not in m]

print( "all known   :", len(all )) 
print("\nall = ",end='')
print (all)

all = ['_thread', 'ak8963', 'apa102', 'apa106', 'array', 'binascii', 'btree', 'builtins', 'cmath', 'collections', 
'curl', 'dht', 'display',  'ds18x20', 'errno', 'esp', 'esp32', 'flashbdev', 'framebuf', 'freesans20', 
'functools', 'gc', 'gsm', 'hashlib', 'heapq', 'inisetup', 'io', 'json', 'logging', 'lwip', 'm5base', 'm5flow/app_manage',
 'm5flow/i2c_bus', 'm5flow/m5cloud', 'm5flow/m5mqtt', 'm5flow/m5stack', 'm5flow/peripheral', 'm5flow/unit/ext_io', 
 'm5flow/unit/ir', 'm5flow/unit/ncir', 'm5flow/unit/relay', 'm5flow/unit/rgb_', 'm5flow/unit/tof', 'm5flow/units', 
 'm5flow/utils', 'm5flow/wifichoose', 'm5flow/wificonfig', 'm5flow/wifisetup', 'm5ui', 'machine', 'math', 'microWebSocket', 
 'microWebSrv', 'microWebTemplate', 'micropython', 'mpu6500', 'mpu9250', 'neopixel', 'network', 'ntptime', 'onewire', 
 'os', 'port_diag', 'pye', 'random', 're', 'requests', 'select', 'socket', 'socketupip', 'ssd1306', 'ssh', 'ssl', 
 'struct', 'sys', 'time', 'tpcalib', 'uasyncio/__init__', 'uasyncio/core', 'ubinascii', 'ucollections', 'ucryptolib', 
 'uctypes', 'uerrno', 'uhashlib', 'uheapq', 'uio', 'ujson', 'umqtt/robust', 'umqtt/simple', 'uos', 'upip', 'upip_utarfile', 
 'urandom', 'ure', 'urequests', 'urllib/urequest', 'uselect', 'usocket', 'ussl', 'ustruct', 'utime', 'utimeq', 'uwebsocket',
  'uzlib', 'webrepl', 'websocket', 'websocket_helper', 'writer', 'ymodem', 'zlib']



all = ['_onewire', '_thread', 'ak8963', 'apa102', 'apa106', 'array', 'binascii', 'btree', 'builtins', 'cmath', 'collections', 
        'curl', 'dht', 'display', 'ds18x20', 'errno', 'esp', 'esp32', 'example_pub_button', 'example_sub_led', 'flashbdev', 
        'framebuf', 'freesans20', 'functools', 'gc', 'gsm', 'hashlib', 'heapq', 'http_client', 'http_client_ssl', 'http_server', 
        'http_server_ssl', 'inisetup', 'io', 'json', 'logging', 'lwip', 'm5base', 'm5flow/app_manage', 'm5flow/i2c_bus', 
        'm5flow/m5cloud', 'm5flow/m5mqtt', 'm5flow/m5stack', 'm5flow/peripheral', 'm5flow/unit/ext_io', 'm5flow/unit/ir', 
        'm5flow/unit/ncir', 'm5flow/unit/relay', 'm5flow/unit/rgb_', 'm5flow/unit/tof', 'm5flow/units', 'm5flow/utils', 
        'm5flow/wifichoose', 'm5flow/wificonfig', 'm5flow/wifisetup', 'm5ui', 'machine', 'math', 'microWebSocket', 'microWebSrv', 
        'microWebTemplate', 'micropython', 'mpu6500', 'mpu9250', 'neopixel', 'network', 'ntptime', 'onewire', 'os', 'port_diag', 
        'pye', 'random', 're', 'requests', 'select', 'socket', 'socketupip', 'ssd1306', 'ssh', 'ssl', 'struct', 'sys', 'time', 
        'tpcalib', 'uasyncio/core', 'ubinascii', 'ucollections', 'ucryptolib', 'uctypes', 'uerrno', 'uhashlib', 'uheapq', 'uio', 
        'ujson', 'umqtt/robust', 'umqtt/simple', 'uos', 'upip', 'upip_utarfile', 'upysh', 'urandom', 'ure', 'urequests', 
        'urllib/urequest', 'uselect', 'usocket', 'ussl', 'ustruct', 'utime', 'utimeq', 'uwebsocket', 'uzlib', 'webrepl', 
        'webrepl_setup', 'websocket', 'websocket_helper', 'writer', 'ymodem', 'zlib']
