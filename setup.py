from setuptools import setup
from setuptools import find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

packages = find_packages()

setup(
    name='germaniumsb',
    version='1.0.0',
    description='Germanium Selector Builder',
    long_description = readme,
    author='Bogdan Mustiata',
    author_email='bogdan.mustiata@gmail.com',
    license='Affero GPL',
    entry_points={
        "console_scripts": [
            "germaniumsb = germaniumsb.mainapp:main"
        ]
    },
	install_requires=["germanium==2.0.11"],
    packages=packages,
    package_data={
        'germaniumsb': ['*.js'],
        'germaniumsb.doc': ['*.html', '*.chm'],
        'germainumsb.doc.images': ['*.png']
    }
)
