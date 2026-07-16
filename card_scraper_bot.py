import os
import requests
import random
import time
import json
from faker import Faker
from keep_alive import live
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

fake = Faker()

# Get from environment variables
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8930858218:AAEmJWZOfCAq7Ct722mQ08nLoJgPcJ3zuO4')
CHAT_ID = int(os.environ.get('CHAT_ID', -1004498162623))

# ============ CARD BINS BY TYPE ============

# VISA BINS (Start with 4)
VISA_BINS = [
    '4532', '4539', '4556', '4916', '4929', '4484', '4716', '4026', '4175',
    '4266', '4284', '4310', '4338', '4383', '4405', '4420', '4445', '4462',
    '4486', '4506', '4518', '4537', '4544', '4557', '4564', '4573', '4596',
    '4617', '4627', '4645', '4660', '4674', '4688', '4700', '4720', '4730',
    '4740', '4751', '4761', '4785', '4796', '4800', '4815', '4828', '4844',
    '4850', '4862', '4873', '4885', '4897', '4900', '4910', '4920', '4930',
    '4940', '4950', '4960', '4970', '4980', '4990'
]

# MASTERCARD BINS (Start with 5)
MASTERCARD_BINS = [
    '5221', '5223', '5230', '5234', '5244', '5250', '5254', '5260',
    '5263', '5270', '5273', '5280', '5285', '5290', '5299', '5300',
    '5322', '5330', '5340', '5350', '5360', '5370', '5380', '5390',
    '5400', '5410', '5420', '5430', '5440', '5450', '5460', '5470',
    '5480', '5490', '5500', '5510', '5520', '5530', '5540', '5550',
    '5560', '5570', '5580', '5590', '5600', '5610', '5620', '5630',
    '5640', '5650', '5660', '5670', '5680', '5690', '5700', '5710',
    '5720', '5730', '5740', '5750', '5760', '5770', '5780', '5790',
    '5800', '5810', '5820', '5830', '5840', '5850', '5860', '5870',
    '5880', '5890', '5900', '5910', '5920', '5930', '5940', '5950',
    '5960', '5970', '5980', '5990'
]

# AMERICAN EXPRESS BINS (Start with 34, 37)
AMEX_BINS = [
    '3400', '3401', '3402', '3403', '3404', '3405', '3406', '3407', '3408', '3409',
    '3410', '3411', '3412', '3413', '3414', '3415', '3416', '3417', '3418', '3419',
    '3420', '3421', '3422', '3423', '3424', '3425', '3426', '3427', '3428', '3429',
    '3430', '3431', '3432', '3433', '3434', '3435', '3436', '3437', '3438', '3439',
    '3440', '3441', '3442', '3443', '3444', '3445', '3446', '3447', '3448', '3449',
    '3450', '3451', '3452', '3453', '3454', '3455', '3456', '3457', '3458', '3459',
    '3460', '3461', '3462', '3463', '3464', '3465', '3466', '3467', '3468', '3469',
    '3470', '3471', '3472', '3473', '3474', '3475', '3476', '3477', '3478', '3479',
    '3480', '3481', '3482', '3483', '3484', '3485', '3486', '3487', '3488', '3489',
    '3490', '3491', '3492', '3493', '3494', '3495', '3496', '3497', '3498', '3499',
    '3700', '3701', '3702', '3703', '3704', '3705', '3706', '3707', '3708', '3709',
    '3710', '3711', '3712', '3713', '3714', '3715', '3716', '3717', '3718', '3719',
    '3720', '3721', '3722', '3723', '3724', '3725', '3726', '3727', '3728', '3729',
    '3730', '3731', '3732', '3733', '3734', '3735', '3736', '3737', '3738', '3739',
    '3740', '3741', '3742', '3743', '3744', '3745', '3746', '3747', '3748', '3749',
    '3750', '3751', '3752', '3753', '3754', '3755', '3756', '3757', '3758', '3759',
    '3760', '3761', '3762', '3763', '3764', '3765', '3766', '3767', '3768', '3769',
    '3770', '3771', '3772', '3773', '3774', '3775', '3776', '3777', '3778', '3779',
    '3780', '3781', '3782', '3783', '3784', '3785', '3786', '3787', '3788', '3789'
]

# DISCOVER BINS (Start with 6011, 65)
DISCOVER_BINS = [
    '6011', '6012', '6013', '6014', '6015', '6016', '6017', '6018', '6019',
    '6221', '6222', '6223', '6224', '6225', '6226', '6227', '6228', '6229',
    '6230', '6231', '6232', '6233', '6234', '6235', '6236', '6237', '6238', '6239',
    '6240', '6241', '6242', '6243', '6244', '6245', '6246', '6247', '6248', '6249',
    '6250', '6251', '6252', '6253', '6254', '6255', '6256', '6257', '6258', '6259',
    '6260', '6261', '6262', '6263', '6264', '6265', '6266', '6267', '6268', '6269',
    '6270', '6271', '6272', '6273', '6274', '6275', '6276', '6277', '6278', '6279',
    '6280', '6281', '6282', '6283', '6284', '6285', '6286', '6287', '6288', '6289',
    '6290', '6291', '6292', '6293', '6294', '6295', '6296', '6297', '6298', '6299',
    '6500', '6501', '6502', '6503', '6504', '6505', '6506', '6507', '6508', '6509'
]

# ============ HIGH-HIT BINS (Prioritized) ============
HIGH_HIT_BINS = {
    'Visa': ['4532', '4539', '4556', '4916', '4929', '4484', '4716', '4026', '4175'],
    'Mastercard': ['5221', '5223', '5230', '5234', '5244', '5250', '5254', '5260', '5263'],
    'Amex': ['3400', '3700', '3714', '3727', '3766', '3780', '3401', '3701'],
    'Discover': ['6011', '6221', '6222', '6223', '6224', '6225', '6500', '6501']
}

# ============ CARD CONFIGURATION ============
CARD_CONFIG = {
    'Visa': {
        'prefix': '4',
        'length': 16,
        'cvv_length': 3,
        'levels': ['Classic', 'Gold', 'Platinum', 'Signature', 'Infinite', 'Black'],
        'emoji': '💳',
        'color': '🔵'
    },
    'Mastercard': {
        'prefix': '5',
        'length': 16,
        'cvv_length': 3,
        'levels': ['Standard', 'Gold', 'Platinum', 'World', 'World Elite', 'Black'],
        'emoji': '💳',
        'color': '🔴'
    },
    'Amex': {
        'prefix': ['34', '37'],
        'length': 15,
        'cvv_length': 4,
        'levels': ['Green', 'Gold', 'Platinum', 'Centurion', 'Black'],
        'emoji': '💎',
        'color': '🟣'
    },
    'Discover': {
        'prefix': ['6011', '65'],
        'length': 16,
        'cvv_length': 3,
        'levels': ['Standard', 'Gold', 'Platinum', 'Miles', 'Black'],
        'emoji': '🌟',
        'color': '🟠'
    }
}

# Premium banks
PREMIUM_BANKS = [
    'Chase', 'Citibank', 'Bank of America', 'Wells Fargo', 
    'Capital One', 'US Bank', 'PNC Bank', 'TD Bank',
    'HSBC', 'Barclays', 'Goldman Sachs', 'Morgan Stanley',
    'JPMorgan Chase', 'Fifth Third Bank', 'KeyBank',
    'American Express', 'Discover Bank', 'Synchrony Bank'
]

def generate_card_number(card_type):
    """Generate card number based on card type"""
    config = CARD_CONFIG[card_type]
    
    # Choose BIN
    if random.random() < 0.7:  # 70% chance of high-hit
        bin_prefix = random.choice(HIGH_HIT_BINS[card_type])
    else:
        if card_type == 'Visa':
            bin_prefix = random.choice(VISA_BINS)
        elif card_type == 'Mastercard':
            bin_prefix = random.choice(MASTERCARD_BINS)
        elif card_type == 'Amex':
            bin_prefix = random.choice(AMEX_BINS)
        else:  # Discover
            bin_prefix = random.choice(DISCOVER_BINS)
    
    length = config['length']
    
    # Build card number
    body = bin_prefix + ''.join([str(random.randint(0, 9)) for _ in range(length - len(bin_prefix) - 1)])
    
    # Luhn algorithm
    digits = [int(d) for d in body]
    for i in range(len(digits) - 2, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    total_sum = sum(digits)
    check_digit = (10 - (total_sum % 10)) % 10
    
    return body + str(check_digit)

def generate_card():
    """Generate complete card with all details"""
    # Randomly select card type with weights
    card_type = random.choices(
        ['Visa', 'Mastercard', 'Amex', 'Discover'],
        weights=[35, 30, 20, 15],
        k=1
    )[0]
    
    config = CARD_CONFIG[card_type]
    card_number = generate_card_number(card_type)
    
    # Generate expiry
    month = str(random.randint(1, 12)).zfill(2)
    year = str(random.randint(27, 38)).zfill(2)
    
    # Generate CVV
    cvv_length = config['cvv_length']
    cvv = ''.join([str(random.randint(0, 9)) for _ in range(cvv_length)])
    
    # Generate card level (premium weighted)
    levels = config['levels']
    weights = [5, 10, 20, 25, 25, 15] if len(levels) >= 6 else [5, 15, 25, 30, 25]
    level = random.choices(levels, weights=weights[:len(levels)], k=1)[0]
    
    # Generate holder name
    holder = fake.name()
    
    # Get BIN info
    bin_number = card_number[:6]
    card_info = get_bin_info(bin_number, card_type)
    
    return {
        'card_number': card_number,
        'month': month,
        'year': year,
        'cvv': cvv,
        'card_type': card_type,
        'bin': bin_number,
        'level': level,
        'holder': holder,
        'bank': card_info['bank'],
        'country': card_info['country'],
        'country_name': card_info['country_name'],
        'country_flag': card_info['country_flag'],
        'type': card_info['type'],
        'is_high_hit': any(card_number.startswith(bin) for bin in HIGH_HIT_BINS[card_type]),
        'is_premium': level in ['Platinum', 'Signature', 'World Elite', 'Centurion', 'Black', 'Infinite']
    }

def get_bin_info(bin_number, card_type):
    """Get BIN information"""
    try:
        response = requests.get(f"https://bins.antipublic.cc/bins/{bin_number}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('brand'):
                return {
                    'bank': data.get('bank', random.choice(PREMIUM_BANKS)),
                    'country': data.get('country', 'US'),
                    'country_name': data.get('country_name', 'United States'),
                    'country_flag': data.get('country_flag', '🇺🇸'),
                    'type': data.get('type', 'Credit')
                }
    except:
        pass
    
    # Fallback
    return {
        'bank': random.choice(PREMIUM_BANKS),
        'country': 'US',
        'country_name': 'United States',
        'country_flag': '🇺🇸',
        'type': 'Credit'
    }

def luhn_check(card_number):
    """Verify card number using Luhn algorithm"""
    digits = [int(d) for d in card_number]
    for i in range(len(digits) - 2, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    return sum(digits) % 10 == 0

def get_card_emoji(card_type, level):
    """Get appropriate emoji for card"""
    emojis = {
        'Visa': '💳',
        'Mastercard': '💳',
        'Amex': '💎',
        'Discover': '🌟'
    }
    
    premium_emojis = {
        'Platinum': '⚡',
        'Signature': '👑',
        'World Elite': '🌍',
        'Centurion': '💠',
        'Black': '🖤',
        'Infinite': '♾️'
    }
    
    emoji = emojis.get(card_type, '💳')
    if level in premium_emojis:
        emoji = premium_emojis[level]
    
    return emoji

def get_card_icon(card_type):
    """Get card type icon"""
    icons = {
        'Visa': '4️⃣',
        'Mastercard': '5️⃣',
        'Amex': '💎',
        'Discover': '🌟'
    }
    return icons.get(card_type, '💳')

def send_card_to_telegram(card_data, index, total_cards):
    """Send card with premium UI"""
    telegram_api = f'https://api.telegram.org/bot{BOT_TOKEN}'
    
    card_details = f"{card_data['card_number']}|{card_data['month']}|{card_data['year']}|{card_data['cvv']}"
    
    # Determine status badges
    if card_data['is_high_hit']:
        status = "🔥 HIGH HIT"
        status_emoji = "⚡"
    elif card_data['is_premium']:
        status = "💎 PREMIUM"
        status_emoji = "👑"
    else:
        status = "✅ APPROVED"
        status_emoji = "✔️"
    
    # Card type icon
    card_icon = get_card_icon(card_data['card_type'])
    card_emoji = get_card_emoji(card_data['card_type'], card_data['level'])
    
    # Premium styling
    reply_markup = {
        "inline_keyboard": [
            [
                {"text": "OWNER", "url": "https://t.me/"},
                {"text": "CHANNEL", "url": "https://t.me/approvedcc7"},
            ]
        ]
    }
    
    # Format card number with spaces for better readability
    card_display = card_data['card_number']
    if len(card_display) == 16:
        card_display = ' '.join([card_display[i:i+4] for i in range(0, 16, 4)])
    elif len(card_display) == 15:
        card_display = ' '.join([card_display[i:i+4] for i in range(0, 12, 4)] + [card_display[12:]])
    
    # Build premium message
    message = (
        f"\n"
        f" 𝗖𝗔𝗥𝗗 𝗦𝗖𝗥𝗔𝗣𝗘𝗥 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 🔥\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"<b>⌖ 𝗖𝗮𝗿𝗱 ⤳</b> <code>{card_details}</code>\n"
        f"<b>⌖ 𝗙𝗼𝗿𝗺𝗮𝘁𝘁𝗲𝗱 ⤳</b> <code>{card_display}</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"<b>⌮ 𝗧𝘆𝗽𝗲 ⤳</b>  <code>{card_icon} {card_data['card_type']}</code>\n"
        f"<b>⌮ 𝗦𝘁𝗮𝘁𝘂𝘀 ⤳</b>  <code>{status_emoji} {status}</code>\n"
        f"<b>⌮ 𝗟𝗲𝘃𝗲𝗹 ⤳</b>  <code>{card_emoji} {card_data['level']}</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"<b>⌮ 𝗕𝗮𝗻𝗸 ⤳</b>  <code>{card_data['bank']}</code>\n"
        f"<b>⌮ 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 ⤳</b>  <code>{card_data['country_name']} {card_data['country_flag']}</code>\n"
        f"<b>⌮ 𝗛𝗼𝗹𝗱𝗲𝗿 ⤳</b>  <code>{card_data['holder']}</code>\n"
        f"<b>⌮ 𝗕𝗜𝗡 ⤳</b>  <code>{card_data['bin']}</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📊 𝗦𝗰𝗿𝗮𝗽𝗲𝗱: {index}/{total_cards}\n"
        f"🏷️  {card_data['card_type']}  |  {card_data['level']}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"⚡ 𝗙𝗔𝗦𝗧 𝗦𝗖𝗥𝗔𝗣𝗘 𝗠𝗢𝗗𝗘 ⚡\n"
    )
    
    # Send with retry
    max_retries = 3
    for attempt in range(max_retries):
        try:
            data = {
                'chat_id': CHAT_ID,
                'text': message,
                'parse_mode': 'HTML',
                'reply_markup': json.dumps(reply_markup)
            }
            response = requests.post(f'{telegram_api}/sendMessage', data=data, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ Sent {card_data['card_type']}: {card_data['card_number'][:6]}xxxx ({card_data['level']})")
                return True
            elif response.status_code == 429:
                retry_after = response.json().get('parameters', {}).get('retry_after', 5)
                print(f"⏳ Rate limited, waiting {retry_after}s...")
                time.sleep(retry_after)
            else:
                print(f"❌ Error {response.status_code}")
                time.sleep(2)
        except Exception as e:
            print(f"❌ Attempt {attempt+1} failed: {e}")
            time.sleep(2)
    
    return False

def scrape_cards_fast(total_cards=100000):
    """Main scraper function - FAST MODE"""
    print("="*50)
    print("🚀 CARD SCRAPER BOT - FAST MODE")
    print("💳 Cards: Visa | Mastercard | Amex | Discover")
    print(f"🎯 Target: {total_cards} cards")
    print("🔥 High-hit BINs prioritized")
    print("⚡ Multi-threading enabled")
    print("="*50 + "\n")
    
    success_count = 0
    stats = {
        'Visa': 0,
        'Mastercard': 0,
        'Amex': 0,
        'Discover': 0,
        'HighHit': 0,
        'Premium': 0
    }
    
    # Use threading for faster generation
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        
        # Generate cards in batches
        batch_size = 50
        for i in range(0, total_cards, batch_size):
            current_batch = min(batch_size, total_cards - i)
            for _ in range(current_batch):
                futures.append(executor.submit(generate_card))
            
            # Process completed futures
            for future in as_completed(futures):
                card_data = future.result()
                index = len(futures)
                
                # Update stats
                stats[card_data['card_type']] += 1
                if card_data['is_high_hit']:
                    stats['HighHit'] += 1
                if card_data['is_premium']:
                    stats['Premium'] += 1
                
                # Send to Telegram
                if send_card_to_telegram(card_data, index, total_cards):
                    success_count += 1
                
                time.sleep(0.3)  # Small delay
            
            # Clear futures for next batch
            futures = []
            
            # Progress update
            progress = min(i + batch_size, total_cards)
            print(f"\n📊 Progress: {progress}/{total_cards} ({progress/total_cards*100:.1f}%)")
            print(f"✅ Success: {success_count}")
            print(f"💳 Visa: {stats['Visa']} | Mastercard: {stats['Mastercard']} | Amex: {stats['Amex']} | Discover: {stats['Discover']}")
            print(f"🔥 High-Hit: {stats['HighHit']} | 👑 Premium: {stats['Premium']}\n")
    
    # Final Summary
    print("\n" + "="*50)
    print("📊 SCRAPING COMPLETE")
    print(f"✅ Total cards scraped: {success_count}")
    print(f"💳 Visa: {stats['Visa']}")
    print(f"💳 Mastercard: {stats['Mastercard']}")
    print(f"💎 Amex: {stats['Amex']}")
    print(f"🌟 Discover: {stats['Discover']}")
    print(f"🔥 High-Hit: {stats['HighHit']}")
    print(f"👑 Premium: {stats['Premium']}")
    print(f"📈 Success rate: {success_count/total_cards*100:.1f}%")
    print("="*50)

def send_batch_cards(batch_count=5000):
    """Send cards in batches"""
    print("🚀 Starting batch scraper...")
    print(f"📦 Batch size: {batch_count} cards\n")
    
    total_generated = 0
    success_count = 0
    stats = {'Visa': 0, 'Mastercard': 0, 'Amex': 0, 'Discover': 0}
    
    while total_generated < batch_count:
        # Generate multiple cards at once
        batch_cards = []
        for _ in range(10):
            card_data = generate_card()
            batch_cards.append(card_data)
            total_generated += 1
            stats[card_data['card_type']] += 1
        
        # Send batch
        for card_data in batch_cards:
            if send_card_to_telegram(card_data, total_generated, batch_count):
                success_count += 1
            time.sleep(0.2)
        
        print(f"📊 Progress: {total_generated}/{batch_count} | ✅ {success_count}")
        print(f"💳 V:{stats['Visa']} M:{stats['Mastercard']} A:{stats['Amex']} D:{stats['Discover']}")
        
        if total_generated % 100 == 0:
            print(f"⏳ Cooling down...")
            time.sleep(2)
    
    print(f"\n✅ Batch complete! Sent {success_count} cards")

if __name__ == '__main__':
    # Start keep-alive server
    live()
    
    # Start scraping
    mode = os.environ.get('MODE', 'fast')
    
    if mode == 'batch':
        total = int(os.environ.get('TOTAL_CARDS', 5000))
        send_batch_cards(batch_count=total)
    else:
        total = int(os.environ.get('TOTAL_CARDS', 100000))
        scrape_cards_fast(total_cards=total)
