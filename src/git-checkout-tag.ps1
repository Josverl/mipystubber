# get 
# simple in powershell, too complex in python 
param(
    $repo = ".",
    $tag 
)
$current = $PWD
try {
    cd $repo
    $result = (&git checkout tags/$tag ---quiet --force) 
    cd $current
    return $true
} catch {
    cd $current
    return $false
} 
