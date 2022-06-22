import setuptools

with open('requirements.txt') as f:
    requirements = f.read().strip().split('\n')

print(requirements)

# https://docs.python.org/3/distutils/setupscript.html
setuptools.setup(
    name='vysion',
    version='0.2.1',    # TODO Read from __version__
    description='The official Python client library for Vysion',
    license='Apache 2',
    license_files = ('LICENSE'),
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url='https://gitlab.com/byronlabs/vysion/vysion-py',
    packages=['vysion', 'vysion.client', 'vysion.model', 'vysion.taxonomy'],
    python_requires='>=3.7.0',
    install_requires=requirements,
    # setup_requires=['pytest-runner'],
    # extras_require={'test': ['pytest', 'pytest_httpserver', 'pytest_asyncio']},
    classifiers=[
       'Programming Language :: Python :: 3',
       'License :: OSI Approved :: Apache Software License',
       'Operating System :: OS Independent',
    ]
)
