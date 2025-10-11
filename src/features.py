"""
Feature Engineering for Phone Number Price Prediction (Part 1)
By Alex - World-Class AI Expert

This file contains all feature engineering functions.
Split into parts due to size limitations.
"""
import pandas as pd
import numpy as np
from scipy import stats
from collections import Counter
from itertools import groupby
import math
import warnings
warnings.filterwarnings('ignore')

from src.config import CONFIG

# ====================================================================================
# BASIC FEATURE FUNCTIONS
# ====================================================================================

def get_digit_sum(n):
    """ผลรวมตัวเลขทั้งหมด"""
    return sum(int(d) for d in n)

def get_unique_digits(n):
    """จำนวนตัวเลขที่ไม่ซ้ำ"""
    return len(set(n))

def get_max_consecutive_digit(n):
    """จำนวนตัวเลขซ้ำติดกันสูงสุด"""
    return max(len(list(g)) for _, g in groupby(n))

def has_repeating_pattern(n, length=2):
    """ตรวจสอบว่ามี pattern ซ้ำหรือไม่"""
    for i in range(len(n) - length * 2 + 1):
        pattern = n[i:i+length]
        if pattern == n[i+length:i+length*2]:
            return 1
    return 0

def get_good_digit_count(n):
    """นับจำนวนเลขมงคล"""
    return sum(1 for d in n if d in CONFIG['GOOD_DIGITS'])

def get_bad_digit_count(n):
    """นับจำนวนเลขไม่ดี"""
    return sum(1 for d in n if d in CONFIG['BAD_DIGITS'])

def get_premium_pair_count(n):
    """นับจำนวนคู่เลขมงคล"""
    count = 0
    for i in range(len(n) - 1):
        if n[i:i+2] in CONFIG['PREMIUM_PAIRS']:
            count += 1
    return count

def get_ending_score(n):
    """คะแนนท้ายเบอร์"""
    last_4 = n[-4:]
    last_3 = n[-3:]
    last_2 = n[-2:]
    
    score = 0
    if last_4 in CONFIG['ENDING_PREMIUM']:
        score += CONFIG['ENDING_PREMIUM'][last_4]
    elif last_3 in CONFIG['ENDING_PREMIUM']:
        score += CONFIG['ENDING_PREMIUM'][last_3]
    elif last_2 in CONFIG['ENDING_PREMIUM']:
        score += CONFIG['ENDING_PREMIUM'][last_2]
    
    return score

def get_sequence_score(n):
    """คะแนนเลขเรียงกัน"""
    score = 0
    for seq, seq_score in CONFIG['LUCKY_SEQUENCES'].items():
        if seq in n:
            score += seq_score
    return score

def get_digit_frequency(n):
    """ความถี่ของแต่ละตัวเลข"""
    return dict(Counter(n))

def has_triple_repeat(n):
    """มีเลขซ้ำ 3 ตัวหรือไม่"""
    for i in range(len(n) - 2):
        if n[i] == n[i+1] == n[i+2]:
            return 1
    return 0

def has_quad_repeat(n):
    """มีเลขซ้ำ 4 ตัวหรือไม่"""
    for i in range(len(n) - 3):
        if n[i] == n[i+1] == n[i+2] == n[i+3]:
            return 1
    return 0

def get_ascending_count(n):
    """นับเลขเรียงขึ้น"""
    count = 0
    for i in range(len(n) - 1):
        if int(n[i+1]) == int(n[i]) + 1:
            count += 1
    return count

def get_descending_count(n):
    """นับเลขเรียงลง"""
    count = 0
    for i in range(len(n) - 1):
        if int(n[i+1]) == int(n[i]) - 1:
            count += 1
    return count

def has_mirror_pattern(n):
    """มี pattern กระจกหรือไม่"""
    # Full mirror
    if n == n[::-1]:
        return 2
    # Partial mirror
    if n[:4] == n[-4:][::-1] or n[:3] == n[-3:][::-1]:
        return 1
    return 0

def get_complexity_score(n):
    """คะแนนความซับซ้อน"""
    unique = get_unique_digits(n)
    
    if unique <= 2:
        return CONFIG['COMPLEXITY_SCORES']['very_simple']
    elif unique <= 3:
        return CONFIG['COMPLEXITY_SCORES']['simple']
    elif unique <= 5:
        return CONFIG['COMPLEXITY_SCORES']['moderate']
    elif unique <= 7:
        return CONFIG['COMPLEXITY_SCORES']['complex']
    else:
        return CONFIG['COMPLEXITY_SCORES']['very_complex']

def get_power_sum(n):
    """ผลรวมพลังเลข"""
    return sum(CONFIG['POWER_WEIGHTS'].get(d, 0) for d in n)

def get_special_lucky_score(n):
    """คะแนนคู่เลขมงคลพิเศษ"""
    score = 0
    for i in range(len(n) - 1):
        pair = n[i:i+2]
        if pair in CONFIG['SPECIAL_LUCKY_PAIRS']:
            score += CONFIG['SPECIAL_LUCKY_PAIRS'][pair]['score']
    return score

def get_mystical_pair_score(n):
    """คะแนนคู่เลขลึกลับ"""
    score = 0
    for i in range(len(n) - 1):
        pair = n[i:i+2]
        if pair in CONFIG['MYSTICAL_PAIRS']:
            score += CONFIG['MYSTICAL_PAIRS'][pair]
    return score

def has_forbidden_pair(n):
    """มีคู่เลขห้ามหรือไม่"""
    for i in range(len(n) - 1):
        if n[i:i+2] in CONFIG['FORBIDDEN_PAIRS']:
            return 1
    return 0

# ====================================================================================
# ADVANCED FEATURE FUNCTIONS
# ====================================================================================

def get_digit_variance(n):
    """ความแปรปรวนของตัวเลข"""
    digits = [int(d) for d in n]
    return np.var(digits)

def get_alternating_pattern_score(n):
    """คะแนน pattern สลับ"""
    score = 0
    for i in range(len(n) - 2):
        if n[i] == n[i+2] and n[i] != n[i+1]:
            score += 1
    return score

def get_ascending_sequences(n):
    """นับชุดเลขเรียงขึ้น"""
    sequences = 0
    current_length = 1
    
    for i in range(len(n) - 1):
        if int(n[i+1]) == int(n[i]) + 1:
            current_length += 1
        else:
            if current_length >= 3:
                sequences += 1
            current_length = 1
    
    if current_length >= 3:
        sequences += 1
    
    return sequences

def get_descending_sequences(n):
    """นับชุดเลขเรียงลง"""
    sequences = 0
    current_length = 1
    
    for i in range(len(n) - 1):
        if int(n[i+1]) == int(n[i]) - 1:
            current_length += 1
        else:
            if current_length >= 3:
                sequences += 1
            current_length = 1
    
    if current_length >= 3:
        sequences += 1
    
    return sequences

def has_repeated_block(n, block_size=2):
    """ตรวจสอบ block ซ้ำ"""
    for i in range(len(n) - block_size * 2 + 1):
        block = n[i:i+block_size]
        if n[i+block_size:i+block_size*2] == block:
            return 1
    return 0

def get_max_consecutive_same(n):
    """จำนวนเลขซ้ำติดกันสูงสุด"""
    max_count = 1
    current_count = 1
    
    for i in range(1, len(n)):
        if n[i] == n[i-1]:
            current_count += 1
            max_count = max(max_count, current_count)
        else:
            current_count = 1
    
    return max_count

def get_symmetry_score(n):
    """คะแนนความสมมาตร"""
    score = 0
    
    # Check full symmetry
    if n == n[::-1]:
        score += 10
    
    # Check partial symmetry
    for i in range(1, 5):
        if n[:i] == n[-i:][::-1]:
            score += i
    
    return score

def has_lucky_combo(n):
    """มีชุดเลขนำโชคหรือไม่"""
    lucky_combos = ['168', '888', '999', '789', '456', '555']
    for combo in lucky_combos:
        if combo in n:
            return 1
    return 0

def analyze_middle_section(n):
    """วิเคราะห์ส่วนกลางเบอร์"""
    middle = n[3:7]  # ตัวที่ 4-7
    return get_power_sum(middle)

def analyze_ending_pattern(n):
    """วิเคราะห์ pattern ท้ายเบอร์"""
    last_4 = n[-4:]
    
    # Check for repeating
    if len(set(last_4)) == 1:
        return 100  # AAAA
    elif last_4[0] == last_4[1] and last_4[2] == last_4[3]:
        return 80   # AABB
    elif last_4[0] == last_4[2] and last_4[1] == last_4[3]:
        return 70   # ABAB
    
    # Check for sequence
    digits = [int(d) for d in last_4]
    if all(digits[i+1] == digits[i] + 1 for i in range(3)):
        return 60   # Ascending
    elif all(digits[i+1] == digits[i] - 1 for i in range(3)):
        return 50   # Descending
    
    return 0

def get_double_triple_quad_scores(n):
    """คะแนนเลขซ้ำ 2, 3, 4"""
    freq = Counter(n)
    
    double_score = sum(1 for count in freq.values() if count == 2) * 5
    triple_score = sum(1 for count in freq.values() if count == 3) * 15
    quad_score = sum(1 for count in freq.values() if count >= 4) * 30
    
    return double_score, triple_score, quad_score

def analyze_digit_positions_advanced(n, digit):
    """วิเคราะห์ตำแหน่งของเลขแต่ละตัวแบบละเอียด"""
    positions = [i for i, d in enumerate(n) if d == str(digit)]
    
    if not positions:
        return {
            'count': 0,
            'first_pos': -1,
            'last_pos': -1,
            'spread': 0,
            'clustering': 0,
            'in_end': 0
        }
    
    spread = max(positions) - min(positions) if len(positions) > 1 else 0
    clustering = sum(1 for i in range(len(positions)-1) if positions[i+1] - positions[i] == 1)
    in_end = 1 if any(p >= 6 for p in positions) else 0
    
    return {
        'count': len(positions),
        'first_pos': positions[0],
        'last_pos': positions[-1],
        'spread': spread,
        'clustering': clustering,
        'in_end': in_end
    }

# ====================================================================================
# POSITION-BASED FEATURES
# ====================================================================================

def get_position_weights(n):
    """น้ำหนักตามตำแหน่ง"""
    weights = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.5, 1.8, 2.0]
    return sum(int(d) * w for d, w in zip(n, weights))

def get_ending_pattern_type(n):
    """ประเภท pattern ท้ายเบอร์"""
    last_4 = n[-4:]
    
    if len(set(last_4)) == 1:
        return 'quad'
    elif len(set(last_4)) == 2:
        if last_4[0] == last_4[1] == last_4[2] or last_4[1] == last_4[2] == last_4[3]:
            return 'triple_plus'
        else:
            return 'double_double'
    elif len(set(last_4)) == 3:
        return 'one_pair'
    else:
        return 'all_different'

def get_prefix_score(n):
    """คะแนน prefix (3 ตัวแรก)"""
    prefix = n[:3]
    
    # Special prefixes
    special_prefixes = {
        '088': 50, '089': 45, '081': 40, '086': 35,
        '095': 30, '096': 28, '097': 26, '098': 24
    }
    
    if prefix in special_prefixes:
        return special_prefixes[prefix]
    
    # Calculate based on digits
    return sum(CONFIG['POWER_WEIGHTS'].get(d, 0) for d in prefix)

def get_middle_pattern_score(n):
    """คะแนน pattern ตรงกลาง"""
    middle = n[3:7]
    
    score = 0
    # Check for repeating
    if len(set(middle)) == 1:
        score += 40
    # Check for pattern
    elif has_repeating_pattern(middle, 2):
        score += 20
    # Check for sequence
    elif all(int(middle[i+1]) == int(middle[i]) + 1 for i in range(3)):
        score += 30
    
    return score

"""
Feature Engineering for Phone Number Price Prediction (Part 2)
By Alex - World-Class AI Expert

Advanced and Master Features + Main Feature Creation Function
"""

# ====================================================================================
# ADVANCED FEATURES V3.0
# ====================================================================================

def get_sum_diff_halves(n):
    """ผลต่างผลรวมครึ่งหน้า-หลัง"""
    first_half = sum(int(d) for d in n[:5])
    second_half = sum(int(d) for d in n[5:])
    return abs(first_half - second_half)

def get_num_peaks(n):
    """จำนวน peaks (ตัวเลขที่มากกว่าข้างๆ)"""
    peaks = 0
    digits = [int(d) for d in n]
    for i in range(1, len(digits) - 1):
        if digits[i] > digits[i-1] and digits[i] > digits[i+1]:
            peaks += 1
    return peaks

def get_num_valleys(n):
    """จำนวน valleys (ตัวเลขที่น้อยกว่าข้างๆ)"""
    valleys = 0
    digits = [int(d) for d in n]
    for i in range(1, len(digits) - 1):
        if digits[i] < digits[i-1] and digits[i] < digits[i+1]:
            valleys += 1
    return valleys

def get_longest_increasing_subsequence(n):
    """ความยาว subsequence ที่เพิ่มขึ้นยาวที่สุด"""
    digits = [int(d) for d in n]
    n_len = len(digits)
    lis = [1] * n_len
    
    for i in range(1, n_len):
        for j in range(i):
            if digits[i] > digits[j] and lis[i] < lis[j] + 1:
                lis[i] = lis[j] + 1
    
    return max(lis)

def get_digit_entropy(n):
    """Entropy ของการกระจายตัวเลข"""
    freq = Counter(n)
    probs = [count/len(n) for count in freq.values()]
    return -sum(p * np.log2(p) for p in probs if p > 0)

def get_run_length_encoding_size(n):
    """ขนาดหลังทำ run-length encoding"""
    if not n:
        return 0
    
    encoded = []
    count = 1
    
    for i in range(1, len(n)):
        if n[i] == n[i-1]:
            count += 1
        else:
            encoded.append((n[i-1], count))
            count = 1
    
    encoded.append((n[-1], count))
    return len(encoded)

def get_digit_distance_sum(n):
    """ผลรวมระยะห่างระหว่างตัวเลขติดกัน"""
    return sum(abs(int(n[i+1]) - int(n[i])) for i in range(len(n) - 1))

def get_unique_digit_ratio(n):
    """อัตราส่วนตัวเลขไม่ซ้ำต่อทั้งหมด"""
    return len(set(n)) / len(n)

def has_arithmetic_sequence(n, length=3):
    """มีลำดับเลขคณิตหรือไม่"""
    digits = [int(d) for d in n]
    
    for i in range(len(digits) - length + 1):
        seq = digits[i:i+length]
        if len(seq) >= 3:
            diffs = [seq[j+1] - seq[j] for j in range(len(seq)-1)]
            if len(set(diffs)) == 1 and diffs[0] != 0:
                return 1
    return 0

def get_num_unique_pairs(n):
    """จำนวนคู่ตัวเลขที่ไม่ซ้ำ"""
    pairs = set()
    for i in range(len(n) - 1):
        pairs.add(n[i:i+2])
    return len(pairs)

def get_num_unique_triplets(n):
    """จำนวนชุด 3 ตัวที่ไม่ซ้ำ"""
    triplets = set()
    for i in range(len(n) - 2):
        triplets.add(n[i:i+3])
    return len(triplets)

def get_weighted_sum_score(n):
    """คะแนนผลรวมถ่วงน้ำหนักตามตำแหน่ง"""
    weights = [1, 1.2, 1.5, 1.8, 2, 2.5, 3, 3.5, 4, 5]
    return sum(int(d) * w for d, w in zip(n, weights))

def get_special_to_normal_ratio(n):
    """อัตราส่วนเลขพิเศษต่อเลขปกติ"""
    special_count = sum(1 for d in n if d in '56899')
    normal_count = len(n) - special_count
    return special_count / (normal_count + 1)

def get_power_to_sum_ratio(n):
    """อัตราส่วนคะแนนพลังต่อผลรวม"""
    power_sum = get_power_sum(n)
    digit_sum = get_digit_sum(n)
    return power_sum / (digit_sum + 1)

def get_ending_power_concentration(n):
    """ความเข้มข้นของพลังท้ายเบอร์"""
    last_4 = n[-4:]
    last_4_power = sum(CONFIG['POWER_WEIGHTS'].get(d, 0) for d in last_4)
    total_power = sum(CONFIG['POWER_WEIGHTS'].get(d, 0) for d in n)
    return last_4_power / (total_power + 1)

def get_negative_pairs_count(n):
    """จำนวนคู่เลขไม่ดี"""
    count = 0
    negative_pairs = ['00', '02', '04', '07', '13', '17', '20', '22', '27', '40', '44', '70', '77']
    for i in range(len(n) - 1):
        if n[i:i+2] in negative_pairs:
            count += 1
    return count

def get_investment_grade_score(n):
    """คะแนนเกรดการลงทุน"""
    score = 0
    
    # ตรวจสอบเลขซ้ำท้าย
    if n[-4:] == n[-1] * 4:
        score += 50
    elif n[-3:] == n[-1] * 3:
        score += 30
    
    # ตรวจสอบเลขเรียง
    if '1234' in n or '5678' in n or '6789' in n:
        score += 20
    
    # ตรวจสอบเลขมงคล
    lucky_count = sum(1 for d in n if d in '5689')
    score += lucky_count * 5
    
    return score

def get_market_tier_score(n):
    """คะแนนระดับตลาด"""
    # สร้างคะแนนพื้นฐานจาก features
    base_score = (
        get_ending_score(n) * 2 +
        get_sequence_score(n) * 1.5 +
        get_special_lucky_score(n) * 1.2 +
        get_power_sum(n)
    )
    
    # จัดระดับ
    if base_score >= 300:
        return 5  # Ultra Premium
    elif base_score >= 200:
        return 4  # Premium
    elif base_score >= 100:
        return 3  # High
    elif base_score >= 50:
        return 2  # Medium
    else:
        return 1  # Low

# ====================================================================================
# MASTER FEATURES V4.0
# ====================================================================================

def has_triple_power_digit(n):
    """ตรวจสอบว่ามีเลขพลังสูง 3 ตัวติดกันหรือไม่"""
    power_digits = ['5', '9', '8', '6']
    for i in range(len(n) - 2):
        if all(n[i+j] in power_digits for j in range(3)):
            return 1
    return 0

def calculate_position_weighted_score(n):
    """คำนวณคะแนนถ่วงน้ำหนักตามตำแหน่ง"""
    score = 0
    position_weights = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.5, 1.8, 2.0]
    
    for i, digit in enumerate(n):
        digit_value = CONFIG['POWER_WEIGHTS'].get(digit, 0)
        score += digit_value * position_weights[i]
    
    return score

def calculate_ending_power_score(n):
    """คำนวณคะแนนพลังท้ายเบอร์"""
    last_4 = n[-4:]
    score = 0
    
    # คะแนนพื้นฐานจากตัวเลข
    for i, digit in enumerate(last_4):
        multiplier = 1 + (i * 0.5)  # ยิ่งท้ายยิ่งสำคัญ
        score += CONFIG['POWER_WEIGHTS'].get(digit, 0) * multiplier
    
    # โบนัสพิเศษ
    if last_4 in CONFIG['ENDING_PREMIUM']:
        score += CONFIG['ENDING_PREMIUM'][last_4]
    
    return score

def calculate_mirror_score(n):
    """คำนวณคะแนน mirror pattern"""
    score = 0
    
    # Full mirror
    if n == n[::-1]:
        score += 100
    
    # Partial mirror (หน้า-หลัง)
    if n[:4] == n[-4:][::-1]:
        score += 50
    elif n[:3] == n[-3:][::-1]:
        score += 30
    
    # Mini mirror patterns
    for i in range(len(n) - 3):
        if n[i:i+2] == n[i+2:i+4][::-1]:
            score += 10
    
    return score

def calculate_number_balance(n):
    """คำนวณความสมดุลของเบอร์"""
    # แบ่งเป็น 2 ส่วน
    first_half = n[:5]
    second_half = n[5:]
    
    # คำนวณผลรวม
    sum_first = sum(int(d) for d in first_half)
    sum_second = sum(int(d) for d in second_half)
    
    # คะแนนความสมดุล (ยิ่งใกล้เคียงยิ่งดี)
    diff = abs(sum_first - sum_second)
    balance_score = max(0, 50 - diff * 5)
    
    return balance_score

def calculate_famous_sequence_score(n):
    """คะแนนเลขชุดพิเศษ"""
    score = 0
    
    for seq, seq_score in CONFIG['FAMOUS_SEQUENCES'].items():
        if seq in n:
            score += seq_score
            
            # โบนัสตำแหน่ง
            if n.endswith(seq):
                score += seq_score * 0.5
    
    return score

def calculate_famous_sequence_score_advanced(n):
    """คะแนนเลขชุดพิเศษแบบขั้นสูง"""
    score = 0
    
    for seq, seq_score in CONFIG['FAMOUS_SEQUENCES'].items():
        if seq in n:
            base_score = seq_score
            
            # โบนัสตำแหน่ง
            if n.endswith(seq):
                base_score *= 2.5
            elif seq in n[-4:]:
                base_score *= 1.8
            elif seq in n[:3]:
                base_score *= 1.3
            
            score += base_score
    
    return score

def get_wave_pattern_score(n):
    """คะแนน pattern คลื่น (ขึ้น-ลง-ขึ้น-ลง)"""
    score = 0
    digits = [int(d) for d in n]
    
    # ตรวจสอบ wave pattern
    ups = 0
    downs = 0
    
    for i in range(len(digits) - 1):
        if digits[i+1] > digits[i]:
            ups += 1
            if i > 0 and digits[i] < digits[i-1]:  # Valley
                score += 5
        elif digits[i+1] < digits[i]:
            downs += 1
            if i > 0 and digits[i] > digits[i-1]:  # Peak
                score += 5
    
    # โบนัสสำหรับ balanced wave
    if abs(ups - downs) <= 1:
        score += 20
    
    return score

def calculate_rarity_score(n):
    """คะแนนความหายาก"""
    score = 0
    
    # 1. เลขซ้ำ 4 ตัวท้าย
    if n[-4:] == n[-1] * 4:
        score += 100
    
    # 2. เลขเรียง 5+ ตัว
    for i in range(6):
        seq = ''.join(str((int(n[0]) + j) % 10) for j in range(5))
        if seq in n:
            score += 80
            break
    
    # 3. Pattern พิเศษ
    special_patterns = ['0000', '1111', '8888', '9999', '1234', '5678']
    for pattern in special_patterns:
        if pattern in n:
            score += 60
    
    # 4. ความไม่ซ้ำ
    if len(set(n)) >= 9:
        score += 40
    
    return score

def get_mathematical_beauty_score(n):
    """คะแนนความงามทางคณิตศาสตร์"""
    score = 0
    digits = [int(d) for d in n]
    
    # 1. Fibonacci sequence
    fib = [0, 1, 1, 2, 3, 5, 8]
    for i in range(len(digits) - 2):
        if digits[i:i+3] in [[f1, f2, f3] for f1, f2, f3 in zip(fib, fib[1:], fib[2:])]:
            score += 30
    
    # 2. Prime numbers
    primes = [2, 3, 5, 7]
    prime_count = sum(1 for d in digits if d in primes)
    score += prime_count * 5
    
    # 3. Perfect squares
    squares = [0, 1, 4, 9]
    square_count = sum(1 for d in digits if d in squares)
    score += square_count * 3
    
    # 4. Mathematical constants
    if '314' in n:  # Pi
        score += 25
    if '271' in n:  # e
        score += 25
    if '161' in n:  # Golden ratio
        score += 25
    
    return score

def calculate_abc_position_score_advanced(n):
    """คะแนน ABC position แบบขั้นสูง (ผสม position + pattern)"""
    score = 0
    
    # A positions (ตำแหน่งสำคัญสูง)
    a_positions = [0, 6, 7, 8, 9]  # ตัวแรก และ 4 ตัวท้าย
    # B positions (ตำแหน่งสำคัญปานกลาง)
    b_positions = [1, 2, 5]
    # C positions (ตำแหน่งสำคัญน้อย)
    c_positions = [3, 4]
    
    # คำนวณคะแนนตามตำแหน่งและค่าตัวเลข
    for i, digit in enumerate(n):
        digit_value = CONFIG['POWER_WEIGHTS'].get(digit, 0)
        
        if i in a_positions:
            score += digit_value * 3
        elif i in b_positions:
            score += digit_value * 2
        else:
            score += digit_value * 1
    
    # โบนัสสำหรับ pattern ดีในตำแหน่ง A
    for i in a_positions:
        if i < len(n) and n[i] in '5689':
            score += 10
    
    return score

# ====================================================================================
# SPECIAL FEATURES V5.0
# ====================================================================================

def get_special_lucky_score_advanced(n):
    """คะแนนเลขมงคลพิเศษแบบขั้นสูง"""
    score = 0
    
    # 1. ตรวจสอบคู่มงคลพิเศษ
    for i in range(len(n) - 1):
        pair = n[i:i+2]
        if pair in CONFIG['SPECIAL_LUCKY_PAIRS']:
            base_score = CONFIG['SPECIAL_LUCKY_PAIRS'][pair]['score']
            
            # โบนัสตำแหน่ง
            if i >= 6:  # คู่ท้ายเบอร์
                base_score *= 2
            elif i == 0:  # คู่หน้าเบอร์
                base_score *= 1.3
            
            score += base_score
    
    # 2. ตรวจสอบชุดมงคล 3 ตัว
    lucky_triplets = ['168', '888', '999', '789', '456', '555']
    for triplet in lucky_triplets:
        if triplet in n:
            if n.endswith(triplet):
                score += 50
            else:
                score += 25
    
    # 3. โบนัสพิเศษสำหรับเบอร์มงคลสูง
    if n.count('8') >= 4:
        score += 40
    if n.count('9') >= 4:
        score += 45
    if n.count('5') >= 3:
        score += 30
    
    return score

def calculate_market_demand_score(n):
    """คะแนนความต้องการของตลาด"""
    score = 0
    
    # 1. เบอร์สวยตามความนิยม
    popular_endings = ['9999', '8888', '6666', '5555', '9988', '8899', '6688']
    for ending in popular_endings:
        if n.endswith(ending):
            score += 100
            break
    
    # 2. เบอร์มงคลทั่วไป
    if any(n.endswith(str(i)*2) for i in range(10)):
        score += 30
    
    # 3. เลขเรียงนิยม
    sequences = ['1234', '2345', '3456', '4567', '5678', '6789']
    for seq in sequences:
        if seq in n:
            score += 40
    
    # 4. ความสมดุล
    balance = calculate_number_balance(n)
    if balance > 40:
        score += 20
    
    return score

def get_tier_classification_score(n):
    """คะแนนสำหรับจัดระดับเบอร์"""
    # รวมคะแนนจากหลายมิติ
    total_score = (
        get_ending_score(n) * 3 +
        calculate_rarity_score(n) * 2 +
        get_special_lucky_score_advanced(n) * 2 +
        calculate_market_demand_score(n) * 1.5 +
        get_mathematical_beauty_score(n) * 1 +
        calculate_position_weighted_score(n) * 0.8
    )
    
    return total_score

"""
Feature Engineering for Phone Number Price Prediction (Part 4)
By Alex - World-Class AI Expert

Missing Features Functions from trainmodel10withtest fix.txt
This file completes the feature engineering pipeline
"""

# ====================================================================================
# MASTER FEATURES FUNCTIONS (MISSING FROM PARTS 1-3)
# ====================================================================================

def get_weighted_sum_score(n):
    """คะแนนผลรวมถ่วงน้ำหนักตามตำแหน่ง"""
    weights = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.5, 1.8, 2.0]
    score = 0
    for i, digit in enumerate(n):
        digit_val = int(digit)
        # พิจารณาทั้งค่าตัวเลขและพลังเลข
        base_score = digit_val * weights[i]
        power_bonus = CONFIG['POWER_WEIGHTS'].get(digit, 0) * weights[i]
        score += base_score + power_bonus
    return score

def get_special_to_normal_ratio(n):
    """อัตราส่วนเลขพิเศษต่อเลขธรรมดา"""
    special_count = sum(1 for d in n if d in '56899')
    normal_count = sum(1 for d in n if d not in '56899')
    if normal_count == 0:
        return 10.0  # All special
    return special_count / normal_count

def get_power_to_sum_ratio(n):
    """อัตราส่วนพลังเลขต่อผลรวม"""
    power_sum = sum(CONFIG['POWER_WEIGHTS'].get(d, 0) for d in n)
    digit_sum = sum(int(d) for d in n)
    if digit_sum == 0:
        return 0
    return power_sum / digit_sum

def get_ending_power_concentration(n):
    """ความเข้มข้นของพลังเลขท้ายเบอร์"""
    last_4 = n[-4:]
    total_power = sum(CONFIG['POWER_WEIGHTS'].get(d, 0) for d in n)
    ending_power = sum(CONFIG['POWER_WEIGHTS'].get(d, 0) for d in last_4)
    
    if total_power == 0:
        return 0
    
    concentration = ending_power / total_power
    # Bonus for high ending power
    if ending_power > 15:
        concentration *= 1.5
    
    return concentration * 100

def get_negative_pairs_count(n):
    """นับจำนวนคู่เลขไม่ดี"""
    count = 0
    for i in range(len(n) - 1):
        pair = n[i:i+2]
        if pair in CONFIG['FORBIDDEN_PAIRS']:
            count += 1
    return count

def get_investment_grade_score(n):
    """คะแนนเกรดการลงทุน"""
    score = 0
    
    # ท้ายเบอร์ premium
    last_4 = n[-4:]
    if last_4 in ['8888', '9999', '6666', '5555']:
        score += 100
    elif last_4 in ['8899', '6688', '5566']:
        score += 80
    elif len(set(last_4)) == 1:  # 4 ตัวซ้ำ
        score += 60
    
    # Pattern พิเศษ
    if '888' in n or '999' in n:
        score += 40
    if '168' in n or '268' in n:
        score += 30
    
    # ความหายาก
    unique_ratio = len(set(n)) / len(n)
    if unique_ratio < 0.3:  # Very rare
        score += 50
    elif unique_ratio < 0.5:  # Rare
        score += 30
    
    return score

def get_market_tier_score(n):
    """คะแนนระดับตลาด"""
    tier_score = 0
    
    # Tier 1: Ultra Premium (ท้าย 4-6 ตัวซ้ำ)
    if n[-4:] == n[-5:-1] or n[-6:] == n[-7:-1]:
        tier_score = 1000
    elif len(set(n[-4:])) == 1:
        tier_score = 800
    
    # Tier 2: Premium (pattern พิเศษ)
    elif any(seq in n for seq in ['8888', '9999', '6666', '123456', '234567']):
        tier_score = 600
    
    # Tier 3: High Value
    elif any(seq in n for seq in ['888', '999', '666', '168', '268']):
        tier_score = 400
    
    # Tier 4: Good
    elif len(set(n[-3:])) == 1 or '88' in n[-4:] or '99' in n[-4:]:
        tier_score = 200
    
    # Tier 5: Standard
    else:
        tier_score = 100
    
    return tier_score

def has_triple_power_digit(n):
    """มีเลขพลังซ้ำ 3 ตัวหรือไม่"""
    for i in range(len(n) - 2):
        if n[i] == n[i+1] == n[i+2] and n[i] in '56899':
            return 1
    return 0

def calculate_position_weighted_score(n):
    """คะแนนถ่วงน้ำหนักตามตำแหน่ง (ขั้นสูง)"""
    position_weights = {
        0: 0.3, 1: 0.4, 2: 0.5,  # หน้าเบอร์
        3: 0.8, 4: 0.9, 5: 1.0,  # ABC
        6: 1.5, 7: 2.0, 8: 2.5, 9: 3.0  # ท้ายเบอร์
    }
    
    score = 0
    for i, digit in enumerate(n):
        digit_score = int(digit) + CONFIG['POWER_WEIGHTS'].get(digit, 0)
        position_multiplier = position_weights.get(i, 1.0)
        score += digit_score * position_multiplier
    
    return score

def calculate_ending_power_score(n):
    """คะแนนพลังท้ายเบอร์ (ขั้นสูง)"""
    last_4 = n[-4:]
    score = 0
    
    # Check each ending pattern
    for length in [4, 3, 2]:
        ending = n[-length:]
        if ending in CONFIG['ENDING_PREMIUM']:
            score += CONFIG['ENDING_PREMIUM'][ending] * (length / 2)
    
    # Power digit bonus
    power_count = sum(1 for d in last_4 if d in '56899')
    score += power_count * 10
    
    # Pattern bonus
    if len(set(last_4)) == 1:  # 4 ซ้ำ
        score *= 3
    elif len(set(last_4)) == 2:  # 2 ชนิด
        score *= 1.5
    
    return score

def calculate_mirror_score(n):
    """คะแนน pattern กระจก"""
    score = 0
    
    # Full mirror
    if n == n[::-1]:
        score += 100
    
    # Partial mirrors
    for length in [2, 3, 4, 5]:
        for i in range(len(n) - length * 2 + 1):
            part1 = n[i:i+length]
            part2 = n[i+length:i+length*2]
            if part1 == part2[::-1]:
                score += length * 10
    
    # ท้ายเบอร์ mirror
    if n[-2:] == n[-4:-2][::-1]:
        score += 30
    if n[-3:] == n[-6:-3][::-1]:
        score += 50
    
    return score

def calculate_number_balance(n):
    """คำนวณความสมดุลของเบอร์"""
    first_half = n[:5]
    second_half = n[5:]
    
    # ผลรวมแต่ละครึ่ง
    sum1 = sum(int(d) for d in first_half)
    sum2 = sum(int(d) for d in second_half)
    
    # คะแนนความสมดุล
    diff = abs(sum1 - sum2)
    if diff == 0:
        return 50
    elif diff <= 5:
        return 30
    elif diff <= 10:
        return 15
    else:
        return 0

def get_wave_pattern_score(n):
    """คะแนน pattern คลื่น (ขึ้น-ลง)"""
    score = 0
    changes = []
    
    for i in range(len(n) - 1):
        diff = int(n[i+1]) - int(n[i])
        if diff != 0:
            changes.append(1 if diff > 0 else -1)
    
    # Check for wave pattern
    if len(changes) >= 3:
        wave_count = 0
        for i in range(len(changes) - 1):
            if changes[i] * changes[i+1] < 0:  # Change direction
                wave_count += 1
        
        if wave_count >= 3:
            score = wave_count * 10
    
    return score

def calculate_rarity_score(n):
    """คะแนนความหายาก"""
    rarity = 0
    
    # จำนวนตัวเลขที่ไม่ซ้ำ
    unique_ratio = len(set(n)) / len(n)
    
    # Very rare patterns
    if len(set(n)) <= 2:
        rarity += 100
    elif len(set(n)) <= 3:
        rarity += 60
    
    # 4+ ตัวซ้ำ
    digit_counts = Counter(n)
    max_repeat = max(digit_counts.values())
    if max_repeat >= 5:
        rarity += 80
    elif max_repeat >= 4:
        rarity += 50
    
    # Special sequences
    if any(seq in n for seq in ['0000', '1111', '2222', '3333', '4444', '5555', '6666', '7777', '8888', '9999']):
        rarity += 70
    
    return rarity

def get_mathematical_beauty_score(n):
    """คะแนนความสวยงามทางคณิตศาสตร์"""
    score = 0
    
    # Fibonacci sequence check
    fib = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    for i in range(len(n) - 1):
        if int(n[i:i+2]) in fib:
            score += 20
    
    # Perfect squares
    for i in range(len(n) - 1):
        num = int(n[i:i+2])
        if num > 0 and int(np.sqrt(num))**2 == num:
            score += 15
    
    # Arithmetic sequence
    diffs = [int(n[i+1]) - int(n[i]) for i in range(len(n) - 1)]
    if len(set(diffs)) == 1:  # Constant difference
        score += 40
    
    # Geometric patterns
    if len(set(n[::2])) == 1 and len(set(n[1::2])) == 1:  # Alternating
        score += 30
    
    return score

# ====================================================================================
# SPECIAL FEATURES V5.0 FUNCTIONS
# ====================================================================================

def get_special_lucky_score_advanced(n):
    """คะแนนความเป็นมงคลขั้นสูง v5.0"""
    score = 0
    
    # Base lucky score
    for i in range(len(n) - 1):
        pair = n[i:i+2]
        if pair in CONFIG['SPECIAL_LUCKY_PAIRS']:
            base_score = CONFIG['SPECIAL_LUCKY_PAIRS'][pair]['score']
            
            # Position multiplier
            if i >= 6:  # ท้ายเบอร์
                base_score *= 2.5
            elif i >= 3:  # ABC
                base_score *= 1.5
            
            score += base_score
    
    # Triple lucky bonus
    for i in range(len(n) - 2):
        triple = n[i:i+3]
        if triple in ['888', '999', '666', '168', '268', '369']:
            score += 50
    
    # Full number analysis
    if n.count('8') >= 4:
        score += 100
    if n.count('9') >= 3:
        score += 80
    
    return score

def calculate_market_demand_score(n):
    """คะแนนความต้องการของตลาด"""
    demand = 0
    
    # Popular patterns
    popular_patterns = {
        '88': 30, '99': 30, '888': 50, '999': 50,
        '8888': 100, '9999': 100, '168': 40, '268': 40,
        '1234': 35, '5678': 35, '6789': 40
    }
    
    for pattern, score in popular_patterns.items():
        if pattern in n:
            demand += score
            # Bonus if at end
            if n.endswith(pattern):
                demand += score * 0.5
    
    # Market preferences
    if len(set(n[-4:])) == 1:  # 4 ตัวท้ายซ้ำ
        demand += 150
    elif len(set(n[-3:])) == 1:  # 3 ตัวท้ายซ้ำ
        demand += 80
    
    # Easy to remember
    if len(set(n)) <= 4:
        demand += 60
    
    return demand

def get_tier_classification_score(n):
    """คะแนนการจัดระดับชั้น"""
    classification = 0
    
    # Ultra Premium indicators
    if n[-4:] in ['8888', '9999', '6666', '5555']:
        classification = 1000
    elif len(set(n[-4:])) == 1:
        classification = 800
    
    # Premium indicators
    elif any(pattern in n for pattern in ['888888', '999999', '123456']):
        classification = 600
    
    # High-end indicators
    elif any(pattern in n[-4:] for pattern in ['888', '999', '168', '268']):
        classification = 400
    
    # Mid-tier indicators
    elif len(set(n[-3:])) == 1 or any(d * 2 in n for d in '56789'):
        classification = 200
    
    # Standard
    else:
        classification = 100
    
    # Bonus for overall pattern
    if len(set(n)) <= 3:
        classification *= 1.5
    
    return classification

# ====================================================================================
# ADDITIONAL HELPER FUNCTIONS
# ====================================================================================

def get_digit_variance(n):
    """ความแปรปรวนของตัวเลข"""
    digits = [int(d) for d in n]
    return np.var(digits)

def get_alternating_pattern_score(n):
    """คะแนน pattern สลับ"""
    score = 0
    for i in range(len(n) - 2):
        if n[i] == n[i+2] and n[i] != n[i+1]:
            score += 10
    return score

def get_ascending_sequences(n):
    """นับ sequences ที่เพิ่มขึ้น"""
    count = 0
    i = 0
    while i < len(n) - 1:
        j = i
        while j < len(n) - 1 and int(n[j+1]) == int(n[j]) + 1:
            j += 1
        if j > i:
            count += 1
            i = j
        else:
            i += 1
    return count

def get_descending_sequences(n):
    """นับ sequences ที่ลดลง"""
    count = 0
    i = 0
    while i < len(n) - 1:
        j = i
        while j < len(n) - 1 and int(n[j+1]) == int(n[j]) - 1:
            j += 1
        if j > i:
            count += 1
            i = j
        else:
            i += 1
    return count

def has_repeated_block(n, block_size=2):
    """ตรวจสอบ block ที่ซ้ำ"""
    for i in range(len(n) - block_size * 2 + 1):
        block = n[i:i+block_size]
        if n[i+block_size:i+block_size*2] == block:
            return 1
    return 0

def get_max_consecutive_same(n):
    """จำนวนตัวเลขเดียวกันติดกันสูงสุด"""
    if not n:
        return 0
    
    max_count = 1
    current_count = 1
    
    for i in range(1, len(n)):
        if n[i] == n[i-1]:
            current_count += 1
            max_count = max(max_count, current_count)
        else:
            current_count = 1
    
    return max_count

def get_symmetry_score(n):
    """คะแนนความสมมาตร"""
    score = 0
    
    # Check different symmetry types
    mid = len(n) // 2
    
    # Perfect symmetry
    if n[:mid] == n[-mid:][::-1]:
        score += 50
    
    # Partial symmetry
    for length in [2, 3, 4]:
        if n[:length] == n[-length:][::-1]:
            score += length * 5
    
    return score

def has_lucky_combo(n):
    """มีชุดตัวเลขนำโชคหรือไม่"""
    lucky_combos = ['168', '268', '369', '888', '999', '789', '456']
    for combo in lucky_combos:
        if combo in n:
            return 1
    return 0

def analyze_middle_section(n):
    """วิเคราะห์ส่วนกลางเบอร์"""
    middle = n[3:7]  # Positions 3-6
    score = 0
    
    # Repeating in middle
    if len(set(middle)) == 1:
        score += 40
    
    # Pattern in middle
    if has_repeating_pattern(middle, 2):
        score += 20
    
    # Power digits in middle
    power_count = sum(1 for d in middle if d in '56899')
    score += power_count * 5
    
    return score

def analyze_ending_pattern(n):
    """วิเคราะห์ pattern ท้ายเบอร์โดยละเอียด"""
    last_4 = n[-4:]
    score = 0
    
    # Perfect endings
    perfect_endings = ['8888', '9999', '6666', '5555', '1688', '2688']
    if last_4 in perfect_endings:
        return 200
    
    # Check pattern types
    unique_count = len(set(last_4))
    
    if unique_count == 1:  # AAAA
        score = 150
    elif unique_count == 2:  # AABB, AAAB, etc.
        digit_counts = Counter(last_4)
        if 3 in digit_counts.values():  # AAAB
            score = 100
        else:  # AABB
            score = 80
    elif unique_count == 3:  # AABC
        score = 50
    else:  # ABCD
        # Check if sequential
        digits = [int(d) for d in last_4]
        if all(digits[i+1] == digits[i] + 1 for i in range(3)):
            score = 60
        elif all(digits[i+1] == digits[i] - 1 for i in range(3)):
            score = 60
        else:
            score = 20
    
    return score

def get_double_triple_quad_scores(n):
    """คะแนนสำหรับเลขซ้ำ 2, 3, 4 ตัว"""
    double_score = 0
    triple_score = 0
    quad_score = 0
    
    # Count doubles
    for i in range(len(n) - 1):
        if n[i] == n[i+1]:
            double_score += 5
            if n[i] in '56899':  # Power digit
                double_score += 5
    
    # Count triples
    for i in range(len(n) - 2):
        if n[i] == n[i+1] == n[i+2]:
            triple_score += 20
            if n[i] in '56899':
                triple_score += 10
    
    # Count quads
    for i in range(len(n) - 3):
        if n[i] == n[i+1] == n[i+2] == n[i+3]:
            quad_score += 50
            if n[i] in '56899':
                quad_score += 25
    
    return double_score, triple_score, quad_score

def analyze_digit_positions_advanced(n, digit):
    """วิเคราะห์ตำแหน่งของตัวเลขแบบละเอียด"""
    positions = [i for i, d in enumerate(n) if d == str(digit)]
    
    if not positions:
        return {
            'count': 0,
            'first_pos': -1,
            'last_pos': -1,
            'spread': 0,
            'clustering': 0,
            'in_end': 0
        }
    
    spread = positions[-1] - positions[0] if len(positions) > 1 else 0
    clustering = sum(1 for i in range(len(positions)-1) if positions[i+1] - positions[i] == 1)
    in_end = 1 if any(p >= 6 for p in positions) else 0
    
    return {
        'count': len(positions),
        'first_pos': positions[0],
        'last_pos': positions[-1],
        'spread': spread,
        'clustering': clustering,
        'in_end': in_end
    }

# ====================================================================================
# HELPER FUNCTION FOR REPEATING PATTERN (if not in other parts)
# ====================================================================================

def has_repeating_pattern(n, length=2):
    """ตรวจสอบว่ามี pattern ซ้ำหรือไม่"""
    for i in range(len(n) - length * 2 + 1):
        pattern = n[i:i+length]
        if pattern == n[i+length:i+length*2]:
            return 1
    return 0

# ====================================================================================
# MARKET ANALYSIS FEATURES
# ====================================================================================

def calculate_market_price_features(n, market_stats=None):
    """คำนวณ features ที่เกี่ยวกับราคาตลาด"""
    if market_stats is None:
        # Default market statistics
        market_stats = {
            'avg_price_by_ending': {
                '8888': 50000, '9999': 45000, '888': 20000,
                '999': 18000, '88': 5000, '99': 4500
            },
            'avg_price_by_pattern': {
                'quad': 30000, 'triple': 15000, 'double': 8000
            }
        }
    
    features = {}
    
    # Expected price based on ending
    last_4 = n[-4:]
    last_3 = n[-3:]
    last_2 = n[-2:]
    
    expected_price = 1000  # Base price
    
    if last_4 in market_stats['avg_price_by_ending']:
        expected_price = market_stats['avg_price_by_ending'][last_4]
    elif last_3 in market_stats['avg_price_by_ending']:
        expected_price = market_stats['avg_price_by_ending'][last_3]
    elif last_2 in market_stats['avg_price_by_ending']:
        expected_price = market_stats['avg_price_by_ending'][last_2]
    
    features['expected_market_price'] = expected_price
    
    # Price tier
    if expected_price >= 30000:
        features['price_tier'] = 5
    elif expected_price >= 15000:
        features['price_tier'] = 4
    elif expected_price >= 8000:
        features['price_tier'] = 3
    elif expected_price >= 3000:
        features['price_tier'] = 2
    else:
        features['price_tier'] = 1
    
    return features

print("✅ Features Part 4 loaded successfully!")
print("   This file contains all missing feature functions")
print("   Total new functions: 40+")

"""
Feature Engineering for Phone Number Price Prediction (Part 3)
By Alex - World-Class AI Expert

Main feature creation functions and complete feature pipeline
"""

# ====================================================================================
# MAIN FEATURE CREATION FUNCTION
# ====================================================================================

def create_masterpiece_features(df, market_stats=None):
    """
    สร้าง features ทั้งหมดสำหรับ DataFrame
    Enhanced Features v4.0 - Masterpiece Edition
    Target: R² > 0.90
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with phone_number column
    market_stats : dict, optional
        Market statistics from training data
    """
    print("\n🔧 Creating Masterpiece Features v4.0...")
    print("   Target: 250+ High-Quality Features")
    
    # Validate input
    if 'phone_number' not in df.columns:
        raise ValueError("DataFrame must contain 'phone_number' column")
    
    # Create a copy to avoid modifying original
    df = df.copy()
    
    # ============ Basic Features ============
    print("\n   📊 Creating Basic Features...")
    df['digit_sum'] = df['phone_number'].apply(get_digit_sum)
    df['unique_digits'] = df['phone_number'].apply(get_unique_digits)
    df['max_consecutive'] = df['phone_number'].apply(get_max_consecutive_digit)
    df['has_pattern_2'] = df['phone_number'].apply(lambda x: has_repeating_pattern(x, 2))
    df['has_pattern_3'] = df['phone_number'].apply(lambda x: has_repeating_pattern(x, 3))
    df['good_digit_count'] = df['phone_number'].apply(get_good_digit_count)
    df['bad_digit_count'] = df['phone_number'].apply(get_bad_digit_count)
    df['premium_pair_count'] = df['phone_number'].apply(get_premium_pair_count)
    df['ending_score'] = df['phone_number'].apply(get_ending_score)
    df['sequence_score'] = df['phone_number'].apply(get_sequence_score)
    df['has_triple'] = df['phone_number'].apply(has_triple_repeat)
    df['has_quad'] = df['phone_number'].apply(has_quad_repeat)
    df['ascending_count'] = df['phone_number'].apply(get_ascending_count)
    df['descending_count'] = df['phone_number'].apply(get_descending_count)
    df['mirror_pattern'] = df['phone_number'].apply(has_mirror_pattern)
    df['complexity_score'] = df['phone_number'].apply(get_complexity_score)
    df['power_sum'] = df['phone_number'].apply(get_power_sum)
    df['special_lucky_score'] = df['phone_number'].apply(get_special_lucky_score)
    df['mystical_pair_score'] = df['phone_number'].apply(get_mystical_pair_score)
    df['has_forbidden'] = df['phone_number'].apply(has_forbidden_pair)
    
    # Digit frequency features
    for digit in range(10):
        df[f'count_{digit}'] = df['phone_number'].apply(lambda x: x.count(str(digit)))
    
    # Power features for each position
    for i in range(10):
        df[f'pos_{i}_power'] = df['phone_number'].apply(
            lambda x: CONFIG['POWER_WEIGHTS'].get(x[i], 0)
        )
    
    # ============ Advanced Features v3.0 ============
    print("   📊 Creating Advanced Features v3.0...")
    df['sum_diff_halves'] = df['phone_number'].apply(get_sum_diff_halves)
    df['num_peaks'] = df['phone_number'].apply(get_num_peaks)
    df['num_valleys'] = df['phone_number'].apply(get_num_valleys)
    df['longest_increasing'] = df['phone_number'].apply(get_longest_increasing_subsequence)
    df['digit_entropy'] = df['phone_number'].apply(get_digit_entropy)
    df['run_length_encoding'] = df['phone_number'].apply(get_run_length_encoding_size)
    df['digit_distance_sum'] = df['phone_number'].apply(get_digit_distance_sum)
    df['unique_ratio'] = df['phone_number'].apply(get_unique_digit_ratio)
    df['has_arithmetic_seq'] = df['phone_number'].apply(has_arithmetic_sequence)
    df['num_unique_pairs'] = df['phone_number'].apply(get_num_unique_pairs)
    df['num_unique_triplets'] = df['phone_number'].apply(get_num_unique_triplets)
    df['num_unique_no_zero'] = df['phone_number'].apply(
        lambda x: len(set(x.replace('0', '')))
    )
    df['power_digit_ratio'] = df['phone_number'].apply(
        lambda x: sum(1 for d in x if d in '56899') / len(x)
    )
    df['weighted_power_score'] = df['phone_number'].apply(
        lambda x: sum(int(d) * CONFIG['POWER_WEIGHTS'].get(d, 0) for d in x)
    )
    
    # ============ Features จาก v2.0 ============
    df['digit_variance'] = df['phone_number'].apply(get_digit_variance)
    df['alternating_pattern_score'] = df['phone_number'].apply(get_alternating_pattern_score)
    df['ascending_sequences'] = df['phone_number'].apply(get_ascending_sequences)
    df['descending_sequences'] = df['phone_number'].apply(get_descending_sequences)
    df['has_repeated_block_2'] = df['phone_number'].apply(has_repeated_block)
    df['has_repeated_block_3'] = df['phone_number'].apply(lambda x: has_repeated_block(x, 3))
    df['max_consecutive_same'] = df['phone_number'].apply(get_max_consecutive_same)
    df['symmetry_score'] = df['phone_number'].apply(get_symmetry_score)
    df['has_lucky_combo'] = df['phone_number'].apply(has_lucky_combo)
    
    # Position-based features
    df['first_4_sum'] = df['phone_number'].apply(lambda x: sum(int(d) for d in x[:4]))
    df['middle_2_sum'] = df['phone_number'].apply(lambda x: sum(int(d) for d in x[4:6]))
    df['last_4_sum'] = df['phone_number'].apply(lambda x: sum(int(d) for d in x[6:]))
    df['middle_section_power'] = df['phone_number'].apply(analyze_middle_section)
    df['max_ending_score'] = df['phone_number'].apply(analyze_ending_pattern)
    
    # Double, Triple, Quad scores
    for i, (name, scores) in enumerate([('double', get_double_triple_quad_scores),
                                        ('triple', get_double_triple_quad_scores),
                                        ('quad', get_double_triple_quad_scores)]):
        df[f'{name}_score'] = df['phone_number'].apply(lambda x: scores(x)[i])
    
    # Position-based analysis for each digit
    for digit in range(10):
        analysis = df['phone_number'].apply(lambda x: analyze_digit_positions_advanced(x, digit))
        df[f'digit_{digit}_count'] = [a['count'] for a in analysis]
        df[f'digit_{digit}_spread'] = [a['spread'] for a in analysis]
        df[f'digit_{digit}_in_end'] = [a['in_end'] for a in analysis]
    
    # ============ Master Features v4.0 ============
    print("   🏆 Creating Master Features v4.0...")
    df['position_weights'] = df['phone_number'].apply(get_position_weights)
    df['ending_pattern_type'] = df['phone_number'].apply(get_ending_pattern_type)
    df['prefix_score'] = df['phone_number'].apply(get_prefix_score)
    df['middle_pattern_score'] = df['phone_number'].apply(get_middle_pattern_score)
    df['weighted_sum_score'] = df['phone_number'].apply(get_weighted_sum_score)
    df['special_to_power_ratio'] = df['phone_number'].apply(get_special_to_normal_ratio)
    df['power_to_sum_ratio'] = df['phone_number'].apply(get_power_to_sum_ratio)
    df['ending_power_concentration'] = df['phone_number'].apply(get_ending_power_concentration)
    df['negative_pairs_count'] = df['phone_number'].apply(get_negative_pairs_count)
    df['investment_grade_score'] = df['phone_number'].apply(get_investment_grade_score)
    df['market_tier_score'] = df['phone_number'].apply(get_market_tier_score)
    df['has_triple_power'] = df['phone_number'].apply(has_triple_power_digit)
    df['position_weighted_score'] = df['phone_number'].apply(calculate_position_weighted_score)
    df['ending_power_score'] = df['phone_number'].apply(calculate_ending_power_score)
    df['mirror_score'] = df['phone_number'].apply(calculate_mirror_score)
    df['number_balance'] = df['phone_number'].apply(calculate_number_balance)
    df['famous_sequence_score'] = df['phone_number'].apply(calculate_famous_sequence_score)
    df['famous_sequence_score_advanced'] = df['phone_number'].apply(calculate_famous_sequence_score_advanced)
    df['wave_pattern'] = df['phone_number'].apply(get_wave_pattern_score)
    df['rarity_score'] = df['phone_number'].apply(calculate_rarity_score)
    df['mathematical_beauty_score'] = df['phone_number'].apply(get_mathematical_beauty_score)
    df['abc_position_score_advanced'] = df['phone_number'].apply(calculate_abc_position_score_advanced)
    
    # ============ Special Features v5.0 ============
    print("   ✨ Creating Special Features v5.0...")
    df['special_lucky_score_advanced'] = df['phone_number'].apply(get_special_lucky_score_advanced)
    df['market_demand_score'] = df['phone_number'].apply(calculate_market_demand_score)
    df['tier_classification_score'] = df['phone_number'].apply(get_tier_classification_score)
    
    # ============ Market-based Features (No Data Leakage) ============
    if market_stats is not None:
        print("   📊 Creating Market Features from Training Statistics...")
        
        # Apply market features using training statistics
        def create_market_features_for_row(phone_number):
            features = {}
            
            # Ending patterns
            for length in [4, 3, 2]:
                ending = phone_number[-length:]
                if ending in market_stats.get('avg_prices', {}):
                    features[f'market_avg_price_{length}'] = market_stats['avg_prices'][ending]
                else:
                    features[f'market_avg_price_{length}'] = market_stats.get('global_median', 5000)
            
            # Pattern popularity
            popularity_sum = 0
            for length in [4, 3, 2]:
                ending = phone_number[-length:]
                if ending in market_stats.get('popularity', {}):
                    popularity_sum += market_stats['popularity'][ending]
            features['market_popularity_score'] = popularity_sum
            
            return pd.Series(features)
        
        # Apply to all rows
        market_features = df['phone_number'].apply(create_market_features_for_row)
        df = pd.concat([df, market_features], axis=1)
    else:
        # Default values if no market stats
        print("   ⚠️ No market statistics provided - using defaults")
        df['market_avg_price_4'] = 5000
        df['market_avg_price_3'] = 5000
        df['market_avg_price_2'] = 5000
        df['market_popularity_score'] = 0

    # Power interaction features
    df['power_x_sum'] = df['power_sum'] * df['digit_sum']
    df['power_x_unique'] = df['power_sum'] * df['unique_digits']
    df['power_x_ending'] = df['power_sum'] * df['ending_score']
    df['lucky_x_ending'] = df['special_lucky_score'] * df['ending_score']
    
    # Ratio features
    df['good_to_bad_ratio'] = df['good_digit_count'] / (df['bad_digit_count'] + 1)
    df['special_to_total_ratio'] = df['special_lucky_score'] / (df['digit_sum'] + 1)
    df['ending_to_total_ratio'] = df['ending_score'] / (df['sequence_score'] + df['ending_score'] + 1)
    
    # Complex interaction features
    df['complexity_x_power'] = df['complexity_score'] * df['power_sum']
    df['rarity_x_demand'] = df['rarity_score'] * df['market_demand_score']
    df['beauty_x_balance'] = df['mathematical_beauty_score'] * df['number_balance']
    
    # Categorical features - encode and drop string columns
    df['ending_pattern_encoded'] = pd.Categorical(df['ending_pattern_type']).codes
    df.drop('ending_pattern_type', axis=1, inplace=True)  # Remove string column
    df['complexity_class'] = pd.cut(
        df['complexity_score'],
        bins=[-20, -5, 0, 5, 10, 20],
        labels=False  # Use numeric labels instead of strings
    )

    # Market-based features
    df['estimated_tier'] = pd.cut(
        df['tier_classification_score'],
        bins=[0, 100, 300, 600, 1000, float('inf')],
        labels=False  # Use numeric labels instead of strings
    )
    
    # Polynomial features for key variables
    df['ending_score_squared'] = df['ending_score'] ** 2
    df['power_sum_squared'] = df['power_sum'] ** 2
    df['special_lucky_score_squared'] = df['special_lucky_score'] ** 2
    df['rarity_score_squared'] = df['rarity_score'] ** 2
    
    # Log transformations for skewed features
    df['log_ending_score'] = np.log1p(df['ending_score'])
    df['log_sequence_score'] = np.log1p(df['sequence_score'])
    df['log_tier_score'] = np.log1p(df['tier_classification_score'])
    
    # ============ Final Premium Score v4.0 ============
    print("   🎯 Calculating Final Premium Score v4.0...")
    df['final_premium_score_v4'] = (
        df['ending_power_score'] * 3.0 +
        df['famous_sequence_score_advanced'] * 2.5 +
        df['special_lucky_score_advanced'] * 2.0 +
        df['rarity_score'] * 2.0 +
        df['mathematical_beauty_score'] * 1.5 +
        df['market_demand_score'] * 1.5 +
        df['position_weighted_score'] * 1.0 +
        df['abc_position_score_advanced'] * 0.8 +
        df['wave_pattern'] * 0.5 +
        df['number_balance'] * 0.3
    )
    
    # Drop phone_number column if it exists
    if 'phone_number' in df.columns:
        df = df.drop('phone_number', axis=1)

    # Drop price column if it exists (for feature creation)
    if 'price' in df.columns:
        df = df.drop('price', axis=1)

    # 🔴 CRITICAL: Drop sample_weight (causes data leakage!)
    # sample_weight is calculated from price → must NOT be a feature
    if 'sample_weight' in df.columns:
        df = df.drop('sample_weight', axis=1)
        print("   ⚠️  Removed 'sample_weight' feature (data leakage prevention)")

    print(f"\n✅ Created {len(df.columns)} features successfully!")

    return df

# ====================================================================================
# WRAPPER FUNCTION FOR COMPLETE PIPELINE
# ====================================================================================

def create_all_features(df_cleaned, market_stats=None):
    """
    Create all features from cleaned dataframe
    
    Parameters:
    -----------
    df_cleaned : pd.DataFrame
        Cleaned dataframe with 'phone_number' and 'price' columns
    market_stats : dict, optional
        Market statistics from training data only
    
    Returns:
    --------
    X : pd.DataFrame
        Feature matrix
    y : pd.Series
        Target variable (log-transformed)
    sample_weights : np.array
        Sample weights based on price distribution
    """
    print("\n" + "="*100)
    print("🔧 FEATURE ENGINEERING PIPELINE")
    print("="*100)
    
    # Create features
    features_df = create_masterpiece_features(df_cleaned, market_stats)
    
    # Prepare target variable
    y = np.log1p(df_cleaned['price'])  # Log transform
    
    # Get sample weights (already calculated from training data)
    if 'sample_weight' in df_cleaned.columns:
        sample_weights = df_cleaned['sample_weight'].values
        print("\n📊 Using pre-calculated sample weights")
    else:
        # Fallback to simple weights
        print("\n📊 Creating simple sample weights...")
        sample_weights = np.ones(len(df_cleaned))
    
    print(f"\n✅ Feature engineering completed!")
    print(f"   - Features: {features_df.shape[1]}")
    print(f"   - Samples: {features_df.shape[0]}")
    print(f"   - Target range: {y.min():.2f} - {y.max():.2f}")
    
    return features_df, y, sample_weights

# ====================================================================================
# FEATURE VALIDATION AND TESTING
# ====================================================================================

def validate_features(df, phase="unknown"):
    """Validate feature DataFrame"""
    print(f"\n🔍 Validating features ({phase})...")
    
    # Check for NaN
    nan_counts = df.isna().sum()
    if nan_counts.sum() > 0:
        print(f"⚠️ Found NaN values in {nan_counts[nan_counts > 0].shape[0]} features")
    else:
        print("✅ No NaN values found")
    
    # Check for infinite values
    inf_counts = np.isinf(df.select_dtypes(include=[np.number])).sum()
    if inf_counts.sum() > 0:
        print(f"⚠️ Found infinite values in {inf_counts[inf_counts > 0].shape[0]} features")
    else:
        print("✅ No infinite values found")
    
    # Check feature statistics
    print(f"\n📊 Feature statistics:")
    print(f"   - Total features: {df.shape[1]}")
    print(f"   - Numeric features: {df.select_dtypes(include=[np.number]).shape[1]}")
    print(f"   - Categorical features: {df.select_dtypes(include=['object', 'category']).shape[1]}")
    
    return df

def quick_feature_test(phone_number):
    """Quick test for a single phone number"""
    test_df = pd.DataFrame([{'phone_number': phone_number, 'price': 0}])
    features = create_masterpiece_features(test_df)
    
    print(f"\n📱 Quick test for: {phone_number}")
    print(f"   - Total features: {len(features.columns)}")
    print(f"   - Final premium score: {features['final_premium_score_v4'].iloc[0]:.2f}")
    print(f"   - Top 5 feature values:")
    
    top_features = features.iloc[0].nlargest(5)
    for feat, val in top_features.items():
        print(f"     - {feat}: {val:.2f}")
    
    return features
