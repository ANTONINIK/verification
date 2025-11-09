from typing import List, Tuple, Any


RangeRecord = Tuple[int, int, Any]  # (start, end, owner)


class Memory:
    @staticmethod
    def is_contained(ranges: List[RangeRecord], start: int, end: int) -> bool:
        for s, e, _ in ranges:
            if start >= s and end <= e:
                return True
        return False

    @staticmethod
    def ranges_overlap(a_start: int, a_end: int, b_start: int, b_end: int) -> bool:
        return not (a_end < b_start or a_start > b_end)

    @staticmethod
    def check_conflict(ranges: List[RangeRecord], start: int, end: int, owner) -> bool:
        for s, e, o in ranges:
            if o is owner:
                continue
            if o is not None and Memory.ranges_overlap(start, end, s, e):
                return True
        return False

    @staticmethod
    def allocate(ranges: List[RangeRecord], start: int, end: int, owner: Any) -> bool:
        if start > end:
            raise Exception(f"Invalid memory range: start ({start}) > end ({end})")

        if Memory.check_conflict(ranges, start, end, owner):
            raise Exception(f"Memory range conflict detected for [{start}, {end}]")

        ranges.append((start, end, owner))
        return True

    @staticmethod
    def release(ranges: List[RangeRecord], start: int, end: int) -> None:
        ranges[:] = [(s, e, o) for (s, e, o) in ranges if not (s == start and e == end)]
