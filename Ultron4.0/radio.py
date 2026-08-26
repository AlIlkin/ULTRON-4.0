import webbrowser

def play_radio(speak_func, listen_func):
    """
    Opens Radio Garden and uses its direct search URL parameter 
    to look up the station you specify.
    """
    speak_func("Which station would you like to listen to?")
    station_name = listen_func()
    
    if station_name:
        speak_func(f"Searching for {station_name} on Radio Garden.")
        
        query = station_name.strip().replace(" ", "+")
        radio_search_url = f"https://radio.garden/search?q={query}"
        
        webbrowser.open(radio_search_url)
    else:
        speak_func("I didn't catch the station name.")
