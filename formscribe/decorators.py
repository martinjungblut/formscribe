from copy import copy

from formscribe.error import ValidationError


def integer(message):
    def method_modifier(method):
        def implementation(self, value):
            try:
                value = int(value)
            except (ValueError, TypeError):
                raise ValidationError(message)
            else:
                return method(self, value)
        return implementation

    def class_modifier(cls):
        cls.validate = method_modifier(cls.validate)
        return cls

    return class_modifier


def oneof(group, message):
    def method_modifier(method):
        def implementation(self, value):
            if value not in group:
                raise ValidationError(message)
            else:
                return method(self, value)
        return implementation

    def class_modifier(cls):
        cls.validate = method_modifier(cls.validate)
        return cls

    return class_modifier


def required(message):
    def method_modifier(method):
        def implementation(self, value):
            nvalue = copy(value)
            try:
                nvalue = nvalue.strip()
            except AttributeError:
                pass

            if not nvalue:
                raise ValidationError(message)
            else:
                return method(self, value)
        return implementation

    def class_modifier(cls):
        cls.validate = method_modifier(cls.validate)
        return cls

    return class_modifier


def boolean(cls):
    def method_modifier(method):
        def implementation(self, value):
            value = bool(value)
            return method(self, value)
        return implementation

    cls.validate = method_modifier(cls.validate)
    return cls
