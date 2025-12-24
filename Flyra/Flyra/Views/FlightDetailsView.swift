//
//  FlightDetailsView.swift
//  Flyra
//
//  Created by Kadir B. on 12/24/25.
//

import SwiftUI

struct FlightDetailsView: View {
    let flight: Flight
    @Environment(\.dismiss) var dismiss
    
    var body: some View {
        ZStack {
            // Sky-like gradient background
            LinearGradient(
                colors: [
                    Color(red: 0.85, green: 0.88, blue: 0.95),
                    Color(red: 0.75, green: 0.85, blue: 0.95),
                    Color(red: 0.80, green: 0.92, blue: 0.88)
                ],
                startPoint: .top,
                endPoint: .bottom
            )
            .ignoresSafeArea()
            
            ScrollView {
                VStack(spacing: 24) {
                    // Header
                    HStack {
                        Button(action: {
                            dismiss()
                        }) {
                            Image(systemName: "chevron.left")
                                .font(.system(size: 18, weight: .semibold))
                                .foregroundColor(Color(red: 0.15, green: 0.25, blue: 0.40))
                        }
                        
                        Spacer()
                        
                        Text("Flight Details")
                            .font(.system(size: 20, weight: .bold, design: .rounded))
                            .foregroundColor(Color(red: 0.15, green: 0.25, blue: 0.40))
                        
                        Spacer()
                        
                        // Invisible button for centering
                        Button(action: {}) {
                            Image(systemName: "chevron.left")
                                .font(.system(size: 18, weight: .semibold))
                                .foregroundColor(.clear)
                        }
                        .disabled(true)
                    }
                    .padding(.horizontal, 20)
                    .padding(.top, 10)
                    
                    // Flight Card
                    VStack(spacing: 20) {
                        // Flight Number
                        VStack(spacing: 8) {
                            Text("Flight Number")
                                .font(.system(size: 14, weight: .medium, design: .rounded))
                                .foregroundColor(.gray)
                            
                            Text(flight.flight_number)
                                .font(.system(size: 36, weight: .bold, design: .rounded))
                                .foregroundColor(Color(red: 0.15, green: 0.25, blue: 0.40))
                        }
                        .padding(.top, 20)
                        
                        Divider()
                            .padding(.horizontal, 20)
                        
                        // Status
                        VStack(alignment: .leading, spacing: 12) {
                            HStack {
                                Text("Status")
                                    .font(.system(size: 16, weight: .semibold, design: .rounded))
                                    .foregroundColor(.gray)
                                
                                Spacer()
                                
                                Text(flight.flight_status)
                                    .font(.system(size: 18, weight: .bold, design: .rounded))
                                    .foregroundColor(statusColor(for: flight.flight_status))
                                    .padding(.horizontal, 16)
                                    .padding(.vertical, 8)
                                    .background(statusColor(for: flight.flight_status).opacity(0.2))
                                    .cornerRadius(12)
                            }
                            
                            // Flight Details Grid
                            VStack(spacing: 16) {
                                DetailRow(label: "Date", value: flight.flight_date)
                                DetailRow(label: "Time", value: flight.flight_time)
                                DetailRow(label: "Gate", value: flight.flight_gate)
                                DetailRow(label: "Terminal", value: flight.flight_terminal)
                            }
                            .padding(.top, 8)
                        }
                        .padding(.horizontal, 20)
                        .padding(.bottom, 20)
                    }
                    .background(Color.white.opacity(0.9))
                    .cornerRadius(20)
                    .shadow(color: Color.black.opacity(0.1), radius: 10, x: 0, y: 5)
                    .padding(.horizontal, 20)
                    
                    Spacer()
                }
                .padding(.top, 20)
            }
        }
        .navigationBarHidden(true)
    }
    
    private func statusColor(for status: String) -> Color {
        let lowercased = status.lowercased()
        if lowercased.contains("on time") || lowercased.contains("on-time") {
            return Color.green
        } else if lowercased.contains("delayed") {
            return Color.orange
        } else if lowercased.contains("cancelled") || lowercased.contains("canceled") {
            return Color.red
        } else {
            return Color.blue
        }
    }
}

struct DetailRow: View {
    let label: String
    let value: String
    
    var body: some View {
        HStack {
            Text(label)
                .font(.system(size: 16, weight: .medium, design: .rounded))
                .foregroundColor(.gray)
            
            Spacer()
            
            Text(value)
                .font(.system(size: 16, weight: .semibold, design: .rounded))
                .foregroundColor(Color(red: 0.15, green: 0.25, blue: 0.40))
        }
    }
}

struct FlightDetailsView_Previews: PreviewProvider {
    static var previews: some View {
        FlightDetailsView(flight: Flight(
            flight_id: "UA837",
            flight_number: "UA837",
            flight_status: "On time",
            flight_time: "10:00 AM",
            flight_date: "2025-01-01",
            flight_gate: "A1",
            flight_terminal: "1"
        ))
    }
}

