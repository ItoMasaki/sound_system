from setuptools import setup

package_name = 'sound_system'

setup(
    name=package_name,
    version='0.0.1',
    packages=[],
    py_modules=[
        'sound_system'
    ],
    install_requires=['setuptools'],
    data_files=[
        ('lib/' + package_name, ['package.xml']),
        ('lib/' + package_name+'/ros2_function',
         ['ros2_function/module_QandA.py',
          'ros2_function/module_speak.py',
          'ros2_function/module_angular.py',
          'ros2_function/module_detect.py'
          ]),
        ('lib/sound_system/dictionary/',
         ['dictionary/hey_ducker_simple.dict',
          'dictionary/hey_ducker_simple.gram',
          'dictionary/spr_question.dict',
          'dictionary/spr_question.gram'
          ]),
        ('lib/sound_system/dictionary/QandA',
            ['dictionary/QandA/qanda.csv'])
    ],
    zip_safe=True,
    author='ItoMasaki,MatudaYamato,HiroseChihiro',
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
    description='sound package for SPR',
    license='Apache License, Version 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'sound_system = sound_system:main',
        ],
    },
)
