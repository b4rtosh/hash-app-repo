from django.db import models


class CrackHashModel(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    ]
    HASH_CHOICES = [
        ('0', 'MD5'), ('100', '100'), ('1400', 'SHA256'), ('1700', 'SHA512')
    ]
    task_id = models.CharField(max_length=255, unique=True)
    hash_value = models.CharField(max_length=100)
    hash_algorithm = models.CharField(max_length=10, default='0', choices=HASH_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    cracked_password = models.CharField(max_length=255, null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
