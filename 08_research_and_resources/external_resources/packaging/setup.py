#
# Setup file for
# pylib example
#
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
# 
from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(name='pylib',
      version='0.18',
      description='pylib Tools & Skills',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Yves Hilpisch',
      author_email='training@tpq.io',
      url='http://certificate.tpq.io',
      packages=['pylib', 'pylib.suba', 'pylib.subb'],
      )
