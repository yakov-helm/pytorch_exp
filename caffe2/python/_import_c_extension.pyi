import collections
from typing import Any, Dict, List, Optional, Protocol, Tuple, Union, overload

import numpy as np
import google.protobuf.message
import torch
from caffe2.proto import caffe2_pb2

from . import core

# pybind11 will automatically accept either Python str or bytes for C++ APIs
# that accept std::string.
_PybindStr = Union[str, bytes]
_PerOpEnginePrefType = Dict[int, Dict[str, List[str]]]
_EnginePrefType = Dict[int, List[str]]

Int8Tensor = collections.namedtuple("Int8Tensor", ["data", "scale", "zero_point"])

class _HasProto(Protocol):
    def Proto(self) -> Any: ...

class TensorCPU:
    def init(self, dims: List[int], caffe_type: int) -> None: ...
    def to_torch(self) -> torch.Tensor: ...

class Blob:
    def feed(
        self,
        arg: Any,
        device_option: Union[
            None,
            str,
            bytes,
            google.protobuf.message.Message,
            _HasProto,
        ] = None,
    ) -> bool: ...
    def is_tensor(self) -> bool: ...
    def as_tensor(self) -> TensorCPU: ...
    def tensor(self) -> TensorCPU: ...
    def to_torch(self) -> torch.Tensor: ...
    def fetch(self) -> Any: ...

class Net:
    def run(self) -> None: ...
    def cancel(self) -> None: ...

class Workspace:
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, workspace: "Workspace") -> None: ...
    @property
    def blobs(self) -> Dict[str, Blob]: ...
    def create_blob(self, name: _PybindStr) -> Blob: ...
    def fetch_blob(self, name: _PybindStr) -> Any: ...
    def fetch_int8_blob(
        self, name: Union[str, bytes, core.BlobReference]
    ) -> Int8Tensor: ...
    def _create_net(self, _def: bytes, overwrite: bool) -> Net: ...
    def create_net(
        self,
        net: Union[str, bytes, core.Net, caffe2_pb2.NetDef],
        overwrite: bool = False,
    ) -> Net: ...
    def _run_net(self, _def: bytes) -> None: ...
    def _run_operator(self, _def: bytes) -> None: ...
    def _run_plan(self, _def: bytes) -> None: ...
    def run(
        self,
        obj: Union[
            caffe2_pb2.PlanDef,
            caffe2_pb2.NetDef,
            caffe2_pb2.OperatorDef,
            _HasProto,
        ],
    ) -> None: ...
    def feed_blob(
        self,
        name: Union[str, bytes, core.BlobReference],
        arr: Union[caffe2_pb2.TensorProto, np.ndarray],
        device_option: Optional[caffe2_pb2.DeviceOption] = None,
    ) -> bool: ...
    def remove_blob(self, blob: Any) -> None: ...

    current: "Workspace"

class Argument:
    @property
    def name(self) -> str: ...
    @property
    def description(self) -> str: ...
    @property
    def required(self) -> bool: ...

class OpSchema:
    @staticmethod
    def get(key: str) -> "OpSchema": ...
    @property
    def args(self) -> List[Argument]: ...
    @property
    def input_desc(self) -> List[Tuple[str, str]]: ...
    @property
    def output_desc(self) -> List[Tuple[str, str]]: ...
    @property
    def max_input(self) -> int: ...
    @property
    def max_output(self) -> int: ...
    @property
    def min_input(self) -> int: ...
    @property
    def min_output(self) -> int: ...
    def inplace_enforced(self, x: int, y: int) -> bool: ...

class DummyName: ...
class Graph: ...
class Node: ...
class Edge: ...
class NeuralNetOperator: ...
class NeuralNetData: ...
class NNSubgraph: ...
class NNMatchGraph: ...
class Annotation: ...

is_asan: bool
has_mkldnn: bool
use_mkldnn: bool
has_fbgemm: bool
use_rocm: bool
use_trt: bool
define_caffe2_no_operator_schema: bool

def registered_dbs() -> List[str]: ...
def get_build_options() -> Dict[str, str]: ...
def set_per_op_engine_pref(pref: _PerOpEnginePrefType) -> None: ...
def set_global_engine_pref(pref: _EnginePrefType) -> None: ...
def set_engine_pref(
    per_op_pref: _PerOpEnginePrefType, global_pref: _EnginePrefType
) -> None: ...
def set_op_engine_pref(op_type: _PybindStr, op_pref: _EnginePrefType) -> None: ...
def op_registry_key(op_type: _PybindStr, engine: _PybindStr) -> str: ...
def global_init(args: List[str]) -> None: ...
def registered_operators() -> List[str]: ...
def on_module_exit() -> None: ...
@overload
def switch_workspace(ws: Workspace): ...
@overload
def switch_workspace(name: _PybindStr, create_if_missing: Optional[bool] = None): ...
def create_child_workspace(
    parent_ws_name: _PybindStr, child_ws_name: _PybindStr
) -> None: ...
def root_folder() -> str: ...
def current_workspace() -> str: ...
def workspaces() -> List[str]: ...
def benchmark_net(
    name: _PybindStr, warmup_runs: int, main_runs: int, run_individual: bool
) -> List[float]: ...
def benchmark_net_once(name: _PybindStr) -> float: ...
def blobs() -> Dict[str, Blob]: ...
def has_blob(name: _PybindStr) -> bool: ...
def create_blob(name: _PybindStr) -> bool: ...
def reset_blob(name: _PybindStr) -> None: ...
@overload
def deserialize_blob(content: _PybindStr) -> Blob: ...
@overload
def deserialize_blob(name: _PybindStr, serialized: bytes) -> None: ...
def serialize_blob(name: _PybindStr) -> bytes: ...
def get_stats() -> Dict[str, int]: ...
def is_numa_enabled() -> bool: ...
def get_num_numa_nodes() -> int: ...
def get_blob_numa_node(blob_name: _PybindStr) -> int: ...
def get_blob_size_bytes(blob_name: _PybindStr) -> int: ...
def create_offline_tensor(name: _PybindStr, dims: List[int], datatype: int) -> bool: ...
def fakeFp16FuseOps(net_str: bytes) -> bytes: ...
def num_cuda_devices() -> int: ...
def get_cuda_version() -> int: ...
def get_cudnn_version() -> int: ...
def get_gpu_memory_info(device_id: int) -> Tuple[int, int]: ...
def get_device_properties(deviceid: int) -> Dict[str, Any]: ...
def num_hip_devices() -> int: ...
def get_hip_version() -> int: ...
def get_miopen_version() -> int: ...

has_hip_support: bool
has_cuda_support: bool
has_gpu_support: bool
