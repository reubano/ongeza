ongeza: your project versioning personal assistant
==================================================
|travis| |versions| |pypi|

.. image:: https://raw.githubusercontent.com/reubano/ongeza/master/ongeza.png
    :alt: sample ongeza usage
    :width: 800
    :align: center

Index
-----
`Introduction`_ | `Requirements`_ | `Motivation`_ | `Usage`_ | `Installation`_ |
`Project Structure`_ | `Design Principles`_ | `Limitations`_ | `Scripts`_ |
`Contributing`_ | `License`_

Introduction
------------

ongeza (Swahili for "increase") is a Python `command line application <#usage>`_ (CLI)
that makes following the `Semantic Versioning Specification`_ a breeze.
If called with no options, ``ongeza`` will print the repo's current git tag
version. With ongeza, you can

- Quickly bump to a ``patch``, ``minor``, or ``major`` version
- Stash uncommitted changes before bumping
- Create a git tag with the new version number
- Bump python, php, and javascript projects
- and much more...

Requirements
------------

ongeza has been tested and is known to work on Python 2.7, 3.4, and 3.5;
and PyPy 4.0

Motivation
----------

I think we can all agree that `semver`_ is awesome sauce. But while
coding, who has time to constantly look up the current version and figure out
the new version? I created ongeza to relieve myself from this pain of having to
worry about version numbers. For example, to bump to a ``minor`` version
inside a python ``git`` repo, simply type:

.. code-block:: bash

    ongeza --type=minor

Or via the short option style:

.. code-block:: bash

    ongeza -tn

As long as the repo contains a git tag with the current version, ongeza will
automagically:

- calculate the new version number
- figure out which file(s) to update with the new version number
- make the appropriate updates and commit the changes
- create a git tag with the new version number

Usage
-----

ongeza is intended to be used from the command line.

.. code-block:: bash

	ongeza [options] <dir>

Basic Examples
~~~~~~~~~~~~~~

*show help*

.. code-block:: bash

    ongeza -h

.. code-block:: bash

	usage: ongeza [options] <dir>

	description: ongeza makes following the Semantic Versioning Specification a breeze.
	If called with no options, ongeza will print the current git repository's tag version.
	If <dir> is not specified, the current dir is used.

	positional arguments:
	  dir                   the project directory (default: /Users/reubano/Documents/Projects/ongeza).

    optional arguments:
      -h, --help            show this help message and exit
      -t TYPE, --type TYPE  version bump type, must be one of:
                              m or major: [x].0.0
                              n or minor: x.[y].0
                              p or patch: x.y.[z]
      -s VERSION, --set VERSION
                            set arbitrary version number
      -S, --skip-commit     skip committing version bumped files
      -T, --tag             create git tag at HEAD with the bumped version number
      -p, --push            push to the remote origin
      -a, --stash           stash uncommitted changes
      -f FORMAT, --tag-format FORMAT
                            git tag format
      -F FORMAT, --tag-msg-format FORMAT
                            git tag message format
      -c FORMAT, --commit-msg-format FORMAT
                            git commit message format
      -g, --sign            make a GPG-signed tag (implies `--tag`)
      -i FILE, --file FILE  the versioned file
      -v, --version         Show version and exit.
      -V, --verbose         increase output verbosity

*view current version*

.. code-block:: bash

	ongeza

*bump to a `minor` version*

.. code-block:: bash

	ongeza --type=minor

or

.. code-block:: bash

    ongeza -tn

*manually set a version*

.. code-block:: bash

    ongeza --set 1.0.2

or

.. code-block:: bash

	ongeza -s 1.0.2

*bump to a `major` version and add a git tag*

.. code-block:: bash

	ongeza --tag --type=major

or

.. code-block:: bash

    ongeza -Ttm

*stash uncommitted changes and bump to a `patch` version*

.. code-block:: bash

    ongeza --stash --type=patch

or

.. code-block:: bash

	ongeza -atp

Advanced Examples
~~~~~~~~~~~~~~~~~

*bump to a `major` version and add a GPG signed git tag*

.. code-block:: bash

    ongeza --sign --type=major

or

.. code-block:: bash

    ongeza -gtm

*bump `weird.file` to a `minor` version and use custom formats*

.. code-block:: bash

	ongeza -tn --file='weird.file' --tag-format='{version}' --commit-msg-format='New version: {version}'

*bump a remote directory to a `minor` version and use a custom tag message format*

.. code-block:: bash

	ongeza -tn --tag-msg-format='Release: {version}' /path/to/remote/dir

Installation
------------

At the command line, install ongeza using either ``pip`` (*recommended*)

.. code-block:: bash

    pip install --user ongeza

or (if you must) ``easy_install``

.. code-block:: bash

    easy_install ongeza

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
    │   └── ongeza
    ├── ongeza
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
    │   └── test_ongeza.py
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

ongeza comes with a built in task manager ``manage.py``

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

Contributing
------------

Please mimic the coding style/conventions used in this repo.
If you add new classes or functions, please add the appropriate doc blocks with
examples. Also, make sure the python linter and nose tests pass.

Please see the `contributing doc`_ for more details.

License
-------

ongeza is distributed under the `MIT License`_.

.. |travis| image:: https://img.shields.io/travis/reubano/ongeza/master.svg
    :target: https://travis-ci.org/reubano/ongeza

.. |versions| image:: https://img.shields.io/pypi/pyversions/ongeza.svg
    :target: https://pypi.python.org/pypi/ongeza

.. |pypi| image:: https://img.shields.io/pypi/v/ongeza.svg
    :target: https://pypi.python.org/pypi/ongeza

.. _MIT License: http://opensource.org/licenses/MIT
.. _semver: http://semver.org/
.. _Semantic Versioning Specification: http://semver.org/
.. _virtualenv: http://www.virtualenv.org/en/latest/index.html
.. _contributing doc: https://github.com/reubano/ongeza/blob/master/CONTRIBUTING.rst
