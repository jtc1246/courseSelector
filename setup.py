from setuptools import setup

setup(
    name='courseSelector',
    version='1.0.8',
    author='Tiancheng Jiao',
    author_email='jtc1246@outlook.com',
    url='https://github.com/jtc1246/courseSelector',
    description='An automatic course selection program for SJTU-JI',
    packages=['courseSelector'],
    install_requires=['urllib3'],
    python_requires='>=3',
    platforms=["all"],
    license='GPL-2.0 License'
)


