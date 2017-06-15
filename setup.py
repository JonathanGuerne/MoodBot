"""MoodBot for Discord"""

from setuptools import setup


setup(
    name='discord-moodbot',
    version='0.1',  
    python_requires='>=3.5',
    author='Jeanbourquin Paul & Guerne Jonathan',
    author_email='paul.jeanbourquin@he-arc.ch & jonathan.guerne@he-arc.ch',
    url='https://github.com/JonathanGuerne/MoodBot',
    license='https://opensource.org/licenses/BSD-3-Clause',
    keywords='discord mood bot',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Education',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ),
    install_requires=(
        'discord>=0.16.8',
        'textblob>=0.12.0'
    ),
    extras_require={ },
)