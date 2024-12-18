import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class UppercaseAndSymbolValidator:
    """
    Validates that a password contains at least one uppercase letter and one symbol.
    """
    def validate(self, password, user=None):
        if not any(char.isupper() for char in password):
            raise ValidationError(
                _("The password must contain at least one uppercase letter."),
                code='password_no_uppercase',
            )
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(
                _("The password must contain at least one symbol (e.g., !, @, #, $, etc.)."),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least one uppercase letter and one symbol."
        )
