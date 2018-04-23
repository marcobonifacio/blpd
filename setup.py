from setuptools import setup

setup(name='blpd',
      version='0.1',
      description='Bloomberg formulas with Python and Pandas',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      url='https://github.com/mbonix/blpd',
      author='Marco Bonifacio',
      author_email='bonifacio.marco@gmail.com',
      license='MIT',
      packages=['blpd'],
      install_requires=[
      'blpapi',
      'pandas',
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      zip_safe=False)
