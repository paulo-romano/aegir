import functools

from abc import ABC, abstractmethod
from inspect import isclass


class RequestPayloadValidation(ABC):
    """Base request validation class."""

    def __init__(self):
        self.handler = None

    def __str__(self):
        return self.__class__.__name__

    async def __call__(self):
        try:
            await self.validate(self.handler.request.arguments)
        except Exception as ex:
            handler_validation_messages = \
                getattr(self.handler, '_validation_messages')

            handler_validation_messages.append({str(self): ex.args[0]})

    @abstractmethod
    def validate(self, payload):
        raise NotImplementedError


class ValidateRequest:
    """Decorator to execute request Validations."""

    def __init__(self, *validations):
        self._validations = validations

    def __call__(self, func):
        @functools.wraps(func)
        async def inner(handler):
            for validation in self._validations:
                if isclass(validation):
                    validation = validation()

                validation.handler = handler

                await validation()

            if not handler.write_validation():
                return await func(handler)

        return inner


validate_request = ValidateRequest

__all__ = [
    'RequestPayloadValidation',
    'validate_request',
]
