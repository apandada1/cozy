from gi.repository import Gtk, Pango, GObject, Gdk

from cozy.control.string_representation import seconds_to_str
from cozy.model.chapter import Chapter


@Gtk.Template.from_resource('/com/github/geigi/cozy/chapter_element.ui')
class ChapterElement(Gtk.EventBox):
    __gtype_name__ = "ChapterElement"

    icon_event_box: Gtk.EventBox = Gtk.Template.Child()
    icon_stack: Gtk.Stack = Gtk.Template.Child()
    number_label: Gtk.Label = Gtk.Template.Child()
    play_icon: Gtk.Image = Gtk.Template.Child()
    title_label: Gtk.Label = Gtk.Template.Child()
    duration_label: Gtk.Label = Gtk.Template.Child()

    def __init__(self, chapter: Chapter):
        self.selected = False
        self.chapter: Chapter = chapter

        super().__init__()

        self.connect("enter-notify-event", self._on_enter_notify)
        self.connect("leave-notify-event", self._on_leave_notify)
        self.connect("button-press-event", self._on_button_press)
        self.set_tooltip_text(_("Play this part"))

        # This box contains all content
        self.box = Gtk.Box()
        self.box.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.box.set_spacing(3)
        self.box.set_halign(Gtk.Align.FILL)
        self.box.set_valign(Gtk.Align.CENTER)

        # These are the widgets that contain data
        self.play_img = Gtk.Image()
        no_label = Gtk.Label()
        title_label = Gtk.Label()
        dur_label = Gtk.Label()

        self.play_img.set_margin_right(5)
        self.play_img.props.width_request = 16

        if self.chapter.number > 0:
            no_label.set_text(str(self.chapter.number))
        no_label.props.margin = 4
        no_label.set_margin_right(7)
        no_label.set_margin_left(0)
        no_label.set_size_request(30, -1)
        no_label.set_xalign(1)

        self.number_label.set_text(str(self.chapter.number))
        self.title_label.set_text(self.chapter.name)
        self.duration_label.set_text(seconds_to_str(self.chapter.length))

        self.icon_event_box.connect("enter-notify-event", self._on_enter_notify)
        self.icon_event_box.connect("leave-notify-event", self._on_leave_notify)

    def _on_button_press(self, _, event):
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button != 1:
            return False

        self.emit("play-pause-clicked", self.chapter)
        return True

    def _on_enter_notify(self, _, __):
        if not self.selected:
            self.icon_stack.set_visible_child_name("play_icon")
        self.get_style_context().add_class("box_hover")
        self.play_icon.get_style_context().add_class("box_hover")

    def _on_leave_notify(self, _, __):
        self.get_style_context().remove_class("box_hover")
        self.play_icon.get_style_context().remove_class("box_hover")

        if not self.selected:
            self.icon_stack.set_visible_child_name("number")

    def select(self):
        self.selected = True
        self.icon_stack.set_visible_child_name("play_icon")

    def deselect(self):
        self.selected = False
        self.icon_stack.set_visible_child_name("number")

    def set_playing(self, playing):
        if playing:
            self.play_icon.set_from_icon_name("pause-symbolic", Gtk.IconSize.SMALL_TOOLBAR)
        else:
            self.play_icon.set_from_icon_name("play-symbolic", Gtk.IconSize.SMALL_TOOLBAR)


GObject.type_register(ChapterElement)
GObject.signal_new('play-pause-clicked', ChapterElement, GObject.SIGNAL_RUN_LAST, GObject.TYPE_PYOBJECT,
                   (GObject.TYPE_PYOBJECT,))
