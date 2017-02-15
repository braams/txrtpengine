from distutils.core import setup

setup(name='txrtpengine',
      version='0.1',
      description='Twisted based rtpengine client',
      author='Max Nesterov',
      author_email='braams@braams.ru',
      url='https://github.com/braams/txrtpengine/',
      packages=['txrtpengine'],
      install_requires=['Twisted', 'better_bencode'],
      )
