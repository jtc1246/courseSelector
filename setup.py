from setuptools import setup

setup(
    name='courseSelector',
    version='1.1.0',
    author='Tiancheng Jiao',
    author_email='jtc1246@outlook.com',
    url='https://github.com/jtc1246/courseSelector',
    description='An automatic course selection program for SJTU-JI',
    packages=['courseSelector'],
    install_requires=['urllib3','myBasics','selenium==3.11.0','pillow','ddddocr','phantomjs-packages'],
    python_requires='>=3',
    platforms=["all"],
    license='GPL-2.0 License'
)


