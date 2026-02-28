"""
Eli5AI Demo
Generate a sample thread with mock data (no API keys needed).
"""

import sys
sys.path.insert(0, 'src')

from generate import ThreadGenerator
from visual import InfographicRenderer
from datetime import datetime


def mock_llm_client(prompt: str) -> str:
    """Simulate LLM response for demo."""
    # This is what Kimi would generate based on the style guide
    return """x402 Revival: The Internet's Native Payment System

The internet always had a payment code called HTTP 402, but it was never activated.

x402 finally activates it, turning the web into a programmable payment layer for both humans and AI agents.

Everything you need to know about x402 in 30s 🧵

— — —

► What is x402?

x402 is an open payment protocol by @coinbase that enables instant stablecoin payments over HTTP.

It activates the unused HTTP 402 Payment Required code, originally meant for online payments.

With x402, websites and AI agents can accept payments instantly without accounts.

Core features:

▸ Instant settlement: Payments confirm within seconds
▸ Zero protocol fees: No base-level charges  
▸ Blockchain-agnostic: Works across @base, @solana, and more
▸ One-line setup: Accept crypto payments with a single line of code

—

► How it Works

x402 works through standard HTTP requests.

❶ Request: A user requests a paid resource
❷ Response: Server returns HTTP 402 with payment details
❸ Payment: User sends $USDC through x402 facilitator
❹ Verification: Server verifies payment
❺ Access: Once confirmed, access is granted instantly

—

► Why It Matters

The internet never had a native payment system.

Developers depended on cards and subscriptions that were slow and expensive.

x402 enables real micropayments — pay per API call instead of monthly.

As AI agents transact independently, x402 becomes the foundation.

—

► Adoption (Last 30 Days)

▸ 43,000+ transactions
▸ $50,000+ total volume
▸ 300+ buyers
▸ 190+ sellers

—

► Ecosystem

➤ Client Integrations
▸ @heurist_ai
▸ @thirdweb

➤ Services
▸ @AEON_Community
▸ @pinatacloud
▸ @firecrawl_dev

➤ Infrastructure
▸ @CoinbaseDev
▸ @1shotapi

—

► Wrap-Up

x402 revives the forgotten HTTP 402 code, creating a native payment layer.

It enables instant, account-free USDC payments between websites and AI agents.

By combining web standards with on-chain settlement, x402 removes payment friction.

—

CC - @jessepollak | @brian_armstrong | @coinbase"""


def main():
    print("🤖 Eli5AI Demo")
    print("=" * 50)
    
    # Mock story data
    story_data = {
        'title': 'x402 Payment Protocol',
        'summary': 'x402 is an open payment protocol by Coinbase that activates the unused HTTP 402 status code for instant stablecoin payments.',
        'source': 'github',
        'url': 'https://github.com/coinbase/x402',
        'tags': ['crypto', 'payments', 'ai-agents', 'infrastructure'],
        'extra_context': '43K+ transactions, $50K volume in 30 days. Used by AI agents for autonomous payments.'
    }
    
    # Generate thread
    print("\n✍️  Generating thread...")
    generator = ThreadGenerator(model_client=mock_llm_client)
    thread = generator.generate(story_data)
    
    print(f"\n📝 Generated {len(thread.tweets)} tweets:\n")
    print(thread.to_string())
    
    # Generate infographic
    print("\n🎨 Rendering infographic...")
    visual = InfographicRenderer(output_dir="assets/infographics")
    
    # Use step flow template for this topic
    thread.infographic_spec['template'] = 'step_flow'
    
    html_path = visual.render(
        thread.infographic_spec,
        filename=f"demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    )
    
    print(f"\n✅ Infographic saved: {html_path}")
    print("\n💡 To convert HTML to PNG, install Playwright:")
    print("   pip install playwright && playwright install chromium")
    print("\n📋 Next steps:")
    print("   1. Add KIMI_API_KEY to config/config.json")
    print("   2. Add TYPEFULLY_API_KEY for publishing")
    print("   3. Run: python src/main.py --test")


if __name__ == "__main__":
    main()
