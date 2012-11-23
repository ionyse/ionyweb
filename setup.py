# coding=utf-8
"""Python packaging."""
import os
from setuptools import setup


def read_relative_file(filename):
    """Returns contents of the given file, which path is supposed relative
    to this module."""
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()


NAME = 'ionyweb'
README = read_relative_file('README.rst')
VERSION = read_relative_file('VERSION').strip()
PACKAGES = ['ionyweb']
REQUIRES = ['django>=1.4', 'Jinja2', 'MySQL-python', 'PIL', 'PyYAML', 'South',
            'django-floppyforms', 'django-mptt', 'django-tinymce', 
            'djangorestframework==0.4.0', 'dnspython', 'python-magic', 'requests',
            'django-less', 'django-sekizai', 'django-grappelli']


setup(name=NAME,
      version=VERSION,
      description='A javascript UI based on REST API CMS based on Django.',
      long_description=README,
      classifiers=['Development Status :: 1 - Planning',
                   'License :: OSI Approved :: BSD License',
                   'Programming Language :: Python :: 2.7',
                   'Framework :: Django',
                   ],
      keywords='django cms',
      author='Ionyse',
      author_email='contact@ionyse.com',
      url='https://github.com/ionyse/%s' % NAME,
      license='BSD',
      packages=PACKAGES,
      include_package_data=True,
      zip_safe=False,
      install_requires=REQUIRES,
      entry_points={
          'console_scripts': [
              'ionyweb-manage = ionyweb.bin.manage:main',
              'ionyweb-quickstart = ionyweb.bin.quickstart:main',
          ]
      },
      )
