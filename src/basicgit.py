"simple Git module, where needed via powershell "
import subprocess
import os


def scriptpath(script: str):
    try:
        _scriptpath = os.path.dirname(os.path.realpath(__file__))
    except:
        _scriptpath = "./src"
    return os.path.join(_scriptpath, script)

def get_tag(repo: str = None) -> str:
    """
    get the most recent git version tag of a local repo"
    repo should be in the form of : path/.git
        ../micropython/.git
    returns the tag or None
    """
    if not repo:
        repo = './.git'
    elif not repo.endswith('.git'):
        repo += '/.git'

    cmd = ['git', '--git-dir='+ repo, 'describe']
    try:
        result = subprocess.run(cmd, capture_output=True, check=True)
        if result.stderr != b'':
            print(result.stderr.decode("utf-8"))
            raise Exception(result.stderr.decode("utf-8"))
        tag: str = result.stdout.decode("utf-8")
        tag = tag.replace('\r', '').replace('\n', '')
        return tag
    except  subprocess.CalledProcessError as e:
        print("Error: ", e.returncode, e.stderr)
        raise Exception(e.stderr)



def checkout_tag(tag: str, repo: str = None) -> bool:
    """
    get the most recent git version tag of a local repo"
    repo should be in the form of : path/.git
        ../micropython/.git
    returns the tag or None
    """
    if not repo:
        repo = '.'
    elif repo.endswith('.git'):
        repo = os.path.basename(repo)

    cmd = ["pwsh", scriptpath('git-checkout-tag.ps1'), '-repo', repo,'-tag' , tag]
    try:
        result = subprocess.run(cmd, capture_output=True, check=True)
        if result.returncode >= 0:
            # actually a good result
            print(result.stderr.decode("utf-8"))
            return True
        else: 
            raise Exception(result.stderr.decode("utf-8"))

    except  subprocess.CalledProcessError as e:
        print(e)
        return False


    # todo: retry withouth powershell
    # cmd = ['git', 'checkout', 'tags/'+ tag]
    # try:
    #     result = subprocess.run(cmd, capture_output=True, check=True, cwd='../micropython')
    #     if result.stderr != b'':
    #         print(result.stderr.decode("utf-8"))        # todo: raise error 
    #         return False
    #     print(result.stdout)
    #     return True
    # except  subprocess.CalledProcessError as e:
    #     print("Error: ", e.returncode, e.stderr)        # todo: raise error 
    #     return False
