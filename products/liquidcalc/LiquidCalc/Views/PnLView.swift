//
//  PnLView.swift
//  LiquidCalc
//
//  Profit & Loss calculator for trades
//

import SwiftUI

struct PnLView: View {
    @StateObject private var viewModel = PnLViewModel()
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    // Trade Direction
                    directionSelector
                    
                    // Trade Details
                    tradeDetailsSection
                    
                    // Calculate Button
                    calculateButton
                    
                    // Results
                    if viewModel.showResults {
                        resultsSection
                    }
                }
                .padding()
            }
            .navigationTitle("P&L Calculator")
            .background(Color(.systemGroupedBackground))
        }
    }
    
    private var directionSelector: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("TRADE DIRECTION")
                .font(.caption)
                .fontWeight(.bold)
                .foregroundColor(.secondary)
            
            Picker("Direction", selection: $viewModel.tradeDirection) {
                ForEach(TradeDirection.allCases) { direction in
                    Text(direction.rawValue).tag(direction)
                }
            }
            .pickerStyle(SegmentedPickerStyle())
        }
        .padding()
        .background(Color(.secondarySystemGroupedBackground))
        .cornerRadius(12)
    }
    
    private var tradeDetailsSection: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("TRADE DETAILS")
                .font(.caption)
                .fontWeight(.bold)
                .foregroundColor(.secondary)
            
            InputField(title: "Entry Price", value: $viewModel.entryPrice, placeholder: "e.g. 45000", suffix: "USDT")
            
            InputField(title: "Exit Price", value: $viewModel.exitPrice, placeholder: "e.g. 50000", suffix: "USDT")
            
            InputField(title: "Position Size", value: $viewModel.positionSize, placeholder: "e.g. 1000", suffix: "USDT")
            
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
            
            InputField(title: "Trading Fee", value: $viewModel.tradingFee, placeholder: "e.g. 0.05", suffix: "%")
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
            Text("Calculate P&L")
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
            Text("TRADE RESULTS")
                .font(.caption)
                .fontWeight(.bold)
                .foregroundColor(.secondary)
            
            ResultCard(
                title: "Profit/Loss",
                value: String(format: "%.2f", viewModel.profitLoss),
                unit: "USDT",
                color: viewModel.profitLoss >= 0 ? .green : .red
            )
            
            HStack(spacing: 12) {
                ResultCardSmall(
                    title: "ROI",
                    value: String(format: "%.2f%%", viewModel.roi),
                    color: viewModel.roi >= 0 ? .green : .red
                )
                
                ResultCardSmall(
                    title: "ROE",
                    value: String(format: "%.2f%%", viewModel.roe),
                    color: viewModel.roe >= 0 ? .green : .red
                )
            }
            
            HStack(spacing: 12) {
                ResultCardSmall(
                    title: "Fees Paid",
                    value: String(format: "%.2f", viewModel.totalFees),
                    unit: "USDT",
                    color: .orange
                )
                
                ResultCardSmall(
                    title: "Net P&L",
                    value: String(format: "%.2f", viewModel.netProfitLoss),
                    unit: "USDT",
                    color: viewModel.netProfitLoss >= 0 ? .green : .red
                )
            }
        }
        .padding()
        .background(Color(.secondarySystemGroupedBackground))
        .cornerRadius(12)
    }
}

#Preview {
    PnLView()
}