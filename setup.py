import codecs
from setuptools import setup, find_packages

VERSION = '0.0.0'

entry_points = {
    'console_scripts': [
    ],
}

import platform
py_impl = getattr(platform, 'python_implementation', lambda: None)
IS_PYPY = py_impl() == 'PyPy'

TESTS_REQUIRE = [
    'nose',
    'nose2[coverage_plugin]',
    'nose-timer',
    'nose-progressive',
    'nose-pudb',
    'pyhamcrest',
    'zope.testing',
    'nti.testing',
    'nti.nose_traceback_info',
]

setup(
    name='nti.common',
    version=VERSION,
    author='Jason Madden',
    author_email='jason@nextthought.com',
    description="NTI Store",
    long_description=codecs.open('README.rst', encoding='utf-8').read(),
    license='Proprietary',
    keywords='utils',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
		'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
	packages=find_packages('src'),
	package_dir={'': 'src'},
	namespace_packages=['nti'],
    tests_require=TESTS_REQUIRE,
	install_requires=[
		'setuptools',
        'zope.cachedescriptors',
        'zope.dottedname'
	],
    dependency_links=[],
	entry_points=entry_points
)
