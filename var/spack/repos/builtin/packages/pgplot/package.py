# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install pgplot
#
# You can edit this file again by typing:
#
#     spack edit pgplot
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *
from llnl.util.tty import info, msg, debug
import fileinput
import re


class Pgplot(Package):
    """The PGPLOT Graphics Subroutine Library is a Fortran- or C-callable, device-independent graphics package for making simple scientific graphs. It is intended for making graphical images of publication quality with minimum effort on the part of the user. For most applications, the program can be device-independent, and the output can be directed to the appropriate device at run time.  """

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.astro.caltech.edu/~tjp/pgplot/"
    url      = "ftp://ftp.astro.caltech.edu/pub/pgplot/pgplot522.tar.gz"

    # FIXME: Add proper versions and checksums here.
    # version('1.2.3', '0123456789abcdef0123456789abcdef')
    version('5.2.2', 'e8a6e8d0d5ef9d1709dfb567724525ae')

    # FIXME: Add dependencies if required.
    # depends_on('foo')

    variant('png', default=True, description='Add /PNG and /TPNG driver.')
    variant('iterm', default=False, description='Add /ITERM driver.')
    variant('latex', default=True, description='Add /LATEX driver.')
    variant('xwindows', default=True, description='Add /XWINDOWS driver.')
    variant('xserve', default=True, description='Add /xserve driver.')
    variant('ps', default=True, description='Add all ps related drivers.')

    depends_on('libpng', when='+png')
    depends_on('zlib', when='+png')

    depends_on('libx11', when='+xwindows')
    depends_on('libx11', when='+xserve')

    patch('remove_f2c.patch')
    patch('select_driver.patch')
    patch('png.patch')
    patch('png_jmpbuf.patch')
    patch('env.patch')

    parallel = False


    def url_for_version(self, version):
        url = "ftp://ftp.astro.caltech.edu/pub/pgplot/pgplot{}.tar.gz"
        return url.format(version.joined)

    def setup_run_environment(self, env):
        env.set('PGPLOT_DIR', self.prefix)
        env.set('PGPLOT_FONT', self.prefix)

    def install(self, spec, prefix):
        def select_driver(driver):
            driver = driver.upper()
            match = re.compile(r'(^!)(.+/{}.+)'.format(driver))
            for line in fileinput.input('drivers.list', inplace=True):
                result = match.search(line)
                if result:
                    line = ' '+result.groups()[1]
                print(line.rstrip())

        if ('+png' in spec):
            select_driver('png')
            select_driver('tpng')
        if ('+iterm' in spec):
            select_driver('iterm')
        if ('+latex' in spec):
            select_driver('latex')
        if ('+xwindows' in spec):
            select_driver('xwindows')
        if ('+xserve' in spec):
            select_driver('xserve')
        if ('+ps' in spec):
            for d in ['ps', 'vps', 'cps', 'vcps' ]:
                select_driver(d)


        source_path = self.stage.source_path
        makemake = which(source_path+'/makemake')
        makemake(source_path,'linux', 'f77_gcc')

        # if('+png' in spec):
        #     for line in fileinput.input('makefile', inplace=True):
        #         if re.match(r'^XINCL', line):
        #             line = line.rstrip() + ' -I{}'.format(spec['libpng'].prefix.include) +' -I{}'.format(spec['zlib'].prefix.include) 
        #         if re.match(r'^SHARED_LIB_LIBS', line):
        #             line = line.rstrip() + ' -L{} -lz'.format(spec['zlib'].prefix.lib) + ' -L{} -lpgplot'.format(source_path)
        #         print(line.rstrip())

        filter_file(r'^FCOMPL\s*=.*', 'FCOMPL={}'.format(spack_fc), source_path+'/makefile') 
        filter_file(r'^CCOMPL\s*=.*', 'CCOMPL={}'.format(spack_cc), source_path+'/makefile') 

        filter_file(r'^FFLAGC\s*=.*', 'FFLAGC=', source_path+'/makefile') 
        filter_file(r'^FFLAGD\s*=.*', 'FFLAGD=', source_path+'/makefile') 


        env['XINCL'] = '-I/usr/X11R6/include '

        libs = 'LIBS=-L/usr/X11R6/lib -lX11 `$(SRC)/cpg/libgcc_path.sh` -lm -L. -lpgplot '
        if('+png' in spec):
            env['XINCL'] = env['XINCL'] + '-I{}'.format(spec['libpng'].prefix.include)
            env['XINCL'] = env['XINCL'] + '-I{}'.format(spec['zlib'].prefix.include)
            env['SHARED_LIB_LIBS'] = '-L{} -lpng -L{} -lz'.format(spec['libpng'].prefix.lib, 
                                                                  spec['zlib'].prefix.lib)

            filter_file(r'^LIBS\s*=.*', 
                        libs+'-L{} -lpng'.format(spec['libpng'].prefix.lib),
                        source_path+'/makefile')
            filter_file(r'^PGPLOT_LIB\s*=.*', 
                        libs+'-L{} -lpng'.format(spec['libpng'].prefix.lib),
                        source_path+'/makefile')
        else:
            filter_file(r'^LIBS\s*=.*', libs, source_path+'/makefile')

        filter_file(r'^SHARED_LD\s*=.*', 'SHARED_LD=ifort -shared -o libpgplot.so', source_path+'/makefile') 
        make()

        ## copy files
        files = ['drivers.list', 'grexec.f', 'grfont.dat', 
                 'libpgplot.a', 'libpgplot.so', 'pgdisp',
                 'pgplot.doc', 'pgxwin_server', 'rgb.txt']
        cp = which('cp')
        for f in files:
            try: 
                cp(f, prefix)
            except:
                pass
