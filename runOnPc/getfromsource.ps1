
# extact class  information from Micropython source files 

$path = 'C:\develop\MyPython\micropython\ports\esp32'

$filename = "C:\develop\MyPython\micropython\ports\esp32\machine_pin.c"

#ref : https://regexr.com/4ovv8
# (?smi) --> mULTIPLINE MATCH

# regex Patern to also get the prototype details 
$P2= "(?:\/\/\s*(?<py_proto>.*\(.*)\n\r*)?"+                                                                        # optional comment with python proto
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

$regexPattern = $p2
$fileContent = Get-Content $filename -Raw

$AllMatches = $fileContent | Select-String $regexPattern -AllMatches 

$SourceInformation = $AllMatches.Matches|
    ForEach-Object{ 
        write-host '---------------'  
        write-host -f green $_.Groups[1]
        $info = [PSCustomObject]@{
            FileName    = $filename
            StartChar   = $_.Index
            py_proto    = $_.Groups['py_proto']
            C_args      = $_.Groups['c_args']
            C_function  = $_.Groups['c_function']
            C_result    = $_.Groups['c_result']
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

$SourceInformation | ft c_function , py_proto, c_args,  params