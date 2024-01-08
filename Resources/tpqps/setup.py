#
# Setup file for
# tpqps -- Streaming Plots with Plotly
#
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#
from setuptools import setup

with open('README.md', 'r') as f:
      long_description = f.read()

setup(name='tpqps',
      version='0.0.1',
      description='tpqps Streaming Plots with Plotly',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Yves Hilpisch',
      author_email='team@tpq.io',
      url='http://training.tpq.io',
      packages=['tpqps'],
      install_requires=[
          'plotly'
      ]
      )
