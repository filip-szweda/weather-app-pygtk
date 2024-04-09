import requests
import re

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
from googletrans import Translator

api_key = "a873d523875cab9a1f04d55526e2d604"

is_sunny = True

lat = "50.06143"
lon = "19.93658"

background_color, foreground_color, selection_color, text_field_color = "#282A36", "#6272A4", "#44475A", "#F8F8F2"

def is_hex_color(s):
    hex_color_regex = r'(?:[0-9a-fA-F]{3}){1,2}$'
    if(bool(re.search(hex_color_regex, s))):
        print("Color is correct")
    return bool(re.search(hex_color_regex, s))


def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)
    global is_sunny
    if response.status_code == 200:
        data = response.json()
        message = data["weather"][0]["description"]
        is_sunny = "rain" in message or "cloud" in message
        return data
    is_sunny = True
    return {
        "weather": [
            {
                "description": "N/A"
            }
        ],
        "main": {
            "temp": "N/A",
            "feels_like": "N/A",
            "pressure": "N/A",
            "humidity": "N/A"
        },
        "wind": {
            "speed": "N/A"
        }
    }

def change_city(city):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    global lat, lon
    if response.status_code == 200 and data:
        lat = data[0]["lat"]
        lon = data[0]["lon"]
    else:
        lat = None
        lon = None

class BaseWindow(Gtk.Window):
    main_box = Gtk.Box()

    def __init__(self):
        super().__init__(title="Weather App")
        self.set_default_size(1280, 720)
        self.set_resizable(False)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("styles.css")

        context = Gtk.StyleContext()
        screen = Gdk.Screen.get_default()
        context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def build_menu_bar(self):
        menu_bar = Gtk.MenuBar()
        menu_bar.set_name("menu-bar")

        logo = Gtk.MenuItem(label="Prognoza Pogody")
        logo.connect("activate", self.on_weather_clicked)
        menu_bar.append(logo)

        localisation_menu = Gtk.Menu()
        localisation = Gtk.MenuItem(label="Lokalizacja")
        localisation.set_submenu(localisation_menu)

        change_coordinates_menu = Gtk.Menu()
        change_coordinates = Gtk.MenuItem(label="Zmień Koordynaty")
        change_coordinates.set_submenu(change_coordinates_menu)
        change_coordinates.set_name("menu-item")
        localisation_menu.append(change_coordinates)

        longitude = Gtk.MenuItem(label="Długość Geo.")
        longitude.connect("activate", self.on_longitude_clicked)
        longitude.set_name("menu-item")
        change_coordinates_menu.append(longitude)

        latitude = Gtk.MenuItem(label="Szerokość Geo.")
        latitude.connect("activate", self.on_latitude_clicked)
        latitude.set_name("menu-item")
        change_coordinates_menu.append(latitude)

        change_city = Gtk.MenuItem(label="Zmień Miasto")
        change_city.connect("activate", self.on_change_city_clicked)
        change_city.set_name("menu-item")
        localisation_menu.append(change_city)

        menu_bar.append(localisation)

        settings_menu = Gtk.Menu()
        settings = Gtk.MenuItem(label="Ustawienia")
        settings.set_submenu(settings_menu)

        theme = Gtk.MenuItem(label="Motyw")
        theme.connect("activate", self.on_theme_clicked)
        theme.set_name("menu-item")
        settings_menu.append(theme)

        menu_bar.append(settings)

        about_program = Gtk.MenuItem(label="O Programie")
        about_program.connect("activate", self.on_about_program_clicked)

        menu_bar.append(about_program)

        self.main_box.pack_start(menu_bar, False, False, 0)

    def on_weather_clicked(self, _):
        weather_window = WeatherWindow()
        weather_window.show_all()
    
    def on_longitude_clicked(self, _):
        longitude_window = LongitudeWindow()
        longitude_window.show_all()
        
    def on_latitude_clicked(self, _):
        latitude_window = LatitudeWindow()
        latitude_window.show_all()

    def on_change_city_clicked(self, _):
        change_city_window = ChangeCityWindow()
        change_city_window.show_all()

    def on_theme_clicked(self, _):
        theme_window = ThemeWindow()
        theme_window.show_all()

    def on_about_program_clicked(self, _):
        about_program_window = AboutProgramWindow()
        about_program_window.show_all()

    def on_quit_activate(self, _):
        Gtk.main_quit()

class WeatherWindow(BaseWindow):
    def __init__(self):
        super().__init__()

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_name("main-box")
        self.add(self.main_box)

        self.build_menu_bar()

        layout = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.main_box.pack_start(layout, True, True, 0)

        image_layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        layout.pack_start(image_layout, True, True, 0)

        image_label = Gtk.Image()
        pixmap = GdkPixbuf.Pixbuf.new_from_file("sunny.png" if is_sunny else "cloudy.png")
        image_label.set_from_pixbuf(pixmap)
        image_layout.pack_start(image_label, False, False, 0)

        weather_layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        layout.pack_start(weather_layout, True, True, 0)

        weather = get_weather()

        temp = weather["main"]["temp"]
        temp_info = Gtk.Label(label=f"{temp}ºC")
        temp_info.set_name("temperature")
        temp_info.set_halign(Gtk.Align.START)
        weather_layout.pack_start(temp_info, False, False, 0)

        feels_like_temp = weather["main"]["feels_like"]
        feels_like_temp_info = Gtk.Label(label=f"Odczuwalnie: {feels_like_temp}ºC")
        feels_like_temp_info.set_halign(Gtk.Align.START)
        weather_layout.pack_start(feels_like_temp_info, False, False, 0)

        translator = Translator()
        message = weather["weather"][0]["description"]
        translated_message = translator.translate(message, dest="pl").text.lower() if message != "N/A" else "N/A"
        message_info = Gtk.Label(label=f"Spodziewaj się: {translated_message}!")
        message_info.set_halign(Gtk.Align.START)
        weather_layout.pack_start(message_info, False, False, 0)

        pressure = weather["main"]["pressure"]
        pressure_info = Gtk.Label(label=f"Ciśnienie:\t{pressure} hPa")
        pressure_info.set_halign(Gtk.Align.START)
        weather_layout.pack_start(pressure_info, False, False, 0)

        humidity = weather["main"]["humidity"]
        humidity_info = Gtk.Label(label=f"Wilgotność:\t{humidity}%")
        humidity_info.set_halign(Gtk.Align.START)
        weather_layout.pack_start(humidity_info, False, False, 0)

        wind_speed = weather["wind"]["speed"]
        wind_speed_info = Gtk.Label(label=f"Prędkość:\t{wind_speed}km/h")
        wind_speed_info.set_halign(Gtk.Align.START)
        weather_layout.pack_start(wind_speed_info, False, False, 0)

class LongitudeWindow(BaseWindow):
    def __init__(self):
        super().__init__()

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=100)
        self.set_name("main-box")
        self.add(self.main_box)

        self.build_menu_bar()

        center_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.main_box.pack_start(center_box, True, True, 0)

        inner_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        inner_box.set_name("inner-box")
        inner_box.set_margin_start(100)
        inner_box.set_margin_end(100)
        inner_box.set_margin_top(100)
        inner_box.set_margin_bottom(100)
        inner_box.set_size_request(400, 200)
        center_box.pack_start(inner_box, True, True, 0)

        close_button = Gtk.Button(label="X")
        close_button.set_margin_start(1200)
        close_button.set_margin_top(10)
        close_button.connect("clicked", self.on_weather_clicked)
        inner_box.pack_start(close_button, False, False, 0)

        longitude_label = Gtk.Label(label="Podaj długość geograficzną:")
        inner_box.pack_start(longitude_label, False, False, 0)

        self.number_entry = Gtk.Entry()
        self.number_entry.set_placeholder_text("<długość geograficzna>")
        self.number_entry.set_margin_start(50)
        self.number_entry.set_margin_end(50)
        inner_box.pack_start(self.number_entry, False, False, 0)

        save_button = Gtk.Button(label="Zatwierdź")
        save_button.set_margin_start(550)
        save_button.set_margin_end(550)
        save_button.connect("clicked", self.save_number)
        inner_box.pack_start(save_button, False, False, 0)

    def save_number(self, button):
        global lon
        lon = self.number_entry.get_text()
        self.on_weather_clicked(button)

class LatitudeWindow(BaseWindow):
    def __init__(self):
        super().__init__()

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=100)
        self.set_name("main-box")
        self.add(self.main_box)

        self.build_menu_bar()

        center_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.main_box.pack_start(center_box, True, True, 0)

        inner_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        inner_box.set_name("inner-box")
        inner_box.set_margin_start(100)
        inner_box.set_margin_end(100)
        inner_box.set_margin_top(100)
        inner_box.set_margin_bottom(100)
        inner_box.set_size_request(400, 200)
        center_box.pack_start(inner_box, True, True, 0)

        close_button = Gtk.Button(label="X")
        close_button.set_margin_start(1200)
        close_button.set_margin_top(10)
        close_button.connect("clicked", self.on_weather_clicked)
        inner_box.pack_start(close_button, False, False, 0)

        longitude_label = Gtk.Label(label="Podaj szerokość geograficzną:")
        inner_box.pack_start(longitude_label, False, False, 0)

        self.number_entry = Gtk.Entry()
        self.number_entry.set_placeholder_text("<szerokość geograficzna>")
        self.number_entry.set_margin_start(50)
        self.number_entry.set_margin_end(50)
        inner_box.pack_start(self.number_entry, False, False, 0)

        save_button = Gtk.Button(label="Zatwierdź")
        save_button.set_margin_start(550)
        save_button.set_margin_end(550)
        save_button.connect("clicked", self.save_number)
        inner_box.pack_start(save_button, False, False, 0)

    def save_number(self, button):
        global lat
        lat = self.number_entry.get_text()
        self.on_weather_clicked(button)

class ChangeCityWindow(BaseWindow):
    def __init__(self):
        super().__init__()

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=100)
        self.set_name("main-box")
        self.add(self.main_box)

        self.build_menu_bar()

        center_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.main_box.pack_start(center_box, True, True, 0)

        inner_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        inner_box.set_name("inner-box")
        inner_box.set_margin_start(100)
        inner_box.set_margin_end(100)
        inner_box.set_margin_top(100)
        inner_box.set_margin_bottom(100)
        inner_box.set_size_request(400, 200)
        center_box.pack_start(inner_box, True, True, 0)

        close_button = Gtk.Button(label="X")
        close_button.set_margin_start(1200)
        close_button.set_margin_top(10)
        close_button.connect("clicked", self.on_weather_clicked)
        inner_box.pack_start(close_button, False, False, 0)

        longitude_label = Gtk.Label(label="Podaj miasto:")
        inner_box.pack_start(longitude_label, False, False, 0)

        self.city_entry = Gtk.Entry()
        self.city_entry.set_placeholder_text("<miasto>")
        self.city_entry.set_margin_start(50)
        self.city_entry.set_margin_end(50)
        inner_box.pack_start(self.city_entry, False, False, 0)

        save_button = Gtk.Button(label="Zatwierdź")
        save_button.set_margin_start(550)
        save_button.set_margin_end(550)
        save_button.connect("clicked", self.save_city)
        inner_box.pack_start(save_button, False, False, 0)

    def save_city(self, button):
        city = self.city_entry.get_text()
        change_city(city)
        self.on_weather_clicked(button)

class AboutProgramWindow(BaseWindow):
    def __init__(self):
        super().__init__()

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=100)
        self.set_name("main-box")
        self.add(self.main_box)

        self.build_menu_bar()

        center_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.main_box.pack_start(center_box, True, True, 0)

        inner_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        inner_box.set_name("inner-box")
        inner_box.set_margin_start(100)
        inner_box.set_margin_end(100)
        inner_box.set_margin_top(100)
        inner_box.set_margin_bottom(100)
        inner_box.set_size_request(400, 200)
        center_box.pack_start(inner_box, True, True, 0)

        info_label = Gtk.Label(label="Aplikacja prognozy pogody pozwala na natychmiastowe uzyskanie aktualnych informacji o: temperaturze wraz z\n\nwartością odczuwalną, podsumowaniu pogody, ciśnieniu, wilgotności i prędkości wiatru. Wyświetlana jest ikona\n\nprzedstawiająca obecną sytuację pogodową. Działanie programu wymaga ustawienia lokalizacji według miasta\n\nlub współrzędnych geograficznych.")
        info_label.set_name("about-program")
        info_label.set_margin_top(100)
        inner_box.pack_start(info_label, False, False, 0)

class ThemeWindow(BaseWindow):
    def __init__(self):
        super().__init__()

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=100)
        self.set_name("main-box")
        self.add(self.main_box)

        self.build_menu_bar()

        center_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.main_box.pack_start(center_box, True, True, 0)

        inner_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        inner_box.set_name("inner-box")
        inner_box.set_margin_start(100)
        inner_box.set_margin_end(100)
        inner_box.set_margin_top(100)
        inner_box.set_margin_bottom(100)
        inner_box.set_size_request(400, 200)
        center_box.pack_start(inner_box, True, True, 0)

        close_button = Gtk.Button(label="X")
        close_button.set_margin_start(1200)
        close_button.set_margin_top(10)
        close_button.connect("clicked", self.on_weather_clicked)
        inner_box.pack_start(close_button, False, False, 0)

        longitude_label = Gtk.Label(label="Podaj kolor tła w kodzie hex (bez #):")
        inner_box.pack_start(longitude_label, False, False, 0)

        self.background_color_entry = Gtk.Entry()
        self.background_color_entry.set_placeholder_text("<kolor tła w kodzie hex (bez #)>")
        self.background_color_entry.set_margin_start(50)
        self.background_color_entry.set_margin_end(50)
        inner_box.pack_start(self.background_color_entry, False, False, 0)

        longitude_label = Gtk.Label(label="Podaj kolor pierwszoplanowy w kodzie hex (bez #):")
        inner_box.pack_start(longitude_label, False, False, 0)

        self.foreground_entry = Gtk.Entry()
        self.foreground_entry.set_placeholder_text("<kolor pierwszoplanowy w kodzie hex (bez #)>")
        self.foreground_entry.set_margin_start(50)
        self.foreground_entry.set_margin_end(50)
        inner_box.pack_start(self.foreground_entry, False, False, 0)

        longitude_label = Gtk.Label(label="Podaj kolor zaznaczenia w kodzie hex (bez #):")
        inner_box.pack_start(longitude_label, False, False, 0)

        self.selection_entry = Gtk.Entry()
        self.selection_entry.set_placeholder_text("<kolor zaznaczenia w kodzie hex (bez #)>")
        self.selection_entry.set_margin_start(50)
        self.selection_entry.set_margin_end(50)
        inner_box.pack_start(self.selection_entry, False, False, 0)

        longitude_label = Gtk.Label(label="Podaj kolor pola tekstowego w kodzie hex (bez #):")
        inner_box.pack_start(longitude_label, False, False, 0)

        self.text_field_entry = Gtk.Entry()
        self.text_field_entry.set_placeholder_text("<kolor pola tekstowego w kodzie hex (bez #)>")
        self.text_field_entry.set_margin_start(50)
        self.text_field_entry.set_margin_end(50)
        inner_box.pack_start(self.text_field_entry, False, False, 0)

        save_button = Gtk.Button(label="Zatwierdź")
        save_button.set_margin_start(550)
        save_button.set_margin_end(550)
        save_button.connect("clicked", self.update_styles_css)
        inner_box.pack_start(save_button, False, False, 0)

    def update_styles_css(self, button):
        global background_color, foreground_color, selection_color, text_field_color
        background_color = self.background_color_entry.get_text() if is_hex_color(self.background_color_entry.get_text()) else "0A0D11"
        foreground_color = self.foreground_entry.get_text() if is_hex_color(self.foreground_entry.get_text()) else "6272A4"
        selection_color = self.selection_entry.get_text() if is_hex_color(self.selection_entry.get_text()) else "44475A"
        text_field_color = self.text_field_entry.get_text() if is_hex_color(self.text_field_entry.get_text()) else "F8F8F2"
        styles_css = f"""
#menu-bar {{
    background-color: #{foreground_color}; 
    color: #FFFFFF;
    font-size: 24px;           
}}

#menu-item {{
    background-color: #{text_field_color};
    color: #000000;
}}

#main-box {{
    background-color: #{background_color};
    color: #FFFFFF;
    font-size: 24px;
}}

#inner-box {{
    background-color: #{selection_color};
    font-size: 24px;
}}

#temperature {{
    font-size: 96px;
}}

#about-program {{
    font-size: 20px;
}}
"""
        with open("styles.css", "w") as file:
            file.write(styles_css)
        self.on_weather_clicked(button)

    
if __name__ == "__main__":
    win = WeatherWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
