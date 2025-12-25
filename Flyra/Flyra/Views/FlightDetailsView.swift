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
    @State private var calmingMessage: String?
    @State private var isLoadingCalmingMessage: Bool = false
    @State private var calmingMessageError: String?
    
    private let flightService = FlightService()
    
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
                    
                    // Calming Message Button
                    Button(action: {
                        Task {
                            await fetchCalmingMessage()
                        }
                    }) {
                        HStack {
                            if isLoadingCalmingMessage {
                                ProgressView()
                                    .progressViewStyle(CircularProgressViewStyle(tint: .white))
                                    .scaleEffect(0.8)
                            } else {
                                Image(systemName: "heart.fill")
                                    .font(.system(size: 18, weight: .semibold))
                                Text("Get Words of Encouragement")
                                    .font(.system(size: 18, weight: .semibold, design: .rounded))
                            }
                        }
                        .foregroundColor(.white)
                        .frame(maxWidth: .infinity)
                        .frame(height: 56)
                        .background(
                            LinearGradient(
                                colors: [
                                    Color(red: 0.60, green: 0.80, blue: 0.90), // Soft blue
                                    Color(red: 0.70, green: 0.85, blue: 0.75)  // Soft green
                                ],
                                startPoint: .leading,
                                endPoint: .trailing
                            )
                        )
                        .cornerRadius(16)
                        .shadow(color: Color.black.opacity(0.1), radius: 8, x: 0, y: 4)
                    }
                    .disabled(isLoadingCalmingMessage)
                    .opacity(isLoadingCalmingMessage ? 0.7 : 1.0)
                    .padding(.horizontal, 20)
                    
                    // Calming Message Display
                    if let message = calmingMessage {
                        CalmingMessageCard(message: message)
                            .padding(.horizontal, 20)
                            .transition(.asymmetric(
                                insertion: .opacity.combined(with: .move(edge: .bottom)).combined(with: .scale(scale: 0.9)),
                                removal: .opacity.combined(with: .scale(scale: 0.95))
                            ))
                            .animation(.spring(response: 0.6, dampingFraction: 0.8), value: calmingMessage != nil)
                    }
                    
                    // Error Message
                    if let error = calmingMessageError {
                        Text(error)
                            .font(.system(size: 14, weight: .medium, design: .rounded))
                            .foregroundColor(.red)
                            .padding(.horizontal, 20)
                    }
                    
                    Spacer()
                }
                .padding(.top, 20)
            }
        }
        .navigationBarHidden(true)
    }
    
    private func fetchCalmingMessage() async {
        isLoadingCalmingMessage = true
        calmingMessageError = nil
        
        do {
            let response = try await flightService.fetchCalmingMessage(flightID: flight.flight_id)
            await MainActor.run {
                self.calmingMessage = response.calming_message
                self.isLoadingCalmingMessage = false
            }
        } catch {
            await MainActor.run {
                self.isLoadingCalmingMessage = false
                self.calmingMessageError = error.localizedDescription
            }
        }
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

struct CalmingMessageCard: View {
    let message: String
    
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            HStack {
                Image(systemName: "sparkles")
                    .font(.system(size: 24, weight: .medium))
                    .foregroundColor(Color(red: 0.50, green: 0.70, blue: 0.85))
                
                Text("Words of Encouragement")
                    .font(.system(size: 20, weight: .bold, design: .rounded))
                    .foregroundColor(Color(red: 0.15, green: 0.25, blue: 0.40))
                
                Spacer()
            }
            
            Text(message)
                .font(.system(size: 17, weight: .regular, design: .rounded))
                .foregroundColor(Color(red: 0.20, green: 0.30, blue: 0.45))
                .lineSpacing(6)
                .fixedSize(horizontal: false, vertical: true)
        }
        .padding(24)
        .background(
            LinearGradient(
                colors: [
                    Color(red: 0.95, green: 0.97, blue: 1.0), // Very light blue
                    Color(red: 0.92, green: 0.96, blue: 0.98)  // Soft white-blue
                ],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
        )
        .cornerRadius(20)
        .shadow(color: Color.black.opacity(0.08), radius: 12, x: 0, y: 4)
        .overlay(
            RoundedRectangle(cornerRadius: 20)
                .stroke(
                    LinearGradient(
                        colors: [
                            Color(red: 0.70, green: 0.85, blue: 0.95).opacity(0.3),
                            Color(red: 0.75, green: 0.90, blue: 0.85).opacity(0.3)
                        ],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    ),
                    lineWidth: 1
                )
        )
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

