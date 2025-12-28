import SwiftUI

struct FlightDetailsView: View {
    @State var flight: Flight
    @State private var calmingMessage: CalmingMessage?
    @State private var isLoadingCalmingMessage = false
    @State private var calmingMessageError: String?
    @Environment(\.dismiss) var dismiss
    
    var body: some View {
        ZStack {
            // Cozy gradient background
            LinearGradient(
                colors: [
                    Color(red: 0.95, green: 0.97, blue: 1.0), // Very light blue-white
                    Color(red: 0.90, green: 0.95, blue: 0.98), // Soft sky blue
                    Color(red: 0.92, green: 0.96, blue: 0.95)  // Soft mint
                ],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .ignoresSafeArea()
            
            ScrollView {
                VStack(spacing: 24) {
                    // Flight Info Card
                    VStack(alignment: .leading, spacing: 16) {
                        HStack {
                            Image(systemName: "airplane")
                                .font(.title2)
                                .foregroundColor(Color(red: 0.40, green: 0.70, blue: 0.90))
                            Text("Flight Information")
                                .font(.title2)
                                .fontWeight(.semibold)
                                .foregroundColor(.primary)
                        }
                        .padding(.bottom, 4)
                        
                        Divider()
                            .background(Color.gray.opacity(0.2))
                        
                        VStack(spacing: 14) {
                            InfoRow(label: "Flight Number", value: flight.flightNumber, icon: "number")
                            InfoRow(label: "Status", value: flight.flightStatus, icon: "checkmark.circle.fill")
                            InfoRow(label: "Date", value: flight.flightDate, icon: "calendar")
                            InfoRow(label: "Time", value: flight.flightTime, icon: "clock.fill")
                            InfoRow(label: "Gate", value: flight.flightGate, icon: "door.left.hand.open")
                            InfoRow(label: "Terminal", value: flight.flightTerminal, icon: "building.2")
                            
                            if let aircraft = flight.aircraftType {
                                InfoRow(label: "Aircraft", value: aircraft, icon: "airplane.circle.fill")
                            }
                            
                            if let dep = flight.departureAirport {
                                InfoRow(label: "Departure", value: dep, icon: "airplane.departure")
                            }
                            
                            if let arr = flight.arrivalAirport {
                                InfoRow(label: "Arrival", value: arr, icon: "airplane.arrival")
                            }
                        }
                    }
                    .padding(20)
                    .background(
                        RoundedRectangle(cornerRadius: 20)
                            .fill(Color.white)
                            .shadow(color: Color.black.opacity(0.08), radius: 12, x: 0, y: 4)
                    )
                    .padding(.horizontal, 20)
                    .padding(.top, 8)
                    
                    // Live Tracking Card
                    VStack(alignment: .leading, spacing: 16) {
                        HStack {
                            Image(systemName: "location.fill")
                                .font(.title2)
                                .foregroundColor(Color(red: 0.50, green: 0.80, blue: 0.70))
                            Text("Live Tracking")
                                .font(.title2)
                                .fontWeight(.semibold)
                                .foregroundColor(.primary)
                        }
                        .padding(.bottom, 4)
                        
                        Divider()
                            .background(Color.gray.opacity(0.2))
                        
                        VStack(spacing: 14) {
                            if let altitude = flight.altitudeFt {
                                InfoRow(label: "Altitude", value: "\(altitude) ft", icon: "arrow.up.circle.fill")
                            }
                            
                            if let speed = flight.speedMph {
                                InfoRow(label: "Speed", value: "\(speed) mph", icon: "speedometer")
                            }
                            
                            if let eta = flight.eta {
                                InfoRow(label: "ETA", value: eta, icon: "clock.badge.checkmark")
                            }
                            
                            if let distance = flight.distanceMiles {
                                InfoRow(label: "Distance Remaining", value: "\(distance) miles", icon: "map.fill")
                            }
                        }
                        
                        // Map showing plane location - only show if we have valid coordinates
                        if let lat = flight.latitude, let lng = flight.longitude,
                           lat >= -90 && lat <= 90 && lng >= -180 && lng <= 180 {
                            VStack(alignment: .leading, spacing: 8) {
                                Text("Current Location")
                                    .font(.subheadline)
                                    .fontWeight(.medium)
                                    .foregroundColor(.secondary)
                                    .padding(.top, 8)
                                
                                FlightMapView(flight: flight)
                                    .frame(height: 250)
                                    .cornerRadius(16)
                                    .overlay(
                                        RoundedRectangle(cornerRadius: 16)
                                            .stroke(Color.gray.opacity(0.2), lineWidth: 1)
                                    )
                            }
                        }
                    }
                    .padding(20)
                    .background(
                        RoundedRectangle(cornerRadius: 20)
                            .fill(Color.white)
                            .shadow(color: Color.black.opacity(0.08), radius: 12, x: 0, y: 4)
                    )
                    .padding(.horizontal, 20)
                    
                    // Calming Message Section
                    VStack(spacing: 16) {
                        Button(action: {
                            Task {
                                await fetchCalmingMessage()
                            }
                        }) {
                            HStack {
                                if isLoadingCalmingMessage {
                                    ProgressView()
                                        .progressViewStyle(CircularProgressViewStyle(tint: .white))
                                } else {
                                    Image(systemName: "heart.fill")
                                        .font(.title3)
                                }
                                Text(isLoadingCalmingMessage ? "Loading..." : "Get Words of Encouragement")
                                    .font(.headline)
                                    .fontWeight(.semibold)
                            }
                            .foregroundColor(.white)
                            .frame(maxWidth: .infinity)
                            .padding(.vertical, 16)
                            .background(
                                LinearGradient(
                                    colors: [
                                        Color(red: 0.40, green: 0.70, blue: 0.90),
                                        Color(red: 0.50, green: 0.80, blue: 0.70)
                                    ],
                                    startPoint: .leading,
                                    endPoint: .trailing
                                )
                            )
                            .cornerRadius(16)
                            .shadow(color: Color(red: 0.40, green: 0.70, blue: 0.90).opacity(0.3), radius: 8, x: 0, y: 4)
                        }
                        .disabled(isLoadingCalmingMessage)
                        .padding(.horizontal, 20)
                        
                        if let message = calmingMessage {
                            CalmingMessageCard(message: message)
                                .padding(.horizontal, 20)
                        }
                        
                        if let error = calmingMessageError {
                            Text(error)
                                .foregroundColor(.red)
                                .font(.subheadline)
                                .padding(.horizontal, 20)
                        }
                    }
                }
                .padding(.vertical, 20)
            }
        }
        .navigationTitle("Flight Details")
        .navigationBarTitleDisplayMode(.inline)
    }
    
    private func fetchCalmingMessage() async {
        isLoadingCalmingMessage = true
        calmingMessageError = nil
        
        do {
            let message = try await FlightService.shared.fetchCalmingMessage(flightID: flight.id)
            await MainActor.run {
                calmingMessage = message
                isLoadingCalmingMessage = false
            }
        } catch let urlError as URLError {
            await MainActor.run {
                switch urlError.code {
                case .badServerResponse:
                    calmingMessageError = "Server error. Make sure OPENAI_KEY is set in the server's .env file."
                case .cannotConnectToHost:
                    calmingMessageError = "Cannot connect to server."
                default:
                    calmingMessageError = "Network error: \(urlError.localizedDescription)"
                }
                isLoadingCalmingMessage = false
            }
        } catch {
            await MainActor.run {
                calmingMessageError = "Failed to fetch calming message: \(error.localizedDescription)"
                isLoadingCalmingMessage = false
            }
        }
    }
}

struct InfoRow: View {
    let label: String
    let value: String
    let icon: String
    
    var body: some View {
        HStack(spacing: 12) {
            Image(systemName: icon)
                .font(.system(size: 16))
                .foregroundColor(Color(red: 0.40, green: 0.70, blue: 0.90))
                .frame(width: 24)
            
            Text(label + ":")
                .foregroundColor(.secondary)
                .font(.body)
            Spacer()
            Text(value)
                .fontWeight(.semibold)
                .foregroundColor(.primary)
        }
    }
}

struct CalmingMessageCard: View {
    let message: CalmingMessage
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Image(systemName: "sparkles")
                    .font(.title3)
                    .foregroundColor(Color(red: 0.50, green: 0.80, blue: 0.70))
                Text("Words of Encouragement")
                    .font(.title3)
                    .fontWeight(.semibold)
                    .foregroundColor(.primary)
            }
            
            Text(message.message)
                .font(.body)
                .foregroundColor(.secondary)
                .lineSpacing(4)
                .fixedSize(horizontal: false, vertical: true)
        }
        .padding(20)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(
            RoundedRectangle(cornerRadius: 20)
                .fill(
                    LinearGradient(
                        colors: [
                            Color.white,
                            Color(red: 0.98, green: 0.99, blue: 1.0)
                        ],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )
                )
                .shadow(color: Color.black.opacity(0.1), radius: 12, x: 0, y: 4)
        )
    }
}

struct FlightDetailsView_Previews: PreviewProvider {
    static var previews: some View {
        NavigationStack {
            FlightDetailsView(
                flight: Flight(
                    id: "AB61510",
                    flightNumber: "AB61510",
                    flightStatus: "Active",
                    flightTime: "10:30 AM",
                    flightDate: "2024-12-24",
                    flightGate: "G12",
                    flightTerminal: "3",
                    aircraftType: "Boeing 777",
                    departureAirport: "San Francisco International",
                    arrivalAirport: "Narita International Airport",
                    altitudeFt: 37000,
                    speedMph: 550,
                    eta: "2:30 PM",
                    distanceMiles: 1500
                )
            )
        }
    }
}
