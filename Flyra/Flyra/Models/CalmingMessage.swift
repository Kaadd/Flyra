//
//  CalmingMessage.swift
//  Flyra
//
//  Created by Kadir B. on 12/24/25.
//

import Foundation

struct CalmingMessageResponse: Codable {
    let flight_info: FlightInfo
    let calming_message: String
}

struct FlightInfo: Codable {
    let flight_number: String?
    let flight_status: String?
    let flight_time: String?
    let flight_date: String?
    let flight_gate: String?
    let flight_terminal: String?
}

