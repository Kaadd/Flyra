import SwiftUI
import MapKit

struct FlightMapView: UIViewRepresentable {
    let flight: Flight
    
    func makeUIView(context: Context) -> MKMapView {
        let mapView = MKMapView()
        mapView.delegate = context.coordinator
        mapView.showsUserLocation = false
        mapView.mapType = .standard
        return mapView
    }
    
    func updateUIView(_ mapView: MKMapView, context: Context) {
        // Only update if we have valid plane coordinates
        guard let lat = flight.latitude,
              let lng = flight.longitude,
              lat >= -90 && lat <= 90,
              lng >= -180 && lng <= 180,
              !lat.isNaN && !lng.isNaN else {
            return
        }
        
        // Update on main thread with delay to ensure map is ready
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.3) {
            context.coordinator.updateMap(mapView, with: flight)
        }
    }
    
    func makeCoordinator() -> Coordinator {
        Coordinator()
    }
    
    class Coordinator: NSObject, MKMapViewDelegate {
        var planeAnnotation: MKPointAnnotation?
        var departureAnnotation: MKPointAnnotation?
        var arrivalAnnotation: MKPointAnnotation?
        
        func updateMap(_ mapView: MKMapView, with flight: Flight) {
            guard Thread.isMainThread else {
                DispatchQueue.main.async {
                    self.updateMap(mapView, with: flight)
                }
                return
            }
            
            var annotations: [MKPointAnnotation] = []
            var coordinates: [CLLocationCoordinate2D] = []
            
            // Add departure airport
            if let depLat = flight.departureLatitude,
               let depLng = flight.departureLongitude,
               depLat >= -90 && depLat <= 90,
               depLng >= -180 && depLng <= 180,
               !depLat.isNaN && !depLng.isNaN {
                let depCoord = CLLocationCoordinate2D(latitude: depLat, longitude: depLng)
                coordinates.append(depCoord)
                
                // Remove old if exists
                if let old = departureAnnotation {
                    mapView.removeAnnotation(old)
                }
                
                let depAnnotation = MKPointAnnotation()
                depAnnotation.coordinate = depCoord
                depAnnotation.title = flight.departureAirport ?? "Origin"
                depAnnotation.subtitle = "Departure"
                departureAnnotation = depAnnotation
                annotations.append(depAnnotation)
            }
            
            // Add plane position
            if let planeLat = flight.latitude,
               let planeLng = flight.longitude,
               planeLat >= -90 && planeLat <= 90,
               planeLng >= -180 && planeLng <= 180,
               !planeLat.isNaN && !planeLng.isNaN {
                let planeCoord = CLLocationCoordinate2D(latitude: planeLat, longitude: planeLng)
                coordinates.append(planeCoord)
                
                // Remove old if exists
                if let old = planeAnnotation {
                    mapView.removeAnnotation(old)
                }
                
                let planeAnn = MKPointAnnotation()
                planeAnn.coordinate = planeCoord
                planeAnn.title = "Current Position"
                planeAnn.subtitle = "Flight \(flight.flightNumber)"
                planeAnnotation = planeAnn
                annotations.append(planeAnn)
            }
            
            // Add arrival airport
            if let arrLat = flight.arrivalLatitude,
               let arrLng = flight.arrivalLongitude,
               arrLat >= -90 && arrLat <= 90,
               arrLng >= -180 && arrLng <= 180,
               !arrLng.isNaN && !arrLat.isNaN {
                let arrCoord = CLLocationCoordinate2D(latitude: arrLat, longitude: arrLng)
                coordinates.append(arrCoord)
                
                // Remove old if exists
                if let old = arrivalAnnotation {
                    mapView.removeAnnotation(old)
                }
                
                let arrAnnotation = MKPointAnnotation()
                arrAnnotation.coordinate = arrCoord
                arrAnnotation.title = flight.arrivalAirport ?? "Destination"
                arrAnnotation.subtitle = "Arrival"
                arrivalAnnotation = arrAnnotation
                annotations.append(arrAnnotation)
            }
            
            // Add all annotations
            if !annotations.isEmpty {
                mapView.addAnnotations(annotations)
                
                // Center map on plane position first
                if let planeAnn = planeAnnotation {
                    let region = MKCoordinateRegion(
                        center: planeAnn.coordinate,
                        latitudinalMeters: 2000000,
                        longitudinalMeters: 2000000
                    )
                    mapView.setRegion(region, animated: true)
                } else if let first = annotations.first {
                    // Fallback to first annotation if no plane
                    let region = MKCoordinateRegion(
                        center: first.coordinate,
                        latitudinalMeters: 2000000,
                        longitudinalMeters: 2000000
                    )
                    mapView.setRegion(region, animated: true)
                }
            }
        }
        
        // MARK: - MKMapViewDelegate
        
        func mapView(_ mapView: MKMapView, viewFor annotation: MKAnnotation) -> MKAnnotationView? {
            guard let pointAnnotation = annotation as? MKPointAnnotation else {
                return nil
            }
            
            // Check if it's the plane annotation (has "Current Position" title)
            if pointAnnotation.title == "Current Position" {
                let identifier = "PlaneAnnotation"
                var annotationView = mapView.dequeueReusableAnnotationView(withIdentifier: identifier)
                
                if annotationView == nil {
                    annotationView = MKAnnotationView(annotation: annotation, reuseIdentifier: identifier)
                    annotationView?.canShowCallout = true
                } else {
                    annotationView?.annotation = annotation
                }
                
                // Use airplane icon
                if let airplaneImage = UIImage(systemName: "airplane") {
                    annotationView?.image = airplaneImage.withTintColor(.systemBlue, renderingMode: .alwaysOriginal)
                }
                
                return annotationView
            } else {
                // Airport annotations (departure/arrival)
                let identifier = "AirportAnnotation"
                var annotationView = mapView.dequeueReusableAnnotationView(withIdentifier: identifier)
                
                if annotationView == nil {
                    annotationView = MKMarkerAnnotationView(annotation: annotation, reuseIdentifier: identifier)
                    annotationView?.canShowCallout = true
                } else {
                    annotationView?.annotation = annotation
                }
                
                if let markerView = annotationView as? MKMarkerAnnotationView {
                    // Green for departure, red for arrival
                    if pointAnnotation.subtitle == "Departure" {
                        markerView.markerTintColor = .systemGreen
                    } else {
                        markerView.markerTintColor = .systemRed
                    }
                    markerView.glyphImage = UIImage(systemName: "mappin.circle.fill")
                }
                
                return annotationView
            }
        }
    }
}
