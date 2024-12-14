import csv
import hashlib
import time
import json
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

class BlockchainCertificator:
    def __init__(self, data_file='data.csv'):
        self.data_file = data_file
        self.chain = []
        self.load_data()

    def load_data(self):
        # 從CSV檔案中載入資料，並依序將每筆資料轉換為區塊，鏈接成區塊鏈
        try:
            with open(self.data_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                previous_hash = '0'
                for row in reader:
                    block = self.create_block(row, previous_hash)
                    self.chain.append(block)
                    previous_hash = block['hash']
        except FileNotFoundError:
            print("資料檔案未找到。")

    def create_block(self, data, previous_hash):
        block_content = {
            'index': len(self.chain) + 1,
            'student_id': data['student ID'],
            'name': data['name'],
            'department': data['department'],
            'previous_hash': previous_hash,
            'timestamp': time.time()
        }
        block_content['hash'] = self.hash_block(block_content)
        return block_content

    def hash_block(self, block):
        # 將區塊內容轉為字串後進行SHA-256雜湊
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def sign_block(self, private_key, block):
        # 使用私鑰對區塊內容進行簽名
        block_string = json.dumps(block, sort_keys=True).encode()
        signature = private_key.sign(
            block_string,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return signature

    def verify_signature(self, public_key, block, signature):
        # 驗證簽名是否與區塊內容匹配
        block_string = json.dumps(block, sort_keys=True).encode()
        try:
            public_key.verify(
                signature,
                block_string,
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False

    def print_chain(self):
        # 列印整個區塊鏈內容
        for block in self.chain:
            print(json.dumps(block, indent=4))

if __name__ == '__main__':
    # 示例：生成私鑰與公鑰（實際部署應安全存儲）
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    # 初始化區塊鏈證書系統
    certificator = BlockchainCertificator()
    certificator.print_chain()

    # 示例：對最後一個區塊進行簽名與驗證
    if certificator.chain:
        last_block = certificator.chain[-1]
        signature = certificator.sign_block(private_key, last_block)
        verified = certificator.verify_signature(public_key, last_block, signature)
        print(f"簽名驗證結果: {verified}")