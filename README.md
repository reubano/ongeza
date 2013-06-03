keybump
=======


### introduction

keybump makes following the [semantic versioning specification](http://semver.org/)
a breeze. if called with no options, keybump will print the script's current
git tag version.

it has been tested on the following configuration:

* macosx *10.7.6*
* python *2.7.1*


-----


### requirements

keybump requires the following in order to run properly:

* [python >= *2.5*](http://python.org)
* [git >= *1.8*](http://git-scm.org)


-----


### preparation

check that the correct version of git + python are installed

    $ python --version
    $ git --version

-----


### installation

install keybump with pip (recommended to lock in the version)

    $ pip install keybump==3.0.0

-----

### usage

    $ keybump [options]

options:

    --bump                  version bump type to increment. must be  one of:
                              major [x].x.x     minor x.[x].x     patch x.x.[x]
    --skip-interactive      skips the script from using the interactive command line interface
    --skip-commit           skips commiting any changes to the changelog file
    --skip-tag              skips creating a git tag at the current HEAD
    --skip-push             skips pushing to the remote origin
    --pypi_distribute       build the release and upload to the python package index
    --changelog-file        path to a changelog history file
    --changelog-fmt         string format of the changelog version summary
    --git-commit-fmt        string format of the git commit message
    --git-tag-fmt           string format of the git tag


#### examples

*normal usage*

    $ keybump --bump patch

*view current project version*

    $ keybump


-----


### limitations

* no built-in support for pre-release or build numbers
  - 1.0.0-alpha, 1.0.0-alpha.1, 1.0.0-0.3.7, 1.0.0-x.7.z.92
  - 1.0.0+build.1, 1.3.7+build.11.e0f985a
* doesn't check validity of user set versions


-----


### license

keybump is distributed under the [MIT License](http://opensource.org/licenses/mit-license.php)
