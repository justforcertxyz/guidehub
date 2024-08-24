from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.files.storage import FileSystemStorage

pdf_storage = FileSystemStorage(location=settings.GUIDE_PDF_ROOT)
User = get_user_model()


class Guide(models.Model):
    title = models.CharField("Title", max_length=50)
    pub_date = models.DateTimeField("Date Published", default=timezone.now)
    slug = models.SlugField("Slug", max_length=30, unique=True)
    description = models.TextField(
        "Guide Text", max_length=2000, blank=True, null=True)
    pages = models.PositiveIntegerField("Amount of Pages", default=1)
    current_price = models.DecimalField(
        "Current Guide Price", max_digits=6, decimal_places=2)
    price_history = models.JSONField("Price History", blank=True, null=True)
    author = models.ForeignKey(
        User, verbose_name="Author", on_delete=models.CASCADE)
    thumbnail = models.ImageField(
        "Thumbnal", upload_to="img/", blank=True, null=True)
    guide_pdf = models.FileField("Full Guide PDF", storage=pdf_storage,
                                 validators=[FileExtensionValidator(allowed_extensions=["pdf"])])
    owned_by = models.ManyToManyField(
        User, verbose_name="Owned By", blank=True, related_name="owned_by")

    language = models.CharField("Language", max_length=7, default="deutsch")
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title

    def set_price(self, new_price, commit=True):
        self.price = new_price
        self.price_history.append([f'{new_price}', f'{timezone.now()}'])

        if commit:
            self.save()

    def add_owner(self, new_owner: User):
        self.owned_by.add(new_owner)

    def is_owned(self, user):
        return user in self.owned_by.get_queryset()

    # TODO: Maybe different solution?
    def has_thumbnail(self):
        try:
            self.thumbnail.url
            return True
        except:
            return False

    @classmethod
    def create_guide(cls, title, slug, description, pages, current_price, author: User, guide_pdf, tags=""):
        guide = Guide.objects.create(title=title[:49], slug=slug,
                                     description=description, pages=pages, current_price=current_price,
                                     price_history=[
                                         [f'{current_price}', f'{timezone.now()}']],
                                     author=author,
                                     guide_pdf=guide_pdf,
                                     tags=tags,
                                     )
        guide.add_owner(author)
        if User.objects.filter(is_superuser=True).count() > 0:
            for su in User.objects.filter(is_superuser=True):
                if not guide.is_owned(su):
                    guide.add_owner(su)

        return guide

    def place_order(self, user) -> bool:
        Order.create_order(self, self.current_price, user)
        return True


class Order(models.Model):
    price = models.DecimalField(
        "Price of Order", max_digits=6, decimal_places=2)
    date = models.DateTimeField("Date of Order", default=timezone.now)
    user = models.ForeignKey(
        User, verbose_name="User who ordered", on_delete=models.CASCADE)
    guide = models.ForeignKey(Guide, verbose_name="Guide ordered", on_delete=models.CASCADE)

    @classmethod
    def create_order(cls, guide, price, user):
        return Order.objects.create(guide=guide, price=price, user=user)
