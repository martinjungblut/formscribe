"""
Data centred tests, directly check the form's values and compare them
to expected sets.
"""

import unittest
from contextlib import suppress
from datetime import datetime
from datetime import time

from formscribe import Field
from formscribe import Form
from formscribe import ValidationError


class ProfileManagementForm(Form):
    class ProfileID(Field):
        key = 'profile_id'

        def validate(self, value):
            try:
                value = int(value)
            except (ValueError, TypeError):
                return
            else:
                return value

    class Name(Field):
        key = 'name'

        def validate(self, value):
            with suppress(AttributeError):
                value = value.strip()
            if not value:
                raise ValidationError('O nome é obrigatório.')
            return value

    class EnableSessionTimeout(Field):
        key = 'sessiontimeout-enabled'

        def validate(self, value):
            return bool(value)

    class SessionTimeoutHours(Field):
        key = 'sessiontimeout-hours'
        when_value = {
            'sessiontimeout-enabled': True,
        }

        def validate(self, value):
            invalid_message = 'Número de horas da expiração inválido.'
            with suppress(AttributeError):
                value = value.strip()
            try:
                value = int(value)
            except (TypeError, ValueError):
                raise ValidationError(invalid_message)
            if value < 0:
                raise ValidationError(invalid_message)
            return value

    class SessionTimeoutMinutes(Field):
        key = 'sessiontimeout-minutes'
        when_value = {
            'sessiontimeout-enabled': True,
        }

        def validate(self, value):
            invalid_message = 'Número de minutos da expiração inválido.'
            with suppress(AttributeError):
                value = value.strip()
            try:
                value = int(value)
            except (TypeError, ValueError):
                raise ValidationError(invalid_message)
            if value < 0:
                raise ValidationError(invalid_message)
            if value > 59:
                value = 59
            return value

    class SessionTimeoutSeconds(Field):
        key = 'sessiontimeout-seconds'
        when_value = {
            'sessiontimeout-enabled': True,
        }

        def validate(self, value):
            invalid_message = 'Número de segundos da expiração inválido.'
            with suppress(AttributeError):
                value = value.strip()
            try:
                value = int(value)
            except (TypeError, ValueError):
                raise ValidationError(invalid_message)
            if value < 0:
                raise ValidationError(invalid_message)
            if value > 59:
                value = 59
            return value

    class EnableIdleTimeout(Field):
        key = 'idletimeout-enabled'

        def validate(self, value):
            return bool(value)

    class IdleTimeoutHours(Field):
        key = 'idletimeout-hours'
        when_value = {
            'idletimeout-enabled': True,
        }

        def validate(self, value):
            invalid_message = 'Número de horas de ociosidade inválido.'
            with suppress(AttributeError):
                value = value.strip()
            try:
                value = int(value)
            except (TypeError, ValueError):
                raise ValidationError(invalid_message)
            if value < 0:
                raise ValidationError(invalid_message)
            return value

    class IdleTimeoutMinutes(Field):
        key = 'idletimeout-minutes'
        when_value = {
            'idletimeout-enabled': True,
        }

        def validate(self, value):
            invalid_message = 'Número de minutos de ociosidade inválido.'
            with suppress(AttributeError):
                value = value.strip()
            try:
                value = int(value)
            except (TypeError, ValueError):
                raise ValidationError(invalid_message)
            if value < 0:
                raise ValidationError(invalid_message)
            if value > 59:
                value = 59
            return value

    class IdleTimeoutSeconds(Field):
        key = 'idletimeout-seconds'
        when_value = {
            'idletimeout-enabled': True,
        }

        def validate(self, value):
            invalid_message = 'Número de segundos de ociosidade inválido.'
            with suppress(AttributeError):
                value = value.strip()
            try:
                value = int(value)
            except (TypeError, ValueError):
                raise ValidationError(invalid_message)
            if value < 0:
                raise ValidationError(invalid_message)
            if value > 59:
                value = 59
            return value

    class EnableBandwidthLimit(Field):
        key = 'bandwidth-limit-enabled'

        def validate(self, value):
            return bool(value)

    class MaxBandwidthDown(Field):
        key = 'max-bandwidth-down'
        when_value = {
            'bandwidth-limit-enabled': True,
        }

        def validate(self, value):
            invalid_message = 'O limite de banda para download é inválido.'
            try:
                value = int(value)
            except ValueError:
                raise ValidationError(invalid_message)
            except TypeError:
                value = 0
            return value

    class MaxBandwidthUp(Field):
        key = 'max-bandwidth-up'
        when_value = {
            'bandwidth-limit-enabled': True,
        }

        def validate(self, value):
            invalid_message = 'O limite de banda para upload é inválido.'
            try:
                value = int(value)
            except ValueError:
                raise ValidationError(invalid_message)
            except TypeError:
                value = 0
            return value

    class Default(Field):
        key = 'default'

        def validate(self, value):
            return bool(value)

    class EnableSimultaneousUse(Field):
        key = 'simultaneous-use-enabled'

        def validate(self, value):
            return bool(value)

    class SimultaneousUse(Field):
        key = 'simultaneous-use'
        when_value = {
            'simultaneous-use-enabled': True
        }

        def validate(self, value):
            invalid_message = 'O uso simultâneo é inválido.'
            try:
                value = int(value)
            except (ValueError, TypeError):
                raise ValidationError(invalid_message)

            if value <= 0:
                raise ValidationError(invalid_message)

            return value

    class VoucherProfile(Field):
        key = 'voucher-profile'

        def validate(self, value):
            return bool(value)

    class EnableMaxSessionTime(Field):
        key = 'max-session-time-enabled'

        def validate(self, value):
            return bool(value)

    class MaxSessionTimeHours(Field):
        key = 'max-session-time-hours'
        when_value = {
            'max-session-time-enabled': True,
        }

        def validate(self, value):
            invalid_message = """
            Número de horas do tempo máximo de utilização inválido.
            """
            with suppress(AttributeError):
                value = value.strip()
            try:
                value = int(value)
            except (TypeError, ValueError):
                raise ValidationError(invalid_message)
            if value < 0:
                raise ValidationError(invalid_message)
            return value

    class MaxSessionTimeMinutes(Field):
        key = 'max-session-time-minutes'
        when_value = {
            'max-session-time-enabled': True,
        }

        def validate(self, value):
            invalid_message = """
            Número de minutos do tempo máximo de utilização inválido.
            """
            with suppress(AttributeError):
                value = value.strip()
            try:
                value = int(value)
            except (TypeError, ValueError):
                raise ValidationError(invalid_message)
            if value < 0:
                raise ValidationError(invalid_message)
            if value > 59:
                value = 59
            return value

    class LoginTimeID(Field):
        regex_key = 'login-time-\d+-id'
        regex_group = 'logintimes'
        regex_group_key = 'id'

        def validate(self, value):
            if value == 'new':
                return value
            try:
                return int(value)
            except (TypeError, ValueError):
                raise ValidationError('Ocorreu um erro no formulário. '
                                      'Por favor, tente novamente.')

    class LoginTimeDay(Field):
        regex_key = 'login-time-\d+-day'
        regex_group = 'logintimes'
        regex_group_key = 'day'

        def validate(self, value):
            message = ('Seleção de dia inválida. '
                       'Por favor, tente novamente.')

            try:
                value = int(value)
            except (TypeError, ValueError):
                raise ValidationError(message)

            if value < 1 or value > 9:
                raise ValidationError(message)

            if value >= 1 and value <= 7:
                return {'day': value}
            elif value == 8:
                return {'week_day': True}
            else:
                return {'any_day': True}

    class LoginTimeStart(Field):
        regex_key = 'login-time-\d+-start'
        regex_group = 'logintimes'
        regex_group_key = 'start'

        def validate(self, value):
            message = ('Horário inicial inválido. '
                       'Por favor, tente novamente.')

            try:
                return datetime.strptime(value, '%H:%M').time()
            except (TypeError, ValueError):
                raise ValidationError(message)

    class LoginTimeEnd(Field):
        regex_key = 'login-time-\d+-end'
        regex_group = 'logintimes'
        regex_group_key = 'end'

        def validate(self, value):
            message = ('Horário final inválido. '
                       'Por favor, tente novamente.')

            try:
                return datetime.strptime(value, '%H:%M').time()
            except (TypeError, ValueError):
                raise ValidationError(message)


class Test(unittest.TestCase):
    def test(self):
        data = {
            'bandwidth-limit-enabled': '1',
            'default': '',
            'idletimeout-enabled': '1',
            'idletimeout-hours': '23',
            'idletimeout-minutes': '15',
            'idletimeout-seconds': '30',
            'login-time-1-day': 3,
            'login-time-1-end': '15:00',
            'login-time-1-id': 'new',
            'login-time-1-start': '12:00',
            'login-time-2-day': 5,
            'login-time-2-end': '10:00',
            'login-time-2-id': '5',
            'login-time-2-start': '07:00',
            'max-bandwidth-down': '1024',
            'max-bandwidth-up': '768',
            'max-session-time-enabled': '1',
            'max-session-time-hours': '15',
            'max-session-time-minutes': '12',
            'name': 'teste',
            'profile_id': '350',
            'sessiontimeout-enabled': '1',
            'sessiontimeout-hours': '23',
            'sessiontimeout-minutes': '15',
            'sessiontimeout-seconds': '12',
            'simultaneous-use': '30',
            'simultaneous-use-enabled': True,
            'voucher-profile': '',
        }
        expected = {
            'bandwidth-limit-enabled': True,
            'default': False,
            'idletimeout-enabled': True,
            'idletimeout-hours': 23,
            'idletimeout-minutes': 15,
            'idletimeout-seconds': 30,
            'max-bandwidth-down': 1024,
            'max-bandwidth-up': 768,
            'max-session-time-enabled': True,
            'max-session-time-hours': 15,
            'max-session-time-minutes': 12,
            'name': 'teste',
            'profile_id': 350,
            'sessiontimeout-enabled': True,
            'sessiontimeout-hours': 23,
            'sessiontimeout-minutes': 15,
            'sessiontimeout-seconds': 12,
            'simultaneous-use': 30,
            'simultaneous-use-enabled': True,
            'voucher-profile': False,
        }
        form = ProfileManagementForm(data)
        for key, value in expected.items():
            flag = False
            for validated in form.validated:
                message = "Field wasn't validated correctly: %s" % validated
                if validated.key == key:
                    self.assertEqual(form.values[validated], value, message)
                    flag = True
            message = "%s wasn't validated." % key
            self.assertTrue(flag, message)

        logintimes = [
            {
                'day': {'day': 3},
                'end': time(hour=15),
                'id': 'new',
                'start': time(hour=12),
            },
            {
                'day': {'day': 5},
                'end': time(hour=10),
                'id': 5,
                'start': time(hour=7),
            },
        ]
        kwargs = form.build_kwargs()
        self.assertTrue(kwargs['logintimes'])
        for logintime in logintimes:
            message = 'Logintime {0} not in logintimes.'.format(str(logintime))
            self.assertTrue(logintime in kwargs['logintimes'], message)
