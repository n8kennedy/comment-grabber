from setuptools import setup
setup(
  name = 'comment_grabber',
  version = '0.1',
  scripts = ['comment_grabber.py'],
  author = 'Nate Kennedy',
  description = 'A simple python script for grepping comments from source code',
  license = 'MIT',
  url = 'https://github.com/n8kennedy/comment-grabber',
  entry_points = {
    'console_scripts': ['comments = comment_grabber:setuptools_main']
  }
)
