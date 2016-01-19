"""FormScribe."""

from formscribe.util import (get_attributes, get_attributes_names)


class ValidationError(Exception):
    """
    Raised whenever a validation fails.
    Should be raised from the Form.validate() method.

    Args:
        message (str): the message describing the error.
    """

    def __init__(self, message):
        super().__init__()
        self.message = message


class SubmitError(Exception):
    """
    Raised whenever a given value can't be submitted.
    Should be raised from the Form.submit() method.

    Args:
        message (str): the message describing the error.
    """

    def __init__(self, message):
        super().__init__()
        self.message = message


class Field(object):
    """
    Represents an HTML field.

    Attributes:
        key (str): key used to match the Form's datasource dict-like object.
                   Whatever object is pulled out of the Form's datasource,
                   using this key, will be used as this Field's value, and will
                   be passed on to the validate() method.
        when_validated (list): list of dependencies that must have been
                               previously successfully validated for this
                               field to be validated.
                               Dependencies are matched based on the 'key'
                               attribute of other Field objects.
    """

    key = ''
    when_validated = []
    when_value = {}

    @staticmethod
    def validate(value):
        """
        This method performs value-based validation for a given HTML field.

        Notes:
            You should always override this method. It must always be static.

        Args:
            value (object): object fetched from the dict-like object provided
                            by a given web framework for handling HTTP POST
                            data.

        Raises:
            NotImplementedError: this is the default exception that is raised,
                                 when no overriding method is provided.
        """

        raise NotImplementedError()

    @staticmethod
    def submit(value):
        """
        This method is called whenever a Field object's value has been
        validated, and is ready to be submitted.

        Notes:
            You should always override this method. It must always be static.

        Args:
            value (object): object to be submitted. Its value is always the
                            return value provided by the validate() method.
        """

        raise NotImplementedError()


class Form(object):
    def __init__(self, datasource):
        self.datasource = datasource
        self.errors = []
        self.validated = {}

        fields = self.get_fields()
        for field in fields:
            try:
                self.validate_field(field)
            except ValidationError:
                pass

        kwargs = {}
        for field, value in self.validated.items():
            for name in get_attributes_names(self):
                if getattr(self, name) == field:
                    kwargs[name.lower()] = value
                    break

        try:
            self.validate(**kwargs)
        except ValidationError as error:
            self.errors.append(error)
        except NotImplementedError:
            pass

        if not self.errors:
            for field, value in self.validated.items():
                if value is not None:
                    try:
                        field.submit(value)
                    except SubmitError as error:
                        self.errors.append(error)
                    except NotImplementedError:
                        pass
            try:
                self.submit(**kwargs)
            except SubmitError as error:
                self.errors.append(error)
            except NotImplementedError:
                pass

    def get_fields(self):
        fields = []
        for attr in get_attributes(self):
            try:
                if issubclass(attr, Field):
                    fields.append(attr)
            except TypeError:
                pass
        return fields

    def get_field_dependencies(self, field):
        dependencies = []
        keys = field.when_validated + list(field.when_value.keys())
        for key in set(keys):
            for possible_dependency in self.get_fields():
                if possible_dependency.key == key:
                    dependencies.append(possible_dependency)
        return dependencies

    def validate_field(self, field):
        if field in self.validated:
            return

        self.validated[field] = None

        for dep in self.get_field_dependencies(field):
            try:
                self.validate_field(dep)
            except ValidationError:
                return
            if dep.key in field.when_value:
                if field.when_value[dep.key] != self.validated[dep]:
                    return

        try:
            value = field.validate(self.datasource.get(field.key))
        except ValidationError as error:
            self.errors.append(error)
            raise error
        else:
            self.validated[field] = value

    @staticmethod
    def validate(*args, **kwargs):
        raise NotImplementedError()

    @staticmethod
    def submit(*args, **kwargs):
        raise NotImplementedError()
