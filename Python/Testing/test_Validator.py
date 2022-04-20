import Validator


def test_validate_course_id_good():
    assert Validator.validate_couseID("123") == True


def test_validate_course_id_to_long():
    assert Validator.validate_couseID("1234") == False


def test_validate_course_id_not_numbers():
    assert Validator.validate_couseID("entotrefire") == False


def test_validate_corse_good():
    assert Validator.validate_course("Systemudvikling") == True


def test_validate_course_to_short():
    assert Validator.validate_course("Sund") == False


def test_validate_timefrome_is_to_long():
    assert Validator.validate_timefrome("123456") == False


def test_validate_timefrome_is_not_numbers():
    assert Validator.validate_timefrome("hello") == False


def test_validate_timefrom_not_contain_sign():
    assert Validator.validate_timefrome("1000") == False


def test_validate_timefrom_is_good():
    assert Validator.validate_timefrome("10:00") == True


def test_validate_timeuntil_is_to_long():
    assert Validator.validate_timeuntil("98765") == False


def test_validate_timeuntil_is_not_numbers():
    assert Validator.validate_timeuntil("world") == False


def test_validate_timeuntil_not_cotain_sign():
    assert Validator.validate_timeuntil("1300") == False


def test_validate_timeuntil_is_good():
    assert Validator.validate_timeuntil("13:00") == True


def test_validate_zoom_is_to_long():
    assert Validator.validate_zoom("234") == False


def test_validate_zoom_is_not_number():
    assert Validator.validate_zoom("four") == False


def test_validate_zoom_is_good():
    assert Validator.validate_zoom("0") == True
