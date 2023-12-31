#!/usr/bin/env python3
from pathlib import Path
from vunit import VUnit

ROOT = Path(__file__).parent

VU = VUnit.from_argv()
VU.add_vhdl_builtins()

LIB = VU.add_library("lib")
LIB.add_source_files(ROOT / "*.vhdl")
LIB.add_source_files(ROOT.parent / "src" / "*.vhdl")

VU.main()
