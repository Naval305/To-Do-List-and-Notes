from kivy.lang import Builder
from kivymd.app import MDApp
from task_add import PopContent
from kivymd.uix.picker import MDTimePicker,MDDatePicker
from task_display import Card
from task_store import GetData
from kivy.animation import Animation
import subprocess
from notes_add import NotesContent, read_notes, Notes_edit
from notes_display import Show_card_Notes
from notes_store import GetNotes
from kivymd.uix.menu import MDDropdownMenu
from  kivymd.uix.picker import MDThemePicker
from datetime import datetime
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDIconButton
from kivy.utils import get_color_from_hex
from random import randint
from kivymd.toast import toast

class Test(MDApp):
    condition=''
    check_date=''
    check_time=''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_file('kv_files\\main_screen_kv.kv')
        with open('database_files\\finished_tasks_db.txt', 'r') as o:
            p=o.readlines()
        menu_items = [
            {
                "text": f" {p[i]}",
                "viewclass": "OneLineListItem",
            } for i in range(len(p))
        ]
        self.menu = MDDropdownMenu(
            caller = self.screen.ids.buttonn,
            items = menu_items,
            width_mult = 3,
        )
       
    def build(self):
        self.theme_cls.primary_palette = "LightGreen"
        #self.theme_cls.primary_hue = "200"
        return self.screen

    def check_all_fields(self):                                             # checks if time and date are entered or not
        if self.check_time == 'ok' and self.check_date == 'ok':
            return True
        else:
            return False

    def warning(self):                                                      # opens a snackbar if task/ date/ time is not entered
        Snackbar(text="Make sure you entered everything (Task, Date, Time)").open()

    def finished(self, task):                                                # to store the finished tasks in seperate file
        with open('database_files\\finished_tasks_db.txt','a') as finished_items:
            finished_items.write(f'{task}\n')

    def delete_task(self, task, desc, time, date, priority, condition):     # to delete particular task and it's content(desc, date, time, etc.)
        data_items = GetData('', '', '', '', '')
        data_items.delete_data(task, desc, time, date, priority)
        if condition == 'delete':
            pass
        elif condition == 'done':
            # if condition is done that means task is finished
            self.finished(task)

    def delete_notes(self, task, current_date_time):                        # to delete particular notes and time
        app = GetNotes('' ,'')
        app.deletedata(task, current_date_time)

    def open_popup(self):                                                   # open popup(task adding screen)
        pop_screen=PopContent(app)
        pop_screen.open()

    def opennotes(self):                                                    # open popup(notes adding screen)
        pop_notes=NotesContent(app)
        pop_notes.open()

    def read_notes_popup(self, text, current_date_time):                    # open popup(just to read notes)
        readnotes=read_notes(app, text, current_date_time)
        readnotes.open()

    def edit_notes_popup(self, text, current_date_time):                    # open popup(to edit notes)
        notes_edit=Notes_edit(app, text, current_date_time)
        notes_edit.open()

    def show_date_picker(self):                                             # to open date choosing dialog screen
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save = self.get_date)
        date_dialog.open()

    def show_time_picker(self):                                             # to open time choosing dialog screen
        time_dialog = MDTimePicker()
        time_dialog.bind(time = self.get_time)
        time_dialog.open()

    def get_date(self, instance, value, date_range):                        # to store the date in variables
        self.year = str(value.year)
        self.month = str(value.month)
        self.day = str(value.day)
        # adding 0 to single digit numbers in date
        if int(self.day) < 10:
            self.day = "0" + str(self.day)

        if int(self.month) < 10:
            self.month = "0" + str(self.month)

        self.day_month_yr = self.day + '/' + self.month + '/' + self.year
        self.check_date = 'ok'

    def get_time(self, instance, time):                                     # to store time in variables
        self.hour = str(time.hour)
        self.min = str(time.minute)
        # adding 0 to single digit numbers in time
        if int(self.hour) < 10:
            self.hour = "0" + str(self.hour)

        if int(self.min) < 10:
            self.min = "0" + str(self.min)

        self.hour_min = self.hour + ":" + self.min
        self.check_time = 'ok'

    def callbck(self, slider_value):                                        # getting priority value as 1, 2, 3, 4
        self.priority = int(slider_value)

    def notification_show(self, condition):                                 # to show notifications or not
        self.condition = condition

    def task_desc(self, task, desc):                                        # getting task and description from task adder class(popup)
        self.task = task
        self.description = desc
        self.task_content('user')

    def Notes(self, text, current_date_time):                               # to add notes to widget function
        self.text = text
        self.current_date_time = current_date_time
        self.notes_content('pass')

    def task_content(self, source):                                         # to send the task, desc, date, time, priority to be shown in widget(MDCard)
        self.source = source
        # to confirm that task is added by user
        if self.source == 'user':
            self.card = self.root.ids.box
            # sending content to card
            self.card.add_widget(
                Card(
                    app,
                    self.task,
                    self.description,
                    self.hour_min,
                    self.day_month_yr,
                    self.priority
                )
            )
            # if task is sent by user and has turned on notification, this will call the subprocess and open notification handeling file
            if self.condition == 'True':    
                self.spawn_program(
                    [
                        'python',
                        'notification.py'
                    ]
                )
            toast("Task Saved Successfully")

        # to confirm that task is from stored data in file
        elif self.source == 'database':
            self.stored_task_data= self.stored_task_data
            # iterating over the content as it is in form of list
            for self.one_round in self.stored_task_data:
                self.card = self.root.ids.box
                self.task = self.one_round[0]
                self.description= self.one_round[1]
                self.hour_min = self.one_round[2]
                self.day_month_yr = self.one_round[3]
                self.priority = self.one_round[4]

                self.card.add_widget(
                    Card(
                        app,
                        self.task,
                        self.description,
                        self.hour_min,
                        self.day_month_yr,
                        self.priority
                    )
                )

    def notes_content(self, cond):                                          # to send the notes(text) to be shown in widget(MDCard)
        self.cond=cond

        if self.cond=='pass':
            self.card2=self.root.ids.box2
            self.card2.add_widget(
                Show_card_Notes(
                    app,
                    self.text,
                    self.current_date_time
                )
            )
            toast("Notes Saved Successfully")

        elif self.cond == 'databaase':
            self.gdata=self.gdata

            for self.one in self.gdata:
                self.card2 = self.root.ids.box2
                self.text = self.one[0]
                self.current_date_time = self.one[1]
                self.card2.add_widget(
                    Show_card_Notes(
                        app,
                        self.text,
                        self.current_date_time
                    )
                )

    def delete_all(self):                                                   # open dialog box to confirm if user wants to delete all tasks
        self.dialog = MDDialog(
                title = "Delete all on going tasks?",
                text = "This will delete all the tasks listed permanently and application will be restarted",
                buttons = [
                    MDFlatButton(
                        text = "CANCEL",
                        on_release = lambda x: self.dialog.dismiss()
                    ),
                    MDRaisedButton(
                        text = "DELETE",
                        md_bg_color =  get_color_from_hex('FF0000'),
                        on_press = lambda x: self.restart_delete_content(),
                        on_release = lambda x: self.dialog.dismiss()
                    ),
                ],
            )
        self.dialog.open()

    def restart_delete_content(self):                                       # to delete all file conetent and restart app
        task_file = open("database_files\\tasks_db.txt", "r+")
        task_file.truncate(0)
        task_file.close()
        self.stop()
        self.spawn_program(
            [
                'python',
                'main.py'
            ]
        )

    def quote_info(self):
        self.quote_dialog = MDDialog(
                title =( '[color=FF3D00]\"[/color][b]' + self.the_quote + '[/b][color=FF3D00]\"[/color]\n\n' + 'By: [b][color=FF3D00]' + self.whose + '[/color][/b]')
            )
        self.quote_dialog.open()

    def checkPASS(self):
        p_file=open("database_files\\password.txt", "r")
        temp_file=p_file.read()
        if temp_file == '':
            self.root.ids.screen_manager.current = "scr 2"
        else:
            self.root.ids.screen_manager.current = "unhide_scr"

    def on_start(self):      
        # to make theme dark after 6 pm                                     # when application starts, this runs
        theme_f = open('database_files\\theme.txt', 'r')
        themecurrent = theme_f.read()
        if themecurrent == 'On':

            if int(datetime.now().strftime('%H')) > 18:
                self.theme_cls.theme_style = "Dark"
        else:
            pass
        
        try:
            with open('database_files\\quotes_generator.txt') as quote:
                self.all_quotes = quote.readlines()
                self.all_quotes_= [quo.strip() for quo in self.all_quotes[1:]]
                self.chosen = self.all_quotes_[randint(0, len(self.all_quotes_))]
                self.the_quote = self.chosen[:self.chosen.find(';')]
                self.whose = self.chosen[self.chosen.find(';')+1:].title()
            Snackbar(
                text = "[color=#000000]" + self.the_quote + "[/color]",
                buttons = [ 
                    MDIconButton(
                        icon = "information",
                        on_release = lambda x:self.quote_info()
                    ),
                ],
                bg_color = get_color_from_hex('#b66d3e'),
                snackbar_x = "10dp",
                snackbar_y = "10dp",
                size_hint_x = .85,
                duration = 6
            ).open()

        except IndexError:
            pass

        self.stored_task_data=[]
        data_items= GetData('','','','','')  
        self.all_data_lines = data_items.send_data()
        # to select single lines of data
        if self.all_data_lines != 'database empty':
            for one_line in self.all_data_lines:
                self.stored_task_data.append(
                    one_line[5:].split(';')
                )
            self.task_content('database')
        else: 
            pass

        self.gdata = []
        note = GetNotes('','')
        self.all = note.senddata()
        if self.all != 'databaase empty':
            for one in self.all:
                self.gdata.append(
                    one[5:].split(';')
                )

            self.notes_content('databaase')
        else:
            pass

    def theme(self):                                                        # to set theme as automatic or not
        theme_file = open('database_files\\theme.txt', 'r')
        theme_current = theme_file.read()

        if theme_current == 'On':
            theme_write = open('database_files\\theme.txt', 'w')
            theme_write.write('Off')
            toast("Automatic theme change is OFF")
        else:
            theme_write = open('database_files\\theme.txt', 'w')
            theme_write.write('On')
            toast("Automatic theme change is ON")

    def unhide(self):                                                       # to check if password is correct or not
        password = self.root.ids.password.text
        password_file = open('database_files\\password.txt', 'r')
        self.passw = password_file.readline()
        if password == self.passw:
            self.root.ids.screen_manager.current = "scr 2"
        else:
            self.pass_dialog = MDDialog(
                title = "Wrong Password!",
                buttons = [
                    MDRaisedButton(
                        text = "Try Again...",
                        on_release = lambda x: self.pass_dialog.dismiss()
                    ),    
                ],
            )
            self.pass_dialog.open()
            self.root.ids.password.text = ""
            
    def set_pass(self):                                                     # function to set new password
        check_pass = open('database_files\\password.txt', 'r')
        self.checkpass_file = check_pass.read()

        if self.checkpass_file == "":
            self.root.ids.screen_manager.current = "pass_set"
        else:
            self.root.ids.screen_manager.current = "change_pass"

    def check_file_pass(self):                                              # to confirm password entered
        check_old_pass=open('database_files\\password.txt', 'r+')
        old_pass = check_old_pass.read()

        if old_pass == self.root.ids.pass_change.text:
            check_old_pass.truncate(0)
            check_old_pass.close()
            self.root.ids.screen_manager.current = "pass_set"
        else:
            self.wrong_pass_dialog = MDDialog(
                title = "Wrong Password!",
                buttons = [
                    MDRaisedButton(
                        text = "Try Again...",
                        on_release = lambda x: self.wrong_pass_dialog.dismiss()
                    ),    
                ],
            )
            self.wrong_pass_dialog.open()

    def remove_pass(self):                                                  # check if password already set or not
        check_pas = open('database_files\\password.txt', 'r')
        self.checkpassfile = check_pas.read()

        if self.checkpassfile == "":
            self.root.ids.screen_manager.current = "settings"
            toast("No password set!")
        else:
            self.root.ids.screen_manager.current = "remove_pass"

    def remove_file_pass(self):                                             # remove password from file
        checkoldpass=open('database_files\\password.txt', 'r+')
        Oldpass = checkoldpass.read()
        if Oldpass == self.root.ids.rmv_pass.text:
            checkoldpass.truncate(0)
            checkoldpass.close()
            toast("Password removed successfully")
            self.root.ids.screen_manager.current = "settings"
        else:
            self.wrongpass_dialog = MDDialog(
                title = "Wrong Password!",
                buttons = [
                    MDRaisedButton(
                        text = "Try Again...",
                        on_release = lambda x: self.wrongpass_dialog.dismiss()
                    ),    
                ],
            )
            self.wrongpass_dialog.open()

    def save_pass(self):                                                    # to save new pass in file
        self.new_pass = self.root.ids.pass_confirm.text
        self.confirm_pass = self.root.ids.pass_confirm2.text
        
        if self.new_pass == self.confirm_pass:
            new_pass_file = open('database_files\\password.txt', 'a')
            new_pass_file.write(f'{self.new_pass}')
            self.root.ids.screen_manager.current = "settings"
            toast("Password Changed Successfully")
        else:
            self.pass_confirm_dialog = MDDialog(
                title = "Password do not match!",
                buttons = [
                    MDRaisedButton(
                        text = "Try Again...",
                        on_release = lambda x: self.pass_confirm_dialog.dismiss()
                    ),    
                ],
            )
            self.pass_confirm_dialog.open()

    def delete_finished(self):                                              # dialog to delete finished tasks list
        self.finished_dialog = MDDialog(
                title = "Delete all on completed tasks?",
                text = "This will delete all the completed tasks list permanently",
                buttons = [
                    MDFlatButton(
                        text = "CANCEL",
                        on_release = lambda x: self.finished_dialog.dismiss()
                    ),
                    MDRaisedButton(
                        text = "DELETE",
                        md_bg_color =  get_color_from_hex('FF0000'),
                        on_press = lambda x: self.deletefinished(),
                        on_release = lambda x: self.finished_dialog.dismiss()
                    ),
                ],
            )
        self.finished_dialog.open()
    
    def deletefinished(self):                                               # deletion of finished tasks list
        finish = open('database_files\\finished_tasks_db.txt', 'w')
        finish.write('COMPLETED TASKS:')
        toast("Successfully deleted completed list tasks")

    def spawn_program(self, program):                                       # use of subprocess to start another process
        subprocess.Popen(program)

    def show_theme_picker(self):                                            # to display theme picker at bottom left
        theme_dialog = MDThemePicker()
        theme_dialog.open()
    def about_App(self):
        with open('database_files\\about_app.txt') as about:
            self.content= about.read()
            self.about_app= MDDialog(
                title='About This App?', 
                text=self.content+'\n',
                size_hint=(.458, .80), 
                pos_hint={'center_x':.5, 'top':.90}
                )
            self.about_app.open()
    # Below functions are for animations
    def anime3(self, target3):
        self.target3 = target3
        anime = Animation(
            height=70,
            md_bg_color = [0,1,0,0.2],
            elevation = 0,
            d = 0.3
        )
        anime.start(self.target3)
        anime.bind(on_complete = self.dele2)

    def dele2(self, *args):
        self.root.ids['box'].remove_widget(self.target3)

    def anime2(self, target2):
        self.target2 = target2
        anime = Animation(
            height=70,
            md_bg_color=[1,0,0,0.2],
            elevation=0,
            d=0.3
        )
        anime.start(self.target2)
        anime.bind(on_complete = self.dele)
        
    def dele(self, *args):
        self.root.ids['box'].remove_widget(self.target2)

    def anime4(self, target3):
        self.target3 = target3
        anime= Animation(
            height=70,
            md_bg_color=[1,0,0,0.2],
            elevation=0,
            d=0.3
        )
        anime.start(self.target3)
        anime.bind(on_complete = self.dele8)

    def dele8(self, *args):
        self.root.ids['box2'].remove_widget(self.target3)

if __name__=='__main__':       
    app=Test()
    app.run()