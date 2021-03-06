# coding=utf-8
import os
from setuptools import setup, find_packages
from version import get_version

version = get_version()

setup(
    name='edem.group.messages.topicsdigest',
    version=version,
    description="Customized version of GroupServer's topics digest for E-Democracy",
    long_description=open("README.txt", 'r').read() + "\n" +
        open(os.path.join("docs", "HISTORY.txt"), 'r').read(),
    classifiers=[
      "Development Status :: 4 - Beta",
      "Environment :: Web Environment",
      "Framework :: Zope2",
      "Intended Audience :: Developers",
      "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
      "Natural Language :: English",
      "Operating System :: POSIX :: Linux"
      "Programming Language :: Python",
      "Topic :: Communications :: Email",
      ],
    keywords='e-democracy groupserver topicsdigest html',
    author='Bill Bushey',
    author_email='bill.bushey@e-democracy.org',
    url='http://forums.e-democracy.org/',
    license='other',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['edem', 'edem.group', 'edem.group.messages'],
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'setuptools',
        'edem.skin',
        'sqlalchemy',
        'zope.cachedescriptors',
        'zope.component',
        'zope.formlib',
        'zope.viewlet',
        'gs.database',
        'gs.group.base',
        'gs.group.messages.text',
        'gs.group.messages.topic.digest.base',
        'gs.group.messages.topic.digest.daily',
        'edem.group.messages.topic.digest.weekly',
        'gs.viewlet',
        'Products.GSContent',
        'Products.GSGroupMember',
        # -*- Extra requirements: -*-
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,)
