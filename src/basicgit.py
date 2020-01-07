"simple Git module"
import subprocess
import os

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
            print(result.stderr.decode("utf-8"))        # todo: raise error 
            return None
        tag:str = result.stdout.decode("utf-8")
        tag = tag.replace('\r', '').replace('\n', '')
        return tag
    except  subprocess.CalledProcessError as e:
        print("Error: ", e.returncode, e.stderr)        # todo: raise error 
        return None


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

    cmd = ['git', 'checkout', 'tags/'+ tag]
    try:
        result = subprocess.run(cmd, capture_output=True, check=True, cwd='../micropython')
        if result.stderr != b'':
            print(result.stderr.decode("utf-8"))        # todo: raise error 
            return False
        print(result.stdout)
        return True
    except  subprocess.CalledProcessError as e:
        print("Error: ", e.returncode, e.stderr)        # todo: raise error 
        return False


# # get_gittag.ps1 
# def get_tag_ps1(repo: str = None) -> str:
#     """
#     get the most recent git version tag of a local repo"
#     repo should be in the form of : path/.git
#         ../micropython/.git
#     returns the tag or None
#     """
#     if not repo:
#         repo = './.git'
#     elif not repo.endswith('.git'):
#         repo += '/.git'

#     try:
#         scriptpath = os.path.dirname(os.path.realpath(__file__))
#     except:
#         scriptpath = "./src"
#     scriptpath = os.path.join(scriptpath, "get-gittag.ps1")

#     cmd = ["pwsh", scriptpath, repo]
#     try:
#         result = subprocess.run(cmd, capture_output=True, check=True)
#         if result.stderr != b'':
#             print(result.stderr.decode("utf-8"))
#             return None
#         tag:str = result.stdout.decode("utf-8")
#         tag = tag.replace('\r', '').replace('\n', '')
#         return tag

#     except OSError as e:
#         print(e)
#         return None

def test():
    # very simple test 
    print( get_tag() ) 
    print( get_tag('.') ) 
    print( get_tag('../micropython') ) 


    x = get_tag('../micropython')    
    checkout_tag('v1.11', repo= '../micropython')
    print( get_tag('../micropython') ) 
    checkout_tag(x, repo= '../micropython')
    print( get_tag('../micropython') ) 


    # the below should fail
    print( get_tag('../micropyt') ) 
    print( get_tag('./git') ) 

if __name__ == "__main__":
    test()
    