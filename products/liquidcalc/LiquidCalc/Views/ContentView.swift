//
//  ContentView.swift
//  LiquidCalc
//
//  Main tab view container
//

import SwiftUI

struct ContentView: View {
    @State private var selectedTab = 0
    
    var body: some View {
        TabView(selection: $selectedTab) {
            LiquidationView()
                .tabItem {
                    Label("Liquidation", systemImage: "exclamationmark.triangle")
                }
                .tag(0)
            
            PositionSizingView()
                .tabItem {
                    Label("Position", systemImage: "dollarsign.circle")
                }
                .tag(1)
            
            PnLView()
                .tabItem {
                    Label("P&L", systemImage: "chart.line.uptrend.xyaxis")
                }
                .tag(2)
            
            SettingsView()
                .tabItem {
                    Label("Settings", systemImage: "gear")
                }
                .tag(3)
        }
        .accentColor(.orange)
    }
}

#Preview {
    ContentView()
}