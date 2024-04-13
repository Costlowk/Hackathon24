from PyQt6 import QtCore, QtGui, QtWidgets
import requests
import json

class Ui_GetWeather(object):
    def setupUi(self, GetWeather):
        GetWeather.setObjectName("GetWeather")
        GetWeather.resize(400, 200)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=GetWeather)
        self.buttonBox.setGeometry(QtCore.QRect(30, 150, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.accepted.connect(self.get_weather)
        self.buttonBox.rejected.connect(GetWeather.reject)
        self.label = QtWidgets.QLabel(parent=GetWeather)
        self.label.setGeometry(QtCore.QRect(10, 10, 41, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setScaledContents(False)
        self.label.setObjectName("label")
        self.label.setText("City:")
        self.lineEdit = QtWidgets.QLineEdit(parent=GetWeather)
        self.lineEdit.setGeometry(QtCore.QRect(60, 10, 311, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(parent=GetWeather)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 41, 20))
        self.label_2.setFont(font)
        self.label_2.setScaledContents(False)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("State:")
        self.comboBox = QtWidgets.QComboBox(parent=GetWeather)
        self.comboBox.setGeometry(QtCore.QRect(60, 40, 311, 22))
        self.comboBox.setObjectName("comboBox")
        states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL",
                  "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT",
                  "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI",
                  "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
        self.comboBox.addItems(states)
        self.textEdit = QtWidgets.QTextEdit(parent=GetWeather)
        self.textEdit.setGeometry(QtCore.QRect(10, 70, 381, 71))
        self.textEdit.setObjectName("textEdit")
    
    def get_weather(self):
        city = self.lineEdit.text()
        state = self.comboBox.currentText()
        location = f"{city}, {state}"

        # Get coordinates from U.S. Census Bureau's Geocoding Services API
        formattedadds = f"city={city}&state={state}"
        url = f"https://geocoding.geo.census.gov/geocoder/locations/address?street=100+Main+St&{formattedadds}&benchmark=2020&format=json"
        geoinfo = requests.get(url)
        data = geoinfo.json()
        if data['result']['addressMatches']:
            coordinates = data['result']['addressMatches'][0]['coordinates']
            lat = coordinates['y']
            lon = coordinates['x']

            # Get weather data from weather.gov API
            weather_data = self.get_weather_data(lat, lon)
            if weather_data:
                self.textEdit.setText(weather_data)
            else:
                self.textEdit.setText("Could not get weather data.")
        else:
            self.textEdit.setText("Could not get geolocation data.")

    def get_weather_data(self, lat, lon):
        weather_s = f"https://api.weather.gov/points/{lat},{lon}"
        response = requests.get(weather_s)
        js = json.loads(response.text)
        forecast_URL = js['properties']['forecast']
        final_response = requests.get(forecast_URL)
        js = json.loads(final_response.text)
        return js['properties']['periods'][0]['detailedForecast']

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    GetWeather = QtWidgets.QDialog()
    ui = Ui_GetWeather()
    ui.setupUi(GetWeather)
    GetWeather.show()
    sys.exit(app.exec())
