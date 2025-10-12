"""
Data Handler for ML Project - Load and Clean Data
By Alex - World-Class AI Expert
"""
import pandas as pd
import numpy as np
import os
import warnings
from collections import defaultdict
warnings.filterwarnings('ignore')

from src.config import CONFIG, DATA_PATH, BASE_PATH, ENV_TYPE, DATA_CONFIG
from src.features import PREMIUM_SUFFIX_WEIGHTS

# ====================================================================================
# HELPER FUNCTIONS
# ====================================================================================
def find_phone_column(df):
    """ค้นหาคอลัมน์เบอร์โทรศัพท์อัตโนมัติ"""
    possible_names = DATA_CONFIG['phone_column_names']
    
    for col in df.columns:
        if any(name in col.lower() for name in possible_names):
            print(f"✅ พบคอลัมน์เบอร์โทร: '{col}'")
            return col
    
    # ถ้าไม่เจอจากชื่อ ลองหาจาก pattern
    for col in df.columns:
        sample = df[col].astype(str).iloc[0]
        if len(sample) == 10 and sample.isdigit():
            print(f"✅ พบคอลัมน์เบอร์โทร (จาก pattern): '{col}'")
            return col
    
    raise ValueError("❌ ไม่พบคอลัมน์เบอร์โทรศัพท์!")

def find_price_column(df):
    """ค้นหาคอลัมน์ราคาอัตโนมัติ"""
    possible_names = DATA_CONFIG['price_column_names']
    
    for col in df.columns:
        if any(name in col.lower() for name in possible_names):
            print(f"✅ พบคอลัมน์ราคา: '{col}'")
            return col
    
    # ถ้าไม่เจอจากชื่อ ลองหาจากค่าที่เป็นตัวเลข
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) == 1:
        col = numeric_cols[0]
        print(f"✅ พบคอลัมน์ราคา (จากประเภทข้อมูล): '{col}'")
        return col
    
    raise ValueError("❌ ไม่พบคอลัมน์ราคา!")

def clean_phone_number(phone):
    """ทำความสะอาดเบอร์โทรศัพท์"""
    # แปลงเป็น string และลบช่องว่าง
    phone_str = str(phone).strip().replace(' ', '').replace('-', '')
    
    # ตรวจสอบและแปลงรูปแบบ
    if phone_str.startswith('+66'):
        phone_str = '0' + phone_str[3:]
    elif phone_str.startswith('66') and len(phone_str) == 11:
        phone_str = '0' + phone_str[2:]
    elif phone_str.startswith('0') and len(phone_str) == 10:
        pass  # ถูกต้องแล้ว
    elif len(phone_str) == 9:
        phone_str = '0' + phone_str
    
    # ตรวจสอบความถูกต้อง
    if len(phone_str) == 10 and phone_str.isdigit() and phone_str[0] == '0':
        return phone_str
    else:
        return None

# ====================================================================================
# MAIN DATA LOADING FUNCTION
# ====================================================================================
def load_and_clean_data(file_path=None, auto_clean=True, filter_outliers_param=True, max_price=100000):
    """
    โหลดและทำความสะอาดข้อมูลเบอร์โทรศัพท์

    Parameters:
    -----------
    file_path : str, optional
        Path to data file. If None, will look for files in data/raw/
    auto_clean : bool
        Whether to automatically clean the data
    filter_outliers_param : bool
        Whether to filter price outliers (≥100k)
    max_price : int
        Maximum price threshold for filtering (default: 100,000)

    Returns:
    --------
    df_raw : pd.DataFrame
        Raw data
    df_cleaned : pd.DataFrame
        Cleaned data
    """
    print("="*100)
    print("📂 LOADING AND CLEANING DATA")
    print("="*100)
    
    # Find data file if not specified
    if file_path is None:
        raw_data_path = os.path.join(DATA_PATH, 'raw')
        if os.path.exists(raw_data_path):
            csv_files = [f for f in os.listdir(raw_data_path) if f.endswith('.csv')]
            if csv_files:
                file_path = os.path.join(raw_data_path, csv_files[0])
                print(f"📁 Found data file: {file_path}")
            else:
                # Use centralized configuration from DATA_CONFIG
                default_files = DATA_CONFIG['default_filenames']
                search_paths = DATA_CONFIG['search_paths']

                # Search for data files
                for search_dir in search_paths:
                    if not os.path.exists(search_dir):
                        continue
                    for filename in default_files:
                        potential_path = os.path.join(search_dir, filename)
                        if os.path.exists(potential_path):
                            file_path = potential_path
                            print(f"📁 Auto-detected data file: {file_path}")
                            break
                    if file_path:
                        break
    
    if file_path is None or not os.path.exists(file_path):
        raise FileNotFoundError("❌ ไม่พบไฟล์ข้อมูล! กรุณาระบุ path ที่ถูกต้อง")
    
    # Load data
    print(f"\n📊 Loading data from: {file_path}")
    df_raw = pd.read_csv(file_path)
    print(f"✅ Loaded {len(df_raw):,} rows")
    
    # Auto detect columns
    phone_col = find_phone_column(df_raw)
    price_col = find_price_column(df_raw)
    
    # Rename columns for consistency
    df_raw = df_raw.rename(columns={
        phone_col: 'phone_number',
        price_col: 'price'
    })
    
    # Show sample
    print("\nตัวอย่างข้อมูลดิบ:")
    print(df_raw[['phone_number', 'price']].head())
    
    if not auto_clean:
        return df_raw, None
    
    # Clean data
    print("\n🧹 Cleaning data...")
    
    # Make a copy
    df_cleaned = df_raw.copy()
    
    # Clean phone numbers
    print("\n📱 Cleaning phone numbers...")
    df_cleaned['phone_number'] = df_cleaned['phone_number'].apply(clean_phone_number)
    
    # Remove invalid phone numbers
    initial_count = len(df_cleaned)
    df_cleaned = df_cleaned.dropna(subset=['phone_number'])
    removed_count = initial_count - len(df_cleaned)
    if removed_count > 0:
        print(f"   - ลบเบอร์ที่ไม่ถูกต้อง: {removed_count:,} เบอร์")
    
    # Clean prices
    print("\n💰 Cleaning prices...")
    df_cleaned['price'] = pd.to_numeric(df_cleaned['price'], errors='coerce')
    df_cleaned = df_cleaned.dropna(subset=['price'])
    
    # Remove outliers using domain knowledge
    print("\n📊 การกระจายราคาก่อนทำความสะอาด:")
    print(df_cleaned['price'].describe())
    
    # Calculate percentiles for outlier removal
    p01 = df_cleaned['price'].quantile(0.001)
    p99_9 = df_cleaned['price'].quantile(0.999)
    
    # Filter outliers
    initial_count = len(df_cleaned)
    df_cleaned = df_cleaned[
        (df_cleaned['price'] >= max(50, p01)) &
        (df_cleaned['price'] <= min(10_000_000, p99_9 * 1.5))
    ].copy()
    
    outliers_removed = initial_count - len(df_cleaned)
    print(f"\n🔧 Removed {outliers_removed:,} outliers")
    print(f"   - Price range: ฿{df_cleaned['price'].min():,.0f} - ฿{df_cleaned['price'].max():,.0f}")
    
    # Show distribution
    print("\n💎 การกระจายเบอร์ตามระดับราคา:")
    price_ranges = [
        (100, 1000), (1000, 10000), (10000, 50000),
        (50000, 100000), (100000, 500000), (500000, float('inf'))
    ]
    
    for low, high in price_ranges:
        if high == float('inf'):
            count = len(df_cleaned[df_cleaned['price'] >= low])
            print(f"   - ราคา ≥ ฿{low:,}: {count:,} เบอร์")
        else:
            count = len(df_cleaned[(df_cleaned['price'] >= low) & (df_cleaned['price'] < high)])
            print(f"   - ราคา ฿{low:,} - ฿{high:,}: {count:,} เบอร์")
    
    # Remove duplicates
    initial_count = len(df_cleaned)
    df_cleaned = df_cleaned.drop_duplicates(subset=['phone_number'])
    duplicates_removed = initial_count - len(df_cleaned)
    if duplicates_removed > 0:
        print(f"\n🔄 Removed {duplicates_removed:,} duplicate phone numbers")
    
    # Final summary
    print("\n📊 สรุปการทำความสะอาดข้อมูล:")
    print(f"   - ข้อมูลดิบ: {len(df_raw):,} แถว")
    print(f"   - ข้อมูลสะอาด: {len(df_cleaned):,} แถว")
    print(f"   - คงเหลือ: {len(df_cleaned)/len(df_raw)*100:.1f}%")
    
    # Reset index
    df_cleaned = df_cleaned.reset_index(drop=True)

    # Filter outliers if requested (NEW - Session 012)
    if filter_outliers_param:
        from src.data_filter import filter_outliers
        df_cleaned = filter_outliers(df_cleaned, max_price=max_price, verbose=True)

    # Save cleaned data
    cleaned_path = os.path.join(DATA_PATH, 'processed', 'cleaned_data.csv')
    os.makedirs(os.path.dirname(cleaned_path), exist_ok=True)
    df_cleaned.to_csv(cleaned_path, index=False)
    print(f"\n💾 Saved cleaned data to: {cleaned_path}")

    print("\n✅ Data loading and cleaning completed!")
    print("="*100)

    return df_raw, df_cleaned

# ====================================================================================
# ADDITIONAL DATA UTILITIES
# ====================================================================================
def get_data_info(df):
    """Get detailed information about the dataset"""
    info = {
        'shape': df.shape,
        'columns': list(df.columns),
        'dtypes': df.dtypes.to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'duplicates': df.duplicated().sum(),
        'memory_usage': df.memory_usage(deep=True).sum() / 1024**2  # MB
    }
    
    if 'price' in df.columns:
        info['price_stats'] = {
            'min': df['price'].min(),
            'max': df['price'].max(),
            'mean': df['price'].mean(),
            'median': df['price'].median(),
            'std': df['price'].std()
        }
    
    return info

def validate_phone_numbers(df, phone_col='phone_number'):
    """Validate phone numbers in dataframe"""
    invalid_phones = []
    
    for idx, phone in df[phone_col].items():
        if pd.isna(phone):
            invalid_phones.append((idx, phone, "Missing value"))
        elif not str(phone).startswith('0'):
            invalid_phones.append((idx, phone, "Doesn't start with 0"))
        elif len(str(phone)) != 10:
            invalid_phones.append((idx, phone, f"Invalid length: {len(str(phone))}"))
        elif not str(phone).isdigit():
            invalid_phones.append((idx, phone, "Contains non-numeric characters"))
    
    if invalid_phones:
        print(f"⚠️ Found {len(invalid_phones)} invalid phone numbers")
        return pd.DataFrame(invalid_phones, columns=['index', 'phone_number', 'issue'])
    else:
        print("✅ All phone numbers are valid")
        return None

def create_price_bins(df, price_col='price', n_bins=10):
    """Create price bins for stratification"""
    df['price_bin'] = pd.qcut(df[price_col], q=n_bins, labels=False, duplicates='drop')
    df['price_category'] = pd.qcut(
        df[price_col], 
        q=[0, 0.25, 0.5, 0.75, 0.9, 1.0],
        labels=['low', 'medium-low', 'medium', 'medium-high', 'high']
    )
    return df

# ====================================================================================
# NEW FUNCTIONS FOR DATA LEAKAGE FIX
# ====================================================================================

def calculate_sample_weights(df, is_train=True):
    """
    Calculate sample weights for training data only
    
    Parameters:
    -----------
    df : DataFrame with 'price' column
    is_train : bool, if False returns weight=1 for all
    
    Returns:
    --------
    df : DataFrame with added 'sample_weight' column
    """
    df = df.copy()
    
    if not is_train:
        df['sample_weight'] = 1.0
        return df
    
    print("⚖️ Calculating sample weights from TRAINING data...")
    
    prices = df['price'].clip(lower=100)
    price_log = np.log1p(prices)
    log_scaled = (price_log - price_log.min()) / (price_log.max() - price_log.min() + 1e-9)

    # Base weighting grows smoothly with log price (focus on upper tail)
    base_weight = 0.6 + 1.7 * np.power(log_scaled, 1.25)

    # Tier boosts for premium ranges
    tier_boost = np.select(
        [
            prices >= 50000,
            prices >= 20000,
            prices >= 10000,
            prices >= 5000
        ],
        [2.0, 1.2, 0.8, 0.4],
        default=0.0
    )

    # Slight penalty for very low prices to balance the distribution
    low_price_penalty = np.where(prices < 800, 0.25, 0.0)

    sample_weights = base_weight + tier_boost + low_price_penalty

    # Normalize and guard against extremely small weights
    sample_weights = np.clip(sample_weights, 0.3, None)
    sample_weights = sample_weights / sample_weights.mean()

    df['sample_weight'] = sample_weights
    print(f"✅ Sample weights calculated for {len(df)} samples")
    return df

def calculate_market_statistics(train_df):
    """
    Calculate market statistics from TRAINING data only
    
    Parameters:
    -----------
    train_df : DataFrame with 'phone_number' and 'price' columns
    
    Returns:
    --------
    dict : Market statistics for use in feature engineering
    """
    print("📊 Calculating market statistics from TRAINING data...")
    
    pattern_prices = {}
    premium_suffix_prices = defaultdict(list)
    
    for idx, row in train_df.iterrows():
        phone = str(row['phone_number'])
        price = row['price']
        
        # Ending patterns
        for length in [3, 4]:
            if len(phone) >= length:
                pattern = phone[-length:]
                if pattern not in pattern_prices:
                    pattern_prices[pattern] = []
                pattern_prices[pattern].append(price)
                if pattern in PREMIUM_SUFFIX_WEIGHTS:
                    premium_suffix_prices[pattern].append(price)
        
        # ABC pattern
        if len(phone) >= 6:
            abc = phone[3:6]
            if abc not in pattern_prices:
                pattern_prices[abc] = []
            pattern_prices[abc].append(price)
    
    # Calculate averages and popularity
    pattern_avg_prices = {}
    pattern_popularity = {}
    
    for pattern, prices in pattern_prices.items():
        if len(prices) >= 2:
            pattern_avg_prices[pattern] = np.median(prices)
            pattern_popularity[pattern] = len(prices)
    
    print(f"✅ Market statistics calculated from {len(train_df)} training samples")

    premium_suffix_stats = {
        suffix: float(np.median(prices))
        for suffix, prices in premium_suffix_prices.items()
        if len(prices) >= 2
    }

    return {
        'avg_prices': pattern_avg_prices,
        'popularity': pattern_popularity,
        'n_train_samples': len(train_df),
        'premium_suffix_stats': premium_suffix_stats,
        'global_median': float(train_df['price'].median()),
        'global_mean': float(train_df['price'].mean())
    }
