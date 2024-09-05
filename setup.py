from setuptools import setup

with open("README", 'r') as f:
    long_description = f.read()

setup(
   name='Cardazim',
   version='1.0',
   description='Cardazim',
   long_description = long_description
   author='MrWolterWhite',
   author_email='yakobovitz@mail.tau.ac.il',
   packages=['Cardazim'],  #same as name
   install_requires=['wheel', 'bar', 'greek'], #external packages as dependencies
)
