import os
import random
import time
import asyncio
import logging
from datetime import datetime
from telethon import TelegramClient, events, Button
from faker import Faker

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

fake = Faker()

# ============ CONFIGURATION ============
API_ID = int(os.environ.get('API_ID', '39873730'))
API_HASH = os.environ.get('API_HASH', '80a6d89e7000271f0d29ae05423385ad')
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8934107960:AAGm59UZdm26YSxjGaJIsLT9IIoIW2gYQ4w')

# ============ CARD BINS ============
# AMEX BINS (Start with 34, 37)
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

HIGH_HIT_AMEX = ['3400', '3700', '3714', '3727', '3766', '3780']
HIGH_HIT_VISA = ['4532', '4539', '4556', '4916', '4929', '4484', '4716']
HIGH_HIT_MASTERCARD = ['5221', '5223', '5230', '5234', '5244', '5250', '5254']
HIGH_HIT_DISCOVER = ['6011', '6221', '6222', '6223', '6224', '6500']

PREMIUM_BANKS = [
    'CHASE', 'CITIBANK', 'BANK OF AMERICA', 'WELLS FARGO', 
    'CAPITAL ONE', 'US BANK', 'PNC BANK', 'TD BANK',
    'AMERICAN EXPRESS', 'DISCOVER BANK', 'GOLDMAN SACHS'
]

CARD_LEVELS = ['CLASSIC', 'GOLD', 'PLATINUM', 'SIGNATURE', 'WORLD ELITE', 'CENTURION']

# ============ TELEGRAM CLIENT ============
bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# ============ CARD GENERATION FUNCTIONS ============

def generate_card_number(card_type):
    """Generate valid card number"""
    if card_type == 'AMEX':
        if random.random() < 0.7:
            bin_prefix = random.choice(HIGH_HIT_AMEX)
        else:
            bin_prefix = random.choice(AMEX_BINS)
        length = 15
    elif card_type == 'VISA':
        if random.random() < 0.7:
            bin_prefix = random.choice(HIGH_HIT_VISA)
        else:
            bin_prefix = random.choice(VISA_BINS)
        length = 16
    elif card_type == 'MASTERCARD':
        if random.random() < 0.7:
            bin_prefix = random.choice(HIGH_HIT_MASTERCARD)
        else:
            bin_prefix = random.choice(MASTERCARD_BINS)
        length = 16
    else:  # DISCOVER
        if random.random() < 0.7:
            bin_prefix = random.choice(HIGH_HIT_DISCOVER)
        else:
            bin_prefix = random.choice(DISCOVER_BINS)
        length = 16
    
    body = bin_prefix + ''.join([str(random.randint(0, 9)) for _ in range(length - len(bin_prefix) - 1)])
    
    digits = [int(d) for d in body]
    for i in range(len(digits) - 2, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    total_sum = sum(digits)
    check_digit = (10 - (total_sum % 10)) % 10
    
    return body + str(check_digit)

def luhn_check(card_number):
    """Verify card number using Luhn algorithm"""
    digits = [int(d) for d in card_number]
    for i in range(len(digits) - 2, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    return sum(digits) % 10 == 0

def generate_card():
    """Generate complete card details"""
    card_type = random.choices(['AMEX', 'VISA', 'MASTERCARD', 'DISCOVER'], 
                               weights=[20, 35, 30, 15], k=1)[0]
    card_number = generate_card_number(card_type)
    
    if not luhn_check(card_number):
        return generate_card()
    
    month = str(random.randint(1, 12)).zfill(2)
    year = str(random.randint(27, 38)).zfill(2)
    
    if card_type == 'AMEX':
        cvv = str(random.randint(1000, 9999)).zfill(4)
    else:
        cvv = str(random.randint(100, 999)).zfill(3)
    
    bin_number = card_number[:6]
    bank = random.choice(PREMIUM_BANKS)
    level = random.choices(CARD_LEVELS, weights=[5, 15, 30, 25, 20, 5], k=1)[0]
    card_type_display = random.choice(['DEBIT', 'CREDIT'])
    
    # Get card emoji
    emojis = {'AMEX': '💎', 'VISA': '💳', 'MASTERCARD': '💳', 'DISCOVER': '🌟'}
    
    return {
        'card_number': card_number,
        'month': month,
        'year': year,
        'cvv': cvv,
        'card_type': card_type,
        'bin': bin_number,
        'bank': bank,
        'level': level,
        'country': 'UNITED STATES',
        'country_flag': '🇺🇸',
        'type': card_type_display,
        'emoji': emojis.get(card_type, '💳'),
        'is_high_hit': any(bin_number.startswith(b) for b in HIGH_HIT_AMEX + HIGH_HIT_VISA + HIGH_HIT_MASTERCARD + HIGH_HIT_DISCOVER)
    }

# ============ SCRAPER CONTROL ============
scraper_running = False
scraper_task = None

# ============ BOT HANDLERS ============

@bot.on(events.NewMessage(pattern='/start'))
async def start_command(event):
    """Simple start command - just shows bot is running"""
    await event.reply("🤖 Bot is running!\nUse /scrape to start dropping cards.", parse_mode='html')

@bot.on(events.NewMessage(pattern='/scrape'))
async def scrape_command(event):
    """Handle /scrape command - Start scraping cards"""
    global scraper_running, scraper_task
    
    if scraper_running:
        await event.reply("⚠️ Scraper is already running!\nUse /stop to stop it.", parse_mode='html')
        return
    
    chat_id = event.chat_id
    
    msg = """🚀 SCRAPER STARTED
━━━━━━━━━━━━━━━━━━━━━━━━
💳 Cards: AMEX | VISA | MASTERCARD | DISCOVER
🔥 Mode: High-Hit
📌 Status: Running...
━━━━━━━━━━━━━━━━━━━━━━━━
Use /stop to stop scraping"""
    
    await event.reply(msg, parse_mode='html')
    
    scraper_running = True
    scraper_task = asyncio.create_task(scrape_cards_continuous(chat_id))

@bot.on(events.NewMessage(pattern='/stop'))
async def stop_command(event):
    """Handle /stop command"""
    global scraper_running
    
    if not scraper_running:
        await event.reply("⚠️ Scraper is not running!\nUse /scrape to start.", parse_mode='html')
        return
    
    scraper_running = False
    
    msg = """⛔ SCRAPER STOPPED
━━━━━━━━━━━━━━━━━━━━━━━━
Use /scrape to start again"""
    
    await event.reply(msg, parse_mode='html')

async def send_approved_card(chat_id, card_data=None):
    """Send approved card with 3 buttons"""
    if not card_data:
        card_data = generate_card()
    
    card_details = f"{card_data['card_number']}|{card_data['month']}|20{card_data['year']}|{card_data['cvv']}"
    card_masked = f"{card_data['card_number'][:6]}xxxx|{card_data['month']}|20{card_data['year']}|xxx"
    
    high_hit_badge = " 🔥 HIGH HIT" if card_data['is_high_hit'] else ""
    
    # Get card prefix icon
    prefix_icon = {
        'AMEX': '3️⃣',
        'VISA': '4️⃣',
        'MASTERCARD': '5️⃣',
        'DISCOVER': '6️⃣'
    }.get(card_data['card_type'], '💳')
    
    msg = f"""━━━━━━━━━━━━━━━━━━━━━━━━
✅ <b>𝗔𝗣𝗣𝗥𝗢𝗩𝗘𝗗</b>{high_hit_badge}
━━━━━━━━━━━━━━━━━━━━━━━━
💳 <b>𝗖𝗖</b> <code>{card_details}</code>
🍀 <b>𝗚𝗲𝗻</b> <code>/gen {card_masked}</code>
━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ <b>𝗕𝗜𝗡</b> {card_data['bin']}
🏦 <b>𝗕𝗸</b> {card_data['bank']}
🍒 <b>𝗕𝗱</b> {card_data['card_type']}
📌 <b>𝗧𝗲</b> {card_data['type']
   <b>𝗖𝗶𝘁𝘆</b> {card_data['country']} {card_data['country_flag']}
━━━━━━━━━━━━━━━━━━━━━━━━
@ScarpXdeath_bot
{datetime.now().strftime('%I:%M %p')}"""
    
    buttons = [
        [Button.inline("VIP", "", style="success"), Button.inline("CHARGE", "https://t.me/approvedcc7", style="success")], 
        [Button.inline("MAIN", "", style="success")]
    ]
    
    try:
        await bot.send_message(chat_id, msg, buttons=buttons, parse_mode='html', link_preview=False)
        return True
    except Exception as e:
        logger.error(f"Error sending card: {e}")
        return False

async def scrape_cards_continuous(chat_id, total_cards=1000000, delay=0.5):
    """Continuous card scraping in channel"""
    global scraper_running
    
    logger.info(f"🚀 Starting scraper for chat {chat_id}")
    
    success_count = 0
    stats = {'AMEX': 0, 'VISA': 0, 'MASTERCARD': 0, 'DISCOVER': 0, 'HighHit': 0}
    start_time = time.time()
    
    for i in range(1, total_cards + 1):
        if not scraper_running:
            logger.info(f"⛔ Scraper stopped by user")
            break
            
        try:
            card_data = generate_card()
            
            stats[card_data['card_type']] += 1
            if card_data['is_high_hit']:
                stats['HighHit'] += 1
            
            if await send_approved_card(chat_id, card_data):
                success_count += 1
            
            if i % 50 == 0:
                elapsed = time.time() - start_time
                rate = i / elapsed if elapsed > 0 else 0
                logger.info(f"📊 Progress: {i} cards | Sent: {success_count} | Rate: {rate:.1f}/s")
            
            await asyncio.sleep(delay)
            
        except Exception as e:
            logger.error(f"Error in scraper: {e}")
            await asyncio.sleep(2)
    
    elapsed = time.time() - start_time
    logger.info(f"✅ Scraping complete! Sent {success_count} cards in {elapsed:.1f}s")
    
    summary = f"""📊 SCRAPING COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━
✅ Total cards sent: {success_count}
💎 AMEX: {stats['AMEX']}
💳 VISA: {stats['VISA']}
💳 MASTERCARD: {stats['MASTERCARD']}
🌟 DISCOVER: {stats['DISCOVER']}
🔥 High-Hit: {stats['HighHit']}
⏱️ Time: {elapsed:.1f}s
━━━━━━━━━━━━━━━━━━━━━━━━
Use /scrape to start again"""
    
    await bot.send_message(chat_id, summary, parse_mode='html')
    scraper_running = False

# ============ MAIN ============

async def main():
    """Main function"""
    logger.info("="*50)
    logger.info("🐍 SCRAP BOT STARTED!")
    logger.info("💳 Cards: AMEX | VISA | MASTERCARD | DISCOVER")
    logger.info("🔥 High-hit mode enabled")
    logger.info("📌 Bot is ready!")
    logger.info("="*50)
    
    await bot.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
