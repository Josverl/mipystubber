
# extact class  information from Micropython source files 

#$path = 'C:\develop\MyPython\micropython\ports\esp32'
$path = 'C:\develop\MyPython\micropython\ports\stm32\'

#: get version from git-tag 
$current = $pwd     
cd 'C:\develop\MyPython\micropython\'
$MP_version = &git describe --abbrev=0 --tags
cd $current


# get the port and board from the path 
$P0 = ".*[\\|/]micropython[\\|/]ports[\\|/](?<port>\w+)(?:[\\|/]boards[\\|/](?<board>\w+))?.*[\\|/](?<file>\w+)\.\w*"
# regex to try to get the micropython module name for a source file 
$P1 = "\(MP_QSTR___name__\),\s*MP_ROM_QSTR\(\s*MP_QSTR_(?<module>\w*)\s*\)"
# regex to try to map the py_names to the c_names ( still assumes that _obj is added by the author/dev)
$P2 = "MP_ROM_QSTR\(MP_QSTR_(?<py_name>\w*)\), MP_ROM_PTR\(\&(?<c_name>\w*)_obj\)"
# regex Patern to try to get the prototype details, relevant comments and parameters  
# ref : https://regexr.com/4ovv8
$P3= "(?:\/\/\s*(?<py_proto>.*\(.*)\n\r*)?"+                                                                        # optional comment with python proto
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
$sources = Get-ChildItem -Path $path -Recurse -Filter "*.c"

foreach ($f in $sources){
    $filename = $f.FullName.Replace('C:\develop\MyPython','.')
    Write-Host -F Blue "Starting on $($f.FullName)"
    # Get port and board 
    if ( $F.FullName -match $p0 ) {
        $port  = $Matches.port
        $Board = $Matches.board 
    } else {
        $port  = $Board = $null
    }

    # get module name 
    $ModMatch = Get-Content $f.FullName | Select-String -Pattern $p1
        if ($ModMatch.Matches.Count -ne 0){
        $ModuleName = $ModMatch.Matches.Groups[1].Value
        Write-Host -f Green "Found modulename : $ModuleName"
    } else {
        $ModuleName = '?'
        try {
            $t = $f.Name.Split('.')[0].Split('_')
            $ModuleName = $t[0]
            if($t.Count -GT 1) {
                $Classname = $t[1]
            } else {
                $Classname = $null
            }
            Write-Host -f Yellow "Guessed modulename : $($ModuleName).$classname"
        } catch {
            $ModuleName = '?'
        }
    }
    
    #get function names 
    $fn_names = @{}
    $ModMatch = Get-Content $f.FullName | Select-String -Pattern $p2
    if ($ModMatch.Matches.Count -ne 0){
        $prefix = $ModuleName + '.' 
        if ($Classname) {
            $prefix = $prefix + $Classname + '.' 
        }
        $ModMatch.Matches | ForEach-Object{ 
            if ( -not $fn_names.Contains($_.Groups['c_name'].Value.Trim() ) ) {
                $fn_names.Add( $_.Groups['c_name'].Value.Trim() , ($prefix+ $_.Groups['py_name'].Value).Trim()   )  }
        }
        # $fn_names | Out-String | Write-Host -F Yellow
    }

    
    # multi-line matching , so get the raw sourcefile 
    $fileContent = Get-Content $f.FullName -Raw
    $AllMatches = $fileContent | Select-String $P3 -AllMatches # try to get the prototype details, relevant comments and parameters 
    
    $SourceInformation = $AllMatches.Matches|
        ForEach-Object{ 
            if ($_ -eq $null) {
                Write-Host -F Gray "no relevant signatures found"
            } else  
            {
                $x = $fn_names[$_.Groups['c_function'].Value] 
                $info = [PSCustomObject]@{
                    FileName    = $filename
                    StartChar   = $_.Index
                    port        = $port--?
                    board       = $Board
                    module      = $ModuleName
                    class       = $Classname
                    py_proto    = $_.Groups['py_proto'].Value
                    C_args      = $_.Groups['c_args'].Value
                    C_function  = $_.Groups['c_function'].Value
                    py_name     = $fn_names[$_.Groups['c_function'].Value] # try lookup 
                    C_result    = $_.Groups['c_result'].Value
                    all         = $_.Value
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
    
    $SourceInformation | ft module, class,py_name,  py_proto,c_function , c_args,  params | Out-Host

}
