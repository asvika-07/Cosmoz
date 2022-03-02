from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class MyAccountManager(BaseUserManager):
    def create_user(
        self,
        email,
        RegistrationID,
        password=None,
    ):
        if not email:
            raise ValueError("email is required")

        user = self.model(
            email=self.normalize_email(email),
        )
        # username = self.username
        RegistrationID = RegistrationID
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, RegistrationID):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            RegistrationID=RegistrationID,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


UserTypeOptions = (
    ("Student", "Student"),
    ("Faculty", "Faculty"),
    ("Alumni", "Alumni"),
)


def get_profile_image_filepath(self, filename):
    DirectoryPath = f"media/{self.RegistrationID}/ProfilePicture/{self.username}.jpg"
    return DirectoryPath


def get_default_profile_image():
    return "media/argo.jpg"


class User(AbstractBaseUser):
    def directory(instance, filename):
        DirectoryPath = (
            f"media/{instance.RegistrationID}/ProfilePicture/{instance.username}.jpg"
        )
        print(DirectoryPath)
        return DirectoryPath

    FirstName = models.CharField(max_length=20)
    LastName = models.CharField(max_length=20)
    RegistrationID = models.CharField(max_length=6)
    email = models.EmailField(verbose_name="email", primary_key=True, unique=True)
    CustomPassword = models.CharField(max_length=200)
    ProfilePicture = models.ImageField(
        upload_to=get_profile_image_filepath, default=get_default_profile_image
    )

    MobileNumber = models.CharField(max_length=10)
    DateOfBirth = models.DateField(default=timezone.now)
    UserType = models.CharField(max_length=10, choices=UserTypeOptions)
    Description = models.CharField(max_length=40)
    # IsAuthenticated        = models.BooleanField()

    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    hide_email = models.BooleanField(default=True)
    username = models.CharField(max_length=30, unique=True)

    def save(self, *args, **kwargs):
        self.username = str(self.FirstName) + "_" + str(self.RegistrationID)
        super().save(*args, **kwargs)

    objects = MyAccountManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("RegistrationID",)

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
