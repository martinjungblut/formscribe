"""FormScribe meta classes."""


class FieldMeta(type):
    """Field metaclass."""

    def __call__(cls, *args, **kwargs):
        instance = object.__new__(cls, *args, **kwargs)

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

        instance.__init__()
        return instance
