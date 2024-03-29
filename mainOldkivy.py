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
        self.toolbar = MDToolbar(
            title="Screen 2",
            pos_hint={"top": 1},
        )
        self.toolbar.left_action_items = [["arrow-left", lambda x: self.go_back()]]
        self.add_widget(self.toolbar)

    def go_back(self):
        self.manager.current = "menu_screen"


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
