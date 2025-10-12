#!/usr/bin/env python3
"""
Analyze price distribution and premium pattern coverage.
Use this script after updating the dataset to understand
where high-value numbers concentrate.
"""

from collections import Counter
from pathlib import Path

import numpy as np

from src.data_handler import load_and_clean_data
from src.features import (
    PREMIUM_SUFFIX_WEIGHTS,
    get_high_digit_tail_ratio,
    HIGH_VALUE_DIGITS,
)


def summarize_price_bands(prices):
    bands = [
        (0, 500),
        (500, 1000),
        (1000, 5000),
        (5000, 10000),
        (10000, 20000),
        (20000, 50000),
        (50000, 100000),
    ]

    print("\n🎯 Price band summary")
    print("-" * 64)
    for low, high in bands:
        mask = (prices >= low) & (prices < high)
        count = int(mask.sum())
        pct = count / len(prices) * 100
        label = f"฿{low:,.0f} - ฿{high-1:,.0f}" if high != 100000 else f"≥ ฿{low:,.0f}"
        print(f"{label:<18} : {count:>5,d} numbers ({pct:5.1f}%)")


def summarize_premium_suffixes(numbers, prices):
    print("\n💎 Premium suffix coverage")
    print("-" * 64)
    suffix_hits = Counter()
    for number in numbers:
        for length in range(4, 1, -1):
            suffix = number[-length:]
            if suffix in PREMIUM_SUFFIX_WEIGHTS:
                suffix_hits[suffix] += 1
                break

    if not suffix_hits:
        print("No premium suffix patterns detected in current data.")
        return

    for suffix, count in suffix_hits.most_common(10):
        pct = count / len(numbers) * 100
        print(f"{suffix:<6} : {count:>5,d} numbers ({pct:5.2f}%)")


def summarize_high_digit_density(numbers, prices):
    ratios = np.array([get_high_digit_tail_ratio(num) for num in numbers])
    print("\n🔥 High digit tail density (7/8/9 in last 4 digits)")
    print("-" * 64)
    for threshold in [0.25, 0.5, 0.75, 1.0]:
        share = (ratios >= threshold).mean() * 100
        print(f"Tail ratio ≥ {threshold:0.2f} : {share:5.2f}% of numbers")

    premium_mask = prices >= 20000
    premium_ratios = ratios[premium_mask]
    if premium_ratios.size:
        print("\n   • Among prices ≥ ฿20,000")
        for threshold in [0.25, 0.5, 0.75, 1.0]:
            share = (premium_ratios >= threshold).mean() * 100
            print(f"     ratio ≥ {threshold:0.2f} : {share:5.2f}%")


def main():
    print("=" * 80)
    print("📊 PRICE & PATTERN DIAGNOSTICS")
    print("=" * 80)

    _, df_cleaned = load_and_clean_data(filter_outliers_param=True, max_price=100000)
    prices = df_cleaned["price"].values
    numbers = df_cleaned["phone_number"].astype(str).tolist()

    print(f"\nTotal cleaned samples: {len(df_cleaned):,}")
    print(f"Price range          : ฿{prices.min():,.0f} - ฿{prices.max():,.0f}")
    print(f"Median price         : ฿{np.median(prices):,.0f}")

    summarize_price_bands(prices)
    summarize_premium_suffixes(numbers, prices)
    summarize_high_digit_density(numbers, prices)

    print("\nLegend:")
    print(f" - Premium digits considered: {', '.join(sorted(HIGH_VALUE_DIGITS))}")
    print(" - Premium suffix weights sourced from PREMIUM_SUFFIX_WEIGHTS in src/features.py")
    print("\n✅ Diagnostics complete.\n")


if __name__ == "__main__":
    main()
