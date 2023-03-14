from setuptools import setup

with open('requirements.txt','r') as req:
    requirements = req.read().splitlines()

setup(
    name='pydyn_surv',
    version='0.1.0',
    description='A package with tools for generating a dynamic survey using Machine Learning tools.',
    url='https://github.com/JARA99/Dynamic_Survey_lib',
    author='Jorge Alejandro Rodríguez Aldana',
    author_email='jorgealejandro1999@gmail.com',
    license='Proprietary License',
    packages=['pydyn_surv','pydyn_surv.LinearClassifier','pydyn_surv.classes'],
    install_requires=requirements,

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'License :: Other/Proprietary License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python'
    ],
)