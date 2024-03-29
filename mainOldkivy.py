from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDToolbar
from kivy.uix.button import Button
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.screen import MDScreen
from kivy.uix.textinput import TextInput
from kivymd.uix.dropdownitem import MDDropDownItem
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.filechooser import FileChooserListView
from kivymd.uix.button import MDRaisedButton



class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.default_username = "admin"
        self.default_password = "admin"
        
        self.username_field = MDTextField(
            hint_text="Username",
            size_hint=(None, None),
            width=300,
            pos_hint={"center_x": 0.5, "center_y": 0.6},
        )
        self.password_field = MDTextField(
            hint_text="Password",
            password=True,
            size_hint=(None, None),
            width=300,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.login_button = MDFillRoundFlatButton(
            text="Login",
            size_hint=(None, None),
            width=150,
            pos_hint={"center_x": 0.5, "center_y": 0.4},
            on_release=self.login,
        )
        self.add_widget(self.username_field)
        self.add_widget(self.password_field)
        self.add_widget(self.login_button)

    def login(self, *args):
        username = self.username_field.text
        password = self.password_field.text
        if username == self.default_username and password == self.default_password:
            self.manager.current = "menu_screen"
        else:
            self.password_field.text = ""  # Clear password field on incorrect login


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        num_buttons = 3
        button_height = 1 / num_buttons
        
        self.layout = MDBoxLayout(orientation="vertical", padding=40, spacing=20)

        self.button1 = MDFillRoundFlatButton(
            text="Find your Expert !",
            size_hint=(1, button_height),
            pos_hint={"center_x": 0.5, "center_y": 0.75},
            on_release=self.button1_click,
        )
        self.button2 = MDFillRoundFlatButton(
            text="Are you an Expert",
            size_hint=(1, button_height),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            on_release=self.button2_click,
        )
        self.button3 = MDFillRoundFlatButton(
            text="Your Bookings",
            size_hint=(1, button_height),
            pos_hint={"center_x": 0.5, "center_y": 0.25},
            on_release=self.button3_click,
        )

        self.layout.add_widget(self.button1)
        self.layout.add_widget(self.button2)
        self.layout.add_widget(self.button3)
        self.add_widget(self.layout)

    def button1_click(self, instance):
        self.manager.current = "screen1"

    def button2_click(self, instance):
        self.manager.current = "screen2"

    def button3_click(self, instance):
        self.manager.current = "screen3"


class Screen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        # Create a vertical box layout to hold the toolbar and grid layout
        self.box_layout = MDBoxLayout(orientation="vertical")
        self.add_widget(self.box_layout)

        # Add the toolbar to the box layout
        self.toolbar = MDToolbar(
            title="Screen 1",
            pos_hint={"top": 1},
        )
        self.toolbar.left_action_items = [["arrow-left", lambda x: self.go_back()]]
        self.toolbar.right_action_items = [["magnify", lambda x: self.open_search_bar()]]
        self.box_layout.add_widget(self.toolbar)

        # Layout to hold the cards
        self.scroll_view = ScrollView()
        self.grid_layout = MDGridLayout(cols=1, spacing=10, padding=20, size_hint_y=None)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))
        self.scroll_view.add_widget(self.grid_layout)
        self.box_layout.add_widget(self.scroll_view)

        # Call open_search method to fetch all data when the screen is opened
        self.open_search()

    def go_back(self):
        self.manager.current = "menu_screen"
    
    def open_search_bar(self):
        # Clear existing widgets in the grid layout
        self.grid_layout.clear_widgets()

        # Add search bar to toolbar
        self.search_bar = TextInput(hint_text="Search", multiline=False, size_hint=(None, None), size=(200, 50))
        self.search_bar.bind(on_text_validate=self.search)
        self.toolbar.right_action_items = [["close", lambda x: self.close_search_bar()]]
        self.toolbar.add_widget(self.search_bar)

    def close_search_bar(self):
        self.toolbar.remove_widget(self.search_bar)
        self.toolbar.right_action_items = [["magnify", lambda x: self.open_search_bar()]]
        self.open_search()

    def search(self, *args):
        query = self.search_bar.text
        self.open_search(query)

    def open_search(self, query=None):
        # Call the backend API to fetch the data
        data = self.fetch_data_from_backend()

        # Filter the data based on the search query if provided
        if query:
            filtered_data = [item for item in data if query.lower() in item["title"].lower()]
        else:
            filtered_data = data

        # Clear the existing grid layout
        self.grid_layout.clear_widgets()

        # Update the grid layout with the filtered data
        for item in filtered_data:
            card = MDCard(size_hint=(1, None), height=100)
            card.add_widget(Button(text=item["title"], on_release=lambda x: self.open_detail(item["title"])))
            card.add_widget(Button(text=item["description"], on_release=lambda x: self.open_detail(item["title"])))
            self.grid_layout.add_widget(card)

    def fetch_data_from_backend(self):
        # Call your backend API to fetch all data
        # For now, returning dummy data
        return [
            {"title": "Item 1", "description": "Description for Item 1"},
            {"title": "Item 2", "description": "Description for Item 2"},
            {"title": "Item 3", "description": "Description for Item 3"},
            {"title": "Another Item", "description": "Description for Another Item"},
            # Add more dummy data as needed
        ]

class Screen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.popup = None
        self.selected_file_label = Label(text="No file selected")

        self.box_layout = MDBoxLayout(orientation="vertical", padding=20, spacing=20)
        self.add_widget(self.box_layout)

        self.toolbar = MDToolbar(
            title="Screen 2",
            pos_hint={"top": 1},
        )
        self.toolbar.left_action_items = [["arrow-left", lambda x: self.go_back()]]
        self.box_layout.add_widget(self.toolbar)

        # Layout to hold the form fields
        self.layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        # Create form fields
        self.upload_photo_button = MDFillRoundFlatButton(text="Upload Photo")
        self.upload_photo_button.bind(on_release=self.upload_photo)

        self.phone_field = MDTextField(hint_text="Phone Number")
        self.email_field = MDTextField(hint_text="Email")

        self.dropdown_menu = MDTextField(hint_text="Select Option", readonly=True)
        self.dropdown_menu.bind(on_release=self.show_menu)
        # self.dropdown_menu.bind(on_focus=self.show_menu)

        self.description_field = MDTextField(hint_text="Description", multiline=True)
        self.keywords_field = MDTextField(hint_text="Keywords (comma separated)")
        self.rating_field = MDTextField(hint_text="Rating (out of 10)", input_filter="float")
        self.upload_proofs_button = MDFillRoundFlatButton(text="Upload Videos/Images/Documents of your skills")
        self.upload_proofs_button.bind(on_release=self.upload_proof)
        
        self.save_button = MDFillRoundFlatButton(text="Save", on_release=self.save_data)
        self.cancel_button = MDFillRoundFlatButton(text="Cancel", on_release=self.go_back)

        # Add form fields to the layout
        self.layout.add_widget(self.upload_photo_button)
        self.layout.add_widget(self.phone_field)
        self.layout.add_widget(self.email_field)
        self.layout.add_widget(self.dropdown_menu)
        self.layout.add_widget(self.description_field)
        self.layout.add_widget(self.keywords_field)
        self.layout.add_widget(self.rating_field)
        self.layout.add_widget(self.upload_proofs_button)
        # self.layout.add_widget(self.save_button)
        # self.layout.add_widget(self.cancel_button)

        # Add the layout to the box layout
        self.scroll_view = ScrollView()
        self.scroll_view.add_widget(self.layout)
        self.box_layout.add_widget(self.scroll_view)
        button_layout = MDBoxLayout(orientation="horizontal", spacing=10, size_hint_y=None, height="48dp")
        button_layout.add_widget(self.save_button)
        button_layout.add_widget(self.cancel_button)
        self.box_layout.add_widget(button_layout)

    def go_back(self, *args):
        self.manager.current = "menu_screen"

    def upload_photo(self, *args):
        file_chooser = FileChooserIconView()
        file_chooser.bind(on_submit=self.handle_photo_selection)
        popup = Popup(title="Upload Photo", content=file_chooser, size_hint=(None, None), size=(600, 400))
        popup.open()
    
    def handle_photo_selection(self, chooser, path, filename):
        # Handle the selected photo file
        print("Selected photo file:", filename)
        if self.popup:
            self.popup.dismiss()
        self.selected_file_label.text = f"Selected file: {filename}"
  
    def upload_proof(self, *args):
        file_chooser = FileChooserListView()
        file_chooser.filters = ["*.jpg", "*.png", "*.jpeg", "*.mp4", "*.mov", "*.avi", "*.pdf", "*.doc", "*.docx"]
        file_chooser.bind(on_submit=self.handle_proof_data_selection)
        popup = Popup(title="Upload Video", content=file_chooser, size_hint=(None, None), size=(600, 400))
        popup.open()

    def handle_proof_data_selection(self, chooser, path, filename):
        # Handle the selected video file
        print("Selected file:", filename)
        if self.popup:
            self.popup.dismiss()
        self.selected_file_label.text = f"Selected file: {filename}"

    def save_data(self, *args):
        # Implement logic to save data to the backend
        pass
    
    def show_menu(self, instance):

        menu_content = BoxLayout(orientation='vertical', spacing=10)
        for item_text in ["Item 1", "Item 2", "Item 3"]:
            item_button = MDRaisedButton(text=item_text)
            item_button.bind(on_release=lambda btn, txt=item_text: self.handle_dropdown_selection(instance, txt))
            menu_content.add_widget(item_button)

        menu = Popup(
            title='Select Option',
            content=menu_content,
            size_hint=(None, None),
            size=(200, 200),
        )
        menu.open()

    def handle_dropdown_selection(self, instance, selected_item):
        instance.text = selected_item  # Update the text of the dropdown menu
        # instance.focus = False


class Screen22(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.box_layout = MDBoxLayout(orientation="vertical")
        self.add_widget(self.box_layout)

        self.toolbar = MDToolbar(
            title="Screen 2",
            pos_hint={"top": 1},
        )
        self.toolbar.left_action_items = [["arrow-left", lambda x: self.go_back()]]
        # self.add_widget(self.toolbar)
        self.box_layout.add_widget(self.toolbar)

        # Layout to hold the form
        self.layout = ScrollView()
        self.form_layout = GridLayout(cols=1, spacing=10, padding=20, size_hint_y=None)
        self.form_layout.bind(minimum_height=self.form_layout.setter('height'))
        self.layout.add_widget(self.form_layout)
        self.box_layout.add_widget(self.layout)

         # Create form fields
        self.upload_photo_button = MDFillRoundFlatButton(text="Upload Photo", on_release=self.upload_photo)
        self.phone_field = MDTextField(hint_text="Phone Number")
        self.email_field = MDTextField(hint_text="Email")
        self.dropdown_menu = MDTextField(hint_text="Select Option", readonly=True)
        self.dropdown_menu.bind(on_focus=self.show_menu)
        self.description_field = MDTextField(hint_text="Description", multiline=True)
        self.keywords_field = MDTextField(hint_text="Keywords (comma separated)")
        self.rating_field = MDTextField(hint_text="Rating (out of 10)", input_filter="float")
        self.upload_video_button = MDFillRoundFlatButton(text="Upload Videos", on_release=self.upload_video)
        self.upload_photo_button = MDFillRoundFlatButton(text="Upload Photos", on_release=self.upload_photo)
        self.save_button = MDFillRoundFlatButton(text="Save", on_release=self.save_data)
        self.cancel_button = MDFillRoundFlatButton(text="Cancel", on_release=self.go_back)


        # Add form fields to the layout
        self.box_layout.add_widget(self.upload_photo_button)
        self.box_layout.add_widget(self.phone_field)
        self.box_layout.add_widget(self.email_field)
        self.box_layout.add_widget(self.dropdown_menu)
        self.box_layout.add_widget(self.description_field)
        self.box_layout.add_widget(self.keywords_field)
        self.box_layout.add_widget(self.rating_field)
        self.box_layout.add_widget(MDFillRoundFlatButton(text="Upload Videos", on_release=self.upload_video))
        self.box_layout.add_widget(MDFillRoundFlatButton(text="Save", on_release=self.save_data))
        self.box_layout.add_widget(MDFillRoundFlatButton(text="Cancel", on_release=self.go_back))
        # self.box_layout.add_widget(self.form_layout)

    def go_back(self, *args):
        self.manager.current = "menu_screen"

    def upload_photo(self, *args):
        # Implement logic to upload photo
        pass

    def upload_video(self, *args):
        # Implement logic to upload video
        pass

    def save_data(self, *args):
        # Implement logic to save data to the backend
        pass
    
    def show_menu(self, instance, value):
        if value:
            menu_content = BoxLayout(orientation='vertical')
            menu_content.add_widget(Label(text='Item 1'))
            menu_content.add_widget(Label(text='Item 2'))
            menu_content.add_widget(Label(text='Item 3'))

            menu = Popup(
                title='Select Option',
                content=menu_content,
                size_hint=(0.9, 0.9),
            )
            menu.open()

class Screen3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.toolbar = MDToolbar(
            title="Screen 3",
            pos_hint={"top": 1},
        )
        self.toolbar.left_action_items = [["arrow-left", lambda x: self.go_back()]]
        self.add_widget(self.toolbar)

    def go_back(self):
        self.manager.current = "menu_screen"


class MyApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login_screen"))
        sm.add_widget(MenuScreen(name="menu_screen"))
        sm.add_widget(Screen1(name="screen1"))
        sm.add_widget(Screen2(name="screen2"))
        sm.add_widget(Screen3(name="screen3"))
        return sm


if __name__ == "__main__":
    MyApp().run()
