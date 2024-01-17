import { Injectable } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import * as L from 'leaflet';
import { PopupService } from "./popup.service";
import { Point } from "./model/point";

@Injectable({
  providedIn: 'root'
})
export class MarkerService {
  capitals: string = 'assets/data/usa-capitals.geojson'
  data_p1: string = 'assets/data/coordonnes.json'
  constructor(private http: HttpClient, private popUpService: PopupService) { }

  makeMarkers(map: L.Map, point:Point) {
    const lon = point.longitude;
    const lat = point.latitude;
    const marker = L.marker([lon, lat]);

    marker.bindPopup(this.popUpService.makePopUp(point))

    marker.addTo(map);
  }

  makePath(map: L.Map, points: any[]){
    const polyline = L.polyline(points, {color: 'red', weight: 2, dashArray: '10 10', lineJoin:'round'})
    polyline.addTo(map)
  }
  afficherMarkerIP(map: L.Map, ip: string) {
    /*
    Requete l'API pour la liste des coordonnées d'un produceur
     */

    this.http.get(this.data_p1).subscribe((res: any) => {
      console.log(res)
      this.makeMarkers(map, res[0])
      let points = []
      for(const point of res) {
        points.push([point.longitude, point.latitude])
      }
      this.makePath(map, points)

    })
  }
  /*usaMarkers(map: L.Map) {
    this.http.get(this.capitals).subscribe((res:any)=> {
      this.makeMarkers(map, res.features[0])
      let points = []
      for(const point of res.features) {
        points.push([
          point.geometry.coordinates[1], point.geometry.coordinates[0]
        ])
      }
      console.log(points)

     points = [
        [45.51, -122.68],
        [37.77, -122.43],
        [34.04, -118.2]
      ];
      this.makePath(map, points)
    })
  }*/
}
