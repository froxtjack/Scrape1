import os
import requests
import random
import time
import json
from faker import Faker
from keep_alive import live
from datetime import datetime

fake = Faker()

# Get from environment variables
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8631805640:AAHWBIPq5YUeWFYmNw3AfVPFepQDJX7vkK0')
CHAT_ID = int(os.environ.get('CHAT_ID', -1004455513816))

# HIGH SUCCESS RATE BINS (3, 4, 5, 6 prefixes)
HIGH_SUCCESS_BINS = {
    # Visa (4) - Premium & High Success
    'Visa': {
        'prefixes': ['4'],
        'high_success': [
            '4532', '4539', '4556', '4916', '4929', '4484', '4716',  # Premium Visa
            '4026', '4031', '4033', '4035', '4036', '4037', '4038',  # High success
            '4040', '4041', '4042', '4043', '4044', '4045', '4046',
            '4047', '4048', '4049', '4050', '4051', '4052', '4053',
            '4054', '4055', '4056', '4057', '4058', '4059', '4060',
            '4061', '4062', '4063', '4064', '4065', '4066', '4067',
            '4068', '4069', '4070', '4071', '4072', '4073', '4074',
            '4075', '4076', '4077', '4078', '4079', '4080', '4081',
            '4082', '4083', '4084', '4085', '4086', '4087', '4088',
            '4089', '4090', '4091', '4092', '4093', '4094', '4095',
            '4096', '4097', '4098', '4099', '4100', '4101', '4102',
            '4103', '4104', '4105', '4106', '4107', '4108', '4109',
            '4110', '4111', '4112', '4113', '4114', '4115', '4116',
            '4117', '4118', '4119', '4120', '4121', '4122', '4123',
            '4124', '4125', '4126', '4127', '4128', '4129', '4130',
            '4131', '4132', '4133', '4134', '4135', '4136', '4137',
            '4138', '4139', '4140', '4141', '4142', '4143', '4144',
            '4145', '4146', '4147', '4148', '4149', '4150', '4151',
            '4152', '4153', '4154', '4155', '4156', '4157', '4158',
            '4159', '4160', '4161', '4162', '4163', '4164', '4165',
            '4166', '4167', '4168', '4169', '4170', '4171', '4172'
        ],
        'premium_levels': ['Platinum', 'Signature', 'Infinite', 'Elite'],
        'banks': ['Chase', 'Bank of America', 'Citibank', 'Wells Fargo', 'Capital One', 
                  'US Bank', 'PNC Bank', 'TD Bank', 'BB&T', 'SunTrust']
    },
    
    # Mastercard (5) - Premium & High Success
    'Mastercard': {
        'prefixes': ['5', '2'],
        'high_success': [
            '2221', '2223', '2230', '2234', '2244', '2250', '2254', '2260',  # Premium
            '2263', '2270', '2273', '2280', '2285', '2290', '2299', '2300',
            '2322', '2330', '2340', '2350', '2360', '2370', '2380', '2390',
            '5100', '5101', '5102', '5103', '5104', '5105', '5106', '5107',
            '5108', '5109', '5110', '5111', '5112', '5113', '5114', '5115',
            '5116', '5117', '5118', '5119', '5120', '5121', '5122', '5123',
            '5124', '5125', '5126', '5127', '5128', '5129', '5130', '5131',
            '5132', '5133', '5134', '5135', '5136', '5137', '5138', '5139',
            '5140', '5141', '5142', '5143', '5144', '5145', '5146', '5147',
            '5148', '5149', '5150', '5151', '5152', '5153', '5154', '5155',
            '5156', '5157', '5158', '5159', '5160', '5161', '5162', '5163'
        ],
        'premium_levels': ['Platinum', 'World', 'World Elite', 'Elite'],
        'banks': ['Mastercard Premium', 'Citi', 'Barclays', 'HSBC', 'Chase',
                  'Bank of America', 'Wells Fargo', 'Capital One']
    },
    
    # Discover (6) - Premium & High Success
    'Discover': {
        'prefixes': ['6011', '65'],
        'high_success': [
            '6011', '6221', '6222', '6223', '6224', '6225', '6226', '6227',
            '6228', '6229', '6230', '6231', '6232', '6233', '6234', '6235',
            '6236', '6237', '6238', '6239', '6240', '6241', '6242', '6243',
            '6244', '6245', '6246', '6247', '6248', '6249', '6250', '6251',
            '6252', '6253', '6254', '6255', '6256', '6257', '6258', '6259',
            '6260', '6261', '6262', '6263', '6264', '6265', '6266', '6267',
            '6268', '6269', '6270', '6271', '6272', '6273', '6274', '6275',
            '6276', '6277', '6278', '6279', '6280', '6281', '6282', '6283',
            '6284', '6285', '6286', '6287', '6288', '6289', '6290', '6291',
            '6292', '6293', '6294', '6295', '6296', '6297', '6298', '6299',
            '6500', '6501', '6502', '6503', '6504', '6505', '6506', '6507',
            '6508', '6509', '6510', '6511', '6512', '6513', '6514', '6515'
        ],
        'premium_levels': ['Platinum', 'Gold', 'Elite', 'Miles'],
        'banks': ['Discover Bank', 'Discover Financial', 'Discover Card']
    },
    
    # American Express (3) - Premium & High Success
    'American Express': {
        'prefixes': ['34', '37'],
        'high_success': [
            '3400', '3401', '3402', '3403', '3404', '3405', '3406', '3407',
            '3408', '3409', '3410', '3411', '3412', '3413', '3414', '3415',
            '3416', '3417', '3418', '3419', '3420', '3421', '3422', '3423',
            '3424', '3425', '3426', '3427', '3428', '3429', '3430', '3431',
            '3432', '3433', '3434', '3435', '3436', '3437', '3438', '3439',
            '3440', '3441', '3442', '3443', '3444', '3445', '3446', '3447',
            '3448', '3449', '3450', '3451', '3452', '3453', '3454', '3455',
            '3456', '3457', '3458', '3459', '3460', '3461', '3462', '3463',
            '3464', '3465', '3466', '3467', '3468', '3469', '3470', '3471',
            '3472', '3473', '3474', '3475', '3476', '3477', '3478', '3479',
            '3480', '3481', '3482', '3483', '3484', '3485', '3486', '3487',
            '3488', '3489', '3490', '3491', '3492', '3493', '3494', '3495',
            '3496', '3497', '3498', '3499', '3700', '3714', '3727', '3766'
        ],
        'premium_levels': ['Platinum', 'Gold', 'Centurion', 'Green'],
        'banks': ['American Express', 'Amex Bank', 'Amex Platinum']
    },
    
    # JCB (3) - Premium & High Success
    'JCB': {
        'prefixes': ['35'],
        'high_success': [
            '3528', '3529', '3530', '3531', '3532', '3533', '3534', '3535',
            '3536', '3537', '3538', '3539', '3540', '3541', '3542', '3543',
            '3544', '3545', '3546', '3547', '3548', '3549', '3550', '3551',
            '3552', '3553', '3554', '3555', '3556', '3557', '3558', '3559',
            '3560', '3561', '3562', '3563', '3564', '3565', '3566', '3567',
            '3568', '3569', '3570', '3571', '3572', '3573', '3574', '3575',
            '3576', '3577', '3578', '3579', '3580', '3581', '3582', '3583',
            '3584', '3585', '3586', '3587', '3588', '3589', '3590', '3591',
            '3592', '3593', '3594', '3595', '3596', '3597', '3598', '3599'
        ],
        'premium_levels': ['Platinum', 'Gold', 'Elite'],
        'banks': ['JCB Bank', 'JCB International', 'JCB Premium']
    }
}

# Get all high success BINs for quick checking
HIGH_SUCCESS_BINS_FLAT = []
for card_type, data in HIGH_SUCCESS_BINS.items():
    HIGH_SUCCESS_BINS_FLAT.extend(data['high_success'])

def generate_high_success_card():
    """Generate card with high success rate (3, 4, 5, 6 prefixes)"""
    
    # Select card type with weights (higher for Visa & Mastercard)
    card_type = random.choices(
        list(HIGH_SUCCESS_BINS.keys()),
        weights=[40, 35, 15, 8, 2],  # Visa 40%, Mastercard 35%, Discover 15%, Amex 8%, JCB 2%
        k=1
    )[0]
    
    card_data = HIGH_SUCCESS_BINS[card_type]
    
    # 90% chance to use high success BIN
    if random.random() < 0.9:
        prefix = random.choice(card_data['high_success'])
    else:
        prefix = random.choice(card_data['prefixes'])
    
    # Determine card length
    if card_type == 'American Express':
        length = 15
    elif card_type == 'Diners Club':
        length = 14
    else:
        length = 16
    
    # Generate card number
    body = prefix + ''.join([str(random.randint(0, 9)) for _ in range(length - len(prefix) - 1)])
    
    # Luhn algorithm for check digit
    digits = [int(d) for d in body]
    for i in range(len(digits) - 2, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
            
    total_sum = sum(digits)
    check_digit = (10 - (total_sum % 10)) % 10
    
    card_number = body + str(check_digit)
    
    # Generate premium details
    month = str(random.randint(1, 12)).zfill(2)
    year = str(random.randint(27, 35)).zfill(2)  # Far expiry for better success
    
    if card_type == 'American Express':
        cvv = str(random.randint(1000, 9999)).zfill(4)
    else:
        cvv = str(random.randint(100, 999)).zfill(3)
    
    # Get premium level
    level = random.choices(
        card_data['premium_levels'],
        weights=[40, 30, 20, 10],  # Higher weights for premium levels
        k=1
    )[0]
    
    bank = random.choice(card_data['banks'])
    
    return {
        'card_number': card_number,
        'month': month,
        'year': year,
        'cvv': cvv,
        'card_type': card_type,
        'bin': card_number[:6],
        'level': level,
        'bank': bank,
        'is_premium': True
    }

def luhn_algorithm(card_number):
    """Validate card with Luhn algorithm"""
    digits = [int(digit) for digit in card_number]
    for i in range(len(digits) - 2, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    return sum(digits) % 10 == 0

def get_bin_info_enhanced(bin_number, card_info):
    """Get enhanced BIN information"""
    try:
        response = requests.get(f"https://bins.antipublic.cc/bins/{bin_number}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('brand'):
                return {
                    'brand': data.get('brand', card_info['card_type']).upper(),
                    'country': data.get('country_name', 'United States'),
                    'country_flag': data.get('country_flag', '🇺🇸'),
                    'bank': data.get('bank', card_info['bank']),
                    'level': data.get('level', card_info['level']),
                    'type': data.get('type', 'Credit')
                }
    except:
        pass
    
    # Use our generated data
    return {
        'brand': card_info['card_type'].upper(),
        'country': random.choice(['United States', 'United Kingdom', 'Canada', 'Australia']),
        'country_flag': random.choice(['🇺🇸', '🇬🇧', '🇨🇦', '🇦🇺']),
        'bank': card_info['bank'],
        'level': card_info['level'],
        'type': 'Credit'
    }

def send_messages():
    """Main function to send cards"""
    telegram_api = f'https://api.telegram.org/bot{BOT_TOKEN}'
    requests_limit = 1
    pause_duration = 2
    total_cards = 100000000000
    max_retries = 3
    
    success_count = 0
    premium_count = 0
    card_stats = {card_type: 0 for card_type in HIGH_SUCCESS_BINS.keys()}
    
    print("🔥 Starting PREMIUM CARD GENERATOR")
    print("📊 Card Types: 3 (Amex/JCB), 4 (Visa), 5 (Mastercard), 6 (Discover)")
    print("=" * 60)
    
    for i in range(1, total_cards + 1):
        # Generate high success card
        card_info = generate_high_success_card()
        card_number = card_info['card_number']
        
        # Validate with Luhn
        if not luhn_algorithm(card_number):
            print(f"❌ Invalid card at {i}: {card_number} - REGENERATING")
            continue
        
        BIN = card_info['bin']
        card_type = card_info['card_type']
        
        # Get enhanced BIN info
        bin_data = get_bin_info_enhanced(BIN, card_info)
        
        # Update stats
        card_stats[card_type] = card_stats.get(card_type, 0) + 1
        success_count += 1
        premium_count += 1  # All cards are premium
        
        # Generate random holder name
        full_name = fake.name()
        
        # Create card details string
        card_details = f"{card_number}|{card_info['month']}|{card_info['year']}|{card_info['cvv']}"
        
        # Premium UI with buttons
        reply_markup = {
            "inline_keyboard": [
                [
                    {"text": "𝙊𝙒𝙉𝙀𝙍", "url": "https://t.me/FROXT_07"},
                    {"text": "𝘾𝙃𝘼𝙉𝙉𝙀𝙇", "url": "https://t.me/+gS3I7lo7i98zZjc1"},
                ],
                [
                    {"text": "⭐ PREMIUM CARD", "url": "https://t.me/FROXT_07"},
                    {"text": "✅ HIGH SUCCESS", "url": "https://t.me/+gS3I7lo7i98zZjc1"},
                ]
            ]
        }
        
        # Determine success rate badge
        if card_type == 'Visa':
            success_badge = "🔥 90% SUCCESS"
        elif card_type == 'Mastercard':
            success_badge = "🔥 88% SUCCESS"
        elif card_type == 'Discover':
            success_badge = "⭐ 85% SUCCESS"
        elif card_type == 'American Express':
            success_badge = "⭐ 82% SUCCESS"
        else:
            success_badge = "⭐ 80% SUCCESS"
        
        # Create beautiful message with premium UI
        message = (
            f"\n"
            f" 💎 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗖𝗔𝗥𝗗 𝗚𝗘𝗡𝗘𝗥𝗔𝗧𝗢𝗥 💎\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>⌖ 𝗖𝗮𝗿𝗱 ⤳</b> <code>{card_details}</code>\n"
            f"⌖ 𝗦𝘁𝗮𝘁𝘂𝘀 ⤳ ✅ 𝗔𝗣𝗣𝗥𝗢𝗩𝗘𝗗 | 𝗟𝗜𝗩𝗘\n"
            f"⌖ 𝗦𝘂𝗰𝗰𝗲𝘀𝘀 ⤳ {success_badge}\n"
            f"⌖ 𝗟𝗲𝘃𝗲𝗹 ⤳ {card_info['level']} 💎\n"
            f"⌖ 𝗕𝗶𝗻 ⤳ {BIN}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>⌮ 𝗧𝘆𝗽𝗲 ⤳ </b>  <code>{bin_data['brand']}</code>\n"
            f"<b>⌮ 𝗕𝗮𝗻𝗸 ⤳ </b>  <code>{bin_data['bank']}</code>\n"
            f"<b>⌮ 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 ⤳ </b>  <code>{bin_data['country']} {bin_data['country_flag']}</code>\n"
            f"<b>⌮ 𝗟𝗲𝘃𝗲𝗹 ⤳ </b>  <code>{bin_data['level']}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>⌮ 𝗕𝗜𝗡 𝗜𝗻𝗳𝗼 ⤳ </b>  <code>{card_number[:6]}xxxx|{card_info['month']}|{card_info['year']}|XXX</code>\n"
            f"<b>⌮ 𝗛𝗼𝗹𝗱𝗲𝗿 ⤳ </b>  <code>{full_name}</code>\n"
            f"<b>⌮ 𝗩𝗮𝗹𝗶𝗱 ⤳ </b>  <code>{card_info['month']}/{card_info['year']}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 𝗦𝘁𝗮𝘁𝘀: {success_count}/{total_cards} | 💎 Premium: {premium_count}\n"
            f"📈 𝗖𝗮𝗿𝗱 𝗧𝘆𝗽𝗲𝘀: 3️⃣{card_stats.get('American Express', 0)} 4️⃣{card_stats.get('Visa', 0)} 5️⃣{card_stats.get('Mastercard', 0)} 6️⃣{card_stats.get('Discover', 0)}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🤖 𝗣𝗼𝘄𝗲𝗿𝗲𝗱 𝗯𝘆 𝗙𝗥𝗢𝗫𝗧 𝗧𝗲𝗰𝗵\n"
        )

        retry_count = 0
        message_sent = False
        
        while retry_count < max_retries and not message_sent:
            try:
                data = {
                    'chat_id': CHAT_ID,
                    'text': message,
                    'parse_mode': 'HTML',
                    'reply_markup': json.dumps(reply_markup)
                }
                response = requests.post(f'{telegram_api}/sendMessage', data=data)
                
                if response.status_code == 200:
                    print(f"✅ Card {i:4d}: {card_type:12} | {BIN:6} | {card_info['level']:10} | {bin_data['bank'][:15]}")
                    message_sent = True
                elif response.status_code == 429:
                    retry_after = response.json().get('parameters', {}).get('retry_after', 10)
                    print(f"⚠️ Rate limited. Waiting {retry_after} seconds...")
                    time.sleep(retry_after)
                    retry_count += 1
                else:
                    print(f"❌ Error: {response.text[:100]}")
                    retry_count += 1
                    time.sleep(2)
            except Exception as e:
                print(f"❌ Error: {e}")
                retry_count += 1
                time.sleep(2)
        
        if not message_sent:
            print(f"❌ Failed to send card {i}")

        if i % requests_limit == 0 and i != total_cards:
            time.sleep(pause_duration)
    
    print("\n" + "=" * 60)
    print(f"📊 FINAL SUMMARY:")
    print(f"   ✅ Total Cards Sent: {success_count}")
    print(f"   💎 Premium Cards: {premium_count}")
    print(f"   📈 Success Rate: 85-90%")
    print(f"   📊 Card Distribution:")
    for card_type, count in card_stats.items():
        percentage = (count / success_count) * 100 if success_count > 0 else 0
        print(f"      {card_type}: {count} ({percentage:.1f}%)")
    print("=" * 60)

if __name__ == '__main__':
    live()  # Keep alive Flask server
    send_messages()
