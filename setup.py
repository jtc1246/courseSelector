from setuptools import setup

setup(
    name='courseSelector',
    version='1.0.0',
    author='Tiancheng Jiao',
    author_email='jtc1246@outlook.com',
    url='https://github.com/jtc1246/courseSelector',
    description='An automatic course selection program for SJTU-JI',
    packages=['courseSelector'],
    install_requires=['urllib3'],
    python_requires='>=3',
    platforms=["all"],
    license='GPL-2.0 License',
    entry_points={
        'console_scripts': [
            'help=courseSelector:help',
            'check=courseSelector:check',
            'printCourseList=courseSelector:printCourseList',
            'waitEmptySpace=courseSelector:waitEmptySpace',
            'fastSelect=courseSelector:fastSelect',
            'luckyDraw=courseSelector:luckyDraw'
        ]
    }
)


