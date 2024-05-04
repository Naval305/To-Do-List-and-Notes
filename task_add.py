import os
from kivy.uix.popup import Popup
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.textfield import MDTextField
from kivy.lang import Builder
from kivymd.uix.button import MDFloatingActionButton, MDIconButton
from kivy.utils import get_color_from_hex
from kivymd.uix.tooltip import MDTooltip
from kivymd.uix.chip import MDChip


class TooltipMDIconButton(MDIconButton, MDTooltip):
    pass


class PopContent(Popup):  # adding Popup conataining these widgets
    def __init__(self, app, **kwargs):
        super(PopContent, self).__init__(**kwargs)
        self.app = app
        self.title = "Add your Task"
        self.title_size = "20dp"
        self.size_hint = (0.82, 0.82)
        self.separator_color = [0, 0, 0, 1]
        self.title_align = "center"
        self.title_color = get_color_from_hex("#000000")
        self.background = "atlas://data/images/defaulttheme/button_pressed"
        self.container = MDFloatLayout()

        self.task = MDTextField(  # task field to enter task
            hint_text="Task...",
            size_hint=(0.95, 1),
            font_size="15sp",
            pos_hint={"center_x": 0.5, "y": 0.77},
            helper_text_mode="on_focus",
            mode="fill",
            # fill_color=( 5, 2, 7, 1),
            text_color=get_color_from_hex("#000000"),
        )
        self.task.focus = True
        self.container.add_widget(self.task)

        self.desc = MDTextField(  # description text field
            hint_text="Description...",
            size_hint=(0.95, 1),
            font_size="15sp",
            pos_hint={"center_x": 0.5, "y": 0.53},
            multiline=True,
            mode="fill",
            text_color=get_color_from_hex("#000000"),
        )
        self.container.add_widget(self.desc)

        self.notification = MDChip(  # notification on/ off chip
            text="Click here to enable Notification",
            icon="bell",
            pos_hint={"center_x": 0.5, "y": 0.15},
            selected_chip_color=(0.21176470535294, 0.098039627451, 1, 1),
            check=True,
        )
        self.notification.bind(on_release=lambda x: self.app.notification_show("True"))
        self.container.add_widget(self.notification)

        self.save_button = MDFloatingActionButton(  # button to save content
            icon="content-save",
            pos_hint={"x": 0.85, "y": 0.12},
            md_bg_color=get_color_from_hex("#ffffe0"),
        )
        # to check if task field is empty or not
        self.save_button.bind(
            on_press=lambda x: (
                self.app.task_desc(self.task.text, self.desc.text)
                if self.task.text != "" and app.check_all_fields() == True
                else app.warning()
            )
        )
        self.save_button.bind(
            on_release=lambda x: (
                self.dismiss()
                if self.task.text != "" and app.check_all_fields() == True
                else self.dismiss == False
            )
        )
        self.container.add_widget(self.save_button)

        self.cancel_button = TooltipMDIconButton(  # to go back to previous screen
            icon="step-backward",
            tooltip_text="back",
            user_font_size="30sp",
            pos_hint={"x": 0.001, "y": 0.001},
        )
        self.cancel_button.bind(on_release=lambda x: self.dismiss())
        self.container.add_widget(self.cancel_button)

        self.kv_file = Builder.load_file(
            os.path.join(os.getcwd(), "kv_files", "popup_screen_kv.kv")
        )
        self.container.add_widget(self.kv_file)
        self.add_widget(self.container)
