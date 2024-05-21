# DO NOT EDIT THIS FILE!
#
# This file is generated from the CDP specification. If you need to make
# changes, edit the generator and regenerate all of the modules.
#
# CDP domain: Fetch

from __future__ import annotations
import enum
import typing
from dataclasses import dataclass
from .util import event_class, T_JSON_DICT

from . import io
from . import network
from . import page


class RequestId(str):
    '''
    Unique request identifier.
    '''
    def to_json(self) -> str:
        return self

    @classmethod
    def from_json(cls, json: str) -> RequestId:
        return cls(json)

    def __repr__(self):
        return 'RequestId({})'.format(super().__repr__())


class RequestStage(enum.Enum):
    '''
    Stages of the request to handle. Request will intercept before the request is
    sent. Response will intercept after the response is received (but before response
    body is received).
    '''
    REQUEST = "Request"
    RESPONSE = "Response"

    def to_json(self) -> str:
        return self.value

    @classmethod
    def from_json(cls, json: str) -> RequestStage:
        return cls(json)


@dataclass
class RequestPattern:
    #: Wildcards (``'*'`` -> zero or more, ``'?'`` -> exactly one) are allowed. Escape character is
    #: backslash. Omitting is equivalent to ``"*"``.
    url_pattern: typing.Optional[str] = None

    #: If set, only requests for matching resource types will be intercepted.
    resource_type: typing.Optional[network.ResourceType] = None

    #: Stage at which to begin intercepting requests. Default is Request.
    request_stage: typing.Optional[RequestStage] = None

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        if self.url_pattern is not None:
            json['urlPattern'] = self.url_pattern
        if self.resource_type is not None:
            json['resourceType'] = self.resource_type.to_json()
        if self.request_stage is not None:
            json['requestStage'] = self.request_stage.to_json()
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> RequestPattern:
        return cls(
            url_pattern=str(json['urlPattern']) if json.get('urlPattern', None) is not None else None,
            resource_type=network.ResourceType.from_json(json['resourceType']) if json.get('resourceType', None) is not None else None,
            request_stage=RequestStage.from_json(json['requestStage']) if json.get('requestStage', None) is not None else None,
        )


@dataclass
class HeaderEntry:
    '''
    Response HTTP header entry
    '''
    name: str

    value: str

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['name'] = self.name
        json['value'] = self.value
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> HeaderEntry:
        return cls(
            name=str(json['name']),
            value=str(json['value']),
        )


@dataclass
class AuthChallenge:
    '''
    Authorization challenge for HTTP status code 401 or 407.
    '''
    #: Origin of the challenger.
    origin: str

    #: The authentication scheme used, such as basic or digest
    scheme: str

    #: The realm of the challenge. May be empty.
    realm: str

    #: Source of the authentication challenge.
    source: typing.Optional[str] = None

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['origin'] = self.origin
        json['scheme'] = self.scheme
        json['realm'] = self.realm
        if self.source is not None:
            json['source'] = self.source
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AuthChallenge:
        return cls(
            origin=str(json['origin']),
            scheme=str(json['scheme']),
            realm=str(json['realm']),
            source=str(json['source']) if json.get('source', None) is not None else None,
        )


@dataclass
class AuthChallengeResponse:
    '''
    Response to an AuthChallenge.
    '''
    #: The decision on what to do in response to the authorization challenge.  Default means
    #: deferring to the default behavior of the net stack, which will likely either the Cancel
    #: authentication or display a popup dialog box.
    response: str

    #: The username to provide, possibly empty. Should only be set if response is
    #: ProvideCredentials.
    username: typing.Optional[str] = None

    #: The password to provide, possibly empty. Should only be set if response is
    #: ProvideCredentials.
    password: typing.Optional[str] = None

    def to_json(self) -> T_JSON_DICT:
        json: T_JSON_DICT = dict()
        json['response'] = self.response
        if self.username is not None:
            json['username'] = self.username
        if self.password is not None:
            json['password'] = self.password
        return json

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AuthChallengeResponse:
        return cls(
            response=str(json['response']),
            username=str(json['username']) if json.get('username', None) is not None else None,
            password=str(json['password']) if json.get('password', None) is not None else None,
        )


def disable() -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Disables the fetch domain.
    '''
    cmd_dict: T_JSON_DICT = {
        'method': 'Fetch.disable',
    }
    json = yield cmd_dict


def enable(
        patterns: typing.Optional[typing.List[RequestPattern]] = None,
        handle_auth_requests: typing.Optional[bool] = None
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Enables issuing of requestPaused events. A request will be paused until client
    calls one of failRequest, fulfillRequest or continueRequest/continueWithAuth.

    :param patterns: *(Optional)* If specified, only requests matching any of these patterns will produce fetchRequested event and will be paused until clients response. If not set, all requests will be affected.
    :param handle_auth_requests: *(Optional)* If true, authRequired events will be issued and requests will be paused expecting a call to continueWithAuth.
    '''
    params: T_JSON_DICT = dict()
    if patterns is not None:
        params['patterns'] = [i.to_json() for i in patterns]
    if handle_auth_requests is not None:
        params['handleAuthRequests'] = handle_auth_requests
    cmd_dict: T_JSON_DICT = {
        'method': 'Fetch.enable',
        'params': params,
    }
    json = yield cmd_dict


def fail_request(
        request_id: RequestId,
        error_reason: network.ErrorReason
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Causes the request to fail with specified reason.

    :param request_id: An id the client received in requestPaused event.
    :param error_reason: Causes the request to fail with the given reason.
    '''
    params: T_JSON_DICT = dict()
    params['requestId'] = request_id.to_json()
    params['errorReason'] = error_reason.to_json()
    cmd_dict: T_JSON_DICT = {
        'method': 'Fetch.failRequest',
        'params': params,
    }
    json = yield cmd_dict


def fulfill_request(
        request_id: RequestId,
        response_code: int,
        response_headers: typing.Optional[typing.List[HeaderEntry]] = None,
        binary_response_headers: typing.Optional[str] = None,
        body: typing.Optional[str] = None,
        response_phrase: typing.Optional[str] = None
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    r'''
    Provides response to the request.

    :param request_id: An id the client received in requestPaused event.
    :param response_code: An HTTP response code.
    :param response_headers: *(Optional)* Response headers.
    :param binary_response_headers: *(Optional)* Alternative way of specifying response headers as a \0-separated series of name: value pairs. Prefer the above method unless you need to represent some non-UTF8 values that can't be transmitted over the protocol as text. (Encoded as a base64 string when passed over JSON)
    :param body: *(Optional)* A response body. If absent, original response body will be used if the request is intercepted at the response stage and empty body will be used if the request is intercepted at the request stage. (Encoded as a base64 string when passed over JSON)
    :param response_phrase: *(Optional)* A textual representation of responseCode. If absent, a standard phrase matching responseCode is used.
    '''
    params: T_JSON_DICT = dict()
    params['requestId'] = request_id.to_json()
    params['responseCode'] = response_code
    if response_headers is not None:
        params['responseHeaders'] = [i.to_json() for i in response_headers]
    if binary_response_headers is not None:
        params['binaryResponseHeaders'] = binary_response_headers
    if body is not None:
        params['body'] = body
    if response_phrase is not None:
        params['responsePhrase'] = response_phrase
    cmd_dict: T_JSON_DICT = {
        'method': 'Fetch.fulfillRequest',
        'params': params,
    }
    json = yield cmd_dict


def continue_request(
        request_id: RequestId,
        url: typing.Optional[str] = None,
        method: typing.Optional[str] = None,
        post_data: typing.Optional[str] = None,
        headers: typing.Optional[typing.List[HeaderEntry]] = None,
        intercept_response: typing.Optional[bool] = None
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Continues the request, optionally modifying some of its parameters.

    :param request_id: An id the client received in requestPaused event.
    :param url: *(Optional)* If set, the request url will be modified in a way that's not observable by page.
    :param method: *(Optional)* If set, the request method is overridden.
    :param post_data: *(Optional)* If set, overrides the post data in the request. (Encoded as a base64 string when passed over JSON)
    :param headers: *(Optional)* If set, overrides the request headers. Note that the overrides do not extend to subsequent redirect hops, if a redirect happens. Another override may be applied to a different request produced by a redirect.
    :param intercept_response: **(EXPERIMENTAL)** *(Optional)* If set, overrides response interception behavior for this request.
    '''
    params: T_JSON_DICT = dict()
    params['requestId'] = request_id.to_json()
    if url is not None:
        params['url'] = url
    if method is not None:
        params['method'] = method
    if post_data is not None:
        params['postData'] = post_data
    if headers is not None:
        params['headers'] = [i.to_json() for i in headers]
    if intercept_response is not None:
        params['interceptResponse'] = intercept_response
    cmd_dict: T_JSON_DICT = {
        'method': 'Fetch.continueRequest',
        'params': params,
    }
    json = yield cmd_dict


def continue_with_auth(
        request_id: RequestId,
        auth_challenge_response: AuthChallengeResponse
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    '''
    Continues a request supplying authChallengeResponse following authRequired event.

    :param request_id: An id the client received in authRequired event.
    :param auth_challenge_response: Response to  with an authChallenge.
    '''
    params: T_JSON_DICT = dict()
    params['requestId'] = request_id.to_json()
    params['authChallengeResponse'] = auth_challenge_response.to_json()
    cmd_dict: T_JSON_DICT = {
        'method': 'Fetch.continueWithAuth',
        'params': params,
    }
    json = yield cmd_dict


def continue_response(
        request_id: RequestId,
        response_code: typing.Optional[int] = None,
        response_phrase: typing.Optional[str] = None,
        response_headers: typing.Optional[typing.List[HeaderEntry]] = None,
        binary_response_headers: typing.Optional[str] = None
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,None]:
    r'''
    Continues loading of the paused response, optionally modifying the
    response headers. If either responseCode or headers are modified, all of them
    must be present.

    **EXPERIMENTAL**

    :param request_id: An id the client received in requestPaused event.
    :param response_code: *(Optional)* An HTTP response code. If absent, original response code will be used.
    :param response_phrase: *(Optional)* A textual representation of responseCode. If absent, a standard phrase matching responseCode is used.
    :param response_headers: *(Optional)* Response headers. If absent, original response headers will be used.
    :param binary_response_headers: *(Optional)* Alternative way of specifying response headers as a \0-separated series of name: value pairs. Prefer the above method unless you need to represent some non-UTF8 values that can't be transmitted over the protocol as text. (Encoded as a base64 string when passed over JSON)
    '''
    params: T_JSON_DICT = dict()
    params['requestId'] = request_id.to_json()
    if response_code is not None:
        params['responseCode'] = response_code
    if response_phrase is not None:
        params['responsePhrase'] = response_phrase
    if response_headers is not None:
        params['responseHeaders'] = [i.to_json() for i in response_headers]
    if binary_response_headers is not None:
        params['binaryResponseHeaders'] = binary_response_headers
    cmd_dict: T_JSON_DICT = {
        'method': 'Fetch.continueResponse',
        'params': params,
    }
    json = yield cmd_dict


def get_response_body(
        request_id: RequestId
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,typing.Tuple[str, bool]]:
    '''
    Causes the body of the response to be received from the server and
    returned as a single string. May only be issued for a request that
    is paused in the Response stage and is mutually exclusive with
    takeResponseBodyForInterceptionAsStream. Calling other methods that
    affect the request or disabling fetch domain before body is received
    results in an undefined behavior.
    Note that the response body is not available for redirects. Requests
    paused in the _redirect received_ state may be differentiated by
    ``responseCode`` and presence of ``location`` response header, see
    comments to ``requestPaused`` for details.

    :param request_id: Identifier for the intercepted request to get body for.
    :returns: A tuple with the following items:

        0. **body** - Response body.
        1. **base64Encoded** - True, if content was sent as base64.
    '''
    params: T_JSON_DICT = dict()
    params['requestId'] = request_id.to_json()
    cmd_dict: T_JSON_DICT = {
        'method': 'Fetch.getResponseBody',
        'params': params,
    }
    json = yield cmd_dict
    return (
        str(json['body']),
        bool(json['base64Encoded'])
    )


def take_response_body_as_stream(
        request_id: RequestId
    ) -> typing.Generator[T_JSON_DICT,T_JSON_DICT,io.StreamHandle]:
    '''
    Returns a handle to the stream representing the response body.
    The request must be paused in the HeadersReceived stage.
    Note that after this command the request can't be continued
    as is -- client either needs to cancel it or to provide the
    response body.
    The stream only supports sequential read, IO.read will fail if the position
    is specified.
    This method is mutually exclusive with getResponseBody.
    Calling other methods that affect the request or disabling fetch
    domain before body is received results in an undefined behavior.

    :param request_id:
    :returns: 
    '''
    params: T_JSON_DICT = dict()
    params['requestId'] = request_id.to_json()
    cmd_dict: T_JSON_DICT = {
        'method': 'Fetch.takeResponseBodyAsStream',
        'params': params,
    }
    json = yield cmd_dict
    return io.StreamHandle.from_json(json['stream'])


@event_class('Fetch.requestPaused')
@dataclass
class RequestPaused:
    '''
    Issued when the domain is enabled and the request URL matches the
    specified filter. The request is paused until the client responds
    with one of continueRequest, failRequest or fulfillRequest.
    The stage of the request can be determined by presence of responseErrorReason
    and responseStatusCode -- the request is at the response stage if either
    of these fields is present and in the request stage otherwise.
    Redirect responses and subsequent requests are reported similarly to regular
    responses and requests. Redirect responses may be distinguished by the value
    of ``responseStatusCode`` (which is one of 301, 302, 303, 307, 308) along with
    presence of the ``location`` header. Requests resulting from a redirect will
    have ``redirectedRequestId`` field set.
    '''
    #: Each request the page makes will have a unique id.
    request_id: RequestId
    #: The details of the request.
    request: network.Request
    #: The id of the frame that initiated the request.
    frame_id: page.FrameId
    #: How the requested resource will be used.
    resource_type: network.ResourceType
    #: Response error if intercepted at response stage.
    response_error_reason: typing.Optional[network.ErrorReason]
    #: Response code if intercepted at response stage.
    response_status_code: typing.Optional[int]
    #: Response status text if intercepted at response stage.
    response_status_text: typing.Optional[str]
    #: Response headers if intercepted at the response stage.
    response_headers: typing.Optional[typing.List[HeaderEntry]]
    #: If the intercepted request had a corresponding Network.requestWillBeSent event fired for it,
    #: then this networkId will be the same as the requestId present in the requestWillBeSent event.
    network_id: typing.Optional[network.RequestId]
    #: If the request is due to a redirect response from the server, the id of the request that
    #: has caused the redirect.
    redirected_request_id: typing.Optional[RequestId]

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> RequestPaused:
        return cls(
            request_id=RequestId.from_json(json['requestId']),
            request=network.Request.from_json(json['request']),
            frame_id=page.FrameId.from_json(json['frameId']),
            resource_type=network.ResourceType.from_json(json['resourceType']),
            response_error_reason=network.ErrorReason.from_json(json['responseErrorReason']) if json.get('responseErrorReason', None) is not None else None,
            response_status_code=int(json['responseStatusCode']) if json.get('responseStatusCode', None) is not None else None,
            response_status_text=str(json['responseStatusText']) if json.get('responseStatusText', None) is not None else None,
            response_headers=[HeaderEntry.from_json(i) for i in json['responseHeaders']] if json.get('responseHeaders', None) is not None else None,
            network_id=network.RequestId.from_json(json['networkId']) if json.get('networkId', None) is not None else None,
            redirected_request_id=RequestId.from_json(json['redirectedRequestId']) if json.get('redirectedRequestId', None) is not None else None
        )


@event_class('Fetch.authRequired')
@dataclass
class AuthRequired:
    '''
    Issued when the domain is enabled with handleAuthRequests set to true.
    The request is paused until client responds with continueWithAuth.
    '''
    #: Each request the page makes will have a unique id.
    request_id: RequestId
    #: The details of the request.
    request: network.Request
    #: The id of the frame that initiated the request.
    frame_id: page.FrameId
    #: How the requested resource will be used.
    resource_type: network.ResourceType
    #: Details of the Authorization Challenge encountered.
    #: If this is set, client should respond with continueRequest that
    #: contains AuthChallengeResponse.
    auth_challenge: AuthChallenge

    @classmethod
    def from_json(cls, json: T_JSON_DICT) -> AuthRequired:
        return cls(
            request_id=RequestId.from_json(json['requestId']),
            request=network.Request.from_json(json['request']),
            frame_id=page.FrameId.from_json(json['frameId']),
            resource_type=network.ResourceType.from_json(json['resourceType']),
            auth_challenge=AuthChallenge.from_json(json['authChallenge'])
        )
