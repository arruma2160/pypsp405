from distutils.core import setup

setup(
        name='pyPSP405',
        version='0.1dev',
        author="Arturo Ruiz Mañas",
        author_email="arruma2160@gmail.com",
        packages=['pypsp405',],
        classifiers=[
            'Programming Language :: Python',
            'Intended Audience :: Science/Research',
        ],
        install_requires=['pyserial'],
      )
