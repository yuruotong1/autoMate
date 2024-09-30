# ------------------------------------------------------------------
# Copyright (c) 2024 PyInstaller Development Team.
#
# This file is distributed under the terms of the GNU General Public
# License (version 2.0 or later).
#
# The full license is available in LICENSE, distributed with
# this software.
#
# SPDX-License-Identifier: GPL-2.0-or-later
# ------------------------------------------------------------------

import os

from PyInstaller.utils.hooks import collect_data_files, get_module_attribute, logger

# Collect the headers (eccodes.h, gribapi.h) that are bundled with the package.
datas = collect_data_files('gribapi')

# Collect the eccodes shared library
binaries = []
try:
    library_path = get_module_attribute('gribapi.bindings', 'library_path')
except Exception:
    logger.warning("hook-gribapi: failed to query gribapi.bindings.library_path!", exc_info=True)
    library_path = None

if library_path:
    if not os.path.isabs(library_path):
        from PyInstaller.depend.utils import _resolveCtypesImports
        resolved_binary = _resolveCtypesImports([os.path.basename(library_path)])
        if resolved_binary:
            library_path = resolved_binary[0][1]
        else:
            logger.warning("hook-gribapi: failed to resolve shared library name %r!", library_path)
            library_path = None
else:
    logger.warning("hook-gribapi: could not determine path to eccodes shared library!")

if library_path:
    logger.debug("hook-gribapi: collecting eccodes shared library: %r", library_path)
    binaries.append((library_path, '.'))
