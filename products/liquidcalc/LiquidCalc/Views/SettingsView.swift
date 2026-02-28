//
//  SettingsView.swift
//  LiquidCalc
//
//  App settings and preferences
//

import SwiftUI

struct SettingsView: View {
    @AppStorage("defaultLeverage") private var defaultLeverage: Double = 10
    @AppStorage("defaultRiskPercent") private var defaultRiskPercent: Double = 2
    @AppStorage("defaultFee") private var defaultFee: Double = 0.05
    @AppStorage("currency") private var currency: String = "USDT"
    
    var body: some View {
        NavigationView {
            List {
                Section(header: Text("DEFAULTS")) {
                    HStack {
                        Text("Default Leverage")
                        Spacer()
                        Text("\(Int(defaultLeverage))x")
                            .foregroundColor(.secondary)
                    }
                    
                    Slider(value: $defaultLeverage, in: 1...125, step: 1)
                        .tint(.orange)
                    
                    HStack {
                        Text("Default Risk %")
                        Spacer()
                        Text("\(defaultRiskPercent, specifier: "%.1f")%")
                            .foregroundColor(.secondary)
                    }
                    
                    Slider(value: $defaultRiskPercent, in: 0.5...10, step: 0.5)
                        .tint(.orange)
                    
                    HStack {
                        Text("Default Trading Fee")
                        Spacer()
                        Text("\(defaultFee, specifier: "%.2f")%")
                            .foregroundColor(.secondary)
                    }
                    
                    Slider(value: $defaultFee, in: 0...1, step: 0.01)
                        .tint(.orange)
                }
                
                Section(header: Text("CURRENCY")) {
                    Picker("Currency", selection: $currency) {
                        Text("USDT").tag("USDT")
                        Text("USD").tag("USD")
                        Text("BUSD").tag("BUSD")
                    }
                    .pickerStyle(SegmentedPickerStyle())
                }
                
                Section(header: Text("ABOUT")) {
                    HStack {
                        Text("Version")
                        Spacer()
                        Text("1.0.0")
                            .foregroundColor(.secondary)
                    }
                    
                    HStack {
                        Text("Price")
                        Spacer()
                        Text("$2.99")
                            .foregroundColor(.secondary)
                    }
                    
                    Text("LiquidCalc helps crypto futures traders calculate liquidation prices, position sizes, and P&L with precision.")
                        .font(.caption)
                        .foregroundColor(.secondary)
                        .padding(.vertical, 4)
                }
                
                Section {
                    Button(action: {
                        // Reset to defaults
                        defaultLeverage = 10
                        defaultRiskPercent = 2
                        defaultFee = 0.05
                    }) {
                        Text("Reset to Defaults")
                            .foregroundColor(.red)
                    }
                }
            }
            .navigationTitle("Settings")
        }
    }
}

#Preview {
    SettingsView()
}