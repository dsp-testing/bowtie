from bowtie._utils import pluralize


def test_pluralize_singular():
    assert pluralize(1, "test") == "1 test"


def test_pluralize_plural():
    assert pluralize(2, "test") == "2 tests"


def test_pluralize_zero():
    assert pluralize(0, "test") == "0 tests"


def test_pluralize_negative():
    assert pluralize(-1, "test") == "-1 tests"


def test_pluralize_custom_plural():
    assert pluralize(2, "story", plural="stories") == "2 stories"


def test_pluralize_custom_plural_singular_unaffected():
    assert pluralize(1, "story", plural="stories") == "1 story"
