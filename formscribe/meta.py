"""FormScribe meta classes."""


from formscribe.error import InvalidFieldError


class FieldMeta(type):
    """Field metaclass."""

    def __call__(cls, *args, **kwargs):
        instance = object.__new__(cls, *args, **kwargs)

        if instance.regex_key and not instance.regex_group:
            raise InvalidFieldError('Regex group is required.')

        if instance.regex_key and not instance.regex_group_key:
            raise InvalidFieldError('Regex group key is required.')

        if instance.regex_key and instance.key:
            raise InvalidFieldError('Regex key and key are incompatible.')

        instance.__init__()

        try:
            automatically_validate = kwargs['automatically_validate']
        except KeyError:
            try:
                automatically_validate = args[1]
            except IndexError:
                automatically_validate = True

        try:
            value = kwargs['value']
        except KeyError:
            try:
                value = args[0]
            except IndexError:
                pass

        if automatically_validate:
            try:
                return instance.validate(value)
            except NameError:
                pass

        return instance
