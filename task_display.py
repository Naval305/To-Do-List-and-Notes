from kivymd.uix.card import MDCard
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelTwoLine
from kivymd.uix.list import TwoLineListItem
from task_store import GetData
from kivymd.uix.chip import MDChip
from kivy.utils import get_color_from_hex
from kivymd.uix.label import MDLabel

class Card(MDCard):                                                            # adding Card with task and other deatils, also including widgets
    def __init__(self, app, task, desc, time, date, priority, **kwargs):
        super(Card, self).__init__(**kwargs)
        self.app = app
        self.task = task
        self.desc = desc
        self.time = time
        self.date = date
        self.priority = priority
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = 150
        self.elevation = 12
        self.float = MDFloatLayout()
                                          
        self.data = GetData(                                                   # sending data to GetData class to store it in file
            self.task,
            self.desc,
            self.time,
            self.date,
            self.priority
        )
        self.data.get_data()                                                   # calling get_data function of class GetData
        # adding PM & AM to time
        if int(self.time[0:2]) >= 13:
            temp = int(self.time[0:2])
            temp = temp-12
            if temp < 10:
                self._temp_time = str(0) + str(temp) + ':' + self.time[3:5] + ' PM'
            else:
                self._temp_time = str(temp) + ':' + self.time[3:5] + ' PM'

        elif int(self.time[0:2]) == 12 :
            self._temp_time = self.time + ' PM'
        elif int(self.time[0:2]) == 00:
            self._temp_time = str(12) + ':' + self.time[3:5] + ' AM'
        else:
            self._temp_time = self.time + ' AM'
        
        self.box= MDBoxLayout(                                                 # box layout to hold the content as buttons etc.
            orientation = 'horizontal', 
            size_hint = (.4, .20),
            pos_hint = {
                'top':.88,
                "x":.74
            }, 
            spacing = 7, 
            padding = 8
        )

        self.task_txt = MDExpansionPanel(                                      # to store task, description as well as date
            content = TwoLineListItem(
                text = self._temp_time,
                secondary_text = date
            ),
            panel_cls = MDExpansionPanelTwoLine(
                text = self.task,
                secondary_text = self.desc
            ),
            pos_hint = {
                "center_x":0.5,
                "center_y":0.56
            },
            size_hint=(0.96,1)
        )
        self.float.add_widget(self.task_txt)

        self.done = MDFillRoundFlatIconButton(                                 # to mark that task is completed
            icon = 'calendar-check',
            text = "Save",
            size_hint = (None, None), 
            size = (35,35),
            elevation = 10, 
            theme_text_color = 'Custom',
            text_color = [1,1,1,1]
        )
        self.done.bind(
            on_press = lambda x:self.app.delete_task(
                self.task,
                self.desc,
                self.time,
                self.date,
                self.priority,
                'done'
            )
        )
        self.done.bind(on_release= lambda x :self.app.anime3(self))
        self.box.add_widget(self.done)

        self.delete = MDFillRoundFlatIconButton(                               # to delete an unfinished task
            icon = 'delete',
            text = "Delete",
            size_hint = (None, None), 
            size = (35,35),
            elevation = 10, 
            theme_text_color = 'Custom',
            text_color = [1,1,1,1],
            md_bg_color = get_color_from_hex('#E3242B')
        )
        self.delete.bind(
            on_press= lambda x:self.app.delete_task(
                self.task,
                self.desc,
                self.time,
                self.date,
                self.priority,
                'delete'
            )
        )
        self.delete.bind(on_release= lambda x :self.app.anime2(self)) 
        self.box.add_widget(self.delete)

        self.line_lbl = MDLabel(
            text = "Click here to expand",
            pos_hint = {
                "x":.728,
                "y":.065
            }
        )
        self.float.add_widget(self.line_lbl)

        self.imp=MDChip(
            text="Imp",
            icon='',
            pos_hint={
                "x":.9,
                "y":.1
            },
            color= get_color_from_hex('#3944BC')
        )
        # to check if priority is high or not on basis of it assignng a chip as 'imp'
        if int(self.priority) == 2 or int(self.priority) == 3 or int(self.priority) == 4:
            self.float.add_widget(self.imp)

        self.float.add_widget(self.box)
        self.add_widget(self.float)