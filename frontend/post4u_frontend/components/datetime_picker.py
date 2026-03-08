import reflex as rx
from typing import Set

class DatePicker(rx.Component):
    """A DatePicker component based on react-datepicker."""

    library = "react-datepicker"
    tag = "DatePicker"

    selected: rx.Var[str]

    placeholder_text: rx.Var[str] = "2026-03-19 00:00"

    date_format: rx.Var[str] = "yyyy-MM-dd HH:mm"
    show_time_select: rx.Var[bool] = True
    time_format: rx.Var[str] = "HH:mm"

    # Handle the date conversion in the event trigger
    def get_event_triggers(self) -> dict[str, rx.Var]:
        return {
            **super().get_event_triggers(),
            "on_change": lambda date: [date],
        }

    @classmethod
    def create(cls, *children, **props):
        if "selected" in props and isinstance(props["selected"], str) and props["selected"] == "":
            props["selected"] = None
        return super().create(*children, **props)

    def _get_imports(self) -> rx.utils.imports.ImportDict:
        return rx.utils.imports.merge_imports(
            super()._get_imports(),
            {"": {"react-datepicker/dist/react-datepicker.css"}},
        )

# Helper function for easier usage
def date_picker(**props):
    return DatePicker.create(**props)
