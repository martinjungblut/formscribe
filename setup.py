from distutils.core import setup

setup(
    name='formscribe',
    packages=['formscribe'],
    version='0.4.3',
    description='A practical and flexible web form validation library.',
    author='Martin Jungblut Schreiner',
    author_email='martinjungblut@gmail.com',
    url='https://github.com/martinjungblut/formscribe',
    download_url='https://github.com/martinjungblut/formscribe/archive/v0.4.3.zip',
    keywords=['form', 'validation', 'web'],
    install_requires=[
        'ordereddict',
        'six',
    ],
    license='MIT',
)
