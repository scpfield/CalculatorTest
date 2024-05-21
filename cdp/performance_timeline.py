# DO NOT EDIT THIS FILE!
#
# This file is generated from the CDP specification. If you need to make
# changes, edit the generator and regenerate all of the modules.
#
# CDP domain: PerformanceTimeline (experimental)

from __future__ import annotations
import enum
import typing
from dataclasses import dataclass
from .util import event_class, T_JSON_DICT

from . import dom
from . import network
from . import page


@dataclass
class LargestContentfulPaint:
    '''
    See https://github.com/WICG/LargestContentfulPaint and largest_contentful_paint.idl
    '''
    render_time: network.TimeSinceEpoch

    load_time: network.TimeSinceEpoch

    #: The number of pixels being painted.
    size: float

    #: The id attribute of the element, if available.
    element_id: typing.Optional[str] = None

    #: The URL of the image (may be trimmed).
    url: typing.Optional[str] = None

    node_id: typing.Optional[dom.BackendNodeId] = None

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['renderTime'] = self.render_time.to_json()
        json['loadTime'] = self.load_time.to_json()
        json['size'] = self.size
        if self.element_id is not None:
            json['elementId'] = self.element_id
        if self.url is not None:
            json['url'] = self.url
        if self.node_id is not None:
            json['nodeId'] = self.node_id.to_json()
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> LargestContentfulPaint:
        return cls(
            render_time=network.TimeSinceEpoch.from_json(json['renderTime']),
            load_time=network.TimeSinceEpoch.from_json(json['loadTime']),
            size=float(json['size']),
            element_id=str(json['elementId']) if json.get('elementId', None) is not None else None,
            url=str(json['url']) if json.get('url', None) is not None else None,
            node_id=dom.BackendNodeId.from_json(json['nodeId']) if json.get('nodeId', None) is not None else None,
        )


@dataclass
class LayoutShiftAttribution:
    previous_rect: dom.Rect

    current_rect: dom.Rect

    node_id: typing.Optional[dom.BackendNodeId] = None

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['previousRect'] = self.previous_rect.to_json()
        json['currentRect'] = self.current_rect.to_json()
        if self.node_id is not None:
            json['nodeId'] = self.node_id.to_json()
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> LayoutShiftAttribution:
        return cls(
            previous_rect=dom.Rect.from_json(json['previousRect']),
            current_rect=dom.Rect.from_json(json['currentRect']),
            node_id=dom.BackendNodeId.from_json(json['nodeId']) if json.get('nodeId', None) is not None else None,
        )


@dataclass
class LayoutShift:
    '''
    See https://wicg.github.io/layout-instability/#sec-layout-shift and layout_shift.idl
    '''
    #: Score increment produced by this event.
    value: float

    had_recent_input: bool

    last_input_time: network.TimeSinceEpoch

    sources: typing.List[LayoutShiftAttribution]

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['value'] = self.value
        json['hadRecentInput'] = self.had_recent_input
        json['lastInputTime'] = self.last_input_time.to_json()
        json['sources'] = [i.to_json() for i in self.sources]
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> LayoutShift:
        return cls(
            value=float(json['value']),
            had_recent_input=bool(json['hadRecentInput']),
            last_input_time=network.TimeSinceEpoch.from_json(json['lastInputTime']),
            sources=[LayoutShiftAttribution.from_json(i) for i in json['sources']],
        )


@dataclass
class TimelineEvent:
    #: Identifies the frame that this event is related to. Empty for non-frame targets.
    frame_id: page.FrameId

    #: The event type, as specified in https://w3c.github.io/performance-timeline/#dom-performanceentry-entrytype
    #: This determines which of the optional "details" fields is present.
    type_: str

    #: Name may be empty depending on the type.
    name: str

    #: Time in seconds since Epoch, monotonically increasing within document lifetime.
    time: network.TimeSinceEpoch

    #: Event duration, if applicable.
    duration: typing.Optional[float] = None

    lcp_details: typing.Optional[LargestContentfulPaint] = None

    layout_shift_details: typing.Optional[LayoutShift] = None

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['frameId'] = self.frame_id.to_json()
        json['type'] = self.type_
        json['name'] = self.name
        json['time'] = self.time.to_json()
        if self.duration is not None:
            json['duration'] = self.duration
        if self.lcp_details is not None:
            json['lcpDetails'] = self.lcp_details.to_json()
        if self.layout_shift_details is not None:
            json['layoutShiftDetails'] = self.layout_shift_details.to_json()
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> TimelineEvent:
        return cls(
            frame_id=page.FrameId.from_json(json['frameId']),
            type_=str(json['type']),
            name=str(json['name']),
            time=network.TimeSinceEpoch.from_json(json['time']),
            duration=float(json['duration']) if json.get('duration', None) is not None else None,
            lcp_details=LargestContentfulPaint.from_json(json['lcpDetails']) if json.get('lcpDetails', None) is not None else None,
            layout_shift_details=LayoutShift.from_json(json['layoutShiftDetails']) if json.get('layoutShiftDetails', None) is not None else None,
        )


def enable(
        event_types: typing.List[str]
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Previously buffered events would be reported before method returns.
    See also: timelineEventAdded

    :param event_types: The types of event to report, as specified in https://w3c.github.io/performance-timeline/#dom-performanceentry-entrytype The specified filter overrides any previous filters, passing empty filter disables recording. Note that not all types exposed to the web platform are currently supported.
    '''
    params: T_JSON_DICT = dict()
    params['eventTypes'] = [i for i in event_types]
    cmd_dict: T_JSON_DICT = {
        'method': 'PerformanceTimeline.enable',
        'params': params,
    }
    json = yield cmd_dict


@event_class('PerformanceTimeline.timelineEventAdded')
@dataclass
class TimelineEventAdded:
    '''
    Sent when a performance timeline event is added. See reportPerformanceTimeline method.
    '''
    event: TimelineEvent

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> TimelineEventAdded:
        return cls(
            event=TimelineEvent.from_json(json['event'])
        )
