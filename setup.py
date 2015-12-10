from setuptools import setup

setup(
    name='sirtalkalot',
    version='0.1.0',
    packages=['tests', 'sirtalkalot'],
    install_requires=['docopt', 'libslack', 'ws4py'],
    url='https://github.com/Nicoretti/sirtalkalot',
    license='BSD',
    author='Nicola Coretti',
    author_email='nico.coretti@gmail.com',
    description='A simple service based slack bot',
    package_data={
        '.': ['*.txt', '*.rst']
    },
    entry_points={
        'console_scripts': [
        'sirtalkalot=bots:main',
        ],
    },
    keywords=['slack', 'bot', 'api'],
)
