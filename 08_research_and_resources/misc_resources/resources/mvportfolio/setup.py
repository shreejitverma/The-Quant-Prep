#
# Setup file for
# mvportfolio
#
# The Python Quants GmbH
# 
from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(name='mvportfolio',
      version='0.0.9',
      description='Simple portfolio analysis and management package.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Yves Hilpisch',
      author_email='training@tpq.io',
      url='http://certificate.tpq.io',
      packages=['mvportfolio'],
      # install_requires=['numpy', 'pandas', 'scipy']
      )
