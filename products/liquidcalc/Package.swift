// swift-tools-version:5.7
import PackageDescription

let package = Package(
    name: "LiquidCalc",
    platforms: [
        .iOS(.v15)
    ],
    products: [
        .library(
            name: "LiquidCalc",
            targets: ["LiquidCalc"]
        )
    ],
    dependencies: [],
    targets: [
        .target(
            name: "LiquidCalc",
            dependencies: [],
            path: "LiquidCalc",
            exclude: ["Info.json"]
        )
    ]
)