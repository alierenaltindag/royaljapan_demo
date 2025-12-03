import os
import django
import sys

# Add the project root to the python path
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'royal.settings')
django.setup()

from royal.api.models import User, Product

def setup_data():
    try:
        user = User.objects.first()
        if not user:
            print("Creating test user...")
            user = User.objects.create_user(email="test@example.com", password="password123")
            user.username = "TestUser"
            user.save()
        
        product = Product.objects.first()
        if not product:
            print("Creating test product...")
            product = Product.objects.create(
                seller=user,
                title="Test Product",
                description="This is a test product",
                price_origin=1000,
                price_sell=1000,
                product_id="prod_test123",
                price_id="price_test123"
            )

        print(f"USER_ID={user.id}")
        print(f"PRODUCT_ID={product.id}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    setup_data()
