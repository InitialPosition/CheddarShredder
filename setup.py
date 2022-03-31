#! /usr/bin/env python

from setuptools import setup

setup(
	name='CheddarShredder 1.0',
	version='1.0.0',
	description="A UCI compatible chess engine.",
	author="RedCocoa",
	author_email="herubrin@gmail.com",
	license='open source',
	classifiers=[
		"Programming Language :: Python :: 3",
		"Operating System :: OS Independent"
	],
	packages=['AI'],
	include_package_data=True,
	install_requires=[
		"chess"
	],
	entry_points={"console_scripts": ["realpython=reader.__main__:main"]}
)
