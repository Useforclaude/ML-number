"""
Data Filter Module - Remove Outliers and Clean Data
Filter out unrealistic price outliers while keeping valuable data
"""

import pandas as pd
import numpy as np


def filter_outliers(df, max_price=100000, verbose=True):
    """
    ตัด outliers ราคาสูงเกินจริง (≥100k)
    เก็บราคาต่ำไว้ทั้งหมด เพื่อเรียนรู้ pattern ที่ทำให้ราคาถูก

    Why keep low prices (<1000):
    - เลขไม่สวย: มี 22, 04, 07 (เลขซวย)
    - Pattern ไม่ดี: ซ้ำกัน, ไม่เรียง
    - โมเดลต้องเรียนรู้ว่า pattern ไหนทำให้ราคาถูก

    Why remove high prices (≥100k):
    - ไม่ค่อยมีเบอร์แบบนี้ในตลาดจริง
    - Outliers มหาศาล (10M, 6.5M) ทำให้โมเดลงง

    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe with 'price' column
    max_price : int
        Maximum price threshold (default: 100,000)
    verbose : bool
        Print filtering statistics

    Returns:
    --------
    filtered_df : pd.DataFrame
        Filtered dataframe
    """
    original_count = len(df)

    if verbose:
        print("\n" + "="*80)
        print("✂️  FILTERING OUTLIERS")
        print("="*80)
        print(f"📊 Original data: {original_count} samples")
        print(f"   Price range: ฿{df['price'].min():,.0f} - ฿{df['price'].max():,.0f}")
        print(f"   Median: ฿{df['price'].median():,.0f}")

    # Filter out prices >= max_price
    filtered = df[df['price'] < max_price].copy()
    removed = original_count - len(filtered)

    if verbose:
        print(f"\n✂️  Removed {removed} outliers (≥฿{max_price:,})")
        print(f"   Percentage removed: {removed/original_count*100:.1f}%")

        # Show what was removed
        if removed > 0:
            removed_df = df[df['price'] >= max_price]
            print(f"\n🗑️  Outliers removed:")
            print(f"   Price range: ฿{removed_df['price'].min():,.0f} - ฿{removed_df['price'].max():,.0f}")
            if removed <= 10:
                print(f"\n   Top outliers:")
                for idx, row in removed_df.nlargest(min(5, removed), 'price').iterrows():
                    if 'phone_number' in row:
                        print(f"      {row['phone_number']}: ฿{row['price']:,.0f}")

        print(f"\n✅ Filtered data: {len(filtered)} samples")
        print(f"   Percentage kept: {len(filtered)/original_count*100:.1f}%")
        print(f"   Price range: ฿{filtered['price'].min():,.0f} - ฿{filtered['price'].max():,.0f}")
        print(f"   Median: ฿{filtered['price'].median():,.0f}")

        # Show distribution
        print(f"\n📊 Price distribution (filtered):")
        bins = [0, 1000, 10000, 100000]
        labels = ['< ฿1k', '฿1k-10k', '฿10k-100k']
        for i, label in enumerate(labels):
            count = len(filtered[(filtered['price'] >= bins[i]) & (filtered['price'] < bins[i+1])])
            pct = count / len(filtered) * 100
            print(f"   {label:12s}: {count:5d} samples ({pct:5.1f}%)")

        print("="*80)

    return filtered


def filter_price_range(df, min_price=None, max_price=None, verbose=True):
    """
    Filter data to specific price range

    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe with 'price' column
    min_price : int, optional
        Minimum price threshold
    max_price : int, optional
        Maximum price threshold
    verbose : bool
        Print filtering statistics

    Returns:
    --------
    filtered_df : pd.DataFrame
        Filtered dataframe
    """
    original_count = len(df)
    filtered = df.copy()

    if verbose:
        print("\n" + "="*80)
        print("✂️  FILTERING PRICE RANGE")
        print("="*80)
        print(f"📊 Original data: {original_count} samples")

    if min_price is not None:
        filtered = filtered[filtered['price'] >= min_price]
        if verbose:
            removed = original_count - len(filtered)
            print(f"   Removed {removed} samples < ฿{min_price:,}")

    if max_price is not None:
        before_count = len(filtered)
        filtered = filtered[filtered['price'] < max_price]
        removed = before_count - len(filtered)
        if verbose:
            print(f"   Removed {removed} samples ≥ ฿{max_price:,}")

    if verbose:
        print(f"\n✅ Filtered data: {len(filtered)} samples ({len(filtered)/original_count*100:.1f}%)")
        print(f"   Price range: ฿{filtered['price'].min():,.0f} - ฿{filtered['price'].max():,.0f}")
        print("="*80)

    return filtered


def analyze_outliers(df, threshold=100000):
    """
    Analyze outliers without filtering

    Parameters:
    -----------
    df : pd.DataFrame
        Dataframe with 'price' column
    threshold : int
        Price threshold to analyze

    Returns:
    --------
    stats : dict
        Outlier statistics
    """
    total = len(df)
    outliers = df[df['price'] >= threshold]
    normal = df[df['price'] < threshold]

    stats = {
        'total_samples': total,
        'outliers_count': len(outliers),
        'outliers_percentage': len(outliers) / total * 100,
        'normal_count': len(normal),
        'normal_percentage': len(normal) / total * 100,
        'outliers_price_range': (outliers['price'].min(), outliers['price'].max()) if len(outliers) > 0 else (None, None),
        'normal_price_range': (normal['price'].min(), normal['price'].max()) if len(normal) > 0 else (None, None),
        'outliers_median': outliers['price'].median() if len(outliers) > 0 else None,
        'normal_median': normal['price'].median() if len(normal) > 0 else None
    }

    print("\n" + "="*80)
    print(f"📊 OUTLIER ANALYSIS (threshold: ฿{threshold:,})")
    print("="*80)
    print(f"\nTotal samples: {total}")
    print(f"\n✅ Normal (< ฿{threshold:,}):")
    print(f"   Count: {stats['normal_count']} ({stats['normal_percentage']:.1f}%)")
    if stats['normal_price_range'][0] is not None:
        print(f"   Range: ฿{stats['normal_price_range'][0]:,.0f} - ฿{stats['normal_price_range'][1]:,.0f}")
        print(f"   Median: ฿{stats['normal_median']:,.0f}")

    print(f"\n⚠️  Outliers (≥ ฿{threshold:,}):")
    print(f"   Count: {stats['outliers_count']} ({stats['outliers_percentage']:.1f}%)")
    if stats['outliers_price_range'][0] is not None:
        print(f"   Range: ฿{stats['outliers_price_range'][0]:,.0f} - ฿{stats['outliers_price_range'][1]:,.0f}")
        print(f"   Median: ฿{stats['outliers_median']:,.0f}")

    print("="*80)

    return stats


# Example usage
if __name__ == "__main__":
    # Test with sample data
    import pandas as pd

    # Load data
    df = pd.read_csv('../data/raw/numberdata.csv')

    # Analyze outliers
    stats = analyze_outliers(df, threshold=100000)

    # Filter outliers
    df_filtered = filter_outliers(df, max_price=100000)

    print(f"\n✅ Test complete!")
    print(f"   Original: {len(df)} samples")
    print(f"   Filtered: {len(df_filtered)} samples")
    print(f"   Removed: {len(df) - len(df_filtered)} outliers")
