from apps.shop.models import Product
from django_opensearch_dsl import Document
from django_opensearch_dsl.registries import registry


@registry.register_document
class ProductDocument(Document):
    """Документ для товаров."""

    class Index:
        name = "products"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    class Django:
        model = Product
        fields = [
            "id",
            "title",
            "price",
            "description",
            "info",
            "slug",
            "size",
            "color",
            "cpu_type",
            "available",
            "ram",
            "storage",
        ]
        related_models = ["category", "brand"]
