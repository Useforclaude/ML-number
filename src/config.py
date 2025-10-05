"""
Configuration settings for ML Project
By Alex - World-Class AI Expert
Complete version with all configurations from original code

UPDATED: Now uses dynamic environment detection - no more hardcoded paths!
"""
import os
import sys
from pathlib import Path

# Import environment detector
try:
    from src.environment import get_config_for_environment
    env_config = get_config_for_environment()
    BASE_PATH = str(env_config['BASE_PATH'])
    DATA_PATH = str(env_config['DATA_PATH'])
    MODEL_PATH = str(env_config['MODEL_PATH'])
    RESULTS_PATH = str(env_config['RESULTS_PATH'])
    LOGS_PATH = str(env_config.get('LOGS_PATH', os.path.join(BASE_PATH, 'logs')))
    ENV_TYPE = env_config['ENV_TYPE']
except ImportError:
    # Fallback: Auto-detect without environment module
    if 'PAPERSPACE_NOTEBOOK_REPO_ID' in os.environ or \
       'PAPERSPACE_API_KEY' in os.environ or \
       os.path.exists('/storage'):
        # Paperspace Gradient
        BASE_PATH = '/storage/number-ML'
    elif 'KAGGLE_KERNEL_RUN_TYPE' in os.environ or os.path.exists('/kaggle'):
        # Kaggle
        BASE_PATH = '/kaggle/working'
    elif os.path.exists('/content'):
        # Google Colab
        gdrive = Path('/content/drive/MyDrive/number-ML')
        BASE_PATH = str(gdrive) if gdrive.exists() else '/content/number-ML'
    else:
        # Local - find project root
        current = Path(__file__).parent.parent
        BASE_PATH = str(current)

    DATA_PATH = os.path.join(BASE_PATH, 'data')
    MODEL_PATH = os.path.join(BASE_PATH, 'models')
    RESULTS_PATH = os.path.join(BASE_PATH, 'results')
    LOGS_PATH = os.path.join(BASE_PATH, 'logs')
    ENV_TYPE = 'auto-detected'

# ====================================================================================
# PROJECT PATHS (Dynamic - Auto-configured for Local/Colab/Kaggle/Paperspace)
# ====================================================================================

# Platform-specific notes:
# - Local: Uses project root directory
# - Colab: /content/drive/MyDrive/number-ML (if Drive mounted) or /content/number-ML
# - Kaggle: /kaggle/working (NOT persistent - deleted after session)
# - Paperspace: /storage/number-ML (persistent across restarts) ✅

# ====================================================================================
# DATA LOADING CONFIGURATION
# ====================================================================================
DATA_CONFIG = {
    # Default data filenames to search for (in order of preference)
    'default_filenames': [
        'numberdata.csv',
        'combined_data_v4.csv',
        'numberdata25062025.csv',
        'phone_prices.csv',
        'phone_numbers.csv'
    ],

    # Supported file formats
    'supported_formats': ['csv', 'txt', 'xlsx', 'xls', 'json'],

    # Column name mappings (auto-detect)
    'phone_column_names': [
        'phone', 'phone_number', 'number', 'mobile', 'tel',
        'telephone', 'msisdn', 'หมายเลข', 'เบอร์', 'เบอร์โทร'
    ],

    'price_column_names': [
        'price', 'ราคา', 'value', 'cost', 'amount', 'fee', 'selling_price'
    ],

    # Data validation settings
    'phone_min_length': 10,
    'phone_max_length': 10,
    'price_min': 0,
    'price_max': 10000000,

    # Environment-specific search paths (will be populated dynamically)
    'search_paths': []
}

# Populate search paths based on environment
_search_paths = [
    os.path.join(BASE_PATH, 'data', 'raw'),
    os.path.join(BASE_PATH, 'data'),
    BASE_PATH
]

if ENV_TYPE == 'colab':
    _search_paths.extend([
        '/content/drive/MyDrive/data',
        '/content/drive/MyDrive/number-ML/data/raw',
        '/content/drive/MyDrive/number-ML/data',
        '/content'
    ])
elif ENV_TYPE == 'kaggle':
    _search_paths.extend([
        '/kaggle/input/phone-price-data',
        '/kaggle/input/numberdata',
        '/kaggle/input',
        '/kaggle/working/data/raw',
        '/kaggle/working/data'
    ])

DATA_CONFIG['search_paths'] = _search_paths

# ====================================================================================
# BATCH PREDICTION CONFIGURATION
# ====================================================================================
BATCH_CONFIG = {
    'batch_size': 1000,
    'show_progress': True,
    'export_formats': ['csv', 'xlsx', 'json'],
    'default_export_format': 'csv',
    'include_confidence': True,
    'include_features': False,
    'parallel_processing': True,
    'n_workers': -1
}

# ====================================================================================
# API CONFIGURATION
# ====================================================================================
API_CONFIG = {
    'type': 'fastapi',  # or 'flask'
    'host': '0.0.0.0',
    'port': 8000,
    'debug': False,
    'enable_cors': True,
    'max_batch_size': 10000,
    'timeout': 300,
    'cache_predictions': True,
    'cache_ttl': 3600
}

# ====================================================================================
# LOGGING CONFIGURATION
# ====================================================================================
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file_format': 'json',
    'log_to_file': True,
    'log_to_console': True,
    'log_dir': LOGS_PATH,
    'max_file_size': 10485760,  # 10 MB
    'backup_count': 5
}

# ====================================================================================
# FEATURE ENGINEERING CONFIGURATION
# ====================================================================================
CONFIG = {
    # เลขมงคล
    'GOOD_DIGITS': {'1', '3', '4', '5', '6', '8', '9'},
    
    # น้ำหนักเลขแต่ละตัว (ปรับปรุงใหม่)
    'POWER_WEIGHTS': {
        '5': 10, '9': 8, '8': 6, '6': 8, '3': 4, 
        '4': 6, '1': 5, '7': -2, '0': -5, '2': -1
    },
    
    # คู่เลขมงคลยอดนิยม
    'PREMIUM_PAIRS': [
        '45', '54', '59', '95', '15', '51', '14', '41', '98', '89', 
        '78', '87', '88', '66', '99', '65', '56', '24', '42', '35', 
        '53', '63', '36'
    ],
    
    # คู่เลขมงคลพิเศษ + ความหมาย
    'SPECIAL_LUCKY_PAIRS': {
        '15': {'score': 10, 'meaning': 'มิตรภาพ, สติปัญญา, การเจรจา'},
        '51': {'score': 10, 'meaning': 'มิตรภาพ, สติปัญญา, การเจรจา'},
        '24': {'score': 8, 'meaning': 'การเงินคล่องตัว, โอกาส'},
        '42': {'score': 8, 'meaning': 'การเงินคล่องตัว, โอกาส'},
        '36': {'score': 9, 'meaning': 'เสน่ห์, ความรัก, สุขภาพ'},
        '63': {'score': 9, 'meaning': 'เสน่ห์, ความรัก, สุขภาพ'},
        '45': {'score': 12, 'meaning': 'ผู้ใหญ่เมตตา, โชคลาภ'},
        '54': {'score': 12, 'meaning': 'ผู้ใหญ่เมตตา, โชคลาภ'},
        '56': {'score': 15, 'meaning': 'ความรัก, ความสุข, การเงิน'},
        '65': {'score': 15, 'meaning': 'ความรัก, ความสุข, การเงิน'},
        '69': {'score': 10, 'meaning': 'มีกินมีใช้, โชคลาภ'},
        '96': {'score': 10, 'meaning': 'มีกินมีใช้, โชคลาภ'},
        '78': {'score': 12, 'meaning': 'โชคลาภ, การลงทุน'},
        '87': {'score': 12, 'meaning': 'โชคลาภ, การลงทุน'},
        '28': {'score': 8, 'meaning': 'การเงิน, โชคลาภ'},
        '82': {'score': 8, 'meaning': 'การเงิน, โชคลาภ'},
        '38': {'score': 7, 'meaning': 'การเสี่ยงโชค, การลงทุน'},
        '83': {'score': 7, 'meaning': 'การเสี่ยงโชค, การลงทุน'},
        '19': {'score': 9, 'meaning': 'ชื่อเสียง, การเงิน'},
        '91': {'score': 9, 'meaning': 'ชื่อเสียง, การเงิน'},
        '89': {'score': 11, 'meaning': 'โชคลาภ, การเงิน'},
        '98': {'score': 11, 'meaning': 'โชคลาภ, การเงิน'},
        '14': {'score': 10, 'meaning': 'ผู้ใหญ่เมตตา'},
        '41': {'score': 10, 'meaning': 'ผู้ใหญ่เมตตา'},
        '59': {'score': 13, 'meaning': 'โชคลาภ'},
        '95': {'score': 13, 'meaning': 'โชคลาภ'},
        '88': {'score': 14, 'meaning': 'เลขเบิ้ลมงคล'},
        '99': {'score': 16, 'meaning': 'เลขเบิ้ลมงคล'},
        '66': {'score': 12, 'meaning': 'เลขเบิ้ลมงคล'},
        '55': {'score': 14, 'meaning': 'เลขเบิ้ลมงคล'},
        '32': {'score': -5, 'meaning': 'เลขไม่ดี'},
        '23': {'score': -5, 'meaning': 'เลขไม่ดี'},
        '35': {'score': 9, 'meaning': 'ความสำเร็จ'},
        '53': {'score': 9, 'meaning': 'ความสำเร็จ'}
    },
    
    # เลขเรียงต่อเนื่อง
    'CONSECUTIVE_SEQUENCES': ['123', '234', '345', '456', '567', '678', '789'],
    
    # เลขเบิ้ล/เลขตอง/เลขโฟร์ พร้อมคะแนน
    'DOUBLE_SCORES': {
        '00': 2, '11': 6, '22': 3, '33': 5, '44': 6,
        '55': 10, '66': 9, '77': 4, '88': 12, '99': 14
    },
    
    'TRIPLE_SCORES': {
        '000': 3, '111': 8, '222': 4, '333': 7, '444': 8,
        '555': 15, '666': 12, '777': 6, '888': 20, '999': 20
    },
    
    'QUAD_SCORES': {
        '0000': 5, '1111': 15, '2222': 6, '3333': 10, '4444': 12,
        '5555': 20, '6666': 18, '7777': 14, '8888': 30, '9999': 30
    },
    
    # ผลรวมมงคล พร้อมคะแนนถ่วงน้ำหนัก
    'SUM_SCORES': {
        # ผลรวมดี (เรียงตามความนิยม)
        55: 20, 65: 18, 59: 23, 45: 30, 54: 25, 56: 19,
        41: 15, 36: 10, 42: 10, 51: 15, 46: 8, 47: 5,
        # ผลรวมปกติ
        30: 5, 31: 5, 32: 4, 33: 4, 34: 4, 35: 6,
        37: 5, 38: 5, 39: 6, 40: 5, 43: 5, 44: 6,
        48: 6, 49: 7, 50: 7, 52: 7, 53: 7, 57: 7,
        58: 8, 60: 6, 61: 6, 62: 6, 63: 7, 64: 7
    },
    
    # เบอร์พิเศษชื่อดัง
    'FAMOUS_SEQUENCES': {
        '007': 20, '911': 15, '888': 80, '999': 100,
        '555': 50, '168': 25, '1688': 35, '8888': 150,
        '9999': 200, '5555': 100, '6666': 120,
        '1357': 30, '2468': 25, '1248': 22,
        '369': 18, '147': 15, '258': 13,
        '159': 20, '753': 18, '246': 12,
        '135': 15, '579': 22, '468': 18,
        '789': 30,   # เบอร์มังกร
        '289': 15,   # เบอร์หงส์
        '639': 24,   # เบอร์พิเศษ
        '519': 16,   # เบอร์พิเศษ
        '919': 14,   # เบอร์พิเศษ
        '4289': 25,  # ชุดพิเศษ
        '6395': 30,  # ชุดพิเศษ
        '7895': 30,  # ชุดพิเศษ
        '915': 15,   # เบอร์พิเศษ
    },
    
    # เลขท้ายพิเศษ
    'ENDING_PREMIUM': {
        '9999': 200, '8888': 150, '6666': 120, '5555': 100,
        '999': 100, '888': 80, '666': 60, '555': 50,
        '99': 40, '88': 30, '66': 20, '55': 15,
        '89': 25, '98': 25, '56': 20, '65': 20,
        '789': 45, '456': 40, '123': 35, '678': 35,
        '5678': 60, '6789': 65, '4567': 55, '3456': 50,
        '1234': 45, '2345': 40,
        '456': 25, '789': 30, '639': 25, '6395': 35, '63915': 40,
        '6365': 35, '6595': 25, '6515': 25, '5195': 25, '5915': 25,
        '4159': 20, '4156': 25, '4165': 20, '2456': 30, '2465': 25,
        '4265': 25, '4256': 20, '1456': 30, '1465': 25, '1965': 22,
        '1956': 25, '3656': 30, '6356': 25, '3665': 20, '9156': 25,
        '63965': 40, '6465': 20, '465': 20, '956': 25, '965': 20,
        '5456': 30, '4556': 22, '5156': 25, '6456': 20, '9456': 25
    },
    
    # ตำแหน่ง ABC พิเศษ (ตำแหน่ง 3-5)
    'ABC_PREMIUM': {
        '789': 100,  # มังกร
        '289': 45,   # หงส์
        '639': 65,   # พิเศษ
        '519': 30,   # พิเศษ
        '919': 25,   # พิเศษ
        '888': 30,   # ตองพิเศษ
        '999': 35,   # ตองพิเศษ
        '666': 25,   # ตองพิเศษ
        '555': 28,   # ตองพิเศษ
        '456': 50,   # เรียง
        '567': 30,   # เรียง
        '678': 30,   # เรียง
    },
    
    # คู่เลขไม่ดี
    'NEGATIVE_PAIRS': [
        '10', '01', '12', '21', '13', '31', '17', '71', '18', '81',
        '20', '02', '27', '72', '30', '03', '34', '43', '37', '73',
        '38', '83', '48', '84', '67', '76', '68', '86', '70', '07',
        '80', '08', '32', '23'
    ],
    
    # ตัวเลขไม่ดี
    'BAD_DIGITS': {'0', '2', '7'},
    
    # การให้คะแนนความซับซ้อน
    'COMPLEXITY_SCORES': {
        'very_simple': -2,
        'simple': 0,
        'moderate': 2,
        'complex': 5,
        'very_complex': 10
    },
    
    # เลขคู่มงคลลึกลับ
    'MYSTICAL_PAIRS': {
        '13': -10, '31': -8, '17': -5, '71': -5,
        '04': -8, '40': -8, '20': -6, '02': -6,
        '27': -7, '72': -7, '70': -9, '07': -9,
        '08': -3, '80': -3, '48': -4, '84': -4,
        '21': -3, '12': -3, '37': -5, '73': -5,
        '29': -4, '92': -4, '18': 5, '81': 5,
        '16': 6, '61': 6, '22': -8, '77': -10,
        '00': -15, '44': 8, '33': -5, '11': 3
    },
    
    # คู่เลขห้าม (ลดคะแนนมาก)
    'FORBIDDEN_PAIRS': ['00', '04', '40', '13', '17', '44', '70', '22'],
    
    # เลขมงคลต่อเนื่อง
    'LUCKY_SEQUENCES': {
        '111': 30, '222': -20, '333': 25, '444': 40,
        '555': 50, '666': 60, '777': -30, '888': 80,
        '999': 100, '000': -50,
        '123': 35, '234': 30, '345': 30, '456': 40,
        '567': 45, '678': 50, '789': 55, '890': 25,
        '321': 20, '432': 15, '543': 15, '654': 20,
        '765': 25, '876': 30, '987': 35, '098': 10,
        '1234': 45, '2345': 40, '3456': 50, '4567': 55,
        '5678': 60, '6789': 65, '7890': 30,
        '4321': 25, '5432': 20, '6543': 25, '7654': 30,
        '8765': 35, '9876': 40, '0987': 15
    },
    
    # เลขซ้ำ (Pattern Repeating)
    'REPEATING_PATTERNS': {
        'AA': 10, 'AAA': 25, 'AAAA': 50,
        'ABAB': 20, 'ABCABC': 30,
        'AABB': 15, 'AAABBB': 35,
        'ABBA': 18, 'ABCCBA': 28
    },
    
    # Market-based pricing factors
    'MARKET_TIERS': {
        'ultra_premium': {'min': 100000, 'multiplier': 2.5},
        'premium': {'min': 50000, 'multiplier': 2.0},
        'high': {'min': 20000, 'multiplier': 1.5},
        'medium': {'min': 5000, 'multiplier': 1.2},
        'low': {'min': 0, 'multiplier': 1.0}
    }
}

# ====================================================================================
# MODEL CONFIGURATION - IMPROVED FOR R² > 0.90
# ====================================================================================
MODEL_CONFIG = {
    'target_r2': 0.90,
    'cv_folds': 10,
    'test_size': 0.20,
    'random_state': 42,
    'n_jobs': -1,
    'early_stopping_rounds': 100,
    'optuna_trials': 150,  # 🔥 เพิ่มจาก 50
    'feature_selection_method': 'hybrid',
    'max_features': 250,  # 🔥 เพิ่มจาก 150
    'feature_selection_ratio': 0.85,  # 🔥 เพิ่มจาก 0.8
    'ensemble_method': 'advanced_stacking',
    'use_feature_engineering': True,
    'use_sample_weights': True,
    'use_advanced_preprocessing': True,
    'use_polynomial_features': True,  # 🔥 เพิ่มใหม่
    'polynomial_degree': 2,  # 🔥 เพิ่มใหม่
    'use_feature_interactions': True,  # 🔥 เพิ่มใหม่
    'interaction_depth': 2,  # 🔥 เพิ่มใหม่
    
    # เพิ่มส่วนนี้ทั้งหมด
    'use_tier_models': True,
    'tier_config': {
        'use_dynamic_boundaries': True,
        'use_soft_voting': True,
        'n_tiers': 3,
        'min_samples_per_tier': 50,
        'progressive_weights': {
            'thresholds': [10000, 50000, 100000, 500000, 1000000],
            'weights': [1.0, 2.0, 4.0, 6.0, 8.0, 10.0]
        },
        'tier_models': {
            'standard': {
                'model_class': 'LGBMRegressor',
                'params': {
                    'n_estimators': 500,
                    'learning_rate': 0.05,
                    'max_depth': 15,
                    'num_leaves': 31,
                    'min_child_samples': 20,
                    'subsample': 0.8,
                    'colsample_bytree': 0.8,
                    'random_state': 42,
                    'n_jobs': -1
                }
            },
            'premium': {
                'model_class': 'XGBRegressor', 
                'params': {
                    'n_estimators': 800,
                    'learning_rate': 0.03,
                    'max_depth': 12,
                    'subsample': 0.85,
                    'colsample_bytree': 0.85,
                    'reg_alpha': 0.1,
                    'reg_lambda': 1.0,
                    'random_state': 42,
                    'n_jobs': -1
                }
            },
            'luxury': {
                'model_class': 'CatBoostRegressor',
                'params': {
                    'iterations': 1000,
                    'learning_rate': 0.02,
                    'depth': 10,
                    'l2_leaf_reg': 5,
                    'border_count': 128,
                    'random_state': 42,
                    'verbose': False
                }
            }
        }
    }
}

# ====================================================================================
# ENHANCED TUNING_PARAMS สำหรับเบอร์หายาก
# ====================================================================================
TUNING_PARAMS = {
    # ปรับคะแนนความหลากหลายให้สุดโต่ง - เบอร์ที่ใช้เลขน้อยแต่สวย = แพงมาก
    'VARIETY_SCORES': {
        2: 500,  # ← เพิ่มจาก 100 เป็น 500 (เช่น 0818181818)
        3: 300,  # ← เพิ่มจาก 80 เป็น 300 (เช่น 0897898789)
        4: 150,  # ← เพิ่มจาก 50 เป็น 150
        5: 50,   # ← เพิ่มจาก 20 เป็น 50
        6: 10,   # ← เพิ่มจาก 5 เป็น 10
        7: 0,
        8: 0,
        9: 0
    },
    
    # เพิ่มคะแนนความจำง่ายสำหรับเบอร์พิเศษ
    'MEMORABILITY': {
        'repeat_4_plus': 80,    # ← เพิ่มจาก 20 เป็น 80
        'repeat_3': 40,         # ← เพิ่มจาก 10 เป็น 40
        'sequence_bonus': 150,   # ← เพิ่มจาก 5 เป็น 150 (สำหรับ 12345678)
        'pair_repeat': 100,     # ← เพิ่มจาก 8 เป็น 100 (สำหรับ 56565656)
        'unique_3_or_less': 200, # ← เพิ่มจาก 25 เป็น 200
        'unique_4': 100,        # ← เพิ่มจาก 15 เป็น 100
        'unique_5': 30          # ← เพิ่มจาก 5 เป็น 30
    },
    
    # เพิ่มคะแนนความสวยงาม
    'BEAUTY': {
        'double': 10,           # ← เพิ่มจาก 2 เป็น 10
        'triple': 25,           # ← เพิ่มจาก 3 เป็น 25
        'quad': 50,             # ← เพิ่มจาก 5 เป็น 50
        'alternating_6': 150,   # ← เพิ่มจาก 10 เป็น 150 (121212)
        'pattern_abba': 80,     # ← เพิ่มจาก 8 เป็น 80 (ABBA)
        'pattern_abab': 100     # ← เพิ่มจาก 7 เป็น 100 (ABAB เช่น 56565656)
    },
    
    # เพิ่มน้ำหนักคะแนนรวม
    'TOTAL_WEIGHTS': {
        'repeat_pattern': 50,   # ← เพิ่มจาก 10 เป็น 50
        'mirror_pattern': 80    # ← เพิ่มจาก 15 เป็น 80
    },
    
    # เพิ่มความสำคัญของตำแหน่งท้าย
    'POSITION_MULTIPLIERS': {
        'front': 1.6,   # ← ลดจาก 0.8 เป็น 0.6
        'middle': 1.0,  # ← เพิ่มจาก 1.0 เป็น 1.2
        'end': 2.5      # ← เพิ่มจาก 1.5 เป็น 2.5 (ท้ายเบอร์สำคัญมาก)
    },
    
    # เพิ่มโบนัส ABC Position
    'ABC_BONUS': {
        'triple': 50,   # ← เพิ่มจาก 10 เป็น 50
        'double': 25,   # ← เพิ่มจาก 5 เป็น 25
        'sequence': 40  # ← เพิ่มจาก 8 เป็น 40
    }
}

# ====================================================================================
# HYPERPARAMETER TUNING CONFIGURATION
# ====================================================================================
HYPERPARAMETER_RANGES = {
    'xgboost': {
        'n_estimators': (100, 2000),
        'max_depth': (3, 15),
        'learning_rate': (0.001, 0.3),
        'subsample': (0.5, 1.0),
        'colsample_bytree': (0.5, 1.0),
        'gamma': (0, 10),
        'reg_alpha': (0, 10),
        'reg_lambda': (0, 10),
        'min_child_weight': (1, 10)
    },
    'lightgbm': {
        'n_estimators': (100, 2000),
        'max_depth': (3, 15),
        'learning_rate': (0.001, 0.3),
        'num_leaves': (20, 300),
        'subsample': (0.5, 1.0),
        'colsample_bytree': (0.5, 1.0),
        'reg_alpha': (0, 10),
        'reg_lambda': (0, 10),
        'min_child_samples': (5, 100),
        'max_bin': (50, 500)
    },
    'catboost': {
        'iterations': (100, 2000),
        'depth': (3, 12),
        'learning_rate': (0.001, 0.3),
        'l2_leaf_reg': (1, 10),
        'border_count': (32, 255),
        'bagging_temperature': (0, 1)
    },
    'random_forest': {
        'n_estimators': (100, 1000),
        'max_depth': (5, 50),
        'min_samples_split': (2, 20),
        'min_samples_leaf': (1, 10),
        'max_features': (0.5, 1.0)
    }
}

# ====================================================================================
# PATHS FOR REFACTORING
# ====================================================================================
REFACTORING_MODEL_PATH = os.path.join(MODEL_PATH, 'deployed')
REFACTORING_DATA_PATH = os.path.join(DATA_PATH, 'processed')
REFACTORING_RESULTS_PATH = os.path.join(RESULTS_PATH)

# Create directories if not exist
for path in [REFACTORING_MODEL_PATH, REFACTORING_DATA_PATH, REFACTORING_RESULTS_PATH]:
    os.makedirs(path, exist_ok=True)
