# DO NOT EDIT THIS FILE!
#
# This file is generated from the CDP specification. If you need to make
# changes, edit the generator and regenerate all of the modules.
#
# CDP domain: LayerTree (experimental)

from __future__ import annotations
import enum
import typing
from dataclasses import dataclass
from .util import event_class, T_JSON_DICT

from . import dom


class LayerId(str):
    '''
    Unique Layer identifier.
    '''
    def to_json(self) -> str:
        return self

    @classmethod
    def from_json(cls, json: str) -> LayerId:
        return cls(json)

    def __repr__(self):
        return 'LayerId({})'.format(super().__repr__())


class SnapshotId(str):
    '''
    Unique snapshot identifier.
    '''
    def to_json(self) -> str:
        return self

    @classmethod
    def from_json(cls, json: str) -> SnapshotId:
        return cls(json)

    def __repr__(self):
        return 'SnapshotId({})'.format(super().__repr__())


@dataclass
class ScrollRect:
    '''
    Rectangle where scrolling happens on the main thread.
    '''
    #: Rectangle itself.
    rect: dom.Rect

    #: Reason for rectangle to force scrolling on the main thread
    type_: str

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['rect'] = self.rect.to_json()
        json['type'] = self.type_
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> ScrollRect:
        return cls(
            rect=dom.Rect.from_json(json['rect']),
            type_=str(json['type']),
        )


@dataclass
class StickyPositionConstraint:
    '''
    Sticky position constraints.
    '''
    #: Layout rectangle of the sticky element before being shifted
    sticky_box_rect: dom.Rect

    #: Layout rectangle of the containing block of the sticky element
    containing_block_rect: dom.Rect

    #: The nearest sticky layer that shifts the sticky box
    nearest_layer_shifting_sticky_box: typing.Optional[LayerId] = None

    #: The nearest sticky layer that shifts the containing block
    nearest_layer_shifting_containing_block: typing.Optional[LayerId] = None

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['stickyBoxRect'] = self.sticky_box_rect.to_json()
        json['containingBlockRect'] = self.containing_block_rect.to_json()
        if self.nearest_layer_shifting_sticky_box is not None:
            json['nearestLayerShiftingStickyBox'] = self.nearest_layer_shifting_sticky_box.to_json()
        if self.nearest_layer_shifting_containing_block is not None:
            json['nearestLayerShiftingContainingBlock'] = self.nearest_layer_shifting_containing_block.to_json()
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> StickyPositionConstraint:
        return cls(
            sticky_box_rect=dom.Rect.from_json(json['stickyBoxRect']),
            containing_block_rect=dom.Rect.from_json(json['containingBlockRect']),
            nearest_layer_shifting_sticky_box=LayerId.from_json(json['nearestLayerShiftingStickyBox']) if json.get('nearestLayerShiftingStickyBox', None) is not None else None,
            nearest_layer_shifting_containing_block=LayerId.from_json(json['nearestLayerShiftingContainingBlock']) if json.get('nearestLayerShiftingContainingBlock', None) is not None else None,
        )


@dataclass
class PictureTile:
    '''
    Serialized fragment of layer picture along with its offset within the layer.
    '''
    #: Offset from owning layer left boundary
    x: float

    #: Offset from owning layer top boundary
    y: float

    #: Base64-encoded snapshot data. (Encoded as a base64 string when passed over JSON)
    picture: str

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['x'] = self.x
        json['y'] = self.y
        json['picture'] = self.picture
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> PictureTile:
        return cls(
            x=float(json['x']),
            y=float(json['y']),
            picture=str(json['picture']),
        )


@dataclass
class Layer:
    '''
    Information about a compositing layer.
    '''
    #: The unique id for this layer.
    layer_id: LayerId

    #: Offset from parent layer, X coordinate.
    offset_x: float

    #: Offset from parent layer, Y coordinate.
    offset_y: float

    #: Layer width.
    width: float

    #: Layer height.
    height: float

    #: Indicates how many time this layer has painted.
    paint_count: int

    #: Indicates whether this layer hosts any content, rather than being used for
    #: transform/scrolling purposes only.
    draws_content: bool

    #: The id of parent (not present for root).
    parent_layer_id: typing.Optional[LayerId] = None

    #: The backend id for the node associated with this layer.
    backend_node_id: typing.Optional[dom.BackendNodeId] = None

    #: Transformation matrix for layer, default is identity matrix
    transform: typing.Optional[typing.List[float]] = None

    #: Transform anchor point X, absent if no transform specified
    anchor_x: typing.Optional[float] = None

    #: Transform anchor point Y, absent if no transform specified
    anchor_y: typing.Optional[float] = None

    #: Transform anchor point Z, absent if no transform specified
    anchor_z: typing.Optional[float] = None

    #: Set if layer is not visible.
    invisible: typing.Optional[bool] = None

    #: Rectangles scrolling on main thread only.
    scroll_rects: typing.Optional[typing.List[ScrollRect]] = None

    #: Sticky position constraint information
    sticky_position_constraint: typing.Optional[StickyPositionConstraint] = None

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['layerId'] = self.layer_id.to_json()
        json['offsetX'] = self.offset_x
        json['offsetY'] = self.offset_y
        json['width'] = self.width
        json['height'] = self.height
        json['paintCount'] = self.paint_count
        json['drawsContent'] = self.draws_content
        if self.parent_layer_id is not None:
            json['parentLayerId'] = self.parent_layer_id.to_json()
        if self.backend_node_id is not None:
            json['backendNodeId'] = self.backend_node_id.to_json()
        if self.transform is not None:
            json['transform'] = [i for i in self.transform]
        if self.anchor_x is not None:
            json['anchorX'] = self.anchor_x
        if self.anchor_y is not None:
            json['anchorY'] = self.anchor_y
        if self.anchor_z is not None:
            json['anchorZ'] = self.anchor_z
        if self.invisible is not None:
            json['invisible'] = self.invisible
        if self.scroll_rects is not None:
            json['scrollRects'] = [i.to_json() for i in self.scroll_rects]
        if self.sticky_position_constraint is not None:
            json['stickyPositionConstraint'] = self.sticky_position_constraint.to_json()
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Layer:
        return cls(
            layer_id=LayerId.from_json(json['layerId']),
            offset_x=float(json['offsetX']),
            offset_y=float(json['offsetY']),
            width=float(json['width']),
            height=float(json['height']),
            paint_count=int(json['paintCount']),
            draws_content=bool(json['drawsContent']),
            parent_layer_id=LayerId.from_json(json['parentLayerId']) if json.get('parentLayerId', None) is not None else None,
            backend_node_id=dom.BackendNodeId.from_json(json['backendNodeId']) if json.get('backendNodeId', None) is not None else None,
            transform=[float(i) for i in json['transform']] if json.get('transform', None) is not None else None,
            anchor_x=float(json['anchorX']) if json.get('anchorX', None) is not None else None,
            anchor_y=float(json['anchorY']) if json.get('anchorY', None) is not None else None,
            anchor_z=float(json['anchorZ']) if json.get('anchorZ', None) is not None else None,
            invisible=bool(json['invisible']) if json.get('invisible', None) is not None else None,
            scroll_rects=[ScrollRect.from_json(i) for i in json['scrollRects']] if json.get('scrollRects', None) is not None else None,
            sticky_position_constraint=StickyPositionConstraint.from_json(json['stickyPositionConstraint']) if json.get('stickyPositionConstraint', None) is not None else None,
        )


class PaintProfile(list):
    '''
    Array of timings, one per paint step.
    '''
    def to_json(self) -> typing.List[float]:
        return self

    @classmethod
    def from_json(cls, json: typing.List[float]) -> PaintProfile:
        return cls(json)

    def __repr__(self):
        return 'PaintProfile({})'.format(super().__repr__())


def compositing_reasons(
        layer_id: LayerId
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,typing.Tuple[typing.List[str], typing.List[str]]]:
    '''
    Provides the reasons why the given layer was composited.

    :param layer_id: The id of the layer for which we want to get the reasons it was composited.
    :returns: A tuple with the following items:

        0. **compositingReasons** - A list of strings specifying reasons for the given layer to become composited.
        1. **compositingReasonIds** - A list of strings specifying reason IDs for the given layer to become composited.
    '''
    params: T_JSON_DICT = dict()
    params['layerId'] = layer_id.to_json()
    cmd_dict: T_JSON_DICT = {
        'method': 'LayerTree.compositingReasons',
        'params': params,
    }
    json = yield cmd_dict
    return (
        [str(i) for i in json['compositingReasons']],
        [str(i) for i in json['compositingReasonIds']]
    )


def disable() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Disables compositing tree inspection.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'LayerTree.disable',
    }
    json = yield cmd_dict


def enable() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Enables compositing tree inspection.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'LayerTree.enable',
    }
    json = yield cmd_dict


def load_snapshot(
        tiles: typing.List[PictureTile]
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,SnapshotId]:
    '''
    Returns the snapshot identifier.

    :param tiles: An array of tiles composing the snapshot.
    :returns: The id of the snapshot.
    '''
    params: T_JSON_DICT = dict()
    params['tiles'] = [i.to_json() for i in tiles]
    cmd_dict: T_JSON_DICT = {
        'method': 'LayerTree.loadSnapshot',
        'params': params,
    }
    json = yield cmd_dict
    return SnapshotId.from_json(json['snapshotId'])


def make_snapshot(
        layer_id: LayerId
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,SnapshotId]:
    '''
    Returns the layer snapshot identifier.

    :param layer_id: The id of the layer.
    :returns: The id of the layer snapshot.
    '''
    params: T_JSON_DICT = dict()
    params['layerId'] = layer_id.to_json()
    cmd_dict: T_JSON_DICT = {
        'method': 'LayerTree.makeSnapshot',
        'params': params,
    }
    json = yield cmd_dict
    return SnapshotId.from_json(json['snapshotId'])


def profile_snapshot(
        snapshot_id: SnapshotId,
        min_repeat_count: typing.Optional[int] = None,
        min_duration: typing.Optional[float] = None,
        clip_rect: typing.Optional[dom.Rect] = None
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,typing.List[PaintProfile]]:
    '''
    :param snapshot_id: The id of the layer snapshot.
    :param min_repeat_count: *(Optional)* The maximum number of times to replay the snapshot (1, if not specified).
    :param min_duration: *(Optional)* The minimum duration (in seconds) to replay the snapshot.
    :param clip_rect: *(Optional)* The clip rectangle to apply when replaying the snapshot.
    :returns: The array of paint profiles, one per run.
    '''
    params: T_JSON_DICT = dict()
    params['snapshotId'] = snapshot_id.to_json()
    if min_repeat_count is not None:
        params['minRepeatCount'] = min_repeat_count
    if min_duration is not None:
        params['minDuration'] = min_duration
    if clip_rect is not None:
        params['clipRect'] = clip_rect.to_json()
    cmd_dict: T_JSON_DICT = {
        'method': 'LayerTree.profileSnapshot',
        'params': params,
    }
    json = yield cmd_dict
    return [PaintProfile.from_json(i) for i in json['timings']]


def release_snapshot(
        snapshot_id: SnapshotId
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Releases layer snapshot captured by the back-end.

    :param snapshot_id: The id of the layer snapshot.
    '''
    params: T_JSON_DICT = dict()
    params['snapshotId'] = snapshot_id.to_json()
    cmd_dict: T_JSON_DICT = {
        'method': 'LayerTree.releaseSnapshot',
        'params': params,
    }
    json = yield cmd_dict


def replay_snapshot(
        snapshot_id: SnapshotId,
        from_step: typing.Optional[int] = None,
        to_step: typing.Optional[int] = None,
        scale: typing.Optional[float] = None
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,str]:
    '''
    Replays the layer snapshot and returns the resulting bitmap.

    :param snapshot_id: The id of the layer snapshot.
    :param from_step: *(Optional)* The first step to replay from (replay from the very start if not specified).
    :param to_step: *(Optional)* The last step to replay to (replay till the end if not specified).
    :param scale: *(Optional)* The scale to apply while replaying (defaults to 1).
    :returns: A data: URL for resulting image.
    '''
    params: T_JSON_DICT = dict()
    params['snapshotId'] = snapshot_id.to_json()
    if from_step is not None:
        params['fromStep'] = from_step
    if to_step is not None:
        params['toStep'] = to_step
    if scale is not None:
        params['scale'] = scale
    cmd_dict: T_JSON_DICT = {
        'method': 'LayerTree.replaySnapshot',
        'params': params,
    }
    json = yield cmd_dict
    return str(json['dataURL'])


def snapshot_command_log(
        snapshot_id: SnapshotId
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,typing.List[dict]]:
    '''
    Replays the layer snapshot and returns canvas log.

    :param snapshot_id: The id of the layer snapshot.
    :returns: The array of canvas function calls.
    '''
    params: T_JSON_DICT = dict()
    params['snapshotId'] = snapshot_id.to_json()
    cmd_dict: T_JSON_DICT = {
        'method': 'LayerTree.snapshotCommandLog',
        'params': params,
    }
    json = yield cmd_dict
    return [dict(i) for i in json['commandLog']]


@event_class('LayerTree.layerPainted')
@dataclass
class LayerPainted:
    #: The id of the painted layer.
    layer_id: LayerId
    #: Clip rectangle.
    clip: dom.Rect

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> LayerPainted:
        return cls(
            layer_id=LayerId.from_json(json['layerId']),
            clip=dom.Rect.from_json(json['clip'])
        )


@event_class('LayerTree.layerTreeDidChange')
@dataclass
class LayerTreeDidChange:
    #: Layer tree, absent if not in the compositing mode.
    layers: typing.Optional[typing.List[Layer]]

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> LayerTreeDidChange:
        return cls(
            layers=[Layer.from_json(i) for i in json['layers']] if json.get('layers', None) is not None else None
        )
