"""Control for the huge file widget"""

import mmap
import re
from typing import TYPE_CHECKING, List, Optional

from prompt_toolkit.data_structures import Point
from prompt_toolkit.formatted_text import StyleAndTextTuples
from prompt_toolkit.key_binding.key_bindings import KeyBindingsBase
from prompt_toolkit.layout.controls import GetLinePrefixCallable, UIContent, UIControl
from prompt_toolkit.mouse_events import MouseEvent, MouseEventType

if TYPE_CHECKING:
    from prompt_toolkit.key_binding.key_bindings import NotImplementedOrNone

MAX_LINES = 1000


class HugeFileViewerUIControl(UIControl):
    """UIControl optimized for huge file visualization"""

    def __init__(
        self,
        filename: str,
        key_bindings: Optional[KeyBindingsBase] = None,
    ):
        self._filename = filename
        self._fd = open(self._filename, "r")
        self._mm = mmap.mmap(self._fd.fileno(), 0, access=mmap.ACCESS_READ)
        self._size = self._mm.size()
        self._offset = 0
        self._offset_max = 0
        self.key_bindings = key_bindings
        self._lines: List[StyleAndTextTuples] = []
        self._window_height = 0
        self.update_lines()

    def close(self) -> None:
        self._mm.close()
        self._fd.close()

    def find_prev_newline(self, offset: int) -> int:
        start_offset = (self._size % mmap.PAGESIZE) - 2 * mmap.PAGESIZE
        return self._mm.rfind(b"\n", max(0, start_offset), offset)

    def get_lines(self) -> List[bytes]:
        lines = []
        for _ in range(MAX_LINES):
            line = self._mm.readline()
            if not line:
                break
            line = line.strip()
            lines.append(line)
        return lines

    def update_lines(self) -> None:
        self._mm.seek(self._offset)
        self._lines = [
            [("", line.decode("utf-8", errors="replace"))] for line in self.get_lines()
        ]
        if self._window_height > len(self._lines):
            self.go_up(self._window_height - len(self._lines))

    def preferred_width(self, max_available_width: int) -> Optional[int]:
        return max_available_width

    def preferred_height(
        self,
        width: int,
        max_available_height: int,
        wrap_lines: bool,
        get_line_prefix: Optional[GetLinePrefixCallable],
    ) -> Optional[int]:
        new_height = min(len(self._lines), max_available_height)
        if new_height != self._window_height:
            # Update self._offset_max:
            offset = self._size - 1
            for i in range(new_height):
                # Look at the last 2-3 pages:
                offset = self.find_prev_newline(offset)
                if offset == -1:
                    self._offset_max = 0
                    break
                self._offset_max = offset + 1
        return self._window_height

    def is_focusable(self) -> bool:
        return True  # self.focusable()

    def _get_line(self, lineno: int) -> StyleAndTextTuples:
        if lineno >= len(self._lines):
            return [("", "")]
        return self._lines[lineno]

    def _cursor_position(self) -> Point:
        return Point(x=0, y=0)

    def create_content(self, width: int, height: int) -> UIContent:
        return UIContent(
            get_line=self._get_line,
            line_count=100,
            show_cursor=True,  # False,
            cursor_position=self._cursor_position(),
        )

    def mouse_handler(self, mouse_event: MouseEvent) -> "NotImplementedOrNone":
        if mouse_event.event_type == MouseEventType.SCROLL_UP:
            self.go_up()
        elif mouse_event.event_type == MouseEventType.SCROLL_DOWN:
            self.go_down()
        else:
            return NotImplemented
        return None

    def move_cursor_up(self) -> None:
        self.go_up()

    def move_cursor_down(self) -> None:
        self.go_down()

    def get_key_bindings(self) -> Optional[KeyBindingsBase]:
        return self.key_bindings

    def re_search(self, regex: re.Pattern[bytes]) -> Optional[re.Match[bytes]]:
        return regex.search(bytes(self._mm))

    def go_offset(self, offset: int) -> None:
        if offset < 0:
            self._offset = 0
            return
        if offset >= self._offset_max:
            self._offset = self._offset_max
            return
        self._offset = self.find_prev_newline(offset) + 1
        self.go_up()
        self.update_lines()

    def go_top(self) -> None:
        self._offset = 0
        self.update_lines()

    def go_bottom(self) -> None:
        self._offset = self._offset_max
        self.update_lines()

    def go_up(self, lines: int = 1) -> None:
        offset = self._offset
        for i in range(lines):
            if offset == 0:
                break
            offset = self.find_prev_newline(offset - 1)
            if offset == -1:
                self._offset = 0
                break
            self._offset = offset + 1  # at the start of the next line
        self.update_lines()

    def go_down(self, lines: int = 1) -> None:
        offset = self._offset
        for _ in range(lines):
            if self._offset >= self._offset_max:
                self._offset = self._offset_max
                break
            offset = self._mm.find(b"\n", offset)
            if offset == -1:
                break
            offset += 1
            self._offset = offset
        self.update_lines()
