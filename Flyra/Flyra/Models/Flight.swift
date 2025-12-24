//
//  Flight.swift
//  Flyra
//
//  Created by Kadir B. on 12/24/25.
//

import Foundation

struct Flight: Codable, Identifiable {
    var id: String { flight_id }
    let flight_id: String
    let flight_number: String
    let flight_status: String
    let flight_time: String
    let flight_date: String
    let flight_gate: String
    let flight_terminal: String
}

