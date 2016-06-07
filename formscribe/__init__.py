"""
FormScribe is a simple and powerful form validation library that's expressive,
easy to use and framework agnostic. It supports dynamic dependencies,
post-validation actions, has a built-in type validation system,
and is easily extensible.
"""

import re
from collections import OrderedDict
from operator import itemgetter

from formscribe.error import SubmitError
from formscribe.error import ValidationError
from formscribe.meta import FieldMeta
from formscribe.util import get_attributes


class Field(object, metaclass=FieldMeta):
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

    enabled = True
    key = None
    regex_group = None
    regex_group_key = None
    regex_key = None
    when_validated = []
    when_value = {}

    def __init__(self):
        pass

    def validate(self, value):
        """
        This method performs value-based validation for a given HTML field.

        Notes:
            You should always override this method.

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
            You should always override this method.

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
            field(automatically_validate=False)
            try:
                self.validate_field(field)
            except ValidationError:
                pass

        # validate the form itself
        try:
            self.validate(**self.build_kwargs())
        except ValidationError as error:
            self.errors.append(error)
        except NotImplementedError:
            pass

        # submit the form
        if not self.errors:
            for field, value in self.values.items():
                if value is not None:
                    try:
                        field(automatically_validate=False).submit(value)
                    except SubmitError as error:
                        self.errors.append(error)
                    except NotImplementedError:
                        pass
            try:
                self.submit(**self.build_kwargs())
            except SubmitError as error:
                self.errors.append(error)
            except NotImplementedError:
                pass

    def build_kwargs(self):
        kwargs = {field.__name__.lower(): value
                  for field, value in self.values.items()}
        for group, matches_values in self.regex_values.items():
            for matches, values in matches_values.items():
                values['matches'] = list(matches)
            kwargs[group] = list(matches_values.values())
        return kwargs

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

        # bail out if the 'enabled' callable/attribute is not True
        instance = field(automatically_validate=False)
        try:
            enabled = instance.enabled()
        except TypeError:
            enabled = instance.enabled
        if not enabled:
            return

        # make sure this field isn't validated twice
        self.validated.append(field)

        # it field is key-based, set its default value to None
        if field.key:
            self.values[field] = None

        # validate the field's dependencies first
        for dependency in self.get_field_dependencies(field):
            # dependencies also must not be validated if they already were
            if dependency not in self.validated:
                self.validate_field(dependency)
            try:
                if field.when_value[dependency.key] != self.values[dependency]:
                    return
            except KeyError:
                pass

        # do not validate the field if one of its dependencies
        # couldn't be validated
        if any(dependency in self.invalidated for dependency in
               self.get_field_dependencies(field)):
            return

        # validate the field itself
        if field.key:  # normal validation
            try:
                value = field(value=self.data.get(field.key),
                              automatically_validate=True)
                self.values[field] = value
                return value
            except ValidationError as error:
                self.errors.append(error)
                self.invalidated.append(field)
        elif field.regex_key:  # regex-based validation
            group = field.regex_group
            group_key = field.regex_group_key
            for key, value in self.data.items():
                all_matches = re.findall(field.regex_key, key)
                if all_matches:
                    try:
                        value = field(value=value, automatically_validate=True)

                        # initialise necessary structure
                        if group not in self.regex_values:
                            self.regex_values[group] = {}
                        if tuple(all_matches) not in self.regex_values[group]:
                            self.regex_values[group][tuple(all_matches)] = {}

                        self.regex_values[group][tuple(all_matches)][group_key] = value
                    except ValidationError as error:
                        self.errors.append(error)

    def validate(self, *args, **kwargs):
        raise NotImplementedError()

    def submit(self, *args, **kwargs):
        raise NotImplementedError()
