from setuptools import setup

package_name = 'sound_system'

setup(
    name=package_name,
    version='0.0.1',
    packages=[],
    py_modules=[
        "sound_system",
        "hotword_detector"
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='ItoMasaki,MatudaYamato',
    author_email='is0449sh@ed.ritsumei.ac.jp',
    maintainer='ItoMasaki,MatsudaYamto',
    maintainer_email='is0449sh@ed.ritsumei.ac.jp,is0476hv@ed.ritsumei.ac.jp',
    keywords=['ROS2'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='Examples of minimal publishers using rclpy.',
    license='Apache License, Version 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'sound_system = sound_system:main',
            'hotword_detector = hotword_detector:main'
        ],
    },
)


