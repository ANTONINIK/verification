from typing import List, Tuple, Any

RangeRecord = Tuple[int, int, Any]  # (start, end, owner)

class Memory:
    @staticmethod
    def _ranges_overlap(a_start: int, a_end: int, b_start: int, b_end: int) -> bool:
        return not (a_end < b_start or a_start > b_end)

    @staticmethod
    def check_conflict(ranges: List[RangeRecord], start: int, end: int, owner: Any = None) -> bool:
        for s, e, o in ranges:
            if owner is not None and o is owner:
                continue
            if Memory._ranges_overlap(start, end, s, e):
                return True
        return False

    @staticmethod
    def allocate(ranges: List[RangeRecord], start: int, end: int, owner: Any) -> bool:
        if Memory.check_conflict(ranges, start, end, owner):
             raise Exception("Memory range conflict detected")
        ranges.append((start, end, owner))
        return True

    @staticmethod
    def release(ranges: List[RangeRecord], start: int, end: int) -> None:
        ranges[:] = [
            (s, e, o)
            for (s, e, o) in ranges
            if not (s == start and e == end)
        ]