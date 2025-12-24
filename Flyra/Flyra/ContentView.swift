//
//  ContentView.swift
//  Flyra
//
//  Created by Kadir B. on 12/24/25.
//

import SwiftUI

// Bird Logo Shape
struct BirdLogo: View {
    var body: some View {
        ZStack {
            // Left wing (darker teal-blue)
            Ellipse()
                .fill(
                    LinearGradient(
                        colors: [
                            Color(red: 0.20, green: 0.50, blue: 0.60), // Darker teal-blue
                            Color(red: 0.25, green: 0.55, blue: 0.65)
                        ],
                        startPoint: .leading,
                        endPoint: .trailing
                    )
                )
                .frame(width: 50, height: 30)
                .offset(x: -15, y: 0)
                .rotationEffect(.degrees(-15))
            
            // Right wing (lighter mint green)
            Ellipse()
                .fill(
                    LinearGradient(
                        colors: [
                            Color(red: 0.30, green: 0.65, blue: 0.70), // Lighter teal
                            Color(red: 0.40, green: 0.75, blue: 0.70)  // Mint green
                        ],
                        startPoint: .leading,
                        endPoint: .trailing
                    )
                )
                .frame(width: 50, height: 30)
                .offset(x: 15, y: 0)
                .rotationEffect(.degrees(15))
            
            // Body (mint green)
            Ellipse()
                .fill(
                    LinearGradient(
                        colors: [
                            Color(red: 0.35, green: 0.70, blue: 0.75),
                            Color(red: 0.45, green: 0.80, blue: 0.75)  // Mint green
                        ],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )
                )
                .frame(width: 35, height: 25)
        }
        .frame(width: 80, height: 40)
    }
}

// Cloud Shape
struct CloudShape: Shape {
    func path(in rect: CGRect) -> Path {
        var path = Path()
        let width = rect.width
        let height = rect.height
        
        // Main cloud body
        path.addEllipse(in: CGRect(x: width * 0.1, y: height * 0.3, width: width * 0.4, height: height * 0.4))
        path.addEllipse(in: CGRect(x: width * 0.3, y: height * 0.1, width: width * 0.5, height: height * 0.5))
        path.addEllipse(in: CGRect(x: width * 0.5, y: height * 0.2, width: width * 0.4, height: height * 0.4))
        path.addEllipse(in: CGRect(x: width * 0.6, y: height * 0.3, width: width * 0.3, height: height * 0.3))
        
        return path
    }
}

struct ContentView: View {
    @State private var flightID: String = ""
    @State private var isLoading: Bool = false
    @State private var errorMessage: String?
    @State private var flight: Flight?
    
    private let flightService = FlightService()
    
    var body: some View {
        ZStack {
            // Sky-like gradient background
            LinearGradient(
                colors: [
                    Color(red: 0.85, green: 0.88, blue: 0.95), // Light lavender-blue
                    Color(red: 0.75, green: 0.85, blue: 0.95), // Sky blue
                    Color(red: 0.80, green: 0.92, blue: 0.88)  // Subtle green
                ],
                startPoint: .top,
                endPoint: .bottom
            )
            .ignoresSafeArea()
            
            // Clouds in the lower half
            VStack {
                Spacer()
                HStack {
                    CloudShape()
                        .fill(Color.white.opacity(0.7))
                        .frame(width: 120, height: 60)
                        .offset(x: -40, y: 20)
                    
                    Spacer()
                    
                    CloudShape()
                        .fill(Color.white.opacity(0.6))
                        .frame(width: 100, height: 50)
                        .offset(x: 20, y: 10)
                }
                .padding(.horizontal, 20)
                
                HStack {
                    CloudShape()
                        .fill(Color.white.opacity(0.65))
                        .frame(width: 90, height: 45)
                        .offset(x: 30, y: -10)
                    
                    Spacer()
                    
                    CloudShape()
                        .fill(Color.white.opacity(0.7))
                        .frame(width: 110, height: 55)
                        .offset(x: -30, y: 0)
                }
                .padding(.horizontal, 40)
                .padding(.bottom, 40)
            }
            
            // Main content
            VStack(spacing: 0) {
                Spacer()
                    .frame(height: 60)
                
                // Bird Logo
                BirdLogo()
                    .padding(.bottom, 16)
                
                // App Title
                Text("Flyra")
                    .font(.system(size: 48, weight: .bold, design: .rounded))
                    .foregroundColor(Color(red: 0.15, green: 0.25, blue: 0.40))
                    .padding(.bottom, 8)
                
                // Subtitle
                Text("Enter your flight to begin")
                    .font(.system(size: 16, weight: .regular, design: .rounded))
                    .foregroundColor(.gray)
                    .padding(.bottom, 50)
                
                // Flight Number Input Field
                HStack(spacing: 0) {
                    TextField("Enter flight number", text: $flightID)
                        .font(.system(size: 18, weight: .medium, design: .rounded))
                        .foregroundColor(.primary)
                        .padding(.leading, 20)
                        .padding(.trailing, 12)
                    
                    Divider()
                        .frame(height: 30)
                        .padding(.vertical, 8)
                    
                    Text("ex: UA837")
                        .font(.system(size: 18, weight: .medium, design: .rounded))
                        .foregroundColor(.gray)
                        .padding(.leading, 12)
                        .padding(.trailing, 20)
                }
                .frame(height: 56)
                .background(Color.white.opacity(0.9))
                .cornerRadius(16)
                .shadow(color: Color.black.opacity(0.05), radius: 8, x: 0, y: 4)
                .padding(.horizontal, 32)
                .padding(.bottom, 40)
                
                // Error Message
                if let errorMessage = errorMessage {
                    Text(errorMessage)
                        .font(.system(size: 14, weight: .medium, design: .rounded))
                        .foregroundColor(.red)
                        .padding(.horizontal, 32)
                        .padding(.bottom, 8)
                }
                
                // Track My Flight Button
                Button(action: {
                    Task {
                        await fetchFlight()
                    }
                }) {
                    HStack {
                        if isLoading {
                            ProgressView()
                                .progressViewStyle(CircularProgressViewStyle(tint: .white))
                                .scaleEffect(0.8)
                        } else {
                            Text("Track My Flight")
                                .font(.system(size: 20, weight: .semibold, design: .rounded))
                                .foregroundColor(.white)
                        }
                    }
                    .frame(maxWidth: .infinity)
                    .frame(height: 56)
                    .background(
                        LinearGradient(
                            colors: [
                                Color(red: 0.40, green: 0.70, blue: 0.90), // Light blue
                                Color(red: 0.50, green: 0.80, blue: 0.70)  // Light green
                            ],
                            startPoint: .leading,
                            endPoint: .trailing
                        )
                    )
                    .cornerRadius(16)
                    .shadow(color: Color.black.opacity(0.1), radius: 8, x: 0, y: 4)
                }
                .disabled(flightID.trimmingCharacters(in: .whitespaces).isEmpty || isLoading)
                .opacity(flightID.trimmingCharacters(in: .whitespaces).isEmpty || isLoading ? 0.5 : 1.0)
                .padding(.horizontal, 32)
                
                Spacer()
            }
        }
        .sheet(item: $flight) { flight in
            FlightDetailsView(flight: flight)
        }
    }
    
    private func fetchFlight() async {
        let trimmedID = flightID.trimmingCharacters(in: .whitespaces)
        guard !trimmedID.isEmpty else { return }
        
        isLoading = true
        errorMessage = nil
        
        do {
            let fetchedFlight = try await flightService.fetchFlight(flightID: trimmedID)
            await MainActor.run {
                self.flight = fetchedFlight
                self.isLoading = false
            }
        } catch {
            await MainActor.run {
                self.isLoading = false
                self.errorMessage = error.localizedDescription
            }
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
