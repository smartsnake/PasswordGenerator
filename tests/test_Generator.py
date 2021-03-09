from util.Generator import Generator
import pytest

password_length = 34
invalid_password_length = -10

gen = Generator()

#Testing password generated is the correct length
def test_generate_password():
    password = gen.generate_password(password_length)
    assert len(password) == password_length

#Testing invalid password length
def test_invalid_len_generate_password():
    with pytest.raises(SystemExit):
        gen.generate_password(invalid_password_length)

#Random char come from all_charactors list
def test_random_char():
    assert gen.random_char(gen.all_charactors) in gen.all_charactors