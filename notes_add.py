from kivy.uix.popup import Popup
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFillRoundFlatButton
from datetime import datetime
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.utils import get_color_from_hex
from kivymd.uix.button import MDIconButton, MDFloatingActionButton
from kivymd.uix.tooltip import MDTooltip

class TooltipMDIconButton(MDIconButton, MDTooltip):
    pass

class NotesContent(Popup):
    def __init__(self, app, **kwargs):
        super(NotesContent, self).__init__(**kwargs)
        self.app = app
        self.title = "Add your Text"
        self.title_size = "20dp"
        self.size_hint = (.9,.9)
        self.title_color = get_color_from_hex('#FF3D00')
        self.contain = MDFloatLayout()

        now = datetime.now()
        year_now = now.strftime("%Y")
        month_now = now.strftime("%b")
        day_now = now.strftime("%d")
        hour_now = now.strftime("%I")
        minutes_now = now.strftime("%M")
        x = now.strftime("%a")
        y = now.strftime("%p")

        current_date_time = str(day_now) + str(month_now) + (year_now) + str(x) + str(hour_now) + str(minutes_now) + str(y)

        self.textt = MDTextField(
            hint_text = "Enter your text here",
            multiline = True,
            pos_hint = {
                'top':.97,
                'center_x':.5
            },
            mode = "fill",
            fill_color = ( 255, 255, 255, .3),
            text_color = get_color_from_hex('#FFFFFF')
        )
        self.textt.focus = True
        self.contain.add_widget(self.textt)

        self.button = MDFillRoundFlatButton(
            text = "SAVE",
            pos_hint = {
                'top':.1,
                'center_x':.5
            }
        )
        self.button.bind(
            on_press = lambda x:self.app.Notes(
                self.textt.text,
                current_date_time
            )
        )
        self.button.bind(
            on_release = lambda x:self.dismiss()
        )
        self.contain.add_widget(self.button)

        self.cancel = TooltipMDIconButton(
            icon = "step-backward",
            tooltip_text = "back",
            user_font_size = "30sp",
            pos_hint = {
                'x':.001,
                'y':.001
            },
            theme_text_color = "Custom",
            text_color = app.theme_cls.primary_color   
        )
        self.cancel.bind(
            on_release = lambda x:self.dismiss()
        )
        self.contain.add_widget(self.cancel)

        self.add_widget(self.contain)

class read_notes(Popup):
    def __init__(self, app, text, current_date_time, **kwargs):
        super(read_notes, self).__init__(**kwargs)
        self.app = app
        self.text = text
        self.current_date_time=current_date_time
        self.title = "Your Text"
        self.title_size = "20dp"
        self.size_hint = (.95,.95)
        self.box = MDFloatLayout()
        self.background = 'atlas://data/images/defaulttheme/button_pressed'

        self.textt=MDTextField(
            hint_text="",
            text=self.text,
            pos_hint={
                'top':.97,
                'center_x':.5
            },
            multiline= True,
            readonly=True,
            text_color=get_color_from_hex('#000000')
        )
        self.textt.focus = True
        self.box.add_widget(self.textt)

        self.button=MDFloatingActionButton(
            icon="content-save-edit-outline",
            pos_hint={
                'x':.85,
                'y':.12
            },
            md_bg_color= app.theme_cls.primary_light
        )
        self.button.bind(
            on_press=lambda x:self.app.edit_notes_popup(
                self.textt.text,self.current_date_time
            )
        )
        self.button.bind(
            on_release=lambda x:self.dismiss()
        )
        self.box.add_widget(self.button)

        self.cancel=TooltipMDIconButton(
            icon="step-backward",
            tooltip_text="back",
            user_font_size= "30sp",
            pos_hint={
                'x':.001,
                'y':.001
            },
            theme_text_color= "Custom",
            text_color= app.theme_cls.primary_color
        )
        self.cancel.bind(
            on_release=lambda x:self.dismiss()
        )
        self.box.add_widget(self.cancel)

        self.add_widget(self.box)


class Notes_edit(Popup):
    def __init__(self, app, text, current_date_time, **kwargs):
        super(Notes_edit, self).__init__(**kwargs)
        self.app = app
        self.text = text
        self.current_date_time = current_date_time
        self.title = "Add your Task"
        self.title_size =  "20dp"
        self.size_hint = (.9,.9)

        self.floatbox=MDFloatLayout()

        self.textt=MDTextField(
            hint_text="",
            text=self.text, 
            pos_hint={
                'top':.97,
                'center_x':.5
            },
            multiline= True,
            mode= "fill",
            fill_color=( 255, 255, 255, .3),
            text_color=get_color_from_hex('#FFFFFF')
        )
        self.floatbox.add_widget(self.textt)
        

        self.button=MDFillRoundFlatButton(
            text="SAVE",
            pos_hint={'top':.1,'center_x':.5}
        )
        self.button.bind(
            on_press=lambda x:self.app.Notes(
                self.textt.text,
                self.current_date_time
            )
        )
        self.button.bind(
            on_release=lambda x:self.dismiss()
        )
        self.floatbox.add_widget(self.button)

        self.buttn_back=TooltipMDIconButton(
            icon="step-backward",
            tooltip_text="back",
            user_font_size= "30sp",
            pos_hint={
                'x':.001,
                'y':.001
            },
            theme_text_color= "Custom",
            text_color= app.theme_cls.primary_color
        )
        self.buttn_back.bind(on_release=lambda x:self.dismiss())
        self.floatbox.add_widget(self.buttn_back)

        self.add_widget(self.floatbox)