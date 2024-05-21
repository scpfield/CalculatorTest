# DO NOT EDIT THIS FILE!
#
# This file is generated from the CDP specification. If you need to make
# changes, edit the generator and regenerate all of the modules.
#
# CDP domain: Performance

from __future__ import annotations
import enum
import typing
from dataclasses import dataclass
from .util import event_class, T_JSON_DICT


from deprecated.sphinx import deprecated # type: ignore


@dataclass
class Metric:
    '''
    Run-time execution metric.
    '''
    #: Metric name.
    name: str

    #: Metric value.
    value: float

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['name'] = self.name
        json['value'] = self.value
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Metric:
        return cls(
            name=str(json['name']),
            value=float(json['value']),
        )


def disable() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Disable collecting and reporting metrics.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'Performance.disable',
    }
    json = yield cmd_dict


def enable(
        time_domain: typing.Optional[str] = None
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Enable collecting and reporting metrics.

    :param time_domain: *(Optional)* Time domain to use for collecting and reporting duration metrics.
    '''
    params: T_JSON_DICT = dict()
    if time_domain is not None:
        params['timeDomain'] = time_domain
    cmd_dict: T_JSON_DICT = {
        'method': 'Performance.enable',
        'params': params,
    }
    json = yield cmd_dict


@deprecated(version="1.3")
def set_time_domain(
        time_domain: str
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Sets time domain to use for collecting and reporting duration metrics.
    Note that this must be called before enabling metrics collection. Calling
    this method while metrics collection is enabled returns an error.

    .. deprecated:: 1.3

    **EXPERIMENTAL**

    :param time_domain: Time domain
    '''
    params: T_JSON_DICT = dict()
    params['timeDomain'] = time_domain
    cmd_dict: T_JSON_DICT = {
        'method': 'Performance.setTimeDomain',
        'params': params,
    }
    json = yield cmd_dict


def get_metrics() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,typing.List[Metric]]:
    '''
    Retrieve current values of run-time metrics.

    :returns: Current values for run-time metrics.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'Performance.getMetrics',
    }
    json = yield cmd_dict
    return [Metric.from_json(i) for i in json['metrics']]


@event_class('Performance.metrics')
@dataclass
class Metrics:
    '''
    Current values of the metrics.
    '''
    #: Current values of the metrics.
    metrics: typing.List[Metric]
    #: Timestamp title.
    title: str

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> Metrics:
        return cls(
            metrics=[Metric.from_json(i) for i in json['metrics']],
            title=str(json['title'])
        )
