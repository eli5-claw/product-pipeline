# Build & Deploy

## Local Build
```bash
cd /root/.openclaw/workspace/products/liquidcalc
# Open in Xcode
open LiquidCalc.xcodeproj
```

## Archive for App Store
1. Product > Archive
2. Distribute App > App Store Connect
3. Upload

## Fastlane Setup (Optional)
```bash
fastlane init
fastlane deliver init
```

## App Store Connect API Key
Create API key for CI/CD deployment:
1. App Store Connect > Users and Access > Keys
2. Generate new key with App Manager role
3. Download private key
4. Store Key ID and Issuer ID