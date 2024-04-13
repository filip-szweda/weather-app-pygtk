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
    background-color: {foreground_color}; 
    color: #FFFFFF;
    font-size: 24px;           
}}

#menu-item {{
    background-color: {text_field_color};
    color: #000000;
}}

#main-box {{
    background-color: {background_color};
    color: #FFFFFF;
    font-size: 24px;
}}

#inner-box {{
    background-color: {selection_color};
    color: #FFFFFF;
    font-size: 24px;
}}

#about-program {{
    background-color: {selection_color};
    color: #FFFFFF;
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

        self.css_provider = Gtk.CssProvider()
        self.css_provider.load_from_path("styles.css")

        self.context = Gtk.StyleContext()
        self.screen = Gdk.Screen.get_default()
        self.context.add_provider_for_screen(self.screen, self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

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
        self.temp_info = Gtk.Label(label=f"{temp}ºC")
        self.temp_info.set_name("temperature")
        self.temp_info.set_halign(Gtk.Align.START)
        weather_layout.pack_start(self.temp_info, False, False, 0)

        feels_like_temp = weather["main"]["feels_like"]
        self.feels_like_temp_info = Gtk.Label(label=f"Odczuwalnie: {feels_like_temp}ºC\n")
        self.feels_like_temp_info.set_halign(Gtk.Align.START)
        weather_layout.pack_start(self.feels_like_temp_info, False, False, 0)

        translator = Translator()
        message = weather["weather"][0]["description"]
        translated_message = translator.translate(message, dest="pl").text.lower() if message != "N/A" else "N/A"
        self.message_info = Gtk.Label(label=f"Spodziewaj się: {translated_message}!\n")
        self.message_info.set_halign(Gtk.Align.START)
        weather_layout.pack_start(self.message_info, False, False, 0)

        pressure = weather["main"]["pressure"]
        self.pressure_info = Gtk.Label(label=f"Ciśnienie:\t{pressure} hPa\n")
        self.pressure_info.set_halign(Gtk.Align.START)
        weather_layout.pack_start(self.pressure_info, False, False, 0)

        humidity = weather["main"]["humidity"]
        self.humidity_info = Gtk.Label(label=f"Wilgotność:\t{humidity}%\n")
        self.humidity_info.set_halign(Gtk.Align.START)
        weather_layout.pack_start(self.humidity_info, False, False, 0)

        wind_speed = weather["wind"]["speed"]
        self.wind_speed_info = Gtk.Label(label=f"Prędkość:\t{wind_speed}km/h\n")
        self.wind_speed_info.set_halign(Gtk.Align.START)
        weather_layout.pack_start(self.wind_speed_info, False, False, 0)

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

    def update_weather_in_ui(self, weather):
        temp = weather["main"]["temp"]
        self.temp_info.set_text(f"{temp}ºC")

        feels_like_temp = weather["main"]["feels_like"]
        self.feels_like_temp_info.set_text(f"Odczuwalnie: {feels_like_temp}ºC\n")

        translator = Translator()
        message = weather["weather"][0]["description"]
        translated_message = translator.translate(message, dest="pl").text.lower() if message != "N/A" else "N/A"
        self.message_info.set_text(f"Spodziewaj się: {translated_message}!\n")

        pressure = weather["main"]["pressure"]
        self.pressure_info.set_text(f"Ciśnienie:\t{pressure} hPa\n")

        humidity = weather["main"]["humidity"]
        self.humidity_info.set_text(f"Wilgotność:\t{humidity}%\n")

        wind_speed = weather["wind"]["speed"]
        self.wind_speed_info.set_text(f"Prędkość:\t{wind_speed}km/h\n")

    def update_coordinates_in_ui(self):
        self.coordinates_info.set_text(f"Obecne współrzędne geograficzne:\nDługość ({lon}), Szerokość ({lat})")

    def update_theme_in_ui(self):
        self.css_provider.load_from_path("styles.css")
        self.context.add_provider_for_screen(self.screen, self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def on_change_coordinates_clicked(self, _):
        CoordinatesDialog(self).run()

    def on_change_theme_clicked(self, _):
        ThemeDialog(self).run()

    def on_about_program_clicked(self, _):
        AboutDialog(self).run()

    def on_refresh_clicked(self, _):
        weather = get_weather()
        self.update_weather_in_ui(weather)

    def on_quit_activate(self, _):
        Gtk.main_quit()

class CoordinatesDialog(Gtk.Dialog):
    def __init__(self, parent):
        self.parent = parent

        Gtk.Dialog.__init__(self, "Zmień Współrzędne", parent)
        self.set_default_size(910, 355)
        self.set_name("inner-box")

        box = self.get_content_area()
        box.set_spacing(10)
        box.set_margin_top(10)
        box.set_margin_bottom(10)
        box.set_margin_start(10)
        box.set_margin_end(10)

        longitude_label = Gtk.Label(label="Podaj długość geograficzną w formacie zmiennoprzecinkowym:")
        box.add(longitude_label)

        self.longitude_entry = Gtk.Entry()
        self.longitude_entry.set_placeholder_text("<długość geograficzna>")
        box.add(self.longitude_entry)

        latitude_label = Gtk.Label(label="Podaj szerokość geograficzną w formacie zmiennoprzecinkowym:")
        box.add(latitude_label)

        self.latitude_entry = Gtk.Entry()
        self.latitude_entry.set_placeholder_text("<szerokość geograficzna>")
        box.add(self.latitude_entry)

        save_button = Gtk.Button(label="Zatwierdź")
        save_button.connect("clicked", self.save_coordinates)
        box.add(save_button)

        self.show_all()

    def validate_coordinates(self, lon, lat):
        lon_valid = False
        lat_valid = False
        try:
            lon_float = float(lon)
            lon_valid = True
        except ValueError:
            pass
        try:
            lat_float = float(lat)
            lat_valid = True
        except ValueError:
            pass
        return lon_valid and lat_valid

    def save_coordinates(self, widget):
        tmp_lon = self.longitude_entry.get_text()
        tmp_lat = self.latitude_entry.get_text()
        if self.validate_coordinates(tmp_lon, tmp_lat):
            global lon, lat
            lon = tmp_lon
            lat = tmp_lat
            self.parent.update_coordinates_in_ui()
            self.parent.on_refresh_clicked(None)
            self.destroy()
        else:
            ErrorDialog(self).run()

        
class ErrorDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Błąd", parent, 0)
        self.set_default_size(610, 100)
        self.set_name("inner-box")
        self.set_modal(True)

        box = self.get_content_area()
        box.set_spacing(6)
        box.set_border_width(10)

        error_label = Gtk.Label(label="Niepoprawne współrzędne geograficzne!")
        error_label.set_halign(Gtk.Align.CENTER)
        box.add(error_label)

        self.show_all()

class AboutDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "O Programie", parent, 0)
        self.set_default_size(910, 355)
        self.set_name("about-program")

        box = self.get_content_area()

        label = Gtk.Label()
        label.set_text("Aplikacja prognozy pogody pozwala na natychmiastowe uzyskanie aktualnych informacji o: temperaturze wraz z wartością odzuwalną, podsumowaniu pogody, ciśnieniu, wilgotności i prędkości wiatru. Wyświetlana jest ikona przedstawiająca obecną sytuację pogodową. Działanie programu wymaga ustawienia lokalizacji według miasta lub współrzędnych geograficznych.")
        label.set_justify(Gtk.Justification.FILL)
        label.set_line_wrap(True)
        box.pack_start(label, True, True, 0)

        self.show_all()

class ThemeDialog(Gtk.Dialog):
    def __init__(self, parent):
        self.parent = parent

        Gtk.Dialog.__init__(self, "Zmień Motyw", parent, 0)
        self.set_default_size(910, 355)

        self.set_name("inner-box")

        box = self.get_content_area()

        dracula_theme_button = Gtk.Button(label="Motyw Dracula (Domyślny)")
        dracula_theme_button.connect("clicked", self.on_theme_button_clicked, "Dracula")
        dracula_theme_button.set_margin_top(30)
        box.add(dracula_theme_button)

        oxocarbon_theme_button = Gtk.Button(label="Motyw Seoul256")
        oxocarbon_theme_button.connect("clicked", self.on_theme_button_clicked, "Seoul256")
        oxocarbon_theme_button.set_margin_top(30)
        box.add(oxocarbon_theme_button)

        seoul256_theme_button = Gtk.Button(label="Motyw Gotham")
        seoul256_theme_button.connect("clicked", self.on_theme_button_clicked, "Gotham")
        seoul256_theme_button.set_margin_top(30)
        box.add(seoul256_theme_button)

        dogrun_theme_button = Gtk.Button(label="Motyw Nord")
        dogrun_theme_button.connect("clicked", self.on_theme_button_clicked, "Nord")
        dogrun_theme_button.set_margin_top(30)
        box.add(dogrun_theme_button)

        self.show_all()

    def on_theme_button_clicked(self, widget, theme):
        global background_color, foreground_color, selection_color, text_field_color
        if theme == "Dracula":
            background_color, foreground_color, selection_color, text_field_color = "#0A0D11", "#6272A4", "#44475A", "#F8F8F2"
        elif theme == "Seoul256":
            background_color, foreground_color, selection_color, text_field_color = "#4B4B4B", "#9A7372", "#565656", "#DFDEBD"
        elif theme == "Gotham":
            background_color, foreground_color, selection_color, text_field_color = "#091F2E", "#599CAB", "#2AA889", "#99D1CE"
        elif theme == "Nord":
            background_color, foreground_color, selection_color, text_field_color = "#81A1C1", "#D8DEE9", "#3C4455", "#434C5E"
        update_styles_css(background_color, foreground_color, selection_color, text_field_color)
        self.parent.update_theme_in_ui()
        self.destroy()
    
if __name__ == "__main__":
    update_styles_css("#0A0D11", "#6272A4", "#44475A", "#F8F8F2")
    win = WeatherWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
