def generate_unique_code(UserProfile):
        import random
        while True:
            code = ''.join(random.choices('0123456789', k=8))  # только цифры
            if not UserProfile.objects.filter(telegram_key=code).exists():
                return code
            
