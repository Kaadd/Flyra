import Foundation

struct Flight: Codable, Identifiable, Hashable {
    let id: String
    let flightNumber: String
    let flightStatus: String
    let flightTime: String
    let flightDate: String
    let flightGate: String
    let flightTerminal: String
    
    // Additional context
    let aircraftType: String?
    let departureAirport: String?
    let arrivalAirport: String?
    let departureDelay: Int?
    let arrivalDelay: Int?
    
    // Live tracking data
    let altitudeFt: Int?
    let speedMph: Int?
    let latitude: Double?
    let longitude: Double?
    let direction: Int?
    
    // Airport coordinates
    let departureLatitude: Double?
    let departureLongitude: Double?
    let arrivalLatitude: Double?
    let arrivalLongitude: Double?
    
    // ETA and distance
    let eta: String?
    let distanceMiles: Int?
    
    // Coding keys
    enum CodingKeys: String, CodingKey {
        case id = "flight_id"
        case flightNumber = "flight_number"
        case flightStatus = "flight_status"
        case flightTime = "flight_time"
        case flightDate = "flight_date"
        case flightGate = "flight_gate"
        case flightTerminal = "flight_terminal"
        case aircraftType = "aircraft_type"
        case departureAirport = "departure_airport"
        case arrivalAirport = "arrival_airport"
        case departureDelay = "departure_delay"
        case arrivalDelay = "arrival_delay"
        case altitudeFt = "altitude_ft"
        case speedMph = "speed_mph"
        case latitude
        case longitude
        case direction
        case departureLatitude = "departure_latitude"
        case departureLongitude = "departure_longitude"
        case arrivalLatitude = "arrival_latitude"
        case arrivalLongitude = "arrival_longitude"
        case eta
        case distanceMiles = "distance_miles"
    }
    
    // Custom decoder to handle optional fields gracefully
    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        
        id = try container.decode(String.self, forKey: .id)
        flightNumber = try container.decode(String.self, forKey: .flightNumber)
        flightStatus = try container.decode(String.self, forKey: .flightStatus)
        flightTime = try container.decode(String.self, forKey: .flightTime)
        flightDate = try container.decode(String.self, forKey: .flightDate)
        flightGate = try container.decode(String.self, forKey: .flightGate)
        flightTerminal = try container.decode(String.self, forKey: .flightTerminal)
        
        aircraftType = try container.decodeIfPresent(String.self, forKey: .aircraftType)
        departureAirport = try container.decodeIfPresent(String.self, forKey: .departureAirport)
        arrivalAirport = try container.decodeIfPresent(String.self, forKey: .arrivalAirport)
        departureDelay = try container.decodeIfPresent(Int.self, forKey: .departureDelay)
        arrivalDelay = try container.decodeIfPresent(Int.self, forKey: .arrivalDelay)
        
        altitudeFt = try container.decodeIfPresent(Int.self, forKey: .altitudeFt)
        speedMph = try container.decodeIfPresent(Int.self, forKey: .speedMph)
        latitude = try container.decodeIfPresent(Double.self, forKey: .latitude)
        longitude = try container.decodeIfPresent(Double.self, forKey: .longitude)
        direction = try container.decodeIfPresent(Int.self, forKey: .direction)
        
        departureLatitude = try container.decodeIfPresent(Double.self, forKey: .departureLatitude)
        departureLongitude = try container.decodeIfPresent(Double.self, forKey: .departureLongitude)
        arrivalLatitude = try container.decodeIfPresent(Double.self, forKey: .arrivalLatitude)
        arrivalLongitude = try container.decodeIfPresent(Double.self, forKey: .arrivalLongitude)
        
        eta = try container.decodeIfPresent(String.self, forKey: .eta)
        distanceMiles = try container.decodeIfPresent(Int.self, forKey: .distanceMiles)
    }
    
    // Regular initializer for manual instantiation (e.g., in previews)
    init(
        id: String,
        flightNumber: String,
        flightStatus: String,
        flightTime: String,
        flightDate: String,
        flightGate: String,
        flightTerminal: String,
        aircraftType: String? = nil,
        departureAirport: String? = nil,
        arrivalAirport: String? = nil,
        departureDelay: Int? = nil,
        arrivalDelay: Int? = nil,
        altitudeFt: Int? = nil,
        speedMph: Int? = nil,
        latitude: Double? = nil,
        longitude: Double? = nil,
        direction: Int? = nil,
        departureLatitude: Double? = nil,
        departureLongitude: Double? = nil,
        arrivalLatitude: Double? = nil,
        arrivalLongitude: Double? = nil,
        eta: String? = nil,
        distanceMiles: Int? = nil
    ) {
        self.id = id
        self.flightNumber = flightNumber
        self.flightStatus = flightStatus
        self.flightTime = flightTime
        self.flightDate = flightDate
        self.flightGate = flightGate
        self.flightTerminal = flightTerminal
        self.aircraftType = aircraftType
        self.departureAirport = departureAirport
        self.arrivalAirport = arrivalAirport
        self.departureDelay = departureDelay
        self.arrivalDelay = arrivalDelay
        self.altitudeFt = altitudeFt
        self.speedMph = speedMph
        self.latitude = latitude
        self.longitude = longitude
        self.direction = direction
        self.departureLatitude = departureLatitude
        self.departureLongitude = departureLongitude
        self.arrivalLatitude = arrivalLatitude
        self.arrivalLongitude = arrivalLongitude
        self.eta = eta
        self.distanceMiles = distanceMiles
    }
    
    // Manual Hashable conformance
    func hash(into hasher: inout Hasher) {
        hasher.combine(id)
        hasher.combine(flightNumber)
        hasher.combine(flightStatus)
        hasher.combine(flightTime)
        hasher.combine(flightDate)
        hasher.combine(flightGate)
        hasher.combine(flightTerminal)
    }
    
    static func == (lhs: Flight, rhs: Flight) -> Bool {
        return lhs.id == rhs.id &&
               lhs.flightNumber == rhs.flightNumber &&
               lhs.flightStatus == rhs.flightStatus &&
               lhs.flightTime == rhs.flightTime &&
               lhs.flightDate == rhs.flightDate &&
               lhs.flightGate == rhs.flightGate &&
               lhs.flightTerminal == rhs.flightTerminal
    }
}

