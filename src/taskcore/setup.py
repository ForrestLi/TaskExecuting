from setuptools import setup, find_packages

setup(name='taskcore',
      version='0.1',
      author='fofo',
      author_email='forrest.li@gmail.com',
      license='MIT',
      packages=find_packages(),
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
