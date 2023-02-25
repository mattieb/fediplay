from setuptools import setup

setup(
    name='fediplug',
    version='2.0',
    py_modules=['fediplug'],
    install_requires=[
        'appdirs',
        'click',
        'cssselect',
        'lxml',
        'Mastodon.py',
        'python-dotenv',
        'asyncio',
        'asyncclick',
        'anyio',
        'keyring',
        'buttplug-py'
        
    ],
    entry_points={
        'console_scripts': [
            'fediplug = fediplug:cli'
        ]
    }
)

