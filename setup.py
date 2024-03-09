try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.md') as f:
    readme = f.read()


setup(
    name='submodule',
    version='1.0.0',
    description='Subtitle converter',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Benjamin BARIAL',
    author_email='benjamin.barial.pro@gmail.com',
    url='https://github.com/benjamin-brl/sub',
    keywords='sub converter',
    packages=['sub', 'sub.utils', 'sub.tests'],
    include_package_data=True,
    install_requires=['tkinter', 'langdetect'],
    license='MIT',
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.12.2',
    ]
)