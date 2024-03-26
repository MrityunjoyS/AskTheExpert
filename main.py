from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivymd.uix.screen import MDScreen
from kivy.uix.recycleview import RecycleView
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText

class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "login"

        # Create a layout for the screen
        layout = BoxLayout(orientation="vertical")

        # Add some padding to the layout
        layout.padding = [10, 10, 10, 10]

        # Create a label for the screen
        label = Label(text="Login", font_size=24, halign="center")

        # Create a text input for the username
        self.username_input = TextInput(hint_text="Username")

        # Create a text input for the password
        self.password_input = TextInput(hint_text="Password", password=True)

        # Create a button for the login
        login_button = Button(text="Login")
        login_button.on_press = self.login

        # Create a button for the sign up
        signup_button = Button(text="Sign Up")
        # signup_button.on_press = self.sign_up

        # Add the widgets to the layout
        layout.add_widget(label)
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(login_button)
        layout.add_widget(signup_button)

        # Set the layout as the content of the screen
        self.add_widget(layout)

    def login(self):
        # Get the username and password from the user
        username = self.username_input.text
        password = self.password_input.text

        # Check if the username and password are correct
        if username == "admin" and password == "admin":
            # Login successful
            self.manager.current = "home"
        else:
            # Login failed
            self.show_snackbar("Login failed")

class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "home"

        # Set screen background to white
        self.bg_color = [1, 1, 1, 1]

        # Create a vertical BoxLayout for the buttons
        button_layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        button_layout.bind(minimum_height=button_layout.setter('height'))

        # Create three rectangular buttons with rounded edges and add them to the layout
        button1 = MDButton(
            MDButtonText(text="Find your Expert"),
            size_hint_y=100,
            height="180dp",
            pos_hint={"center_x": 0.5, "center_y": 0.1},
            line_color=(0.529, 0.808, 0.922, 1),  # Sky blue border color
            md_bg_color=(1, 1, 1, 1),  # White button fill color
            on_release=self.callback
            
        )
        button2 = MDButton(
            MDButtonText(text="Are you an Expert?"),
            size_hint_y=None,
            height="180dp",
            pos_hint={"center_x": 0.5, "center_y": 0.2},
            line_color=(0.529, 0.808, 0.922, 1),  # Sky blue border color
            md_bg_color=(1, 1, 1, 1),  # White button fill color
            on_release=self.callback
        )
        button3 = MDButton(
            MDButtonText(text="You Appointments"),
            size_hint_y=None,
            height="180dp",
            pos_hint={"center_x": 0.5, "center_y": 0.3},
            line_color=(0.529, 0.808, 0.922, 1),  # Sky blue border color
            md_bg_color=(1, 1, 1, 1),  # White button fill color
            on_release=self.callback
        )
        
        button_layout.add_widget(button1)
        button_layout.add_widget(button2)
        button_layout.add_widget(button3)

        # Add the button layout to the screen
        self.add_widget(button_layout)

    def callback(self, instance):
        self.manager.current = "Screen1"
        # print("Button '" + instance.text + "' clicked!")

class Screen1(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Screen1"
        label = MDLabel(text="This is the second screen", halign="center")

        # Create a back button
        back_button = MDButton(
            MDButtonText(text="Back"),
            pos_hint={"center_x": 0.5, "center_y": 0.9},
            on_release=self.back_button_callback
        )

        # Add the back button to the screen
        self.add_widget(label)
        self.add_widget(back_button)

    def back_button_callback(self, instance):
        # Switch back to the home screen
        self.manager.current = "home"


class MyApp(MDApp):
    def build(self):
        # Create a screen manager
        screen_manager = ScreenManager()

        # Add the login screen and the home screen to the screen manager
        screen_manager.add_widget(LoginScreen())
        screen_manager.add_widget(HomeScreen())
        screen_manager.add_widget(Screen1())

        # Set the login screen as the initial screen
        screen_manager.current = "login"

        return screen_manager

if __name__ == "__main__":
    MyApp().run()
