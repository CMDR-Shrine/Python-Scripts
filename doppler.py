import os
import subprocess
import time

# Define constants
SECS = 600
RADAR_LOC = os.path.join(os.getenv('XDG_CACHE_HOME', os.path.expanduser('~/.cache')), 'radar')
DOPPLER = os.path.join(os.getenv('XDG_CACHE_HOME', os.path.expanduser('~/.cache')), 'doppler.gif')

# Function to pick location
def pickloc():
    chosen = input("Select a radar to use as default:")
    continentcode, countrycode, radarcode = chosen.split(':')
    # Print codes to radar location file
    with open(RADAR_LOC, 'w') as f:
        f.write(f"{countrycode},{radarcode}\n")

# Function to get Doppler
def getdoppler():
    with open(RADAR_LOC, 'r') as f:
        country, province = f.readline().strip().split(',')
    
    print(f"Pulling most recent Doppler RADAR for {province}.")
    if country == 'US':
        subprocess.run(["curl", "-sL", f"https://radar.weather.gov/ridge/standard/{province}_loop.gif", "-o", DOPPLER])
    elif country == 'DE':
        province = province.lower()
        subprocess.run(["curl", "-sL", f"https://www.dwd.de/DWD/wetter/radar/radfilm_{province}_akt.gif", "-o", DOPPLER])
    elif country == 'NL':
        subprocess.run(["curl", "-sL", "https://cdn.knmi.nl/knmi/map/general/weather-map.gif", "-o", DOPPLER])

# Function to show Doppler
def showdoppler():
    subprocess.Popen(["mpv", "--no-osc", "--loop=inf", "--no-terminal", DOPPLER])

# Main function
def main():
    if not os.path.isfile(RADAR_LOC):
        pickloc()
        getdoppler()
    elif time.time() - os.path.getmtime(DOPPLER) > SECS:
        getdoppler()
    showdoppler()

if __name__ == "__main__":
    main()

