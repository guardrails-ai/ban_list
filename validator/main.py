from typing import Any, Callable, Dict, Optional
from fuzzysearch import find_near_matches

from guardrails.validator_base import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
    ErrorSpan
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
        max_l_dist (int): Maximum Levenshtein distance for fuzzy search. Default is 1.
    """  # noqa

    # If you don't have any init args, you can omit the __init__ method.
    def __init__(
        self,
        banned_words: str,
        max_l_dist: int = 1,
        on_fail: Optional[Callable] = None,
    ):
        super().__init__(on_fail=on_fail, arg_1=banned_words)
        self._banned_words = banned_words
        self._max_l_dist = max_l_dist

    def validate(self, value: Any, metadata: Dict = {}) -> ValidationResult:
        """Validates that output does not have banned words."""
        # Add your custom validator logic here and return a PassResult or FailResult accordingly.
        all_matches = []
        for banned_word in self._banned_words:
            matches = find_near_matches(banned_word, value, max_l_dist=self._max_l_dist)
            all_matches.extend(matches)
        
        if len(all_matches) > 0:
            error_spans = []
            fix_value = value
            for match in all_matches:
                triggering_text = value[match.start:match.end]
                fix_value = fix_value.replace(triggering_text, "")
                error_spans.append(ErrorSpan(
                    start=match.start,
                    end=match.end,
                    reason=f"Found match with banned word '{match.matched}' in '{triggering_text}'"
                ))
            return FailResult(
                error_message="Output contains banned words",
                error_spans=error_spans,
                fix_value=fix_value
            )

        return PassResult()
