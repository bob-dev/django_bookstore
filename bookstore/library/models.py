from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from PIL import Image


# Create your models here.


class Publisher(models.Model):
    # Définition des champs de la table Publisher (Editeur de l'ouvrage)

    name = models.CharField("edition", max_length=20)  # Champs de type chaîne de caractères,
    address = models.CharField("boite postale", max_length=30,
                               null=True)
    # Le 1er paramètre est le nom qui sera affiché dans le navigateur
    city = models.CharField("ville", max_length=20)  # le 2e indique la taille du champ
    country = models.CharField("pays", max_length=20)  # Pour plus d'infos, voir la documentation sur le site

    def __str__(self):
        return self.name


class Topic(models.Model):
    topic_name = models.CharField("d\u00E9signation", max_length=20)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    # Définition d'une clé étrangère, ici le 1er paramètre
    # indique une relation reflexive avec une contrainte de
    # de suppression en cascade

    def __str__(self):
        return self.topic_name


class Author(models.Model):
    author_name = models.CharField("nom", max_length=20)

    def __str__(self):
        return self.author_name


class Book(models.Model):
    # Définit la table Book

    LANGUAGES = [
        ('FR', 'FRANÇAIS'),
        ('ENG', 'ANGLAIS'),
    ]

    title = models.CharField("titre", max_length=100)
    isbn = models.CharField("numero ISBN", max_length=20, unique=True)
    page_size = models.PositiveIntegerField("Nombre de page",
                                            validators=[MaxValueValidator(2000), MinValueValidator(1)])
    language = models.CharField("langue", max_length=5, choices=LANGUAGES, default='FR')
    date_of_publishing = models.DateField("date de parution", default=timezone.now)
    publishing_number = models.PositiveSmallIntegerField("numero d\'edition", default=1)
    picture_location = models.ImageField(upload_to="library/media/library", null=True, blank=True)
    topic = models.ForeignKey(Topic, verbose_name="th\u00E8me de l\'oeuvre")
    editor = models.ForeignKey(Publisher, verbose_name="maison d\'\u00E9dition")
    author = models.ForeignKey(Author, verbose_name="auteur de l\'oeuvre")

    def __str__(self):
        return self.title


class BookCopy(models.Model):
    AVAILABILITIES = [
        ('DI', 'DISPONIBLE'),
        ('EM', 'EMPRUNTE'),
        ('AB', 'ABIME'),
    ]

    copy_id = models.CharField("identifiant de l'exemplaire", max_length=20, primary_key=True)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, to_field='isbn')
    availability = models.CharField("disponibilit\u00E9", max_length=5, choices=AVAILABILITIES, default='DI')

    def __str__(self):
        return self.copy_id

    class Meta:
        verbose_name_plural = 'Book copies'


class CustomerType(models.Model):
    type_label = models.CharField("type", max_length=20)

    def __str__(self):
        return self.type_label


class Customer(models.Model):
    # Définit la Table Customer qui gèrera les abonnés (Étudiants, Enseignants, etc...)

    last_name = models.CharField("nom", max_length=20)
    first_name = models.CharField("pr\u00E9nom", max_length=20)
    id_number = models.CharField("matricule", max_length=20, unique=True)
    customer_type = models.ForeignKey(CustomerType, verbose_name="type de l\'abonn\u00E9")

    def __str__(self):
        return self.id_number


class Reservation(models.Model):
    reservation_date = models.DateTimeField("Date de reservation", default=timezone.now)
    state = models.BooleanField("Cloture", default=False)
    recipient = models.ForeignKey(Customer, verbose_name="auteur de la reservation", to_field='id_number')
    book = models.ManyToManyField(Book, through='BookReserved',
                                  through_fields=('reservation', 'book_reserved'), )

    def __str__(self):
        return "Reservation faite \u00E0 {0} par le matricule {1} ".format(self.date, self.recipient)


class BookReserved(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    book_reserved = models.ForeignKey(Book, on_delete=models.CASCADE, to_field='isbn')


class BooksLoan(models.Model):
    # Définit la table qui gère les retours d'ouvrages
    loan_date = models.DateTimeField("Date de debut", default=timezone.now)
    loan_end = models.DateTimeField("Date de fin", default=timezone.now)
    return_date = models.DateTimeField("Date de remise", default=timezone.now)
    reservation_concerned = models.ForeignKey(Reservation, on_delete=models.CASCADE, verbose_name="reservation")
    copy_loaned = models.ManyToManyField(BookCopy, through='CopyLoaned', through_fields=('loan', 'copy_num'), )


class CopyLoaned(models.Model):
    loan = models.ForeignKey(BooksLoan, on_delete=models.CASCADE, verbose_name="emprunt")
    copy_num = models.ForeignKey(BookCopy, on_delete=models.CASCADE, to_field='copy_id')
