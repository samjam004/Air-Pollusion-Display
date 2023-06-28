import tkinter as tk
import customtkinter
import requests

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class App():    
    
    cities = []

    def __init__(self):
        #Initializes CTk class and root window (root)
        self.root = customtkinter.CTk()
        self.root.title("AQI Display")
        self.root.geometry("1366x768")

        #Quick Display Creation
        self.sml_display_frm = customtkinter.CTkFrame(self.root, corner_radius = 0)

        self.sml_display_lbl = customtkinter.CTkLabel(self.root,
                                                      text = "Air Pollusion Display",
                                                      font=(customtkinter.CTkFont(size=20, weight="bold")))

        #Search Entry Creation
        self.search_btn = customtkinter.CTkButton(self.root, text="Search", font = ("Arial", 20),
                                                  command = self.addCity)
        self.search_entry = customtkinter.CTkEntry(self.root, 
                                                   placeholder_text="Enter A City, ex. New York, NY(optional), USA")


        #Big Display Creation
        self.big_display_frm = customtkinter.CTkFrame(self.root, corner_radius = 0)

        #Grid definition 
        self.root.rowconfigure((0,1,2,3,4), weight = 1)        
        #self.root.rowconfigure((0,4), weight = 1) 
        self.root.columnconfigure((0,1,3), weight = 1)
        self.root.columnconfigure((2), weight = 4)

        #Grid placement
        self.sml_display_frm.grid(row = 0, column = 0, rowspan = 5, columnspan = 2, sticky = "nsew")        
        self.sml_display_lbl.grid(row = 0, columnspan = 2, sticky = "n", pady = (20,20))

        self.big_display_frm.grid(row = 1, rowspan = 3, column = 2, columnspan = 2, sticky = "nsew",
                                  padx = 30)

        self.search_entry.grid(row = 4, column = 2,columnspan = 1, padx = 10, pady = 10, sticky = "sew")
        self.search_btn.grid(row = 4, column = 3, padx = 10, pady = 10, sticky = "sew")
        
        #Sets enter key to addcity function
        self.search_entry.bind("<Return>", self.addCity)
        
        #Preloads Hong Kong so screen isn't blank
        self.addCity("Hong Kong, CN")

        self.root.mainloop()
    
    #Determines if the new city is eligable to added to the small display, and adds it
    #@params preload adds an initial city, set to Hong Kong 
    def addCity(self, preload = None):

        newCity = self.search_entry.get()
        self.search_entry.delete(0, tk.END)

        #if there are no cities it will add Hong Kong so the screen isn't blank
        if len(self.cities) == 0:
            newCity = preload

        #Attempts to ensure that the wiedget space can handle the new city and that there are no repeats 
        #or non-cities
        if newCity not in self.cities and len(self.cities) < 6 and newCity != "":
            new_city_dict = {newCity: {}}
            self.cities.append(new_city_dict)

            #After the new city is added, attempts getAQI function, if it returns none then it removes
            #new city
            newCityAQI = self.getAQI(newCity)
            if newCityAQI is not None:
                self.updateGUI(newCityAQI, newCity)
            else:
                self.cities.remove(new_city_dict)
            #Testing - alerts an update happened with new city
            #print("Updated" + "New City: " + newCity)

        #Testing - Prints list of cities
        #print(self.cities) 

    def updateGUI(self, AQI, city):    
        #New city creation and placement algorithm
        if AQI == 1:
            bgColor = "green"
        if AQI == 2:
            bgColor = "yellow"
        if AQI == 3:
            bgColor = "orange"
        if AQI == 4:
            bgColor = "red"
        if AQI == 5:
            bgColor = "purple"

        newCityLabel = customtkinter.CTkButton(self.root, text = city)

        colset = 0
        if len(self.cities) % 2 == 0:
            colset = 1
        if len(self.cities) % 2 != 0:
            colset = 0

        row = ((len(self.cities) + 1) // 2)

        newCityButton = customtkinter.CTkLabel(self.root, text = "                   " + (str)(AQI) + "                   ",
                                                bg_color = bgColor, font = ('None', 20))
        newCityButton.grid(row = row, column = colset , sticky = "s", pady = (0, 10))

        newCityLabel.grid(row = row, column = colset, sticky = "nsew",
                          padx = 10, pady = 10)

        self.addToBigDisplay(city)
        #Testing Algorithm
        #print((str)((len(self.cities) + 1) // 2) + " " + (str)(colset))
        
    def addToBigDisplay(self, city):
        pass
            
    def getAQI(self, city):
        api_working = True
        API_KEY = "55aacb9295ecb0dcfabd6c36a7a25bd0" 

        city.replace(" ","")
        try:
            BASE_GEO_URL = "http://api.openweathermap.org/geo/1.0/direct?q="
            geo_url = BASE_GEO_URL + city + "&limit=1&appid=" + API_KEY
            geo_response = requests.get(geo_url) 
            #status = geo_response.status_code
            #print(geo_response.json())

            lat = geo_response.json()[0]['lat']
            lon = geo_response.json()[0]['lon']
            #print((str)(lat) + " " + (str)(lon))

            BASE_AQI_URL = "http://api.openweathermap.org/data/2.5/air_pollution/history?lat="
            aqi_url = BASE_AQI_URL + (str)(lat) + "&lon=" + (str)(lon) + "&start=1606223802&end=1606482999&appid=" + API_KEY
            aqi_response = requests.get(aqi_url)
            #print(aqi_response.json())
            aqi = aqi_response.json()['list'][0]['main']['aqi']
            
            contaminants_dict = {
                'aqi':aqi,
                'co':aqi_response.json()['list'][0]['components']['co'],
                'no':aqi_response.json()['list'][0]['components']['no'],
                'o3':aqi_response.json()['list'][0]['components']['o3'],
                'so2':aqi_response.json()['list'][0]['components']['so2'],
                'pm2_5':aqi_response.json()['list'][0]['components']['pm2_5'],
                'pm10':aqi_response.json()['list'][0]['components']['pm10'],
                'nh3':aqi_response.json()['list'][0]['components']['nh3']
            }
            self.cities[len(self.cities) - 1][city].update(contaminants_dict)
            print(self.cities)
        except IndexError:
            aqi = None



        return aqi

if __name__ == "__main__":
    root = App()
    root.mainloop()