import Foundation

class FlightService {
    static let shared = FlightService()
    
    // Update this to your Vercel deployment URL or local server
    private let baseURL = "http://localhost:8000"
    
    private init() {}
    
    func fetchFlight(flightID: String) async throws -> Flight {
        guard var urlComponents = URLComponents(string: "\(baseURL)/api/flight") else {
            throw URLError(.badURL)
        }
        
        urlComponents.queryItems = [
            URLQueryItem(name: "flight_id", value: flightID)
        ]
        
        guard let url = urlComponents.url else {
            throw URLError(.badURL)
        }
        
        do {
            let (data, response) = try await URLSession.shared.data(from: url)
            
            guard let httpResponse = response as? HTTPURLResponse else {
                throw URLError(.badServerResponse)
            }
            
            guard httpResponse.statusCode == 200 else {
                throw URLError(.badServerResponse)
            }
            
            let decoder = JSONDecoder()
            let flight = try decoder.decode(Flight.self, from: data)
            return flight
        } catch {
            throw error
        }
    }
    
    func fetchCalmingMessage(flightID: String) async throws -> CalmingMessage {
        // URL encode the flight ID for the path
        guard let encodedFlightID = flightID.addingPercentEncoding(withAllowedCharacters: .urlPathAllowed),
              let url = URL(string: "\(baseURL)/api/flight/\(encodedFlightID)/calming-message") else {
            throw URLError(.badURL)
        }
        
        do {
            let (data, response) = try await URLSession.shared.data(from: url)
            
            guard let httpResponse = response as? HTTPURLResponse else {
                throw URLError(.badServerResponse)
            }
            
            guard httpResponse.statusCode == 200 else {
                // Try to get error message from response
                if let errorString = String(data: data, encoding: .utf8) {
                    print("Server error response (status \(httpResponse.statusCode)): \(errorString)")
                    // Try to parse as FastAPI error format
                    if let errorJson = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
                       let detail = errorJson["detail"] as? String {
                        throw NSError(domain: "FlightService", code: httpResponse.statusCode, userInfo: [NSLocalizedDescriptionKey: detail])
                    }
                }
                throw URLError(.badServerResponse)
            }
            
            // Print raw JSON for debugging
            if let jsonString = String(data: data, encoding: .utf8) {
                print("Received calming message JSON: \(jsonString)")
            }
            
            let decoder = JSONDecoder()
            // CalmingMessage uses explicit CodingKeys, so don't use keyDecodingStrategy
            do {
                let calmingMessage = try decoder.decode(CalmingMessage.self, from: data)
                return calmingMessage
            } catch let decodingError as DecodingError {
                print("Decoding error details:")
                switch decodingError {
                case .keyNotFound(let key, let context):
                    print("Missing key: \(key.stringValue) at \(context.debugDescription)")
                case .typeMismatch(let type, let context):
                    print("Type mismatch for \(type) at \(context.debugDescription)")
                case .valueNotFound(let type, let context):
                    print("Value not found for \(type) at \(context.debugDescription)")
                case .dataCorrupted(let context):
                    print("Data corrupted: \(context.debugDescription)")
                @unknown default:
                    print("Unknown decoding error")
                }
                throw decodingError
            }
        } catch {
            print("Network error: \(error.localizedDescription)")
            throw error
        }
    }
}

