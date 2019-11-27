
# extract Micropython class information from Micropython C++ source files 
$path = 'C:\develop\MyPython\micropython\ports\esp32'
$path = 'C:\develop\MyPython\micropython\extmod'
#$path = 'C:\develop\MyPython\micropython\ports\stm32\'
$file_mask = '*.c'
#$file_mask = 'network_ppp.c'


$source_path = 'C:\develop\MyPython\micropython\'

$VerbosePreference = "Continue"

#: get version from git-tag 
$current = $pwd     
cd $source_path
$PyVersion = &git describe --abbrev=0 --tags
cd $current

$SourceInformation = @()    #empty array

# get the port and board from the path 
$P0 = ".*[\\|/]micropython[\\|/]ports[\\|/](?<port>\w+)(?:[\\|/]boards[\\|/](?<board>\w+))?.*[\\|/](?<file>\w+)\.\w*"

# regex to try to get the micropython module name for a source file 
$P1 = "\(MP_QSTR___name__\),\s*MP_ROM_QSTR\(\s*MP_QSTR_(?<module>\w*)\s*\)"

# regex to try to map the py_names to the c_names ( still assumes that _obj is added by the author/dev)
$P2 = "MP_ROM_QSTR\(MP_QSTR_(?<py_name>\w*)\), MP_ROM_PTR\(\&(?<c_name>\w+)_\w*\)"

# MP_DEFINE_CONST_FUN_OBJ_KW(machine_i2c_init_obj, 1, machine_i2c_obj_init);
$P4 = "MP_DEFINE_CONST_FUN_OBJ_KW\((?<c_name2>\w+)_\w+\s*,\s*\w+\s*,\s*(?<c_name>\w+)\s*\)"

# regex Patern to try to get the prototype details, relevant comments and parameters  
# ref : https://regexr.com/4ovv8
$P3= "(?:\/\/\s*(?<c_comment>.*\(.*)\n\r*)?"+                                                                        # optional comment with python proto
     "\s*STATIC\s*(?<c_result>\w*)\s*(?<c_function>\w*)\s*(?<c_args>\(.*)\s*{" +                                    # C++ proto 
        "(?:.*\n\r*"+                                                                                               # optional part with parameter details 
            "(?:.*\n)?"+                                                                                            # skip line
            "(?:.*allowed_args.*\n)?"+                                                                              # allowed_args
            "(?<a1>\s*{\sMP_QSTR_(?<a1_name>\w+)\s*,\s*(?<a1_type>[\w| |\|]+)\s*(?:,\s*(?<a1_default>{.*}))?\s*,\n)" +     # arg1 .. 5  
            "(?<a2>\s*{\sMP_QSTR_(?<a2_name>\w+)\s*,\s*(?<a2_type>[\w| |\|]+)\s*(?:,\s*(?<a2_default>{.*}))?\s*,\n)?"+ 
            "(?<a3>\s*{\sMP_QSTR_(?<a3_name>\w+)\s*,\s*(?<a3_type>[\w| |\|]+)\s*(?:,\s*(?<a3_default>{.*}))?\s*,\n)?"+ 
            "(?<a4>\s*{\sMP_QSTR_(?<a4_name>\w+)\s*,\s*(?<a4_type>[\w| |\|]+)\s*(?:,\s*(?<a4_default>{.*}))?\s*,\n)?"+ 
            "(?<a5>\s*{\sMP_QSTR_(?<a5_name>\w+)\s*,\s*(?<a5_type>[\w| |\|]+)\s*(?:,\s*(?<a5_default>{.*}))?\s*,\n)?"+ 
        ")?"                                                                                                        # Section is optional

# get the info for a bunch of files (a port)
$sources = Get-ChildItem -Path $path -Recurse -Filter $file_mask


function GetModuleName{
    param(
        [System.IO.FileInfo]$f
    )
        # get module name 
    # todo: avoid code duplication 
    $ModMatch = Get-Content $f.FullName | Select-String -Pattern $p1
        if ($ModMatch.Matches.Count -ne 0){
        $Modulename = $ModMatch.Matches.Groups[1].Value
        Write-Verbose "Found modulename : $Modulename"
    } else {
        $Modulename = '?'
        try {
            $t = $f.Name.Split('.')[0].Split('_')
            $Modulename = $t[0]
            if($t.Count -GT 1) {
                $Classname = $t[1]
            } else {
                $Classname = $null
            }
            Write-verbose "Guessed modulename : $(Modulename).$classname"
        } catch {
            $Modulename = '?'
        }
    }
    return $Modulename , $classname
}
# first build mapping tables across all files 

function BuildAllMaps{
    param()
    Write-Host -F Blue "Add Mapping tables"

    foreach ($f in $sources){
        BuildMap -f $f
    }
}
function BuildMap{
    param(
        [System.IO.FileInfo]$f  
    )

    $Script:Modulename, $script:Classname = GetModuleName $f

    $ModMatch = Get-Content $f.FullName | Select-String -Pattern $P2
    if ($ModMatch.Matches.Count -ne 0){
        if ($Classname) {
            $prefix = $Classname + '.' 
        } else {
            $prefix = ''
        }
        $ModMatch.Matches | ForEach-Object{ 
            if ($py_name -ne '__del__' ) {
                $c_name = $_.Groups['c_name'].Value.Trim()
                $py_name = $_.Groups['py_name'].Value.Trim()
                if ( -not $script:map_functions.Contains($c_name) ){
                    $script:map_functions.Add( $c_name, $py_name   ) 
                } else {
                    # only warn if there is an actual difference 
                    if ($PY_name -ine  $script:map_functions[$C_name] ){
                        write-host -ForegroundColor DarkMagenta "Duplicate key $C_Name --> $PY_name && $($script:map_functions[$C_name])"
                    }
                }
            }
        }

        # there seems to be a naming pattern class_make_new --> module.class.__init__
        # so lets add that to the lookup 
        if ($Classname) {
            if ( -not  $script:map_functions.Contains( $Classname + "_make_new" ) ) {
                $script:map_functions.Add( $Classname + "_make_new" , $prefix + '__init__')
            }
        }
        # Write-Verbose ( "function map length: {0}" -f $script:map_functions.Count )
        # $script:map_functions | Out-String | Write-Host -F Yellow
    }

    # add another mapping table to resolve indirect function reference 
    $ModMatch = Get-Content $f.FullName | Select-String -Pattern $P4
    if ($ModMatch.Matches.Count -ne 0){
        ## MP_DEFINE_CONST_FUN_OBJ_KW(machine_i2c_init_obj, 1, machine_i2c_obj_init);
        $ModMatch.Matches | ForEach-Object{ 
            $c_name = $_.Groups['c_name'].Value.Trim()
            $c_name2 = $_.Groups['c_name2'].Value.Trim()
            if ( -not $script:map_functions_obj.Contains( $c_name ) ){
                $script:map_functions_obj.Add( $c_name ,  $c_name2  )  
            }
        }
        # Write-Verbose ( "function map2 length: {0}" -f $script:map_functions_obj.Count )
    }
}


# use mapping tables to resolve 
function LookupPyName([string]$c_name){
    if ( $script:map_functions.Contains($c_name)){
        Write-Host -F Green "HIT: $($script:map_functions[$c_name])"
        return $script:map_functions[$c_name] # try lookup 
    } else {
        if ( $script:map_functions_obj.Contains($c_name)){
            Write-Host -F Green "HIT 2: $($script:map_functions[$script:map_functions_obj[$c_name]])"
            return $script:map_functions[$script:map_functions_obj[$c_name]] # try lookup --> lookup
        } 
        # else {
        #     write-warning "function lookup failed for $c_name"
        # }          
    }
    return ""
}

$script:map_functions = @{}
$script:map_functions_obj = @{}
BuildAllMaps $f

foreach ($f in $sources){
    BuildMap $f
    $filename = $f.FullName.Replace('C:\develop\MyPython','.')
    Write-Host -F Blue "Starting on $($f.FullName)"
    # Get port and board 
    if ( $F.FullName -match $p0 ) {
        $PyPort  = $Matches.port
        $PyBoard = $Matches.board 
    } else {
        $Pyport  = $PyBoard = $null
    }
    # get module name 
    $Script:Modulename , $script:Classname = GetModuleName $f
    
    # get function names and build a mapping table
    # the mapping table should help to lookup a C++ function name and relate that to the likely python name
    # module.[class.]method

    # multi-line matching , so get the raw sourcefile 
    $fileContent = Get-Content $f.FullName -Raw
    $AllMatches = $fileContent | Select-String $P3 -AllMatches # try to get the prototype details, relevant comments and parameters 
    
    $FileInformation = $AllMatches.Matches|
        ForEach-Object{ 
            if ($_ -eq $null) {
                Write-Host -F Gray "no relevant signatures found"
            } else  
            {
                $info = [PSCustomObject]@{
                    FileName    = $filename
                    StartChar   = $_.Index
                    port        = $PyPort
                    board       = $PyBoard
                    mp_version  = $PyVersion
                    module      = $Script:Modulename
                    py_class    = $Classname
                    py_proto    = ""
                    c_comment   = $_.Groups['c_comment'].Value
                    C_args      = $_.Groups['c_args'].Value
                    C_function  = $_.Groups['c_function'].Value
                    py_name     = LookupPyName($_.Groups['c_function'].Value) # try lookup 
                    C_result    = $_.Groups['c_result'].Value
                    all         = $_.Value.Replace('\n','').Replace('\r','')
                    params      = @()
                }
                # If a parameter description was found
                if ($_.Groups["a1_name"].Value -ne ""){
                    $params = @()
                    foreach ( $n in (1..5) ){
                        $name = $_.Groups["a$($n)_name"].Value
                        if (-not [string]::IsNullOrEmpty($name)){
                            try {
                                $default = $_.Groups["a$($n)_default"].Value.Replace('{','').Replace('}','').Split('=')[1].Trim()
                            } catch {
                                $default = ""
                            }
        
                            $params = $params + [PSCustomObject]@{
                                name = $name
                                type = $_.Groups["a$($n)_type"].Value
                                default = $default
                            }
                        }
                    }
                    $info.params = $params
                }
                Write-Output $info
            } 
        } 
    
    # $FileInformation | ft module, class,py_name,  py_proto,c_function , c_args,  params | Out-Host
    $SourceInformation = $SourceInformation + $FileInformation
}

# 

# filter to just the functions that are recognised as python 
# $SourceInformation = $SourceInformation.Where({$_.py_name -ne $null  } )

$SourceInformation | FT module, class, py_name, py_proto , c_function, c_comment, params


Write-Host '------------------------------------------------------------------' -f yellow
Write-Host '- Build python prototypes                                        -' -f yellow
Write-Host '------------------------------------------------------------------' -f yellow
# $SourceInformation = $SourceInformation.Where({$_.params -ne $null  } )

$func = $SourceInformation[3]

# todo: Add more types 
$script:map_types = @{
        MP_ARG_INT = 'int' ;
        MP_OBJ_NEW_SMALL_INT = 'int';
}

# todo: Add more defaults  
$script:map_defaults = @{
    mp_const_none = 'None' ;
    MP_OBJ_NULL = 'None';
    'MP_ROM_PTR(&mp_const_none_obj)' =  'None';
    UART_PIN_NO_CHANGE = "UART.PIN.NO_CHANGE" ; 
    'machine_rtc_config.ext1_level' = "machine.rtc.config.ext1_level" ; 
    'MP_OBJ_NEW_SMALL_INT(-1)' = '-1'
}

function HasNoInfo([string]$proto){
    # determine wether or not a c+= function signature has relevant information that can be used for python
    if ($proto -eq ""){
        return $true
    }
    # # Match (size_t n_args, const mp_obj_t *args)
    # $proto -match "\(\s*\w*_t\s+n_args,\s+const\s+mp_obj_t\s+\*args\s*\)"  
    # # match (mp_uint_t n_args, const mp_obj_t *args, mp_map_t *kw_args)"
    # $proto -match "(.*mp_uint_t n_args, const mp_obj_t \*args, mp_map_t \*kw_args.*)" 
    return ($proto -match "\(\s*\w*_t\s+n_args,\s+const\s+mp_obj_t\s+\*args\s*\)"   -or 
            $proto -match "\(\s*size_t\s+n_args\s*,.*\)" -or 
            $proto -match "(mp_uint_t n_args, const mp_obj_t \*args, mp_map_t \*kw_args.*)" ) 
}


# ??         Write-Verbose '  - use comment'

##
foreach( $func in $SourceInformation){
    # 1) use prototype form source comments 
    # 2) build protottyoe from param definition 
    Write-Verbose ('- function : {0}' -f $func.C_function)
    
    $proto=$null
    if( (     ($func.params -ne "" ) -and  ( HasNoInfo($func.C_args) ) ) )  { 
        # A Python parameter definition was found , use that to build a prototype 
        Write-Verbose '  - build py_proto from Py typed C++ params '
        $strParam=""
        foreach ($p in $func.params){
            # start with param name 
            $py_param = $p.name
            #add a type if we know it 
            if ($p.type){
                if ( $script:map_types.Contains($p.type) ){
                    $py_param += ":" + $script:map_types[$p.type]
                }
            }
            # and add a default 
            if ($p.default){
                if ($script:map_defaults.Contains($P.default)) {
                    # map C -> py
                    $py_param += " = " + $script:map_defaults[$p.default]
                } else {
                    # TODO: add logic to reduce lookup table
                    $py_param += " = " + $p.default
                }
            }
            Write-Verbose ('    - ' + $py_param )
            $strParam = $strParam + $py_param + ", "
        } 
        Write-Host $strParam
        $strParam = $strParam.Trim(' ',',')


        $proto = "{0}({1})" -f $func.py_name , $strParam
    
    } 
    elseif ($func.py_proto -eq "" -and $func.py_name -ne "") {
        # 3) build based on C++ function prototype 
        Write-Verbose '  - build py_proto from c_function name '        
        # Not py_proto found, but apparently a py relvant function 
        #  now construct based on C++ function signature 
        # pyname( c_args ) 

        # todo: add module/class name ?

        if( HasNoInfo($func.C_args)) {
            Write-Verbose '    - no parameters found in source' 
            $proto = "{0}()" -f $func.py_name 

            # ToDo: args are a required / variable; how to map this to a python prototype : *args[] ?
        } else {
            $proto = "{0}{1}" -f $func.py_name , $func.C_args

            # remove class instance parameter "mp_obj_t self_in"
            $proto = $proto -replace "mp_obj_t\sself_in\s*,?",""

            # handle micropython parameter types 
            Write-Verbose '    - cleanup parameters found in source' 
            # mp_obj_t - remove , but keep parameter name 
            # 'partition.ioctl( mp_obj_t cmd_in, mp_obj_t arg_in)' -replace '\s?mp_obj_t(\s\w+)\s*','$1'
            $proto = $proto -replace '\s?mp_obj_t(\s\w+)\s*','$1'

            #remove void 
            $proto = $proto -replace "void",""
            #remove const param --> param
            $proto = $proto -replace "const\s+(\w+)",'$1'
        }
        
    } 
    else {
        # now most should be good or blank 
        if ($func.c_comment.length -gt 0){
            Write-Verbose '  - use comment'
            $proto = $func.c_comment
        }
        
    }
    if ($proto ){
        $func.py_proto = $proto        
        Write-Host  -f Green ('  > py prototype : {0}' -f $func.py_proto )
    }
}

$SourceInformation | FT module,py_class, py_name, py_proto , c_function, c_comment, params

Write-Host "save "
$filename = "Sourceinfo MP{2}_{1}_{0}" -f $PyVersion, $PyPort, $PyBoard
$SourceInformation | ConvertTo-Json | Out-File $filename


$sou