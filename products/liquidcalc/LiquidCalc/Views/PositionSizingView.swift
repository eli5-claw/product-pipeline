//
//  PositionSizingView.swift
//  LiquidCalc
//
//  Position sizing calculator for risk management
//

import SwiftUI

struct PositionSizingView: View {
    @StateObject private var viewModel = PositionSizingViewModel()
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    // Account Info
                    accountSection
                    
                    // Risk Parameters
                    riskSection
                    
                    // Trade Setup
                    tradeSetupSection
                    
                    // Calculate Button
                    calculateButton
                    
                    // Results
                    if viewModel.showResults {
                        resultsSection
                    }
                }
                .padding()
            }
                .navigationTitle("Position Sizing")
            .background(Color(.systemGroupedBackground))
        }
    }
    
    private var accountSection: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("ACCOUNT")
                .font(.caption)
                .fontWeight(.bold)
                .foregroundColor(.secondary)
            
            InputField(title: "Account Balance", value: $viewModel.accountBalance, placeholder: "e.g. 10000", suffix: "USDT")
            
            HStack {
                Text("Risk Per Trade")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                Spacer()
                Text("\(Int(viewModel.riskPercent))%")
                    .font(.headline)
                    .foregroundColor(.orange)
            }
            
            Slider(value: $viewModel.riskPercent, in: 0.5...10, step: 0.5)
                .tint(.orange)
            
            Text("Risk Amount: \(String(format: "%.2f", viewModel.riskAmount)) USDT")
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .padding()
        .background(Color(.secondarySystemGroupedBackground))
        .cornerRadius(12)
    }
    
    private var riskSection: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("STOP LOSS")
                .font(.caption)
                .fontWeight(.bold)
                .foregroundColor(.secondary)
            
            InputField(title: "Entry Price", value: $viewModel.entryPrice, placeholder: "e.g. 45000", suffix: "USDT")
            
            InputField(title: "Stop Loss Price", value: $viewModel.stopLossPrice, placeholder: "e.g. 44000", suffix: "USDT")
            
            if viewModel.entryPrice > 0 && viewModel.stopLossPrice > 0 {
                let distance = abs(viewModel.entryPrice - viewModel.stopLossPrice) / viewModel.entryPrice * 100
                HStack {
                    Text("Stop Distance:")
                        .font(.caption)
                    Text("\(String(format: "%.2f", distance))%")
                        .font(.caption)
                        .fontWeight(.bold)
                        .foregroundColor(distance > 5 ? .orange : .green)
                }
            }
        }
        .padding()
        .background(Color(.secondarySystemGroupedBackground))
        .cornerRadius(12)
    }
    
    private var tradeSetupSection: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("LEVERAGE")
                .font(.caption)
                .fontWeight(.bold)
                .foregroundColor(.secondary)
            
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
            Text("Calculate Position Size")
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
            Text("POSITION SIZE")
                .font(.caption)
                .fontWeight(.bold)
                .foregroundColor(.secondary)
            
            ResultCard(
                title: "Position Size",
                value: String(format: "%.2f", viewModel.positionSize),
                unit: "USDT",
                color: .green
            )
            
            HStack(spacing: 12) {
                ResultCardSmall(
                    title: "Margin Required",
                    value: String(format: "%.2f", viewModel.marginRequired),
                    unit: "USDT",
                    color: .blue
                )
                
                ResultCardSmall(
                    title: "Max Leverage",
                    value: "\(Int(viewModel.leverage))x",
                    color: .orange
                )
            }
            
            // Warning if position exceeds account
            if viewModel.positionSize > viewModel.accountBalance * viewModel.leverage {
                HStack {
                    Image(systemName: "exclamationmark.triangle.fill")
                    Text("Position exceeds max leverage!")
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
    PositionSizingView()
}