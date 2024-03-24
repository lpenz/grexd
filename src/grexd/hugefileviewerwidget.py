"""Widget that can display huge files"""

from typing import Optional

from prompt_toolkit.application import get_app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from prompt_toolkit.layout.containers import Container, Window

from .hugefilevieweruicontrol import HugeFileViewerUIControl

E = KeyPressEvent


class HugeFileViewerWidget:
    def __init__(
        self,
        filename: str,
        focusable: bool = True,
        uicontrol: Optional[HugeFileViewerUIControl] = None,
    ):
        self.filename = filename
        if uicontrol:
            self.control = uicontrol
        else:
            self.control = HugeFileViewerUIControl(
                filename=filename, key_bindings=self._init_key_bindings()
            )
        self.window = Window(self.control)

    def _init_key_bindings(self) -> KeyBindings:
        kb = KeyBindings()
        kb.add("home")(self.go_top)
        kb.add("c-home")(self.go_top)
        kb.add("escape", "home")(self.go_top)
        kb.add("end")(self.go_bottom)
        kb.add("c-end")(self.go_bottom)
        kb.add("escape", "end")(self.go_bottom)
        kb.add("up")(self.go_up)
        kb.add("down")(self.go_down)
        kb.add("pageup")(self.go_pageup)
        kb.add("pagedown")(self.go_pagedown)
        return kb

    def go_top(self, event: E) -> None:
        self.control.go_top()

    def go_bottom(self, event: E) -> None:
        self.control.go_bottom()

    def go_up(self, event: E) -> None:
        self.control.go_up()

    def go_down(self, event: E) -> None:
        self.control.go_down()

    def go_pageup(self, event: E) -> None:
        w = self.window
        if w.render_info:
            self.control.go_up(len(w.render_info.displayed_lines) + 1)

    def go_pagedown(self, event: E) -> None:
        w = self.window
        if w.render_info:
            self.control.go_down(len(w.render_info.displayed_lines) - 1)

    def get_style(self) -> str:
        if get_app().layout.has_focus(self.window):
            return "class:hugefilewidget"
        else:
            return "class:hugefilewidget.unfocused"

    def __pt_container__(self) -> Container:
        return self.window
