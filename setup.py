from setuptools import setup

with open('requirements.txt','r') as req:
    requirements = req.read().splitlines()

setup(
    name='pydyn_surv',
    version='1.0.0',
    description='A package with tools for generating a dynamic survey using Machine Learning tools.',
    url='https://github.com/JARA99/Dynamic_Survey_lib',
    author='Jorge Alejandro Rodríguez Aldana',
    author_email='jorgealejandro1999@gmail.com',
    license='License :: OSI Approved :: MIT License',
    packages=['pydyn_surv'],
    install_requires=requirements,

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: Other/Proprietary License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python'
    ],
)