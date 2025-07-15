import requests
from django.core.management import BaseCommand
from django.utils.text import slugify
from product.models import Category, Product
import itertools

class Command(BaseCommand):
    help = 'Import products from FakeStore API'
    
    def generate_unique_slug(self, base_slug, model):
        """Generate unique slug by appending counter if needed"""
        slug = base_slug
        for i in itertools.count(1):
            if not model.objects.filter(slug=slug).exists():
                break
            slug = f"{base_slug}-{i}"
        return slug

    def handle(self, *args, **options):
        print('Creating Data.........')
        try:
            response = requests.get('https://fakestoreapi.com/products').json()
            
            for product in response:
                # Create or get category with unique slug
                category_slug = slugify(product['category'])
                category, _ = Category.objects.get_or_create(
                    title=product['category'],
                    defaults={
                        'slug': self.generate_unique_slug(category_slug, Category),
                        'featured': True
                    }
                )
                
                # Check if product already exists
                product_title = product['title']
                if not Product.objects.filter(title=product_title).exists():
                    # Create product with unique slug
                    product_slug = slugify(product_title)
                    Product.objects.create(
                        category=category,
                        title=product_title,
                        slug=self.generate_unique_slug(product_slug, Product),
                        price=product['price'],
                        thumbnail=product['image'],
                        description=product['description']
                    )
                else:
                    self.stdout.write(self.style.WARNING(f'Product "{product_title}" already exists, skipping...'))
            
            print('Insertion Completed....')
            self.stdout.write(self.style.SUCCESS('Successfully imported products'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))