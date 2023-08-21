from utils import division
import pytest

@pytest.mark.parametrize("a,b, res", [(10,2,5),
                                      (20,10,2),
                                      (10,-2,-5),
                                      (-5,-2,2.5)])
def test_division_good(a,b,res):
    assert division(a,b) == res

@pytest.mark.parametrize("excepted, divider", [(ZeroDivisionError, 0),
                                             (TypeError, "2")])
def test_zero_division(excepted,divider):
    with pytest.raises(excepted):
        division(10,divider)
