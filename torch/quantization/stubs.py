# flake8: noqa: F401
r"""
This file is in the process of migration to `torch/ao/quantization`, and
is kept here for compatibility while the migration process is ongoing.
If you are adding a new entry/functionality, please, add it to the
`torch/ao/quantization/stubs.py`, while adding an import statement
here.
"""

from torch.ao.quantization.stubs import QuantStub, DeQuantStub, QuantWrapper
