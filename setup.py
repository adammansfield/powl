from distutils.core import setup

setup(
    name='Powl',
    version='0.1.0',
    author='Adam Mansfield',
    author_email='adam@adammansfield.org',
    packages=['powl', 'powl.test'],
    scripts=['bin/process_mail.py'],
    url='http://adammansfield.org/Projects/Powl/',
    license='LICENSE.txt',
    description='Mail processor for various actions.',
    long_description=open('README.txt').read(),
)
