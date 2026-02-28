//
//  PnLViewModel.swift
//  LiquidCalc
//
//  ViewModel for P&L calculations
//

import Foundation
import SwiftUI

enum TradeDirection: String, CaseIterable, Identifiable {
    case long = "Long"
    case short = "Short"
    
    var id: String { rawValue }
}

class PnLViewModel: ObservableObject {
    @Published var tradeDirection: TradeDirection = .long
    @Published var entryPrice: String = ""
    @Published var exitPrice: String = ""
    @Published var positionSize: String = ""
    @Published var leverage: Double = 10
    @Published var tradingFee: String = "0.05"
    
    @Published var showResults = false
    @Published var profitLoss: Double = 0
    @Published var roi: Double = 0
    @Published var roe: Double = 0
    @Published var totalFees: Double = 0
    @Published var netProfitLoss: Double = 0
    
    func calculate() {
        guard let entry = Double(entryPrice),
              let exit = Double(exitPrice),
              let size = Double(positionSize),
              let fee = Double(tradingFee),
              entry > 0, exit > 0, size > 0 else {
            return
        }
        
        let feeDecimal = fee / 100
        let margin = size / leverage
        
        // Calculate price change percentage
        var priceChangePercent: Double
        if tradeDirection == .long {
            priceChangePercent = (exit - entry) / entry
        } else {
            priceChangePercent = (entry - exit) / entry
        }
        
        // Gross P&L (with leverage)
        profitLoss = size * priceChangePercent
        
        // ROI (Return on Investment) - based on position size
        roi = priceChangePercent * 100 * leverage
        
        // ROE (Return on Equity) - based on margin used
        roe = (profitLoss / margin) * 100
        
        // Trading fees (entry + exit)
        totalFees = (size * feeDecimal) + (size * (1 + priceChangePercent) * feeDecimal)
        
        // Net P&L
        netProfitLoss = profitLoss - totalFees
        
        showResults = true
    }
}
