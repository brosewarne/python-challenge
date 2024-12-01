from coding_exercise.domain.model.cable import Cable


class Splitter:

    def __validate(self, cable_length: int, times: int):
        if not (1 <= times <= 64):
            raise ValueError('`times` must be between 1 and 64 inclusive.')
        if not (2 <= cable_length <= 1024):
            raise ValueError('`cable_length` must be between 2 and 1024 inclusive.')
        if times >= cable_length - 1:
            raise ValueError('`times` must be less than `cable_length - 1` or the segment lengths will be less than 0.')

    def split(self, cable: Cable, times: int) -> list[Cable]:
        cable_length: int = cable.length
        self.__validate(cable_length, times)

        # the minimum number of segments we get from the first `times` cuts
        min_segments: int = times + 1

        # the maximum length of the segments to the lowest int given the length and minimum number of segments
        max_segment_length: int = cable_length // min_segments

        # create the cables from the first `times` cuts
        cables: list[Cable] = [Cable(max_segment_length, f'{cable.name}-{_:02}') for _ in range(min_segments)]

        remainder: int = cable_length % min_segments
        if remainder == 0:
            # exit early if there's no remainder and no more work to do
            return cables

        # for the remaining cable, get as many segments of `max_segment_length` as we can
        while remainder >= max_segment_length:
            cables.append(Cable(max_segment_length, f'{cable.name}-{len(cables):02}'))
            remainder -= max_segment_length

        # Add the remaining cable (which is now of length remainder, which is < max_segment_length), if any, as the last
        # cable
        if remainder > 0:
            cables.append(Cable(remainder, f'{cable.name}-{len(cables):02}'))
        return cables
