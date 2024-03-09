from setuptools import setup, find_packages
# try:
# except ImportError:
    # from distutils.core import setup


with open('README.md') as f:
    readme = f.read()


setup(
    name='submodule',
    version='0.0.1',
    author='Benjamin BARIAL',
    author_email='benjamin.barial.pro@gmail.com',
    description='Subtitle converter',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/benjamin-brl/sub',
    classifiers=[
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    install_requires=['tkinter', 'langdetect'],
    license='MIT',
    package_dir = {"": "src"},
    packages = find_packages(where="src"),
    python_requires = ">=3.10"
)