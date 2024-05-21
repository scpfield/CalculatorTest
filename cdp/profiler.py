# DO NOT EDIT THIS FILE!
#
# This file is generated from the CDP specification. If you need to make
# changes, edit the generator and regenerate all of the modules.
#
# CDP domain: Profiler

from __future__ import annotations
import enum
import typing
from dataclasses import dataclass
from .util import event_class, T_JSON_DICT

from . import debugger
from . import runtime


@dataclass
class ProfileNode:
    '''
    Profile node. Holds callsite information, execution statistics and child nodes.
    '''
    #: Unique id of the node.
    id_: int

    #: Function location.
    call_frame: runtime.CallFrame

    #: Number of samples where this node was on top of the call stack.
    hit_count: typing.Optional[int] = None

    #: Child node ids.
    children: typing.Optional[typing.List[int]] = None

    #: The reason of being not optimized. The function may be deoptimized or marked as don't
    #: optimize.
    deopt_reason: typing.Optional[str] = None

    #: An array of source position ticks.
    position_ticks: typing.Optional[typing.List[PositionTickInfo]] = None

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['id'] = self.id_
        json['callFrame'] = self.call_frame.to_json()
        if self.hit_count is not None:
            json['hitCount'] = self.hit_count
        if self.children is not None:
            json['children'] = [i for i in self.children]
        if self.deopt_reason is not None:
            json['deoptReason'] = self.deopt_reason
        if self.position_ticks is not None:
            json['positionTicks'] = [i.to_json() for i in self.position_ticks]
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ProfileNode:
        return cls(
            id_=int(json['id']),
            call_frame=runtime.CallFrame.from_json(json['callFrame']),
            hit_count=int(json['hitCount']) if json.get('hitCount', None) is not None else None,
            children=[int(i) for i in json['children']] if json.get('children', None) is not None else None,
            deopt_reason=str(json['deoptReason']) if json.get('deoptReason', None) is not None else None,
            position_ticks=[PositionTickInfo.from_json(i) for i in json['positionTicks']] if json.get('positionTicks', None) is not None else None,
        )


@dataclass
class Profile:
    '''
    Profile.
    '''
    #: The list of profile nodes. First item is the root node.
    nodes: typing.List[ProfileNode]

    #: Profiling start timestamp in microseconds.
    start_time: float

    #: Profiling end timestamp in microseconds.
    end_time: float

    #: Ids of samples top nodes.
    samples: typing.Optional[typing.List[int]] = None

    #: Time intervals between adjacent samples in microseconds. The first delta is relative to the
    #: profile startTime.
    time_deltas: typing.Optional[typing.List[int]] = None

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['nodes'] = [i.to_json() for i in self.nodes]
        json['startTime'] = self.start_time
        json['endTime'] = self.end_time
        if self.samples is not None:
            json['samples'] = [i for i in self.samples]
        if self.time_deltas is not None:
            json['timeDeltas'] = [i for i in self.time_deltas]
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Profile:
        return cls(
            nodes=[ProfileNode.from_json(i) for i in json['nodes']],
            start_time=float(json['startTime']),
            end_time=float(json['endTime']),
            samples=[int(i) for i in json['samples']] if json.get('samples', None) is not None else None,
            time_deltas=[int(i) for i in json['timeDeltas']] if json.get('timeDeltas', None) is not None else None,
        )


@dataclass
class PositionTickInfo:
    '''
    Specifies a number of samples attributed to a certain source position.
    '''
    #: Source line number (1-based).
    line: int

    #: Number of samples attributed to the source line.
    ticks: int

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['line'] = self.line
        json['ticks'] = self.ticks
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PositionTickInfo:
        return cls(
            line=int(json['line']),
            ticks=int(json['ticks']),
        )


@dataclass
class CoverageRange:
    '''
    Coverage data for a source range.
    '''
    #: JavaScript script source offset for the range start.
    start_offset: int

    #: JavaScript script source offset for the range end.
    end_offset: int

    #: Collected execution count of the source range.
    count: int

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['startOffset'] = self.start_offset
        json['endOffset'] = self.end_offset
        json['count'] = self.count
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> CoverageRange:
        return cls(
            start_offset=int(json['startOffset']),
            end_offset=int(json['endOffset']),
            count=int(json['count']),
        )


@dataclass
class FunctionCoverage:
    '''
    Coverage data for a JavaScript function.
    '''
    #: JavaScript function name.
    function_name: str

    #: Source ranges inside the function with coverage data.
    ranges: typing.List[CoverageRange]

    #: Whether coverage data for this function has block granularity.
    is_block_coverage: bool

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['functionName'] = self.function_name
        json['ranges'] = [i.to_json() for i in self.ranges]
        json['isBlockCoverage'] = self.is_block_coverage
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> FunctionCoverage:
        return cls(
            function_name=str(json['functionName']),
            ranges=[CoverageRange.from_json(i) for i in json['ranges']],
            is_block_coverage=bool(json['isBlockCoverage']),
        )


@dataclass
class ScriptCoverage:
    '''
    Coverage data for a JavaScript script.
    '''
    #: JavaScript script id.
    script_id: runtime.ScriptId

    #: JavaScript script name or url.
    url: str

    #: Functions contained in the script that has coverage data.
    functions: typing.List[FunctionCoverage]

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['scriptId'] = self.script_id.to_json()
        json['url'] = self.url
        json['functions'] = [i.to_json() for i in self.functions]
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ScriptCoverage:
        return cls(
            script_id=runtime.ScriptId.from_json(json['scriptId']),
            url=str(json['url']),
            functions=[FunctionCoverage.from_json(i) for i in json['functions']],
        )


def disable() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:

    cmd_dict: T_JSON_DICT = {
        'method': 'Profiler.disable',
    }
    json = yield cmd_dict


def enable() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:

    cmd_dict: T_JSON_DICT = {
        'method': 'Profiler.enable',
    }
    json = yield cmd_dict


def get_best_effort_coverage() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,typing.List[ScriptCoverage]]:
    '''
    Collect coverage data for the current isolate. The coverage data may be incomplete due to
    garbage collection.

    :returns: Coverage data for the current isolate.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'Profiler.getBestEffortCoverage',
    }
    json = yield cmd_dict
    return [ScriptCoverage.from_json(i) for i in json['result']]


def set_sampling_interval(
        interval: int
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Changes CPU profiler sampling interval. Must be called before CPU profiles recording started.

    :param interval: New sampling interval in microseconds.
    '''
    params: T_JSON_DICT = dict()
    params['interval'] = interval
    cmd_dict: T_JSON_DICT = {
        'method': 'Profiler.setSamplingInterval',
        'params': params,
    }
    json = yield cmd_dict


def start() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:

    cmd_dict: T_JSON_DICT = {
        'method': 'Profiler.start',
    }
    json = yield cmd_dict


def start_precise_coverage(
        call_count: typing.Optional[bool] = None,
        detailed: typing.Optional[bool] = None,
        allow_triggered_updates: typing.Optional[bool] = None
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,float]:
    '''
    Enable precise code coverage. Coverage data for JavaScript executed before enabling precise code
    coverage may be incomplete. Enabling prevents running optimized code and resets execution
    counters.

    :param call_count: *(Optional)* Collect accurate call counts beyond simple 'covered' or 'not covered'.
    :param detailed: *(Optional)* Collect block-based coverage.
    :param allow_triggered_updates: *(Optional)* Allow the backend to send updates on its own initiative
    :returns: Monotonically increasing time (in seconds) when the coverage update was taken in the backend.
    '''
    params: T_JSON_DICT = dict()
    if call_count is not None:
        params['callCount'] = call_count
    if detailed is not None:
        params['detailed'] = detailed
    if allow_triggered_updates is not None:
        params['allowTriggeredUpdates'] = allow_triggered_updates
    cmd_dict: T_JSON_DICT = {
        'method': 'Profiler.startPreciseCoverage',
        'params': params,
    }
    json = yield cmd_dict
    return float(json['timestamp'])


def stop() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,Profile]:
    '''


    :returns: Recorded profile.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'Profiler.stop',
    }
    json = yield cmd_dict
    return Profile.from_json(json['profile'])


def stop_precise_coverage() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Disable precise code coverage. Disabling releases unnecessary execution count records and allows
    executing optimized code.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'Profiler.stopPreciseCoverage',
    }
    json = yield cmd_dict


def take_precise_coverage() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,typing.Tuple[typing.List[ScriptCoverage], float]]:
    '''
    Collect coverage data for the current isolate, and resets execution counters. Precise code
    coverage needs to have started.

    :returns: A tuple with the following items:

        0. **result** - Coverage data for the current isolate.
        1. **timestamp** - Monotonically increasing time (in seconds) when the coverage update was taken in the backend.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'Profiler.takePreciseCoverage',
    }
    json = yield cmd_dict
    return (
        [ScriptCoverage.from_json(i) for i in json['result']],
        float(json['timestamp'])
    )


@event_class('Profiler.consoleProfileFinished')
@dataclass
class ConsoleProfileFinished:
    id_: str
    #: Location of console.profileEnd().
    location: debugger.Location
    profile: Profile
    #: Profile title passed as an argument to console.profile().
    title: typing.Optional[str]

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ConsoleProfileFinished:
        return cls(
            id_=str(json['id']),
            location=debugger.Location.from_json(json['location']),
            profile=Profile.from_json(json['profile']),
            title=str(json['title']) if json.get('title', None) is not None else None
        )


@event_class('Profiler.consoleProfileStarted')
@dataclass
class ConsoleProfileStarted:
    '''
    Sent when new profile recording is started using console.profile() call.
    '''
    id_: str
    #: Location of console.profile().
    location: debugger.Location
    #: Profile title passed as an argument to console.profile().
    title: typing.Optional[str]

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ConsoleProfileStarted:
        return cls(
            id_=str(json['id']),
            location=debugger.Location.from_json(json['location']),
            title=str(json['title']) if json.get('title', None) is not None else None
        )


@event_class('Profiler.preciseCoverageDeltaUpdate')
@dataclass
class PreciseCoverageDeltaUpdate:
    '''
    **EXPERIMENTAL**

    Reports coverage delta since the last poll (either from an event like this, or from
    ``takePreciseCoverage`` for the current isolate. May only be sent if precise code
    coverage has been started. This event can be trigged by the embedder to, for example,
    trigger collection of coverage data immediately at a certain point in time.
    '''
    #: Monotonically increasing time (in seconds) when the coverage update was taken in the backend.
    timestamp: float
    #: Identifier for distinguishing coverage events.
    occasion: str
    #: Coverage data for the current isolate.
    result: typing.List[ScriptCoverage]

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PreciseCoverageDeltaUpdate:
        return cls(
            timestamp=float(json['timestamp']),
            occasion=str(json['occasion']),
            result=[ScriptCoverage.from_json(i) for i in json['result']]
        )
