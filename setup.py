from setuptools import setup

setup(
    name='fediplay',
    version='0.1',
    py_modules=['fediplay'],
    install_requires=[
        'Mastodon.py',
        'cssselect',
        'lxml',
        'youtube-dl'
    ],
    entry_points={
        'console_scripts': [
            'fediplay = fediplay:main'
        ]
    }
)

