#%% Markdown
# ## create an overview  of modules across different firmwares 

#%% load known modules

lobo_esp32 = [ ##Loboris
            '_thread', 'ak8963', 'array', 'binascii', 'btree', 'builtins',
            'cmath', 'collections', 'curl', 'display', 'errno', 'framebuf',
            'freesans20', 'functools', 'gc', 'gsm', 'hashlib', 'heapq', 'io',
            'json', 'logging', 'machine', 'math', 'microWebSocket', 'microWebSrv',
            'microWebTemplate', 'micropython', 'mpu6500', 'mpu9250', 'network', 'os',
            'pye', 'random', 're', 'requests', 'select', 'socket', 'ssd1306', 'ssh',
            'ssl', 'struct', 'sys', 'time', 'tpcalib', 'ubinascii', 'ucollections',
            'uctypes', 'uerrno', 'uhashlib', 'uheapq', 'uio', 'ujson', 'uos', 'upip',
            'upip_utarfile', 'upysh', 'urandom', 'ure', 'urequests', 'uselect', 'usocket',
            'ussl', 'ustruct', 'utime', 'utimeq', 'uzlib', 'websocket', 'writer', 'ymodem', 'zlib']

mpy_esp32 = [ #standard ESP32 micropython        
        'framebuf',          'socket'            'upip',
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
        ]

#(sysname='esp8266', nodename='esp8266', release='2.2.0-dev(9422289)', version='v1.11-8-g48dcbbe60 on 2019-05-29', machine='ESP module with ESP8266')
mpy_esp8622 = [
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
        ]

print( "mpy  esp8622:", len(mpy_esp8622))
print( "mpy  esp32  :", len(mpy_esp32) ) 
print( "lobo esp32  :", len(lobo_esp32 )) 

#%% calculate diffs 

shared_esp32 = set(mpy_esp32) & set(lobo_esp32) 
print( "Shared esp32 modules :", len(shared_esp32 )) 

mpy_only = set(mpy_esp32) - set(lobo_esp32) 
print( "mpy 32 only modules :", len(mpy_only)) 

lobo_esp32_only = set(lobo_esp32) - set(mpy_esp32) 
print( "lobo_esp32 only modules :", len(lobo_esp32_only)) 

print( "mpy  modules :", len(mpy_esp32 ),  "=", len(mpy_only)+ len(shared_esp32)) 
print( "lobo_esp32 modules :", len(lobo_esp32 ), "=", len(lobo_esp32_only)+ len(shared_esp32)) 

print("\nshared_esp32 = ",end='')
print (sorted(shared_esp32))

print("\nmpy_only = ",end='')
print (sorted(mpy_only))

print("\nlobo_esp32_only = ",end='')
print (sorted(lobo_esp32_only))

#%% Which are shared between mpy esp32 / esp8622 

shared_mpyEspXX = set(mpy_esp8622) & set(mpy_esp32) 
print( "Shared mpy espxxx modules :", len(shared_mpyEspXX )) 

print("\nall = ",end='')
print (sorted(set(mpy_esp32) | set(lobo_esp32) | set(mpy_esp8622)))


#%%  result is : 

shared = ['_thread', 'array', 'binascii', 'btree', 'builtins', 'cmath', 'collections', 'errno', 'framebuf', 
            'gc', 'hashlib', 'heapq', 'io', 'json', 'machine', 'math', 'micropython', 'network', 'os', 'random', 
            're', 'select', 'ssl', 'struct', 'sys', 'time', 'ubinascii', 'ucollections', 'uctypes', 'uerrno', 
            'uhashlib', 'uheapq', 'uio', 'ujson', 'uos', 'upip_utarfile', 'upysh', 'urandom', 'ure', 'urequests', 
            'uselect', 'usocket', 'ussl', 'ustruct', 'utime', 'utimeq', 'uzlib', 'zlib']

mpy_only = ['_boot', '_onewire', '_webrepl', 'apa106', 'dht', 'ds18x20', 'esp', 'esp32', 'flashbdev', 'inisetup', 
            'neopixel', 'ntptime', 'onewire', 'socketupip', 'ucryptolib', 'umqtt/robust', 'umqtt/simple', 'uwebsocket', 
            'webrepl', 'webrepl_setup', 'websocket_helper']

lobo_esp32_only = ['ak8963', 'curl', 'display', 'freesans20', 'functools', 'gsm', 'logging', 'microWebSocket', 'microWebSrv', 
            'microWebTemplate', 'mpu6500', 'mpu9250', 'pye', 'requests', 'socket', 'ssd1306', 'ssh', 'tpcalib', 'upip', 
            'websocket', 'writer', 'ymodem']

all = [ '_boot', '_onewire', '_thread', '_webrepl', 'ak8963', 'apa102', 'apa106', 'array', 'binascii', 'btree', 'builtins', 'upip',
        'cmath', 'collections', 'curl', 'dht', 'display', 'ds18x20', 'errno', 'esp', 'esp32', 'example_pub_button', 'example_sub_led', 
        'flashbdev', 'framebuf', 'freesans20', 'functools', 'gc', 'gsm', 'hashlib', 'heapq', 'http_client', 'http_client_ssl', 'http_server', 
        'http_server_ssl', 'inisetup', 'io', 'json', 'logging', 'lwip', 'machine', 'math', 'microWebSocket', 'microWebSrv', 'microWebTemplate', 
        'micropython', 'mpu6500', 'mpu9250', 'neopixel', 'network', 'ntptime', 'onewire', 'os', 'port_diag', 'pye', 'random', 're', 'requests', 
        'select', 'socket', 'socketupip', 'ssd1306', 'ssh', 'ssl', 'struct', 'sys', 'time', 'tpcalib', 'uasyncio/__init__', 'uasyncio/core', 'ubinascii', 
        'ucollections', 'ucryptolib', 'uctypes', 'uerrno', 'uhashlib', 'uheapq', 'uio', 'ujson', 'umqtt/robust', 'umqtt/simple', 'uos',  'upip_utarfile', 
        'upysh', 'urandom', 'ure', 'urequests', 'urllib/urequest', 'uselect', 'usocket', 'ussl', 'ustruct', 'utime', 'utimeq', 'uwebsocket', 'uzlib', 'webrepl', 
        'webrepl_setup', 'websocket', 'websocket_helper', 'writer', 'ymodem', 'zlib']


# Adjust order 
# [m for m in all if '/' in m] + [m for m in all if '/' not in m]
# todo: Move upip earlier 
# todo: 




#%%
