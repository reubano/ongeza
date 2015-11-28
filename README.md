bump
=======

manage your versioning like a boss

* bump is an opinionated command-line app to manage versioning workflow + dist + releasing
* bump makes following the [semantic versioning specification](http://semver.org) a breeze
* bump helps to automate the tedious task of summarizing changes from one version to the next by intelligently parsing the commit messages


<br>
**build-status:**

`master  ` [![travis-ci build-status: master](https://secure.travis-ci.org/gregorynicholas/bump.svg?branch=master)](https://travis-ci.org/gregorynicholas/bump)
<br>
`develop ` [![travis-ci build-status: develop](https://secure.travis-ci.org/gregorynicholas/bump.svg?branch=develop)](https://travis-ci.org/gregorynicholas/bump)


**links:**

- [homepage](http://gregorynicholas.github.io/bump)
- [source](http://github.com/gregorynicholas/bump)
- [python-package](http://packages.python.org/bump)
- [changelog](https://github.com/gregorynicholas/bump/blob/master/CHANGES.md)
- [github-issues](http://github.com/gregorynicholas/bump/issues)
- [travis-ci](http://travis-ci.org/gregorynicholas/bump)
- [semantic versioning specification](http://semver.org)


<br>
-----
<br>


### introduction


development + testing done on the following configuration:

* macosx *10.7.6*
* python *2.7.4*


-----


### requirements

bump requires the following in order to run properly:

* [python >= *2.5*](http://python.org)
* [git >= *1.8*](http://git-scm.org)


check that the correct version of git + python are installed

    $ python --version
    $ git --version


<br>
-----
<br>


### installation

install bump with pip

    $ pip install bump==3.0.1


<br>
-----
<br>


### usage

    $ bump [options]

options:

    --bump                  version bump type to increment. must be  one of:
                              major [x].x.x     minor x.[x].x     patch x.x.[x]
    --skip-interactive      skips the script from using the interactive command line interface
    --skip-commit           skips commiting any changes to the changelog file
    --skip-tag              skips creating a git tag at the current HEAD
    --skip-push             skips pushing to the remote origin
    --pypi-dist             build the release and upload to the python package index
    --changelog-file        path to a changelog history file
    --changelog-fmt         string format of the changelog version summary
    --git-commit-fmt        string format of the git commit message
    --git-tag-fmt           string format of the git tag


if called with no options, bump will print the script's current git tag
version.


#### examples

normal usage

    $ bump --bump patch

if called with no options, bump will print the script's current
project's information:

    $ bump


-----


### github-flavored-markdown notes


#### mentions

use a /cc convention to call out people:
[screenshot](https://a248.e.akamai.net/camo.github.com/37adea151a070a7f64794c8b02f3a2a072c9a1db/687474703a2f2f692e696d6775722e636f6d2f71634e50512e706e67)

#### auto-linking

certain [references are auto-linked](https://help.github.com/articles/github-flavored-markdown#references):

* `SHA`              : 16c999e8c71134401a78d4d46435517b2271d6ac
* `User@SHA` ref     : mojombo@16c999e8c71134401a78d4d46435517b2271d6ac
* `User/Project@SHA` : mojombo/github-flavored-markdown@16c999e8...
* `#Num`             : #1
* `User/#Num`        : mojombo#1
* `User/Project#Num` : mojombo/github-flavored-markdown#1


#### task lists

lists can be turned into Task Lists by prefacing list items with:

* `[ ]  complete`
* `[x]  incomplete`


#### referencing github issues

you can use any of the following keywords to close an issue via commit message:

* `close`
* `closes`
* `closed`
* `fix`
* `fixes`
* `fixed`
* `resolve`
* `resolves`
* `resolved`


note:
referencing an issue number within the pull request title won't close it, the
reference must be in a commit message, or the pull request body


-----

### limitations

* no built-in support for pre-release or build numbers
  - 1.0.0-alpha, 1.0.0-alpha.1, 1.0.0-0.3.7, 1.0.0-x.7.z.92
  - 1.0.0+build.1, 1.3.7+build.11.e0f985a
* doesn't check validity of user set versions


-----


### license

bump is distributed under the [MIT License](http://opensource.org/licenses/mit-license.php)
