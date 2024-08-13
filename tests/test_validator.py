# to run these, run 
# make tests

from guardrails import Guard
import pytest
from validator import BanList

@pytest.mark.parametrize("validator, output, expected_result", [
  (BanList(banned_words=['banana', 'athena', 'coconut trees'], max_l_dist=3, on_fail='noop'), 
   "hello world!", 
   True),
  (BanList(banned_words=['banana', 'athena', 'coconut trees'], max_l_dist=3, on_fail='noop'), 
   "bananers athens", False),
  (BanList(banned_words=['banana', 'athena', 'coconut trees'], max_l_dist=3, on_fail='noop'), 
   "boconut breeze", False),

  (BanList(banned_words=['banana', 'athena', 'coconut trees'], max_l_dist=3, on_fail='noop'), 
   "b a n a n a", False),
])
def test_combinations(validator, output, expected_result):
  guard = Guard.from_string(validators=[validator])
  result = guard.parse(output)
  assert result.validation_passed is expected_result