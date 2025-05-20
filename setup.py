from setuptools import setup, find_packages

setup(
    name='qrgen',
    version='0.1',
    packages=find_packages(),
    package_data={
        'qrgen.words': ['*.txt'],
    },
    include_package_data=True,
    install_requires=[
        'qrcode',
        'Pillow',
    ],
    entry_points={
        'console_scripts': [
            'qrgen=qrgen.qrgen:main',
        ],
    },
    author='h0nus',
    description='Tool to generate malformed QR codes for fuzzing QR parsers/readers',
    python_requires='>=3.6',
)
