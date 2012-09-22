# Makefile for development.
# See INSTALL and docs/dev.txt for details.
SHELL = /bin/bash
PROJECT = 'ionyweb'
ROOT_DIR = $(shell pwd)


clean:
	find $(ROOT_DIR)/ -name "*.pyc" -delete

distclean: clean
	rm -rf $(ROOT_DIR)/*.egg-info

apidoc:
	rm -rf docs/api/*
	sphinx-apidoc --suffix rst --output-dir $(ROOT_DIR)/docs/api $(PROJECT)


sphinx:
	make --directory=docs clean html


documentation: sphinx
