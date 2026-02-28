//
//  InputField.swift
//  LiquidCalc
//
//  Reusable input field component
//

import SwiftUI

struct InputField: View {
    let title: String
    @Binding var value: String
    var placeholder: String = ""
    var suffix: String = ""
    var keyboardType: UIKeyboardType = .decimalPad
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(title)
                .font(.subheadline)
                .foregroundColor(.secondary)
            
            HStack {
                TextField(placeholder, text: $value)
                    .keyboardType(keyboardType)
                    .font(.body)
                
                if !suffix.isEmpty {
                    Text(suffix)
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }
            .padding()
            .background(Color(.tertiarySystemGroupedBackground))
            .cornerRadius(8)
        }
    }
}

#Preview {
    InputField(title: "Entry Price", value: .constant("45000"), placeholder: "e.g. 45000", suffix: "USDT")
        .padding()
}