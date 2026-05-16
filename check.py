#! Copyright © by Nguyễn An Khang (KhangToolOfficial)
#! Share lại nhớ ghi nguồn
import os
import requests
from concurrent.futures import ThreadPoolExecutor

os.system('cls' if os.name == 'nt' else 'clear')
print("\033[1;31m#!Copyright © by Nguyễn An Khang (KhangToolOfficial)")
print("\033[1;37m •   Share lại nhớ ghi nguồn! ")
file_path = input('\033[1;32m Nhập File Chứa Keyword: \033[1;33m')
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        keywords = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print('\033[1;31m Không tìm thấy file!')
    exit()

domains = []
total_domains = 0
keyword_progress = 0

def fetch_domains(key):
    global total_domains, keyword_progress
    try:
        response = requests.get(f'https://email-fake.com/search.php?key={key}').json()
        for dm in response:
            domains.append(dm)
            total_domains += 1
        keyword_progress += 1
        print(f'\033[1;33m {key} \033[1;32mTìm Được {len(response)} Domain | Tổng Domain: {total_domains}')
        print(f'\033[1;37m Tiến trình Keyword: {keyword_progress}/{len(keywords)}', end='\r')
    except:
        print(f'\033[1;31m Lỗi -> {key}                ')

# Chạy đa luồng lấy domain
with ThreadPoolExecutor(max_workers=15) as executor:
    executor.map(fetch_domains, keywords)

print('\n\033[1;34m Bắt đầu lọc và check uptime... \033[0m')

checked = 0
valid_domains = []
trash_domains = []

def process_domain(mien):
    global checked
    checked += 1
    first_part = mien.split('.')[0]
    if first_part.isdigit():
        trash_domains.append(mien)
        print(f'\033[1;31m Domain Rác  | {mien}                ')
        print(f'\033[1;37m Tiến trình Check: {checked}/{len(domains)}', end='\r')
        return

    data = {'usr': 'khang', 'dmn': mien}
    try:
        response = requests.post('https://email-fake.com/check_adres_validation3.php', data=data, timeout=5).json()
        uptime = int(response['uptime'])
        print(f'\033[1;32m Domain Thật | {mien} \033[1;37m-> \033[1;33m{uptime}\033[1;32m Ngày trước              ')
        if 0 <= uptime <= 10:
            valid_domains.append((uptime, mien))
            
    except Exception:
        print(f'\033[1;31m Time out hoặc Lỗi -> {mien}                ')
    
    print(f'\033[1;37m Tiến trình Check: {checked}/{len(domains)}', end='\r')

with ThreadPoolExecutor(max_workers=15) as executor:
    executor.map(process_domain, domains)

print('\n\n\033[1;34m Đang sắp xếp và xuất kết quả... \033[0m')

if trash_domains:
    with open('unpass.txt', 'a', encoding='utf-8') as f:
        for d in trash_domains:
            f.write(d + '\n')

valid_domains.sort(key=lambda x: x[0])

if valid_domains:
    with open('pass_sorted_0_10.txt', 'w', encoding='utf-8') as f:
        for uptime, mien in valid_domains:
            info = f'{mien} -> {uptime} Ngày trước'
            f.write(info + '\n')

print(f'\n\033[1;32m Hoàn tất! \n - Đã lưu \033[1;33m{len(valid_domains)}\033[1;32m domain đạt chuẩn vào \033[1;37mpass_sorted_0_10.txt\n\033[1;32m - Đã chuyển \033[1;33m{len(trash_domains)}\033[1;32m domain rác vào \033[1;37munpass.txt\033[0m')
