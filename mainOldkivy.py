from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.card import MDCard
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView, FileChooserListView
from kivymd.uix.button import MDRaisedButton
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dropdownitem import MDDropDownItem
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.menu import MDMenu
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage


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
        # else:
        #     self.password_field.text = ""  # Clear password field on incorrect login


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

        self.box_layout = MDBoxLayout(orientation="vertical")
        self.add_widget(self.box_layout)

        self.toolbar = MDToolbar(
            title="Screen 1",
            pos_hint={"top": 1},
        )
        self.toolbar.left_action_items = [["arrow-left", lambda x: self.go_back()]]
        self.toolbar.right_action_items = [["magnify", lambda x: self.open_search_bar()]]
        self.box_layout.add_widget(self.toolbar)

        self.scroll_view = ScrollView()
        self.grid_layout = MDGridLayout(cols=1, spacing=10, padding=20, size_hint_y=None)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))
        self.scroll_view.add_widget(self.grid_layout)
        self.box_layout.add_widget(self.scroll_view)

        self.open_search()

    def go_back(self):
        self.manager.current = "menu_screen"

    def open_search_bar(self):
        self.grid_layout.clear_widgets()
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
        data = self.fetch_data_from_backend()
        if query:
            filtered_data = [item for item in data if query.lower() in item["title"].lower()]
        else:
            filtered_data = data

        self.grid_layout.clear_widgets()
        for item in filtered_data:
            card = MDCard(size_hint=(1, None), height=100)
            card.add_widget(Button(text=item["title"], on_release=lambda x: self.open_detail(item["title"])))
            card.add_widget(Button(text=item["description"], on_release=lambda x: self.open_detail(item["title"])))
            self.grid_layout.add_widget(card)

    def fetch_data_from_backend(self):
        return [
            {"title": "Item 1", "description": "Description for Item 1"},
            {"title": "Item 2", "description": "Description for Item 2"},
            {"title": "Item 3", "description": "Description for Item 3"},
            {"title": "Another Item", "description": "Description for Another Item"},
        ]

class Screen2(Screen):
    MAX_CONTENTS = 5  # Maximum number of contents allowed
    MAX_TOTAL_SIZE_MB = 5  # Maximum total size allowed in MB

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.contents = []  # List to store uploaded files
        self.total_size = 0  # Total size of uploaded files

        self.popup = None
        self.selected_file_label = Label(text="No file selected")
        self.preview_layout = BoxLayout(orientation="vertical", spacing=10)

        self.box_layout = MDBoxLayout(orientation="vertical", padding=20, spacing=20)
        self.add_widget(self.box_layout)

        self.toolbar = MDToolbar(
            title="Screen 2",
            pos_hint={"top": 1},
        )
        self.toolbar.left_action_items = [["arrow-left", lambda x: self.go_back()]]
        self.box_layout.add_widget(self.toolbar)

        # Upload profile picture button
        self.upload_profile_button = MDFillRoundFlatButton(text="Upload Profile Picture")
        self.upload_profile_button.bind(on_release=self.upload_profile_pic)
        self.box_layout.add_widget(self.upload_profile_button)

        self.layout = MDGridLayout(cols=1, spacing=10, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        self.phone_field = MDTextField(hint_text="Phone Number")
        self.email_field = MDTextField(hint_text="Email")

        self.dropdown_menu = MDTextField(hint_text="Select Option", readonly=True)
        self.dropdown_menu.bind(focus=self.check_focus)

        self.description_field = MDTextField(hint_text="Description", multiline=True)
        self.keywords_field = MDTextField(hint_text="Keywords (comma separated)")
        self.rating_field = MDTextField(hint_text="Rating (out of 10)", input_filter="float")

        self.layout.add_widget(self.phone_field)
        self.layout.add_widget(self.email_field)
        self.layout.add_widget(self.dropdown_menu)
        self.layout.add_widget(self.description_field)
        self.layout.add_widget(self.keywords_field)
        self.layout.add_widget(self.rating_field)

        self.scroll_view = ScrollView()
        self.scroll_view.add_widget(self.layout)
        self.box_layout.add_widget(self.scroll_view)

        # Upload proofs button
        self.upload_proofs_button = MDFillRoundFlatButton(text="Upload Videos/Images/Documents of your skills")
        self.upload_proofs_button.bind(on_release=self.upload_proof)
        self.box_layout.add_widget(self.upload_proofs_button)

        button_layout = MDBoxLayout(orientation="horizontal", spacing=10, size_hint_y=None, height="48dp")
        self.save_button = MDFillRoundFlatButton(text="Save", on_release=self.save_data)
        self.cancel_button = MDFillRoundFlatButton(text="Cancel", on_release=self.go_back)
        button_layout.add_widget(self.save_button)
        button_layout.add_widget(self.cancel_button)
        self.box_layout.add_widget(button_layout)

    def go_back(self, *args):
        self.manager.current = "menu_screen"

    def upload_profile_pic(self, *args):
        # File chooser for photos and videos
        file_chooser = FileChooserListView()
        file_chooser.filters = ["*.jpg", "*.png", "*.jpeg"]
        file_chooser.bind(on_submit=self.handle_photo_video_selection)

        # Popup for uploading photos and videos
        popup = Popup(title="Upload Profile Pic", content=file_chooser, size_hint=(None, None), size=(600, 400))
        popup.open()

    def upload_proof(self, *args):
        # Check if the maximum number of contents has been reached
        if len(self.contents) >= self.MAX_CONTENTS:
            self.show_message("Maximum number of contents reached.")
            return

        # File chooser for photos and videos
        file_chooser = FileChooserListView()
        file_chooser.filters = ["*.jpg", "*.png", "*.jpeg", "*.mp4", "*.mov", "*.avi", "*.pdf", "*.doc", "*.docx"]
        file_chooser.bind(on_submit=self.handle_photo_video_selection)

        # Popup for uploading photos and videos
        popup = Popup(title="Upload Photo/Video", content=file_chooser, size_hint=(None, None), size=(600, 400))
        popup.open()

    def handle_photo_video_selection(self, chooser, path, filename):
        # Calculate the size of the selected file
        file_size_mb = self.get_file_size_mb(path, filename)
        
        # Check if adding the file exceeds the maximum total size
        if self.total_size + file_size_mb > self.MAX_TOTAL_SIZE_MB:
            self.show_message("Maximum total size exceeded.")
            return

        # Update the total size
        self.total_size += file_size_mb

        # Add the selected file to the contents list
        self.selected_file_info = {"type": "photo_video", "filename": filename, "path": path}

        # Show the selected file preview
        self.show_file_preview()

    def show_file_preview(self):
        # Clear existing preview widgets
        self.preview_layout.clear_widgets()

        # Show preview based on the selected file type
        if self.selected_file_info["type"] == "photo_video":
            # Display image preview
            path = self.selected_file_info["path"]
            image_preview = AsyncImage(source=str(path), size_hint=(None, None), size=(200, 200))
            self.preview_layout.add_widget(image_preview)

        # Add upload button
        upload_button = Button(text="Upload", size_hint=(None, None), size=(100, 50))
        upload_button.bind(on_release=self.upload_file)
        self.preview_layout.add_widget(upload_button)

    def upload_file(self, instance):
        # Call the backend API to upload the file
        # Pass the file information (path, filename) to the backend
        # Handle the upload response from the backend
        pass

    def get_file_size_mb(self, path, filename):
        # Logic to calculate file size in MB
        return 0  # Placeholder for actual implementation

    def check_focus(self, instance, value):
        if value:
            self.show_menu(instance)

    def show_menu(self, instance):
        menu_content = BoxLayout(orientation='vertical', spacing=10)
        for item_text in ["Item 1", "Item 2", "Item 3"]:
            item_button = Button(text=item_text)
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
        instance.text = selected_item
        instance.focus = False

    def save_data(self, *args):
        pass


class Screen22(Screen):
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

        self.layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        self.upload_photo_button = MDFillRoundFlatButton(text="Upload Photo")
        self.upload_photo_button.bind(on_release=self.upload_photo)

        self.phone_field = MDTextField(hint_text="Phone Number")
        self.email_field = MDTextField(hint_text="Email")

        self.dropdown_menu = MDTextField(hint_text="Select Option", readonly=True)
        self.dropdown_menu.bind(focus=self.check_focus)

        self.description_field = MDTextField(hint_text="Description", multiline=True)
        self.keywords_field = MDTextField(hint_text="Keywords (comma separated)")
        self.rating_field = MDTextField(hint_text="Rating (out of 10)", input_filter="float")
        self.upload_proofs_button = MDFillRoundFlatButton(text="Upload Videos/Images/Documents of your skills")
        self.upload_proofs_button.bind(on_release=self.upload_proof)

        self.save_button = MDFillRoundFlatButton(text="Save", on_release=self.save_data)
        self.cancel_button = MDFillRoundFlatButton(text="Cancel", on_release=self.go_back)

        self.layout.add_widget(self.upload_photo_button)
        self.layout.add_widget(self.phone_field)
        self.layout.add_widget(self.email_field)
        self.layout.add_widget(self.dropdown_menu)
        self.layout.add_widget(self.description_field)
        self.layout.add_widget(self.keywords_field)
        self.layout.add_widget(self.rating_field)
        self.layout.add_widget(self.upload_proofs_button)

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
        print("Selected file:", filename)
        if self.popup:
            self.popup.dismiss()
        self.selected_file_label.text = f"Selected file: {filename}"

    def save_data(self, *args):
        pass
    
    def check_focus(self, instance, value):
        if value:
            print("Call is here ----- ",flush=True)
            self.show_menu(instance)

    def show_menu(self, instance):
        menu_content = BoxLayout(orientation='vertical', spacing=10)
        for item_text in ["Item 1", "Item 2", "Item 3"]:
            print(" NOW  ====  Call is here ----- ",flush=True)
            item_button = Button(text=item_text)
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
        instance.text = selected_item
        instance.focus = False

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


