"""FormScribe."""

import re
from collections import OrderedDict
from operator import itemgetter

from formscribe.util import get_attributes


class InvalidFieldError(Exception):
    """
    Raised whenever a field has an invalid set of attributes.

    Args:
        message (str): the message describing the error.
    """

    def __init__(self, message):
        super().__init__()
        self.message = message


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
        key (str): key used to match the Form's data dict-like object.
                   Whatever object is pulled out of the Form's data,
                   using this key, will be used as this Field's value, and will
                   be passed on to the validate() method.
        when_validated (list): list of dependencies that must have been
                               previously successfully validated for this
                               field to be validated.
                               Dependencies are matched based on the 'key'
                               attribute of other Field objects.
    """

    key = None
    regex_group = None
    regex_group_key = None
    regex_key = None
    when_validated = []
    when_value = {}

    def __init__(self):
        if self.regex_key and not self.regex_group:
            raise InvalidFieldError('Regex group is required.')
        if self.regex_key and not self.regex_group_key:
            raise InvalidFieldError('Regex group key is required.')
        if self.regex_key and self.key:
            raise InvalidFieldError('Regex key and key are incompatible.')

    def validate(self, value):
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

    def submit(self, value):
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
    def __init__(self, data):
        self.data = OrderedDict(sorted(data.items(), key=itemgetter(0)))
        self.errors = []
        self.invalidated = []
        self.regex_values = {}
        self.validated = []
        self.values = {}

        # validate all fields and their dependencies
        fields = self.get_fields()
        for field in fields:
            # instantiate the field so its InvalidFieldError exceptions
            # are raised
            field()
            if field.regex_key:
                group = field.regex_group
                group_key = field.regex_group_key
                try:
                    self.regex_values[group][group_key] = []
                except KeyError:
                    self.regex_values[group] = {}
                    self.regex_values[group][group_key] = []
            try:
                self.validate_field(field)
            except ValidationError:
                pass

        # convert all field's values to a dictionary which will be used
        # for the form's validation and submitting
        kwargs = {field.__name__.lower(): value
                  for field, value in self.values.items()}
        for group, attributes in self.regex_values.items():
            values = list(filter((lambda x: x if all(x) else None),
                                 zip(*attributes.values())))
            kwargs[group] = [dict(zip(attributes.keys(), value))
                             for value in values]

        # validate the form itself
        try:
            self.validate(**kwargs)
        except ValidationError as error:
            self.errors.append(error)
        except NotImplementedError:
            pass

        # submit the form
        if not self.errors:
            for field, value in self.values.items():
                if value is not None:
                    try:
                        field().submit(value)
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
        for attribute in get_attributes(self):
            try:
                if issubclass(attribute, Field):
                    fields.append(attribute)
            except TypeError:
                pass
        return fields

    def get_field_dependencies(self, field):
        dependencies = []
        dependencies_keys = set(field.when_validated +
                                list(field.when_value.keys()))
        for possible_dependency in self.get_fields():
            if possible_dependency.key in dependencies_keys:
                dependencies.append(possible_dependency)
        return dependencies

    def validate_field(self, field):
        # no need to revalidate if field was already validated
        if field in self.validated:
            return

        self.validated.append(field)
        if field.key:
            self.values[field] = None

        # validate the field's dependencies first
        for dependency in self.get_field_dependencies(field):
            value = self.validate_field(dependency)
            # do not validate the field if one of its dependencies'
            # values don't match the field's requirements
            if dependency.key in field.when_value:
                if field.when_value[dependency.key] != value:
                    return

        # do not validate the field if one of its dependencies
        # couldn't be validated
        if any(dependency in self.invalidated for dependency in
               self.get_field_dependencies(field)):
            return

        # validate the field itself
        if field.key:
            try:
                value = field().validate(self.data.get(field.key))
            except ValidationError as error:
                self.errors.append(error)
                self.invalidated.append(field)
            else:
                self.values[field] = value
                return value
        elif field.regex_key:
            group = field.regex_group
            group_key = field.regex_group_key
            for key, value in self.data.items():
                if re.findall(field.regex_key, key):
                    try:
                        value = field().validate(value)
                        self.regex_values[group][group_key].append(value)
                    except ValidationError as error:
                        self.errors.append(error)

    def validate(self, *args, **kwargs):
        raise NotImplementedError()

    def submit(self, *args, **kwargs):
        raise NotImplementedError()
