//
//  FlightService.swift
//  Flyra
//
//  Created by Kadir B. on 12/24/25.
//

import Foundation

class FlightService {
    // Update this URL to your server URL
    // For local development: "http://localhost:8000"
    // For production: your Vercel deployment URL
    private let baseURL = "http://localhost:8000"
    
    func fetchFlight(flightID: String) async throws -> Flight {
        guard let encodedFlightID = flightID.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed),
              let url = URL(string: "\(baseURL)/api/flight?flight_id=\(encodedFlightID)") else {
            throw FlightError.invalidURL
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw FlightError.invalidResponse
        }
        
        guard httpResponse.statusCode == 200 else {
            throw FlightError.serverError(httpResponse.statusCode)
        }
        
        do {
            let flight = try JSONDecoder().decode(Flight.self, from: data)
            return flight
        } catch {
            throw FlightError.decodingError(error)
        }
    }
}

enum FlightError: LocalizedError {
    case invalidURL
    case invalidResponse
    case serverError(Int)
    case decodingError(Error)
    
    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "Invalid URL"
        case .invalidResponse:
            return "Invalid response from server"
        case .serverError(let code):
            return "Server error: \(code)"
        case .decodingError(let error):
            return "Failed to decode response: \(error.localizedDescription)"
        }
    }
}

