import requests

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
from googletrans import Translator

api_key = "a873d523875cab9a1f04d55526e2d604"

is_sunny = True

lat = "50.06143"
lon = "19.93658"

background_color, foreground_color, selection_color, text_field_color = "#0A0D11", "#6272A4", "#44475A", "#F8F8F2"

def update_styles_css(color1, color2, color3, color4):
    global background_color, foreground_color, selection_color, text_field_color
    background_color = color1
    foreground_color = color2
    selection_color = color3
    text_field_color = color4
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

def get_weather():
    # url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    # response = requests.get(url)
    # global is_sunny
    # if response.status_code == 200:
    #     data = response.json()
    #     message = data["weather"][0]["description"]
    #     is_sunny = "rain" in message or "cloud" in message
    #     return data
    # is_sunny = True
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

class WeatherWindow(Gtk.Window):
    main_box = Gtk.Box()

    def __init__(self):
        super().__init__(title="Prognoza Pogody")
        self.set_default_size(1280, 720)
        self.set_resizable(False)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("styles.css")

        context = Gtk.StyleContext()
        screen = Gdk.Screen.get_default()
        context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

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
        feels_like_temp_info = Gtk.Label(label=f"Odczuwalnie: {feels_like_temp}ºC\n")
        feels_like_temp_info.set_halign(Gtk.Align.START)
        weather_layout.pack_start(feels_like_temp_info, False, False, 0)

        translator = Translator()
        message = weather["weather"][0]["description"]
        translated_message = translator.translate(message, dest="pl").text.lower() if message != "N/A" else "N/A"
        message_info = Gtk.Label(label=f"Spodziewaj się: {translated_message}!\n")
        message_info.set_halign(Gtk.Align.START)
        weather_layout.pack_start(message_info, False, False, 0)

        pressure = weather["main"]["pressure"]
        pressure_info = Gtk.Label(label=f"Ciśnienie:\t{pressure} hPa\n")
        pressure_info.set_halign(Gtk.Align.START)
        weather_layout.pack_start(pressure_info, False, False, 0)

        humidity = weather["main"]["humidity"]
        humidity_info = Gtk.Label(label=f"Wilgotność:\t{humidity}%\n")
        humidity_info.set_halign(Gtk.Align.START)
        weather_layout.pack_start(humidity_info, False, False, 0)

        wind_speed = weather["wind"]["speed"]
        wind_speed_info = Gtk.Label(label=f"Prędkość:\t{wind_speed}km/h\n")
        wind_speed_info.set_halign(Gtk.Align.START)
        weather_layout.pack_start(wind_speed_info, False, False, 0)

        self.coordinates_info = Gtk.Label(label=f"Obecne współrzędne geograficzne:\nDługość ({lon}), Szerokość ({lat})")
        self.coordinates_info.set_halign(Gtk.Align.START)
        weather_layout.pack_start(self.coordinates_info, False, False, 0)

    def build_menu_bar(self):
        menu_bar = Gtk.MenuBar()
        menu_bar.set_name("menu-bar")

        localisation_menu = Gtk.Menu()
        localisation = Gtk.MenuItem(label="Lokalizacja")
        localisation.set_submenu(localisation_menu)

        change_coordinates = Gtk.MenuItem(label="Zmień Współrzędne")
        change_coordinates.connect("activate", self.on_change_coordinates_clicked)
        change_coordinates.set_name("menu-item")
        localisation_menu.append(change_coordinates)

        menu_bar.append(localisation)

        settings_menu = Gtk.Menu()
        settings = Gtk.MenuItem(label="Ustawienia")
        settings.set_submenu(settings_menu)

        change_theme = Gtk.MenuItem(label="Zmień Motyw")
        change_theme.connect("activate", self.on_change_theme_clicked)
        change_theme.set_name("menu-item")
        settings_menu.append(change_theme)

        menu_bar.append(settings)

        about_program = Gtk.MenuItem(label="O Programie")
        about_program.connect("activate", self.on_about_program_clicked)

        menu_bar.append(about_program)

        refresh = Gtk.MenuItem(label="Odśwież")
        refresh.connect("activate", self.on_refresh_clicked)

        menu_bar.append(refresh)

        self.main_box.pack_start(menu_bar, False, False, 0)

    def on_change_coordinates_clicked(self, _):
        pass

    def on_change_theme_clicked(self, _):
        pass

    def on_about_program_clicked(self, _):
        pass

    def on_refresh_clicked(self, _):
        pass

    def on_quit_activate(self, _):
        Gtk.main_quit()
    
if __name__ == "__main__":
    update_styles_css("0A0D11", "6272A4", "44475A", "F8F8F2")
    win = WeatherWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
