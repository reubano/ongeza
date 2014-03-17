import os
import sys

try:
	from setuptools import setup, find_packages
except ImportError:
	from distutils.core import setup, find_packages

from Bump import __version__


def read(fname):
	try:
		with open(os.path.join(os.path.dirname(__file__), fname)) as fh:
			return fh.read()
	except IOError:
		return ''


requirements = read('requirements.txt').splitlines()
packages = find_packages(exclude=['tests'])

# Avoid byte-compiling the shipped template
sys.dont_write_bytecode = True


setup(
	name="bump",
	version=__version__,
	description="Makes following the Semantic Versioning Specification a breeze",
	long_description=read('README.rst'),
	url='https://github.com/reubano/bump',
	license='MIT',
	author='Reuben Cummings',
	author_email='reubano@gmail.com',
	packages=packages,
	include_package_data=True,
	classifiers=[
		'Development Status :: 4 - Beta',
		'Environment :: Console',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Operating System :: POSIX',
		'Operating System :: MacOS :: MacOS X',
		'Operating System :: Microsoft :: Windows',
		'Programming Language :: Python',
		'Topic :: Software Development',
	],
	# platform='OS Independent',
	keywords='semver, versioning',
	scripts=['bump.py'],
	install_requires=requirements,
)
