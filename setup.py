import codecs
from setuptools import setup, find_packages

entry_points = {
    'console_scripts': [
    ],
}

TESTS_REQUIRE = [
    'fudge',
    'nti.testing',
    'zope.dottedname',
    'zope.testrunner',
]


def _read(fname):
    with codecs.open(fname, encoding='utf-8') as f:
        return f.read()


setup(
    name='nti.common',
    version=_read('version.txt').strip(),
    author='Jason Madden',
    author_email='jason@nextthought.com',
    description="NTI common utilities",
    long_description=(
        _read('README.rst')
        + '\n\n'
        + _read("CHANGES.rst")
    ),
    license='Apache',
    keywords='common utils',
    classifiers=[
        'Framework :: Zope3',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    url="https://github.com/OpenNTI/nti.common",
    zip_safe=True,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    namespace_packages=['nti'],
    tests_require=TESTS_REQUIRE,
    install_requires=[
        'anytree',
        'setuptools',
        'emoji',
        'itsdangerous',
        'nameparser',
        'nti.dublincore',
        'nti.property',
        'nti.schema',
        'six',
        'zope.component',
        'zope.configuration',
        'zope.deprecation',
        'zope.deferredimport',
        'zope.dottedname',
        'zope.interface',
    ],
    extras_require={
        'test': TESTS_REQUIRE,
        'docs': [
            'Sphinx',
            'repoze.sphinx.autointerface',
            'sphinx_rtd_theme',
        ],
    },
    entry_points=entry_points,
)
