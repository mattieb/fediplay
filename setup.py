from setuptools import setup

setup(
    name='fediplay',
    version='2.0',
    py_modules=['fediplay'],
    install_requires=[
        'click',
        'cssselect',
        'lxml',
        'Mastodon.py',
        'python-dotenv',
        'youtube-dl'
    ],
    entry_points={
        'console_scripts': [
            'fediplay = fediplay:cli'
        ]
    }
)

