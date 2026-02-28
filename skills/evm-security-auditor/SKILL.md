---
name: evm-security-auditor
description: Audit Ethereum smart contracts for security vulnerabilities using AI-powered detection, remediation, and testing. Use when reviewing Solidity code, assessing DeFi protocols, or hardening smart contracts. Triggers on requests for smart contract audit, EVM security, vulnerability detection, or Solidity code review.
---

# EVM Security Auditor

AI-powered smart contract security. Detect, fix, and test vulnerabilities.

## Overview

Smart contracts protect billions in assets. This skill helps you:
- **Detect** vulnerabilities before deployment
- **Fix** issues while preserving functionality
- **Test** exploit scenarios in safe environments

## Vulnerability Categories

### Critical (Immediate Fix Required)
| Vulnerability | Description |
|---------------|-------------|
| Reentrancy | External calls before state updates |
| Integer Overflow/Underflow | Arithmetic without SafeMath |
| Access Control | Missing ownership checks |
| Unchecked External Calls | Low-level call failures ignored |
| Delegatecall Injection | Malicious delegatecall targets |

### High Risk
| Vulnerability | Description |
|---------------|-------------|
| Front-running | MEV-exploitable transactions |
| Timestamp Dependence | Block.timestamp manipulation |
| Storage Collision | Proxy pattern issues |
| Signature Replay | Reusable signatures |
| Weak Randomness | Predictable random sources |

### Medium Risk
- Gas optimization issues
- Missing event emissions
- Incorrect inheritance order
- Floating pragma versions

## Audit Workflow

### 1. Static Analysis
```solidity
// Example: Detect reentrancy
function withdraw() external {
    uint256 amount = balances[msg.sender];
    (bool success, ) = msg.sender.call{value: amount}("");  // ⚠️ External call
    require(success);
    balances[msg.sender] = 0;  // ⚠️ State update after external call
}
```

### 2. Fix Implementation
```solidity
// Fixed: Checks-Effects-Interactions pattern
function withdraw() external {
    uint256 amount = balances[msg.sender];
    require(amount > 0, "No balance");
    balances[msg.sender] = 0;  // ✅ State update first
    (bool success, ) = msg.sender.call{value: amount}("");  // ✅ Then external call
    require(success, "Transfer failed");
}
```

### 3. Testing Exploits
```javascript
// Test reentrancy attack
it("should prevent reentrancy", async () => {
    const attacker = await ReentrancyAttacker.deploy(contract.address);
    await expect(attacker.attack()).to.be.reverted;
});
```

## Security Patterns

### Checks-Effects-Interactions
```solidity
function transfer(address to, uint256 amount) external {
    // 1. Checks
    require(balanceOf[msg.sender] >= amount, "Insufficient");
    
    // 2. Effects
    balanceOf[msg.sender] -= amount;
    balanceOf[to] += amount;
    
    // 3. Interactions (external calls last)
    emit Transfer(msg.sender, to, amount);
}
```

### Pull Over Push
```solidity
// ❌ Bad: Push payments
function distributeRewards() external {
    for (uint i = 0; i < users.length; i++) {
        users[i].transfer(rewards[i]);  // Can fail, block loop
    }
}

// ✅ Good: Pull payments
function claimReward() external {
    uint256 reward = pendingRewards[msg.sender];
    pendingRewards[msg.sender] = 0;
    payable(msg.sender).transfer(reward);
}
```

## Tools Integration

### Static Analysis
- **Slither** — Trail of Bits analyzer
- **Mythril** — Symbolic execution
- **Solhint** — Linter with security rules

### Testing
- **Foundry** — Fast fuzzing
- **Echidna** — Property-based testing
- **Certora** — Formal verification

### Monitoring
- **Tenderly** — Transaction simulation
- **Forta** — Real-time threat detection

## References

- [SWC Registry](references/swc-registry.md) — Smart contract weakness classification
- [DeFi Security](references/defi-security.md) — Protocol-specific patterns
- [Audit Checklist](references/audit-checklist.md) — Comprehensive review steps
