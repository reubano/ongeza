bump: your semantic versioning personal assistant
=================================================
|travis| |versions| |pypi|

Introduction
------------

bump is a Python command line application_ (CLI) that makes following the
`Semantic Versioning Specification`_ a breeze. If called with no options, bump
will print the repo's current git tag version. With bump, you can

- Quickly bump to a ``patch``, ``minor``, or ``major`` version
- Stash uncommitted changes before bumping
- Create a git tag with the new version number
- Bump python, php, and javascript projects
- and much more...

Requirements
------------

bump has been tested and is known to work on the following `Python versions`_:

- 2.7
- 3.4
- 3.5
- pypy v4.0
- pypy3 v2.4

Motivation
----------

I think we can all agree that Semantic Versioning is awesome sauce. But while
coding, who has time to constantly look up the current version and figure out
the new version? I created bump to relieve myself from this pain of having to
worry about version numbers. For example, to bump to a ``minor`` version
inside a python ``git`` repo, simply type ``bump -Ttn``.

As long as the repo contains a git tag with the current version, bump will
automagically:

- calculate the new version number
- figure out which file(s) to update with the new version number
- make the appropriate updates and commit the changes
- create a git tag with the new version number

.. _application:

Usage
-----

bump is intended to be used from the command line.

.. code-block:: bash

	bump [options] <dir>

Basic Examples
~~~~~~~~~~~~~~

*show help*

.. code-block:: bash

    bump -h

.. code-block:: bash

	usage: bump [options] <dir>

	description: bump makes following the Semantic Versioning Specification a breeze.
	If called with no options, bump will print the current git repository's tag version.
	If <dir> is not specified, the current dir is used.

	positional arguments:
	  dir                   the project directory (default: /Users/reubano/Documents/Projects/bump).


	optional arguments:
	  -h, --help            show this help message and exit
	  -t {m,n,p}, --type {m,n,p}
	                        version bump type, must be one of:
	                          m = major - [x].0.0
	                          n = minor - x.[y].0
	                          p = patch - x.y.[z]
	  -s NEW_VERSION, --set NEW_VERSION
	                        set arbitrary version number
	  -S, --skip-commit     skip committing version bumped files
	  -T, --tag             create git tag at HEAD with the bumped version number
	  -p, --push            push to the remote origin
	  -a, --stash           stash uncommitted changes
	  -f TAG_FORMAT, --tag-format TAG_FORMAT
	                        git tag format
	  -F TAG_MSG_FORMAT, --tag-msg-format TAG_MSG_FORMAT
	                        git tag message format
	  -c COMMIT_MSG_FORMAT, --commit-msg-format COMMIT_MSG_FORMAT
	                        git commit message format
	  -i FILE, --file FILE  the versioned file
	  -v, --version         Show version and exit.
	  -V, --verbose         increase output verbosity

*view current version*

.. code-block:: bash

	bump

*bump to a ``minor`` version*

.. code-block:: bash

	bump -tn

*manually set a version*

.. code-block:: bash

	bump -s 1.0.2

*bump to a ``major`` version and add a git tag*

.. code-block:: bash

	bump -Ttm

*stash uncommitted changes and bump to a ``patch`` version*

.. code-block:: bash

	bump -atp

Advanced Examples
~~~~~~~~~~~~~~~~~

*bump ``weird.file`` to a ``minor`` version and use custom formats*

.. code-block:: bash

	bump -tn --file='weird.file' --tag-format='{version}' --commit-msg-format='New version: {version}'

*bump a remote directory to a ``minor`` version and use a custom tag message format*

.. code-block:: bash

	bump -tn --tag-msg-format='Release: {version}' /path/to/remote/dir

Installation
------------

(You are using a `virtualenv`_, right?)

At the command line, install bump using either ``pip`` (*recommended*)

.. code-block:: bash

    pip install bump

or ``easy_install``

.. code-block:: bash

    easy_install bump

Please see the `installation doc`_ for more details.

Project structure
-----------------

.. code-block:: bash

    ┌── CHANGES.rst
    ├── CONTRIBUTING.rst
    ├── INSTALLATION.rst
    ├── LICENSE
    ├── MANIFEST.in
    ├── Makefile
    ├── README.rst
    ├── bin
    │   └── bump
    ├── bump
    │   ├── __init__.py
    │   ├── git_utils.py
    │   ├── main.py
    │   └── shell_utils.py
    ├── dev-requirements.txt
    ├── helpers
    │   ├── check-stage
    │   ├── clean
    │   ├── docs
    │   ├── pippy
    │   ├── srcdist
    │   └── wheel
    ├── manage.py
    ├── requirements.txt
    ├── setup.cfg
    ├── setup.py
    ├── tests
    │   ├── __init__.py
    │   ├── standard.rc
    │   ├── test.py
    │   └── test_bump.py
    └── tox.ini

Design Principles
-----------------

- KISS: Keep it simple, stupid
- Do one thing (version bumping), and do it well
- Support the most common file types used for project versioning, e.g.,
  ``__init__.py``, ``package.json``, etc.

Limitations
-----------

* no built-in support for pre-release or build numbers, e.g.,
  - 1.0.0-alpha, 1.0.0-alpha.1, 1.0.0-0.3.7, 1.0.0-x.7.z.92
  - 1.0.0+build.1, 1.3.7+build.11.e0f985a

Scripts
-------

bump comes with a built in task manager ``manage.py``

Setup
~~~~~

.. code-block:: bash

    pip install -r dev-requirements.txt

Examples
~~~~~~~~

*Run python linter and nose tests*

.. code-block:: bash

    manage lint
    manage test

License
-------

bump is distributed under the `MIT License`_.

.. _MIT License: http://opensource.org/licenses/MIT
.. _Python versions: http://www.python.org/download
.. _virtualenv: http://www.virtualenv.org/en/latest/index.html
.. _contributing doc: https://github.com/reubano/bump/blob/master/CONTRIBUTING.rst

Contributing
------------

Please mimic the coding style/conventions used in this repo.
If you add new classes or functions, please add the appropriate doc blocks with
examples. Also, make sure the python linter and nose tests pass.

Please see the `contributing doc`_ for more details.

.. |travis| image:: https://img.shields.io/travis/reubano/bump/master.svg
    :target: https://travis-ci.org/reubano/bump

.. |versions| image:: https://img.shields.io/pypi/pyversions/bump.svg
    :target: https://pypi.python.org/pypi/bump

.. |pypi| image:: https://img.shields.io/pypi/v/bump.svg
    :target: https://pypi.python.org/pypi/bump

.. _MIT License: http://opensource.org/licenses/MIT
.. _Semantic Versioning Specification: http://semver.org/
.. _virtualenv: http://www.virtualenv.org/en/latest/index.html
.. _Python versions: http://www.python.org/download
.. _contributing doc: https://github.com/reubano/bump/blob/master/CONTRIBUTING.rst
.. _installation doc: https://github.com/reubano/bump/blob/master/INSTALLATION.rst
