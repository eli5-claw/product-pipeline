//
//  PositionSizingViewModel.swift
//  LiquidCalc
//
//  ViewModel for position sizing calculations
//

import Foundation
import SwiftUI

class PositionSizingViewModel: ObservableObject {
    @Published var accountBalance: String = "10000"
    @Published var riskPercent: Double = 2
    @Published var entryPrice: String = ""
    @Published var stopLossPrice: String = ""
    @Published var leverage: Double = 10
    
    @Published var showResults = false
    @Published var positionSize: Double = 0
    @Published var marginRequired: Double = 0
    @Published var riskAmount: Double = 0
    
    var riskAmountComputed: Double {
        guard let balance = Double(accountBalance) else { return 0 }
        return balance * (riskPercent / 100)
    }
    
    func calculate() {
        guard let balance = Double(accountBalance),
              let entry = Double(entryPrice),
              let stopLoss = Double(stopLossPrice),
              balance > 0, entry > 0, stopLoss > 0 else {
            return
        }
        
        // Calculate risk amount
        riskAmount = balance * (riskPercent / 100)
        
        // Calculate stop loss distance as percentage
        let stopDistance = abs(entry - stopLoss) / entry
        
        guard stopDistance > 0 else { return }
        
        // Position Size = Risk Amount / Stop Distance
        positionSize = riskAmount / stopDistance
        
        // Margin Required = Position Size / Leverage
        marginRequired = positionSize / leverage
        
        showResults = true
    }
}
