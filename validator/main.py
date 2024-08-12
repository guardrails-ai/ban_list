from typing import Any, Callable, Dict, Optional

from guardrails.validator_base import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
)


@register_validator(name="guardrails/ban_list", data_type="string")
class BanList(Validator):
    """Validates that output does not have banned words, using fuzzy search.

    **Key Properties**

    | Property                      | Description                       |
    | ----------------------------- | --------------------------------- |
    | Name for `format` attribute   | `guardrails/ban_list`             |
    | Supported data types          | `string`                          |
    | Programmatic fix              | Removes banned word.              |

    Args:
        banned_words (List[str]): A list of banned words to check for in output.
    """  # noqa

    # If you don't have any init args, you can omit the __init__ method.
    def __init__(
        self,
        banned_words: str,
        on_fail: Optional[Callable] = None,
    ):
        super().__init__(on_fail=on_fail, arg_1=banned_words)
        self._banned_words = banned_words

    def validate(self, value: Any, metadata: Dict = {}) -> ValidationResult:
        """Validates that output does not have banned words."""
        # Add your custom validator logic here and return a PassResult or FailResult accordingly.
        for banned_word in self._banned_words:
            if banned_word in value:
                return FailResult(
                    error_message=f"Output contains banned word: {banned_word}",
                    fix_value=value.replace(banned_word, ""),
                ) 

        if value != "pass": # FIXME
            return FailResult(
                error_message="{A descriptive but concise error message about why validation failed}",
                fix_value="{The programmtic fix if applicable, otherwise remove this kwarg.}",
            )
        return PassResult()
