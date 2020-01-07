# get 
# simple in powershell, too complex in python 
param(
    $repo = ".",
    $tag 
)
$current = $PWD
try {
    cd $repo
    $result = (&git checkout tags/$tag) 
    cd $current
    return $true
} catch {
    cd $current
    return $false
} 
