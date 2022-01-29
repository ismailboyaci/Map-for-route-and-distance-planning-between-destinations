
import pandas as pd
import numpy as np
import csv
import folium
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
from math import sin,cos,radians,sqrt,atan2
class DijkstraAlgorithm:

    def __init__(self):
        

        self.min_dis_index = []
        self.short_dis = []

    def minDistance(self, dist, queue):
        minimum = float("Inf")
        min_index = -1

        for i in range(len(dist)):
            if dist[i] < minimum and i in queue:
                minimum = dist[i]
                min_index = i
        return min_index

    def printPath(self, parent, j):
        if parent[j] == -1:                 
            
            self.min_dis_index.append(j+1)
            return 0
        
        self.printPath(parent, parent[j])
        self.min_dis_index.append(j+1)
        

    def distance(self):
        

        return self.short_dis

    def path(self):
        

        return self.min_dis_index

    def dijkstraWithPath(self, graph, src, des):
        source = src - 1
        row = len(graph)
        col = len(graph[0])

        
        dist = [float('Infinity')] * row
        
        parent = [-1] * row

        
        dist[source] = 0

        queue = []                              
        for i in range(row):
            queue.append(i)

        
        while queue:
            
            u = self.minDistance(dist, queue)
            
            queue.remove(u)

           
            for i in range(col):
                if graph[u][i] and i in queue:  
                    
                    if dist[u] + graph[u][i] < dist[i]:
                        dist[i] = dist[u] + graph[u][i]
                        parent[i] = u

        self.short_dis.append(dist[des-1])  
        return self.printPath(parent, des-1)

def main():

    cities_list=[]
    with open("cities.csv", "r", newline="") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            cities_list.append(row[1])
        cities_list.pop(0)
    cities={"City":cities_list}
    df=pd.DataFrame(cities)
    longitude = []
    latitude = []
   
    def findGeocode(city):
        
        try:
            geolocator = Nominatim(user_agent="your_app_name")
          
            return geolocator.geocode(city)
      
        except GeocoderTimedOut:
          
            return findGeocode(city)    
   
    for i in (df["City"]):
      
        if findGeocode(i) != None:
           
            loc = findGeocode(i)
            latitude.append(loc.latitude)
            longitude.append(loc.longitude)
       
        else:
            latitude.append(np.nan)
            longitude.append(np.nan)

    df["latitude"]=latitude
    df["longitude"]=longitude
  
    def to_distance(lat1,long1,lat2,long2):
        r = 6373
        lon1 = radians(long1)
        lon2 = radians(long2)
        lat1 = radians(lat1)
        lat2 = radians(lat2)
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
 
        c = 2 * atan2(sqrt(a),sqrt(1-a))
        distance=c*r
        
        return distance
    n=len(df[cities])
    w, h = n,n
    distance_matrix = [[0] * w for i in range(h)] 


    for i in range(n):
        for j in range(0, i):
            distance_matrix[i][j] = distance_matrix[j][i] = to_distance(df.latitude[i],df.longitude[i],df.latitude[j],df.longitude[j])

    adj_matrix=[]
    with open("adj.csv", "r", newline="") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            adj_matrix.append(row)

    for i in range(len(adj_matrix)):
        for j in range(len(adj_matrix[i])):
            if adj_matrix[i][j]=="0":
                distance_matrix[i][j]=0
    graph=distance_matrix






    x = DijkstraAlgorithm()
    print("Cities are number below")
    with open("cities.csv", "r", newline="") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            print(row[0], row[1])
    
    source = int(input("\nEnter the source: "))             
    destination = int(input("Enter the destination: "))     
    x.dijkstraWithPath(graph, source, destination)

    shortest_path = x.path()
    distance = x.distance()

    print("\nThe shortest route: ")
    print(*shortest_path)   
    print("The shortest distance is {:.3f}".format(*distance),"km")         
    
    latitudes=[]
    longitudes=[]
    cities_data=pd.read_csv("cities.csv")


    for i in shortest_path:
        latitudes.append(cities_data.iloc[i-1,2])
        longitudes.append(cities_data.iloc[i-1,3])


    df = pd.DataFrame({'origin_lng' : longitudes, 'origin_lat' : latitudes,
                   'destination_lng': longitudes[-1], 'destination_lat': latitudes[-1]})

    centroid_lat = latitude[0]
    centroid_lon = longitude[0]
    m = folium.Map([centroid_lat, centroid_lon], zoom_start=8)
    
    if len(shortest_path)<=2:
        folium.CircleMarker([latitudes[0],longitudes[0]],radius=15,fill_color="green").add_to(m)
        folium.CircleMarker([latitudes[1],longitudes[1]],radius=15,fill_color="red").add_to(m)
        folium.PolyLine([[latitudes[0], longitudes[0]], 
                     [latitudes[1], longitudes[1]]]).add_to(m)
    else:
        folium.CircleMarker([latitudes[0],longitudes[0]],radius=15,fill_color="green").add_to(m)
        for i in range(len(shortest_path)-1):
            folium.CircleMarker([latitudes[0],longitudes[0]],radius=15,fill_color="green").add_to(m)
            folium.CircleMarker([latitudes[i+1],longitudes[i+1]],radius=15,fill_color="red").add_to(m)
            folium.PolyLine([[latitudes[i], longitudes[i]], 
                     [latitudes[i+1], longitudes[i+1]]]).add_to(m)
    m.save("Planned Route.html")

if __name__ == '__main__':
    main()
