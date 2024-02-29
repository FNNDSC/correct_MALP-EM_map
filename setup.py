from setuptools import setup

setup(
    name='correct_malpem_map',
    version='1.0.0',
    author='Stefan Pszczolkowski Parraguez',
    author_email='stefan.pszczolkowskiparraguez@nottingham.ac.uk',
    scripts=['correct_MALP-EM_map.py'],
    install_requires=['nibabel', 'numpy'],
    python_requires='~= 3.6',
)
