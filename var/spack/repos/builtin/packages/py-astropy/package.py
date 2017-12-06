##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class PyAstropy(PythonPackage):
    """The Astropy Project is a community effort to develop a single core
    package for Astronomy in Python and foster interoperability between
    Python astronomy packages."""

    homepage = 'http://www.astropy.org/'
    url = 'https://github.com/astropy/astropy/archive/v2.0.2.tar.gz'
    list_url = 'https://github.com/astropy/astropy/archive/'

    version('develop', git='https://github.com/astropy/astropy.git')
    version('2.0.2',  '3c4027cd59166f2e4524de6c9f37a48a',
            url='https://github.com/astropy/astropy/archive/v2.0.2.tar.gz')
    version('2.0.1',  'e1da08e62ac8e4bf13b9b5241993cba5')
    version('2.0rc1', '62ebc2a60be3db46f8b86e70c6d00db2')
    version('2.0',    '2e979357fd0c103c3f811002519bdb23')
    version('1.3.3',  'aeef4a2b375d9e649286f7f7167f9593')
    version('1.3.2',  '1a8fa8fda4252c78f306bf78ee457e38')
    version('1.3.1',  'cc5ed22c1fa71d132f0634efe150200a')

    version('1.1.2',     'cbe32023b5b1177d1e2498a0d00cda51',
            url='https://pypi.io/packages/source/a/astropy/astropy-1.1.2.tar.gz')
    version('1.1.post1', 'b52919f657a37d45cc45f5cb0f58c44d',
            url='https://pypi.io/packages/source/a/astropy/astropy-1.1.post1.tar.gz')

    # Required dependencies
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))

    # Optional dependencies
    depends_on('py-h5py', type=('build', 'run'))
    depends_on('py-beautifulsoup4', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('libxml2')
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-pytz', type=('build', 'run'))
    depends_on('py-scikit-image', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))

    # System dependencies
    depends_on('cfitsio')
    depends_on('expat')

    def build_args(self, spec, prefix):
        return ['--use-system-cfitsio', '--use-system-expat']
