//
//  LiquidationView.swift
//  LiquidCalc
//
//  Liquidation price calculator for crypto futures
//

import SwiftUI

struct LiquidationView: View {
    @StateObject private var viewModel = LiquidationViewModel()
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    // Market Type Selector
                    marketTypeSelector
                    
                    // Input Section
                    inputSection
                    
                    // Calculate Button
                    calculateButton
                    
                    // Results Section
                    if viewModel.showResults {
                        resultsSection
                    }
                }
                .padding()
            }
            .navigationTitle("Liquidation Calc")
            .background(Color(.systemGroupedBackground))
        }
    }
    
    private var marketTypeSelector: some View {
        Picker("Market Type", selection: $viewModel.marketType) {
            ForEach(MarketType.allCases) { type in
                Text(type.rawValue).tag(type)
            }
        }
        .pickerStyle(SegmentedPickerStyle())
    }
    
    private var inputSection: some View {
        VStack(spacing: 16) {
            // Position Side
            HStack {
                Text("Position")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                Spacer()
                Picker("", selection: $viewModel.positionSide) {
                    Text("Long").tag(PositionSide.long)
                    Text("Short").tag(PositionSide.short)
                }
                .pickerStyle(SegmentedPickerStyle())
                .frame(width: 150)
            }
            
            // Entry Price
            InputField(title: "Entry Price", value: $viewModel.entryPrice, placeholder: "e.g. 45000", suffix: "USDT")
            
            // Position Size
            InputField(title: "Position Size", value: $viewModel.positionSize, placeholder: "e.g. 1000", suffix: "USDT")
            
            // Leverage
            VStack(alignment: .leading, spacing: 8) {
                HStack {
                    Text("Leverage")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                    Spacer()
                    Text("\(Int(viewModel.leverage))x")
                        .font(.headline)
                        .foregroundColor(.orange)
                }
                Slider(value: $viewModel.leverage, in: 1...125, step: 1)
                    .tint(.orange)
            }
            
            // Maintenance Margin Rate
            InputField(title: "Maint. Margin Rate", value: $viewModel.maintenanceMarginRate, placeholder: "e.g. 0.5", suffix: "%")
        }
        .padding()
        .background(Color(.secondarySystemGroupedBackground))
        .cornerRadius(12)
    }
    
    private var calculateButton: some View {
        Button(action: {
            withAnimation {
                viewModel.calculate()
            }
        }) {
            Text("Calculate Liquidation Price")
                .font(.headline)
                .foregroundColor(.white)
                .frame(maxWidth: .infinity)
                .padding()
                .background(Color.orange)
                .cornerRadius(12)
        }
    }
    
    private var resultsSection: some View {
        VStack(spacing: 16) {
            Text("RESULTS")
                .font(.caption)
                .fontWeight(.bold)
                .foregroundColor(.secondary)
            
            ResultCard(
                title: "Liquidation Price",
                value: String(format: "%.2f", viewModel.liquidationPrice),
                unit: "USDT",
                color: .red
            )
            
            HStack(spacing: 12) {
                ResultCardSmall(
                    title: "Distance",
                    value: String(format: "%.2f%%", viewModel.distanceToLiquidation),
                    color: viewModel.positionSide == .long ? .red : .green
                )
                
                ResultCardSmall(
                    title: "MM Required",
                    value: String(format: "%.2f", viewModel.maintenanceMarginRequired),
                    unit: "USDT",
                    color: .orange
                )
            }
            
            // Risk Warning
            if viewModel.distanceToLiquidation < 10 {
                HStack {
                    Image(systemName: "exclamationmark.triangle.fill")
                    Text("High Risk: Liquidation is close!")
                }
                .font(.caption)
                .foregroundColor(.red)
                .padding(.vertical, 8)
            }
        }
        .padding()
        .background(Color(.secondarySystemGroupedBackground))
        .cornerRadius(12)
    }
}

#Preview {
    LiquidationView()
}