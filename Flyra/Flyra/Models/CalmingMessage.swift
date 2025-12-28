import Foundation

struct CalmingMessage: Codable {
    let flightId: String
    let message: String
    let flightData: Flight?
    
    enum CodingKeys: String, CodingKey {
        case flightId = "flight_id"
        case message
        case flightData = "flight_data"
    }
    
    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        
        flightId = try container.decode(String.self, forKey: .flightId)
        message = try container.decode(String.self, forKey: .message)
        flightData = try container.decodeIfPresent(Flight.self, forKey: .flightData)
    }
}

