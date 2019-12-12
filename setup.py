from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pipeline-exec',
    version='0.4',
    packages=['pipeline_exec'],
    url='https://github.com/Sikilabs/pipeline_exec',
    license='MIT',
    author='Sikilabs Technologies Inc',
    author_email='info@sikilabs.com',
    description='A Pipeline to process an Object Collection',
    long_description=long_description,
    long_description_content_type="text/markdown",
)
