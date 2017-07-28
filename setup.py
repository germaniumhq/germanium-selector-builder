from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name='germaniumsb',
    version='2.0.6',
    description='Germanium Selector Builder',
    long_description = readme,
    author='Bogdan Mustiata',
    author_email='bogdan.mustiata@gmail.com',
    license='Affero GPL',
	install_requires=[
        'germanium==2.0.6'
    ],
    packages=['germaniumsb'],
    package_data={
        'germaniumsb': ['*.js'],
    }
)
