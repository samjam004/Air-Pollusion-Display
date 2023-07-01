import tkinter as tk
import customtkinter
import requests

#AQI Display App
#By Samuel Mount
#July 1, 2023

#TO DO
#Fix text shifting upon city names of varying lengths
#AQI Intensity explanation buttons and pop up windows
#Pictures and icons
#Links to powered by 
#API Status display

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class App():    

    cities = {}
    preload_bool = True
    big_aqi_text = "--"
    big_city_text = "--"
    big_coords_text = "--"
    big_temp_text = "--"
    big_hu_text = "__"
    big_ws_text = "__"
    big_station_text = "__"

    def __init__(self):
        #Initializes CTk class and root window (root)
        self.root = customtkinter.CTk()
        self.root.title("AQI Display")  
        self.root.geometry("1366x768")


        #Quick Display Creation
        self.sml_display_frm = customtkinter.CTkFrame(self.root, fg_color="black")

        self.sml_display_lbl_frm = customtkinter.CTkFrame(self.root, fg_color="black", bg_color="black")

        self.sml_display_lbl = customtkinter.CTkLabel(self.sml_display_lbl_frm,
                                                      text = "Air Quality Index Display",
                                                      font = ("San Francisco", 25, 'bold'), 
                                                      text_color="#ffffff")

        #Big Display Creation
        self.big_display_frm = customtkinter.CTkFrame(self.root, fg_color="#212124")
        self.big_display_inr_frm = customtkinter.CTkFrame(self.root, fg_color = "black")
        self.big_display_inr_frm.lift()

        #Search Entry Creation  
        self.search_btn = customtkinter.CTkButton(self.root, text="Search", font = ("San Francisco", 20),
                                                  command = self.addCity)
        self.search_btn.lift()
        self.search_entry = customtkinter.CTkEntry(self.root,
                                                   placeholder_text="Enter A City, ex. New York, NY(optional), USA (optional)")
        self.search_entry.lift()



        self.color_indicator = customtkinter.CTkButton(self.root, fg_color="green",
                                                        text = ("Good").center(30) + "\n\n0 to 50", 
                                                        text_color = "black", 
                                                        font = ("San Francisco", 15, 'bold'), 
                                                        hover_color="white", corner_radius= 0)
        self.color_indicator2 = customtkinter.CTkButton(self.root, fg_color="yellow", 
                                                        text = ("Moderate").center(30) + "\n\n51 to 100", 
                                                        text_color = "black", 
                                                        font = ("San Francisco", 15, 'bold'), 
                                                        hover_color="white", corner_radius= 0)        
        self.color_indicator3 = customtkinter.CTkButton(self.root, fg_color="orange", 
                                                        text = ("Unhealthy \nFor Sensitive Groups").center(30) + "\n101 to 150", 
                                                        text_color = "black", 
                                                        font = ("San Francisco", 15, 'bold'), 
                                                        hover_color="white", corner_radius= 0)
        self.color_indicator4 = customtkinter.CTkButton(self.root, fg_color="red", 
                                                        text = ("Unhealthy").center(30) + "\n\n151 to 200", 
                                                        text_color = "black", 
                                                        font = ("San Francisco", 15, 'bold'), 
                                                        hover_color="white", corner_radius= 0)        
        self.color_indicator5 = customtkinter.CTkButton(self.root, fg_color="purple", 
                                                        text = ("Very Unhealthy").center(30) + "\n\n201 to 300", 
                                                        text_color = "black", 
                                                        font = ("San Francisco", 15, 'bold'), 
                                                        hover_color="white", corner_radius= 0)
        self.color_indicator6 = customtkinter.CTkButton(self.root, fg_color="maroon", 
                                                        text = ("Hazardous").center(30) + "\n\n301+", 
                                                        text_color = "white", 
                                                        font = ("San Francisco", 15, 'bold'), 
                                                        hover_color="white", corner_radius= 0)

        #Big Display Widgets
        self.big_aqi = customtkinter.CTkLabel(self.big_display_inr_frm, 
                                              text = "AQI: " + self.big_aqi_text, 
                                              font = ("San Francisco", 30, 'bold'))
        self.big_city_name = customtkinter.CTkLabel(self.big_display_inr_frm, 
                                                    font = ("San Francisco", 27, 'bold'),
                                                    text_color="white",
                                                    text = self.big_city_text)
        self.big_coords = customtkinter.CTkLabel(self.big_display_inr_frm, 
                                                    font = ("San Francisco", 20),
                                                    text_color="white",
                                                    text = self.big_coords_text)  
        self.big_temp = customtkinter.CTkLabel(self.big_display_inr_frm,
                                               font = ("San Francisco", 25),
                                               text_color = "white",
                                               text = self.big_temp_text)
        self.main_cont = customtkinter.CTkLabel(self.big_display_inr_frm)
        self.big_details = customtkinter.CTkLabel(self.big_display_inr_frm)
        self.big_station = customtkinter.CTkLabel(self.big_display_inr_frm)

        self.powered_by = customtkinter.CTkLabel(self.root, font = ("San Francisco", 15, 'bold'),
                                                text = "Powered by IQAir \n and OpenWeather",
                                                text_color = "white", fg_color = "black")


        #Grid definition 
        self.root.rowconfigure((0,1,2,3,4), weight = 1)        
        self.root.columnconfigure((0,1,2,3,4,5,6,7), weight = 1)        

        #Grid placement
        self.sml_display_frm.grid(row = 0, column = 0, rowspan = 5, columnspan = 2, sticky = "nsew")        
        self.sml_display_lbl.grid(pady = (20,20), sticky = "nsew")
        self.sml_display_lbl_frm.grid(row = 0, column = 0, columnspan = 2)


        #Big Display Grid Definition and placement
        self.big_display_inr_frm.rowconfigure((0,1,2), weight = 1)
        self.big_display_inr_frm.columnconfigure((0,1,2,3,4), weight = 1)       
        self.big_aqi.grid(row = 2, column = 2)
        self.big_city_name.grid(row = 0, column = 2)
        self.big_coords.grid(row = 0, column = 2, pady = (75, 0))

        self.big_temp.grid(row = 0, column = 1, sticky = "nsew")

        
        self.big_display_frm.grid(row = 0, rowspan = 5, column = 2, columnspan = 6, sticky = "nsew")
        self.big_display_inr_frm.grid(row = 0, rowspan = 4, column = 2, columnspan = 6, 
                                      padx = 20, pady = (75, 0), sticky = "nsew")
        
        self.powered_by.grid(row = 4, column = 0, columnspan = 2, sticky = "ews", pady = (0,20))

        #AQI-Level Buttons
        self.color_indicator.grid(row = 4, column = 2, sticky = "ews", pady = (0,50))
        self.color_indicator2.grid(row = 4, column = 3, sticky = "ews", pady = (0,50))
        self.color_indicator3.grid(row = 4, column = 4, sticky = "ews", pady = (0,50))
        self.color_indicator4.grid(row = 4, column = 5, sticky = "ews", pady = (0,50))
        self.color_indicator5.grid(row = 4, column = 6, sticky = "ews", pady = (0,50))
        self.color_indicator6.grid(row = 4, column = 7, sticky = "ews", pady = (0,50))

        #Search field 
        self.search_entry.grid(row = 4, column = 2,columnspan = 5, padx = 10, pady = 10, sticky = "sew")
        self.search_btn.grid(row = 4, column = 7, padx = 10, pady = 10, sticky = "sew")
        
        
        #Sets enter key to addcity function
        self.search_entry.bind("<Return>", self.addCity)
        
        #Preloads Hong Kong so screen isn't blank
        self.addCity("San Francisco")
        self.preload_bool = True
        self.addCity("Hong Kong")
        
        self.root.mainloop()
    
    #Determines if the new city is eligable to added to the small display, and adds it
    #@params preload adds an initial city, set to Hong Kong 
    def addCity(self, preload = None):

        newCity = self.search_entry.get()
        self.search_entry.delete(0, tk.END)

        newCity = ' '.join(word.capitalize() for word in newCity.split())

        #if there are no cities it will add Hong Kong so the screen isn't blank
        if self.preload_bool is True:
            newCity = preload
            self.preload_bool = False

        #Attempts to ensure that the wiedget space can handle the new city and that there are no repeats 
        #or non-cities
        if newCity not in self.cities and len(self.cities) < 8 and newCity != "":
            new_city_data = {}
            self.cities[newCity] = new_city_data
            #After the new city is added, attempts getAQI function, if it returns none then it removes
            #new city
            newCityAQI = self.getAQI(newCity)
            if newCityAQI is not None:
                self.updateGUI(newCityAQI,newCity)
            else:
                self.cities.pop(newCity)
            #Testing - alerts an update happened with new city
            #print("Updated" + "New City: " + newCity)

        #Testing - Prints list of cities
        #print(self.cities) 

    def updateGUI(self, AQI, city):     
        #New city creation and placement algorithm

        if AQI <= 50:
            bgColor = "green"
        elif AQI <=100:
            bgColor = "yellow"
        elif AQI <= 150:
            bgColor = "orange"
        elif AQI <= 200:
            bgColor = "red"
        elif AQI <= 300:
            bgColor = "purple"
        elif AQI >=301:
            bgColor = "maroon"

        colset = 0
        if len(self.cities) % 2 == 0:
            colset = 1
        if len(self.cities) % 2 != 0:
            colset = 0

        row = ((len(self.cities) + 1) // 2)

        newCityButton = customtkinter.CTkButton(self.root, 
                                                text = city + "\n" + (str)(self.cities[city]['temp'])+ chr(176) + "F", 
                                                font=("San Francisco", 20, 'bold'),
                                                fg_color="#212124", border_width = 2,
                                                corner_radius= 8,
                                                text_color="white",
                                                command=lambda c=city: self.addToBigDisplay(c, bgColor))

        newCityButton.grid(row = row, column = colset, sticky = "nsew",
                          padx = 10, pady = 10,)
        
        newCityLabel = customtkinter.CTkLabel(self.root, text = (str)(AQI).center(20),
                                                bg_color = bgColor, font = ("San Francisco", 20, 'bold'),
                                                text_color="black")
        newCityLabel.grid(row = row, column = colset , sticky = "s", pady = (10, 0))



        self.addToBigDisplay(city, bgColor)
        #Testing Algorithm
        #print((str)((len(self.cities) + 1) // 2) + " " + (str)(colset))
        
    def addToBigDisplay(self, city, bgColor):

        self.big_aqi_text = (str)(self.cities[city]['aqi'])
        self.big_city_text = city
        lat = (str)(self.cities[city]['lat'])
        lon = (str)(self.cities[city]['lon'])
        self.big_coords_text = f"({lat}, {lon})"
        self.big_temp_text = (str)(self.cities[city]['temp'])
        self.big_hu_text = "Humidity: " + (str)(self.cities[city]['humidity']) + "%"
        self.big_ws_text = "Wind Speed: " + (str)(self.cities[city]['windspd']) + "m/s"
        self.big_station_text = "Station:\n" + (self.cities[city]['station']).center(25)

        self.big_aqi.destroy()
        self.big_city_name.destroy()
        self.big_coords.destroy()
        self.big_temp.destroy()
        self.big_details.destroy()
        self.big_station.destroy()


        self.big_aqi = customtkinter.CTkLabel(self.big_display_inr_frm,
                                               text = "Air Quality Index:\n" + self.big_aqi_text, 
                                              font = ("San Francisco", 50, 'bold'))
        self.big_city_name = customtkinter.CTkLabel(self.big_display_inr_frm, 
                                                    font = ("San Francisco", 27, 'bold'),
                                                    text_color="white",
                                                    text = self.big_city_text)
        self.big_coords = customtkinter.CTkLabel(self.big_display_inr_frm, 
                                                    font = ("San Francisco", 20),
                                                    text_color="white",
                                                    text = self.big_coords_text)         
        self.big_bar = customtkinter.CTkLabel(self.big_display_inr_frm, fg_color=bgColor, text = "")

        self.big_temp = customtkinter.CTkLabel(self.big_display_inr_frm,
                                               font = ("San Francisco", 27, 'bold'),
                                               text_color = "white",
                                               text = self.big_temp_text + chr(176) + "F")
        self.big_details = customtkinter.CTkLabel(self.big_display_inr_frm, 
                                                  font = ("San Francisco", 15, 'bold'),
                                                  text = self.big_hu_text + "\n" + self.big_ws_text) 
        self.big_station = customtkinter.CTkLabel(self.big_display_inr_frm, 
                                                  text = self.big_station_text,
                                                  font = ("San Francisco", 24, 'bold'))        


        self.big_station.grid(row = 1, column = 4, sticky = "sew")
        self.big_details.grid(row = 2, column = 0, sticky = "new", pady = (0, 150), padx = 20)
        self.big_temp.grid(row = 1, column = 0, sticky = "nsew", padx = 20)        
        self.big_aqi.grid(row = 2, column = 2, sticky = "ewn")
        self.big_city_name.grid(row = 0, column = 2)
        self.big_coords.grid(row = 0, column = 2, pady = (75, 0))        
        self.big_bar.grid(row = 2, columnspan = 5, sticky = "sew", pady = (100,0))
            
    def getAQI(self, city):
        api_working = True
        API_KEY = "55aacb9295ecb0dcfabd6c36a7a25bd0" 

        try:
            BASE_GEO_URL = "http://api.openweathermap.org/geo/1.0/direct?q="
            geo_url = BASE_GEO_URL + city + "&limit=1&appid=" + API_KEY
            geo_response = requests.get(geo_url) 
            
            print(geo_response.status_code)

            #Testing
            #print(geo_response.json())

            lat = geo_response.json()[0]['lat']
            lon = geo_response.json()[0]['lon']

            #Testing
            #print((str)(lat) + " " + (str)(lon))

            AQI_API_KEY = "8bbace4c-0c2b-4bd9-85f8-f22e839ec0ed"
            aqi_url = f"http://api.airvisual.com/v2/nearest_city?lat={lat}&lon={lon}&key={AQI_API_KEY}"
            aqi_response = requests.get(aqi_url)
            #Testing
            print(aqi_response.status_code)
            tempF = (aqi_response.json()['data']['current']['weather']['tp'] * (9/5)) + 32
            city_data = {
                'station':aqi_response.json()['data']['city'],
                'country':aqi_response.json()['data']['country'],
                'lat':aqi_response.json()['data']['location']['coordinates'][0],
                'lon':aqi_response.json()['data']['location']['coordinates'][1],
                'temp': round(tempF),
                'windspd':aqi_response.json()['data']['current']['weather']['ws'],
                'humidity':aqi_response.json()['data']['current']['weather']['hu'],
                'aqi':aqi_response.json()['data']['current']['pollution']['aqius'],
                'mainpol':aqi_response.json()['data']['current']['pollution']['mainus'],
            }
            aqi = city_data['aqi']
            self.cities[city] = city_data
            #print(self.cities)

            #Testing
            #print(self.cities)
        except IndexError:
            aqi = None
        except KeyError:
            aqi = None

        return aqi

if __name__ == "__main__":
    root = App()
    root.mainloop()
