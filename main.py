"""Copy entry.png to the grader output directory.

The entry image is a fixed file shipped in the same directory as this
program. The program copies it unchanged into the directory given by the
MAKEFUN_OUTPUT_DIR environment variable (default /output) and checks that
the copy has exactly the same size as the source, so repeated runs produce
identical bytes. No network, no randomness.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUT = os.path.join(OUT_DIR, "entry.png")

os.makedirs(OUT_DIR, exist_ok=True)
shutil.copyfile(SRC, OUT)

assert os.path.getsize(OUT) == os.path.getsize(SRC), "copy size mismatch"
