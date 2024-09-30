# ------------------------------------------------------------------
# Copyright (c) 2020 PyInstaller Development Team.
#
# This file is distributed under the terms of the GNU General Public
# License (version 2.0 or later).
#
# The full license is available in LICENSE, distributed with
# this software.
#
# SPDX-License-Identifier: GPL-2.0-or-later
# ------------------------------------------------------------------

import sys
import os

# Force CPU
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

# Display only warnings and errors
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# tensorflow 2.16 and keras 3.0 upgraded the interactive progress bar (displayed during dataset download, during model
# fitting, etc.) with fancier version that uses Unicode arrows (←). For this to work, `sys.stdout` must be using utf-8
# encoding. As per https://docs.python.org/3/library/sys.html#sys.stdout, on Windows, python defaults to using utf-8
# for the console device. However, non-character devices such as pipes use the system locale encoding (i.e. the ANSI
# codepage). PyInstaller's `pyi_builder` test fixture runs the build executable via `subprocess.Popen` with stdout
# and stderr redirected to pipes, so the embedded interpreter in the frozen test application ends up using system
# locale encoding (e.g., cp1252) instead of utf-8 for `sys.stdout` and `sys.stderr`. In contrast to unfrozen python,
# the encoding cannot be overridden by the calling process via `PYTHONIOENCODING` environment variable when starting
# the application (sub)process. However, we can reconfigure the encoding on the stream objects here, in the application
# itself. Which, everything considered, is the sanest place to do so.
if sys.stdout.encoding != 'utf8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf8':
    sys.stderr.reconfigure(encoding='utf-8')

# Begin test - import tensorflow after environment variables are set
import tensorflow as tf  # noqa: E402

# Load and normalize the dataset
mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

# Define model...
model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10)
])

# ... and loss function
loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

# Train
model.compile(optimizer='adam', loss=loss_fn, metrics=['accuracy'])
model.fit(x_train, y_train, epochs=1, verbose=1)

# Evaluate
results = model.evaluate(x_test, y_test, verbose=1)

# Expected accuracy after a single epoch is around 95%, so use 90%
# as a passing bar
assert results[1] >= 0.90, "Resulting accuracy on validation set too low!"
