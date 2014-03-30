import hashlib
import pytest
from .. import storage

def setup_function(function):
    storage.init_db()


def teardown_function(function):
    storage.Base.metadata.drop_all(storage.engine)


@pytest.mark.parametrize('username', [
    'roscivs',
    'bottia',
    'srilyk',
])
def test_after_create_user_get_user_should_return_user_with_username(username):
    expected_username = username

    storage.create_user(username=expected_username, password="Whatever")
    user = storage.get_user(username=expected_username)

    assert user.username == expected_username


def test_make_hashword_should_return_same_value_with_repeated_input():
    hash_input = "fnordy"

    output_one = storage._make_hashword(hash_input)
    output_two = storage._make_hashword(hash_input)

    assert output_one == output_two


def test_make_hashword_should_return_sha1_updated_by_pw_and_salt():
    password = "Password123"
    salt = "Sodium Chloride"
    storage.salt = salt
    sha = hashlib.sha256()
    sha.update(password.encode())
    sha.update(salt.encode())

    assert storage._make_hashword(password) == sha.hexdigest()


def test_returned_user_should_have_correct_hashword():
    expected_username = "fnord"
    password = "something you can't see"
    expected_hashword = storage._make_hashword(password)
    storage.create_user(expected_username, password)

    user = storage.get_user(expected_username)

    assert user.username == expected_username
    assert user.hashword == expected_hashword


def test_get_user_for_username_not_added_should_return_None():
    assert storage.get_user('roscivs') == None


def test_create_user_twice_should_throw_ValueError():
    username = 'Jim and I'
    storage.create_user(username, 'whatev')
    with pytest.raises(ValueError):
        storage.create_user(username, 'something different')


def test_update_user_should_update_the_password():
    username = 'fnord'
    old_password = "dirty gym socks"
    new_password = "dirty Jim's sock"
    storage.create_user(username, old_password)
    user = storage.get_user(username)

    user.set_password(new_password)
    storage.update_user(user)
    user = storage.get_user(username)

    assert user.hashword == storage._make_hashword(new_password)


def test_update_user_should_NOT_update_username():
    username = "fnord"
    new_username = "bob"

    storage.create_user(username, "password?")
    user = storage.get_user(username)
    user.username = new_username
    storage.update_user(user)

    assert storage.get_user(new_username) == None


def test_User_set_password_should_update_hashword():
    user = storage.User('whatever', 'some hash')
    new_pw = 'the quick brown fox jumps over the lazy dogs'
    user.set_password(new_pw)

    assert user.hashword == storage._make_hashword(new_pw)
