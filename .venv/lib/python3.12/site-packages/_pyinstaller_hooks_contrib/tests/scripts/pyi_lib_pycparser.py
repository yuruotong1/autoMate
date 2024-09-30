# -----------------------------------------------------------------------------
# Copyright (c) 2014-2020, PyInstaller Development Team.
#
# This file is distributed under the terms of the GNU General Public
# License (version 2.0 or later).
#
# The full license is available in LICENSE, distributed with
# this software.
#
# SPDX-License-Identifier: GPL-2.0-or-later
# -----------------------------------------------------------------------------

import os

fnames_to_track = [
    'lextab.py',
    'yacctab.py',
]


def fnames_found():
    return [fname for fname in fnames_to_track if os.path.isfile(fname)]


if __name__ == '__main__':

    # Confirm no files exist before we start.
    if fnames_found():
        raise SystemExit('FAIL: Files present before test.')

    # Minimal invocation that generates the files.
    from pycparser import c_parser
    parser = c_parser.CParser()

    # Were the files generated?
    fnames_generated = fnames_found()

    # Try to remove them, if so.
    for fname in fnames_generated:
        try:
            os.unlink(fname)
        except OSError:
            pass

    # Did we fail at deleting any file?
    fnames_left = fnames_found()

    # Fail if any file was generated.
    if fnames_generated:
        if fnames_left:
            raise SystemExit('FAIL: Files generated and not removed.')
        else:
            raise SystemExit('FAIL: Files generated but removed.')

    # Success.
