# bump

## Introduction

bump is a command line program that does awesome stuff and has been tested on the following configuration:

* MacOS X 10.5.8
* Python 2.7.3

## Requirements

bump requires the following in order to run properly:

* [Python 2.7](http://python.org/download/)

## Preparation

Check that the correct version of Python is installed `python -V`

## Installation

Install bump using either pip (recommended) `sudo pip install bump` or easy_install `sudo easy_install bump`
	
## Usage

	#!/usr/bin/env php
	<?php
	try {
		require_once 'bump.inc.php';
		$time = time();
		$imageObj = new bump('src', 1000, 600);
		$imageObj->execute();
		$imageObj->saveFile("bump/$time.png");
		echo "done!\n";
		exit(0);
	} catch (Exception $e) {
		fwrite(STDOUT, 'Program '.$program.': '.$e->getMessage()."\n");
		exit(1);
	}
	?>
