keybump
===========

Introduction
------------

keybump makes following the `Semantic Versioning Specification http://semver.org/>`_ a breeze. If called with no options, keybump will print the script's current git tag version. It has been tested on the following configuration:

* MacOS X 10.7.4
* Python 2.7.3

Requirements
------------

keybump requires the following in order to run properly:

* `Python >= 2.5 <http://www.python.org/download>`_

Preparation
-----------

Check that the correct version of Python is installed

  python -V

Installation (not yet implemented)
------------

Install keybump using either pip (recommended)

  sudo pip install keybump

or easy_install

  sudo easy_install keybump

Using keybump
-----------------

Usage
^^^^^

  keybump [options] <dir>

Examples
^^^^^^^^

*normal usage*

  keybump -tn /path/to/git/repo

*view current version*

  keybump /path/to/git/repo

*add new tag*

  keybump -gtn /path/to/git/repo

*manually set version*

  keybump -s 1.0.2  /path/to/git/repo

Options
^^^^^^^

    -h, --help            show this help message and exit
    -t {m,n,p}, --type {m,n,p}
              version bump type:
                m = major - x.0.0
                n = minor - 1.y.0
                p = patch - 1.0.z
    -s SET, --set SET     set arbitrary version number
    -p PATTERN, --pattern PATTERN
              search pattern when setting arbitrary version number
    -v, --verbose         increase output verbosity
    -g, --tag             tag git repo with the bumped version number

Arguments
^^^^^^^^^

+---------+-------------------------------+
| dir     |  the project directory        |
+---------+-------------------------------+

LIMITATIONS
-----------

* no built-in support for pre-release or build numbers
  - 1.0.0-alpha, 1.0.0-alpha.1, 1.0.0-0.3.7, 1.0.0-x.7.z.92
  - 1.0.0+build.1, 1.3.7+build.11.e0f985a
* doesn't check validity of user set versions

LICENSE
-------

bump is distributed under the `MIT License <http://opensource.org/licenses/mit-license.php>`_.