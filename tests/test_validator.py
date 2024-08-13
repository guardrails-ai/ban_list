# to run these, run 
# make tests

from guardrails import Guard
import pytest
from validator import BanList

guard = Guard.from_string(validators=[BanList(banned_words=['banana', 'athena'], max_l_dist=3, on_fail='noop')],)

def test_pass():
  test_output = "hello world!"
  result = guard.parse(test_output)
  
  assert result.validation_passed is True
  assert result.validated_output == test_output

def test_fail():
  test_output = "bananers athens"
  result = guard.parse(test_output)
  
  # Assert the exception has your error_message
  assert result.validation_passed is False
