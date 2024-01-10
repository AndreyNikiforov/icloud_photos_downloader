"""
Fast iteration
TODO:
- make http call
- parse response
- compose
- select next action based on response/parsing
"""

from returns.pipeline import pipe, flow
from returns.pointfree import bind, bind_result, apply, map_, alt, lash, bimap
from returns.pipeline import managed
from returns.result import safe, Result, Success, Failure
from returns.io import IOResultE, impure_safe
from returns.future import Future, future_safe
from returns.iterables import Fold
# from returns.interfaces import Mappable
from typing import Callable, Final, Sequence, TypeVar, cast
import httpx
import anyio


async def main_client():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://httpbin.org/get')
        print(response.json())

@future_safe
async def _get():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://httpbin.org/get')
        return response

@future_safe
async def _request(request: httpx.Request):
    async with httpx.AsyncClient() as client:
        response = await client.send(request)
        return response

def main_direct_get():
    response = httpx.get('https://httpbin.org/get')
    print(response.json())

def main_direct_post():
    response = httpx.post('https://httpbin.org/post', json={'my_param_str': 'my_value_str'})
    print(response.text)

# that is okay to keep this to the minimum
# unless there is a connection failure, we process response and produce new state in the state machine
@future_safe
async def _call_validate():
    async with httpx.AsyncClient() as client:
        response = await client.post('https://setup.icloud.com/setup/ws/1/validate', params={
            # 'clientBuildNumber': '2310Project49', 'clientMasteringNumber':'2310B21', 
            'clientId': '7cb842d6-b68d-433e-a8d5-d55a722a45f5'})
        return response

# system can be in a number of states:
# - Initial
# - InvalidAuthToken - token validation failed, need reset???
# - NeedPassword - expecting password from user
# - NeedMFASelection -- expecting MFA target selector
# - NeedMFA - expecting MFA from user
# - ValidAuthToken - okay to download
# TODO How to model typed state machine?
# GADT for each state that will hold all necessary data, e.g. tokens/cookies

@safe
def _get_json(response: httpx.Response):
    return response.json()

_T = TypeVar('_T')

def _assert(func: Callable[[_T], bool]):
    @safe
    def _intern(input: _T) -> _T:
        assert(func(input) == True)
        return input
    return _intern

# _failed_success: Callable[[httpx.Response], Result[httpx.Response, Exception]] = _assert(lambda response: response.json()['status'] == False )

# class ValidationFailureResponse(Exception):
#     pass

# _failed_validation_parser: Callable[[httpx.Response], Result[httpx.Response, Exception]] = pipe(
#     _assert(lambda response: response.json()['status'] == False ),
#     map_(lambda response: response.json()['error']),
#     map_(lambda error: Failure(ValidationFailureResponse(error)))
# )

# _succeeded_validation_parser: Callable[[httpx.Response], Result[httpx.Response, Exception]] = pipe(
#     map_(lambda response: response.json()['bla']),
# )

class SomeValidResponse:
    pass

class SomeInvalidResponse:
    pass

def _parse_response(response: httpx.Response) -> SomeValidResponse | SomeInvalidResponse:
    raise NotImplementedError()

def _create_request(response: SomeValidResponse) -> httpx.Request:
    raise NotImplementedError()

class InitialState:
    """ start state """
    pass

class WaitForPasswordState:
    """ code is waiting for password from user """
    pass

class WaitForMFAState:
    """ code is waiting for MFA from user """
    pass

# states that requires "external" input from user or timer
WaitingState = InitialState | WaitForPasswordState | WaitForMFAState

def _build_auth_request(state: WaitForPasswordState, password: str) -> httpx.Request:
    raise NotImplementedError()

def _process_auth_response(response: httpx.Response) -> WaitingState:
    raise NotImplementedError()

# transitioning waitforpassword & cmd(password)
# todo how to combine correct state with correct command? Monad singletons (witness) in haskell?
def _run(state: WaitForPasswordState, password: str):
    return flow(
        _build_auth_request(state, password),
        _request,
        bimap(_process_auth_response, lambda _: WaitForPasswordState), # network errors are getting up back to waiting state
    )

# combine http calls into the flow
# def _turn(state: WaitingState) -> WaitingState:
#     return _get().map(_parse_response).map(_create_request).bind(_request)

# def _get_prop(prop: str):
#     @safe
#     def _intern(mappable: Mappable):
#         return mappable.map(lambda property_aware: property_aware[prop])
#     return _intern

StateValidationRejected: Exception #Error Returned by the call to validate service

StateValidated: str

# ValidateResponseOutcome: Result[StateValidated, ValidateError]

# @safe
# def _validate():
#     return pipe(
#         _call_validate,
        

# anyio.run(main_client)
# main_direct_get()
# main_direct_post()
print(anyio.run(_call_validate().awaitable))
