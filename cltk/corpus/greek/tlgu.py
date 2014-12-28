"""Wrapper for `tlgu` command line utility

TODO: Fully implement this.
"""

__author__ = 'Stephen Margheim <stephen.margheim@gmail.com>'
__license__ = 'MIT License. See LICENSE.'


from cltk.corpus.utils.cltk_logger import logger
from cltk.corpus.utils.importer import CorpusImporter
import os
import itertools
import subprocess
import sys


ARGS = {
    'book_breaks': '-b',
    'page_breaks': '-p',
    'latin_text': '-r',
    'level_1': '-v',
    'level_2': '-w',
    'level_3': '-x',
    'level_4': '-y',
    'level_5': '-z',
    'line_tab': '-B',
    'higher_levels': '-X',
    'lower_levels': '-Y',
    'no_spaces': '-N', # break_lines
    'citation_debug': '-C',
    'code_debug': '-S',
    'verbose': '-V',
    'split_works': '-W' #  divide_works
}


class TLGU(object):
    """Check, install, and call TLGU."""
    def __init__(self):
        """Check whether tlgu is installed, if not, import and install."""
        self.check_source()
        self.check_installed()

    @staticmethod
    def check_source():
        """Check if tlgu imported, if not import it."""
        path_rel = '~/cltk_data/greek/software/tlgu/tlgu.h'
        path = os.path.expanduser(path_rel)
        if not os.path.isfile(path):
            try:
                corpus_importer = CorpusImporter('greek')
                corpus_importer.import_corpus('tlgu')
            except:
                logger.error('Failed to import TLGU.')
                sys.exit(1)

    @staticmethod
    def check_installed():
        """Check if tlgu installed, if not install it."""
        try:
            subprocess.check_output(['which', 'tlgu'])
        except:
            logger.info('TLGU not installed.')
            logger.info('Installing TLGU.')
            if not subprocess.check_output(['which', 'gcc']):
                logger.error('GCC seems not to be installed.')
            else:
                tlgu_path_rel = '~/cltk_data/greek/software/tlgu'
                tlgu_path = os.path.expanduser(tlgu_path_rel)
                try:
                    p_out = subprocess.call('cd %s && make install' % tlgu_path, shell=True)
                    if p_out == 0:
                        logger.info('TLGU installed.')
                    else:
                        logger.error('TLGU install without sudo failed.')
                except:
                    logger.error('TLGU install failed.')
                else: #  for Ubuntu and others needing root access to '/usr/local/bin'
                    p_out = subprocess.call('cd %s && sudo make install' % tlgu_path, shell=True)
                    if p_out == 0:
                        logger.info('TLGU installed.')
                    else:
                        logger.error('TLGU install with sudo failed.')
                        sys.exit(1)

    def convert(self, markup=None, break_lines=False, divide_works=False, latin=False, misc_args=None):
        tlgu_options = []
        if markup=='full':
            ['v', 'w', 'x', 'y', 'z']
        if break_lines:
            tlgu_options.append('N')
        if divide_works:
            tlgu_options.append('W')
        if latin:
            tlgu_options.append('r')
        if misc_args is None:
            misc_args = []
        else:
            try:
                misc_args = eval(misc_args)
            except:
                logger.error("Argument 'misc_args' must be a list.")
                sys.exit(1)
            [tlgu_options.append(x) for x in misc_args]
            misc_args = list(set(misc_args))


    '''
    def convert(self, input_path, markup='plain',
                break_lines=False, divide_works=False,
                output_path=None, opts=[]):
        # Add input and output paths
        paths = [input_path]
        if output_path:
            cltk_data.resolve_path(os.path.dirname(output_path))
            paths = [input_path, output_path]
        options.extend(paths)

        p = subprocess.Popen(options,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        output, err = p.communicate()
        return output.decode('utf-8')
        #return output

    def _run_combination_tests(self):
        # TODO: fix paths
        inp = '/Users/smargh/Code/cltk/cltk_data/originals/phi5/LAT1212.TXT'
        out = '/Users/smargh/Code/GitHub/tlgu/tlgu_tests/opts_{}'
        for l in range(len(ARGS.values())):
            i = itertools.combinations(ARGS.values(), l)
            for arg in list(i):
                args = list(arg)
                latin_args = args + ['-r']
                out_path = out.format(''.join(args).replace('-', ''))
                self.run(inp, out_path, opts=latin_args)
    '''

'''
if __name__ == '__main__':
    p = '/Users/smargh/Code/cltk/cltk_data/originals/tlg/LSTSCDCN.DIR'
    o = '/Users/smargh/Code/cltk/cltk_data/tlg_LSTSCDCN.txt'
    out = TLGU(p).convert('plain', True, False, output_path=o)
    print(out.encode('utf-8'))
'''
