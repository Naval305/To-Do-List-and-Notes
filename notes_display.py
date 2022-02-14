from kivymd.uix.card import MDCard
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.textfield import MDTextFieldRect
from notes_store import GetNotes
from kivymd.uix.label import MDLabel

class Show_card_Notes(MDCard):
    def __init__(self, app, text, current_date_time, **kwargs):
        super(Show_card_Notes, self).__init__(**kwargs)
        self.app = app
        self.text = text
        self.current_date_time = current_date_time
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = 180
        self.elevation = 20
        self.float = FloatLayout()

        self.data = GetNotes(
            self.text,
            self.current_date_time
        )
        self.data.getdata()

        self._date_time = self.current_date_time[0:2] + ' ' + self.current_date_time[2:5] + ' ' + self.current_date_time[5:9] + ', ' + self.current_date_time[9:12] + ',  ' + self.current_date_time[12:14] + ':' + self.current_date_time[14:16] + ' ' + self.current_date_time[16:18]
        
        self.upper_btns = MDBoxLayout(
            orientation = 'vertical', 
            size_hint = (.4, .20),
            pos_hint = {
                "top":.25,
                "x":.9
            }, 
            spacing=14, 
            padding=8
        )

        self.notes_text = MDTextFieldRect(
            size_hint = (.85, .8), 
            pos_hint = {
                'x':.04,
                'top':.98
            },
            text=self.text, 
            readonly=True, 
            hint_text='No Description...',
            font_size='18sp'
        )
        self.notes_text.bind(
            on_double_tap= lambda x: self.app.read_notes_popup(
                self.notes_text.text,
                self.current_date_time
            )
        )
        self.float.add_widget(self.notes_text)

        self.edit= MDFloatingActionButton(
            icon='file-document-edit-outline',
            size_hint=(None, None), 
            size=(30,30),
            elevation=10, 
            theme_text_color='Custom',
            text_color=[1,1,1,1]
        )
        self.edit.bind(
            on_press=lambda x:self.app.edit_notes_popup(
                self.notes_text.text,
                self.current_date_time
            )
        )
        self.upper_btns.add_widget(self.edit)

        self.delete= MDFloatingActionButton(
            icon='delete',
            size_hint=(None, None), 
            size=(30,30),
            elevation=10, 
            theme_text_color='Custom',
            text_color=[1,1,1,1]
        )
        self.delete.bind(
            on_press= lambda x:self.app.delete_notes(
                self.notes_text.text,
                self.current_date_time
            )
        )
        self.delete.bind(
            on_release= lambda x :self.app.anime4(self)
        )
        self.upper_btns.add_widget(self.delete)

        self.label=MDLabel(
            text=self._date_time,
            size_hint=(.5,.2),
            pos_hint={'x':.04, 'y':.001}
        )
        self.float.add_widget(self.label)

        self.note=MDLabel(
            text = "Double Click on text to view",
            size_hint=(.5,.2),
            pos_hint={'x':.62, 'y':.001}
        )
        self.float.add_widget(self.note)
        

        self.float.add_widget(self.upper_btns)
        self.add_widget(self.float)