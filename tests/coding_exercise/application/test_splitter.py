from assertpy import assert_that
import pytest

from coding_exercise.application.splitter import Splitter
from coding_exercise.domain.model.cable import Cable


class TestSplitterValidation:
    def test_cuts_between_1_and_64(self):
        with pytest.raises(ValueError, match=r'.* 64 .*'):
            Splitter().split(Cable(1000, 'coconuts'), 65)

        with pytest.raises(ValueError, match=r'.* 64 .*'):
            Splitter().split(Cable(1000, 'coconuts'), 0)

    def test_cable_length_between_2_and_1024(self):
        with pytest.raises(ValueError, match=r'.* 1024 .*'):
            Splitter().split(Cable(1, 'coconuts'), 2)

        with pytest.raises(ValueError, match=r'.* 1024 .*'):
            Splitter().split(Cable(1025, 'coconuts'), 2)

    def test_min_segment_length(self):
        with pytest.raises(ValueError,
                           match=r'.* `cable_length - 1` .* '):
            Splitter().split(Cable(10, 'coconuts'), 9)


class TestSplitter:
    @staticmethod
    def get_splitter_test_params():
        for params in [(10, 1, 2, [Cable(5, 'coconuts-00'), Cable(5, 'coconuts-01')]),
                       (5, 2, 5, [Cable(1, f'coconuts-0{n}') for n in range(5)]),
                       (10, 2, 4, [Cable(3, f'coconuts-0{n}') for n in range(3)] + [Cable(1, 'coconuts-03')])]:
            yield params

    def test_should_not_return_none_when_splitting_cable(self):
        assert_that(Splitter().split(Cable(10, 'coconuts'), 1)).is_not_none()

    @pytest.mark.parametrize('cable_length,cuts,expected_length,expected_cables',
                             get_splitter_test_params())
    def test_splitter(self, cable_length: int, cuts: int, expected_length: int, expected_cables: list[Cable]):
        result = Splitter().split(Cable(cable_length, 'coconuts'), cuts)
        assert_that(len(result)).is_equal_to(expected_length)
        assert_that(result).is_equal_to(expected_cables)
