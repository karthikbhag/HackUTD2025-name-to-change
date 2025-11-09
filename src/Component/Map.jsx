import React, {useEffect, useRef,useState} from "react";
import {MapContainer, Marker,Popup, TileLayer} from "react-leaflet";
import HeatmapLayer from './HeatmapLayer'; 
import "leaflet/dist/leaflet.css";
import "./leaflet2.css"
import 'react-leaflet-markercluster/styles'
import MarkerClusterGroup from "react-leaflet-markercluster";
import {Icon, divIcon} from "leaflet"
import { DISASTERS } from "./data";
import MenuItem from "./MenuItem";

export default function Map({/**The array of reviews and coordinates for each review say its called "Reviews"*/reviews}) {
    const mapRef = useRef(null);
    let [latitude, setLatitude] = useState(35.0078);
    let [longitude, setLongitude] = useState(97.0929);
    
    const options = {
        enableHighAccuracy: true,
        timeout: 1000,
        maximumAge: 0,
    };
    const custumIcon = new Icon({
        iconUrl: "location-pin.png",iconSize: [38,38]
    });

    

    
    const points = reviews.map((d) => [d.latitude, d.longitude]); // 0.5 = intensity (0–1)**/

    return(
        <MapContainer center={[latitude, longitude]} zoom={5} ref={mapRef} style={{height: "500px", width: "1000px"}}>
            
            <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />

            <HeatmapLayer points={points} />
            <MarkerClusterGroup>
            {reviews.map((review,index) => (    
                
                <Marker key ={index} position = {[review.latitude,review.longitude]} icon ={custumIcon}>
                    <Popup> <MenuItem name = {r.name} 
                                        location = {review.location} report = {review.report} date = {review.date} level ={review.review_level} class1 = "popup" /> </Popup>
                </Marker>
                
            ))}
            </MarkerClusterGroup>
            
        

        </MapContainer>

    );
}
