"""FormScribe meta classes."""


from formscribe.error import InvalidFieldError


class FieldMeta(type):
    """Field metaclass."""

    def __call__(cls, *args, **kwargs):
        instance = object.__new__(cls, *args, **kwargs)

        regex_attributes = [getattr(instance, attribute) for attribute in
                            ('regex_group', 'regex_group_key', 'regex_key')]
        if any(regex_attributes) and not all(regex_attributes):
            raise InvalidFieldError('The following attributes are required:'
                                    ' regex_group, regex_group_key,'
                                    ' regex_key.')

        if instance.regex_key and instance.key:
            raise InvalidFieldError('The following attributes are incompatible:'
                                    ' regex_key, key.')

        if not instance.key and not all(regex_attributes):
            raise InvalidFieldError('Field must be either key-based or'
                                    ' regex-based.')

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
