from morphemes_extractor.utils import check_list_len


def test_check_list_len_single_list():
    assert check_list_len([1, 2, 3]) == (3,)


def test_check_list_len_multiple_lists():
    assert check_list_len([1, 2, 3], [4, 5], [6, 7, 8, 9]) == (3, 2, 4)


def test_check_list_len_empty_list():
    assert check_list_len([]) == (0,)


def test_check_list_len_mixed_empty_and_non_empty():
    assert check_list_len([1, 2, 3], [], [4, 5, 6]) == (3, 0, 3)


def test_check_list_len_no_lists():
    assert check_list_len() == ()


def test_check_list_len_single_empty_list():
    assert check_list_len([]) == (0,)


def test_check_list_len_lists_with_different_data_types():
    assert check_list_len([1, 2], ["a", "b", "c"], [True, False, True]) == (2, 3, 3)
