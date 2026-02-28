//
//  ResultCard.swift
//  LiquidCalc
//
//  Reusable result card component
//

import SwiftUI

struct ResultCard: View {
    let title: String
    let value: String
    var unit: String = ""
    var color: Color = .primary
    
    var body: some View {
        VStack(spacing: 8) {
            Text(title)
                .font(.caption)
                .foregroundColor(.secondary)
            
            HStack(alignment: .firstTextBaseline, spacing: 4) {
                Text(value)
                    .font(.system(size: 36, weight: .bold, design: .rounded))
                    .foregroundColor(color)
                
                if !unit.isEmpty {
                    Text(unit)
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                }
            }
        }
        .frame(maxWidth: .infinity)
        .padding()
        .background(Color(.tertiarySystemGroupedBackground))
        .cornerRadius(12)
    }
}

struct ResultCardSmall: View {
    let title: String
    let value: String
    var unit: String = ""
    var color: Color = .primary
    
    var body: some View {
        VStack(spacing: 6) {
            Text(title)
                .font(.caption)
                .foregroundColor(.secondary)
            
            HStack(alignment: .firstTextBaseline, spacing: 2) {
                Text(value)
                    .font(.system(size: 20, weight: .bold, design: .rounded))
                    .foregroundColor(color)
                
                if !unit.isEmpty {
                    Text(unit)
                        .font(.caption2)
                        .foregroundColor(.secondary)
                }
            }
        }
        .frame(maxWidth: .infinity)
        .padding()
        .background(Color(.tertiarySystemGroupedBackground))
        .cornerRadius(12)
    }
}

#Preview {
    VStack {
        ResultCard(title: "Liquidation Price", value: "42,350.00", unit: "USDT", color: .red)
        HStack {
            ResultCardSmall(title: "Distance", value: "5.89%", color: .orange)
            ResultCardSmall(title: "Margin", value: "100.00", unit: "USDT", color: .blue)
        }
    }
    .padding()
}