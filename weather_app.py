import requests

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
from googletrans import Translator

api_key = "a873d523875cab9a1f04d55526e2d604"

lat = "50.06143"
lon = "19.93658"

def get_weather():
    # url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    # response = requests.get(url)
    # if response.status_code == 200:
    #     return response.json()
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
        pass

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
        pixmap = GdkPixbuf.Pixbuf.new_from_file("cloudy.png")
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
        inner_box.set_margin_top(80)
        inner_box.set_margin_bottom(100)
        inner_box.set_size_request(400, 200)
        center_box.pack_start(inner_box, True, True, 0)

        info_label = Gtk.Label(label="Aplikacja prognozy pogody pozwala na natychmiastowe uzyskanie aktualnych informacji o: temperaturze wraz z\n\nwartością odczuwalną, podsumowaniu pogody, ciśnieniu, wilgotności i prędkości wiatru. Wyświetlana jest ikona\n\nprzedstawiająca obecną sytuację pogodową. Działanie programu wymaga ustawienia lokalizacji według miasta\n\nlub współrzędnych geograficznych.")
        info_label.set_name("about-program")
        info_label.set_margin_top(100)
        inner_box.pack_start(info_label, False, False, 0)
    
if __name__ == "__main__":
    win = WeatherWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
