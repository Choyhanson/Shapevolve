from distutils.core import setup

setup(
    name='shapevolve',  # How you named your package folder (MyLib)
    packages=['shapevolve'],  # Chose the same as "name"
    version='v0.1',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='A genetic algorithm to recreate artworks using simple shapes, with Python 3.',
    # Give a short description about your library
    author='Evan Zheng',  # Type in your name
    author_email='evan.ty.zheng@gmail.com',  # Type in your E-Mail
    url='https://richmondvan.github.io/Shapevolve/',  # Provide either the link to your github or to your website
    download_url='https://github.com/richmondvan/Shapevolve/archive/0.1.tar.gz',  # I explain this later on
    install_requires=[  # I get to this in a second
        'opencv-python',
        'matplotlib',
        'numpy',
        'scikit-image',
        "Pillow",
        "ColorThief"
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Science/Research',  # Define that your audience are developers
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
