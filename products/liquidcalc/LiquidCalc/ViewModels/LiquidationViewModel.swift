//
//  LiquidationViewModel.swift
//  LiquidCalc
//
//  ViewModel for liquidation calculations
//

import Foundation
import SwiftUI

enum MarketType: String, CaseIterable, Identifiable {
    case isolated = "Isolated"
    case cross = "Cross"
    
    var id: String { rawValue }
}

enum PositionSide: String, CaseIterable, Identifiable {
    case long = "Long"
    case short = "Short"
    
    var id: String { rawValue }
}

class LiquidationViewModel: ObservableObject {
    @Published var marketType: MarketType = .isolated
    @Published var positionSide: PositionSide = .long
    @Published var entryPrice: String = ""
    @Published var positionSize: String = ""
    @Published var leverage: Double = 10
    @Published var maintenanceMarginRate: String = "0.5"
    
    @Published var showResults = false
    @Published var liquidationPrice: Double = 0
    @Published var distanceToLiquidation: Double = 0
    @Published var maintenanceMarginRequired: Double = 0
    
    func calculate() {
        guard let entry = Double(entryPrice),
              let size = Double(positionSize),
              let mmRate = Double(maintenanceMarginRate),
              entry > 0, size > 0 else {
            return
        }
        
        let mmRateDecimal = mmRate / 100
        let margin = size / leverage
        
        if marketType == .isolated {
            // Isolated margin liquidation formula
            if positionSide == .long {
                liquidationPrice = entry * (1 - 1/leverage + mmRateDecimal)
            } else {
                liquidationPrice = entry * (1 + 1/leverage - mmRateDecimal)
            }
        } else {
            // Cross margin (simplified - assumes no other positions)
            if positionSide == .long {
                liquidationPrice = entry * (1 - margin/size + mmRateDecimal)
            } else {
                liquidationPrice = entry * (1 + margin/size - mmRateDecimal)
            }
        }
        
        // Calculate distance to liquidation
        distanceToLiquidation = abs(entry - liquidationPrice) / entry * 100
        
        // Calculate maintenance margin required
        maintenanceMarginRequired = size * mmRateDecimal
        
        showResults = true
    }
}
