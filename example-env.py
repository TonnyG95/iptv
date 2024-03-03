"""
Da bi koristio ovaj fajl popuni potrbne informacije za aplikaciju.
i onda samo premimenuj ovaj fajl u env.py i sve bi trebalo raditi

"""

import os

# Main Settings

os.environ["SECRET_KEY"] = "YouSecretKey"
os.environ["DEBUG"] = "1" # Broj 1 znaci da je debug mod ukljucen sto ce ti pomoci rijesiti ako naidjes na neke problem ako zelis koristi ovo live onda 1 zamjeni sa 0 i aplikacija je produkcijski spremna

# AWS S3 Settings

# Main Settings
os.environ["AWS_ACCESS_KEY_ID"] = 'Your AWS Access Key'
os.environ["AWS_SECRET_ACCESS_KEY"] = 'Your AWS Access Secret'
os.environ["AWS_STORAGE_BUCKET_NAME"] = 'Your Bucket Name'
os.environ["AWS_S3_REGION_NAME"] = 'Your Bucket Region'

# S3 Addition Settings
os.environ["AWS_S3_CUSTOM_DOMAIN"] = ''  
os.environ["AWS_DEFAULT_ACL"] = ''  
os.environ["AWS_QUERYSTRING_AUTH"] = 'False'  
os.environ["AWS_S3_FILE_OVERWRITE"] = 'False' 
os.environ["AWS_S3_SIGNATURE_VERSION"] = '' 

# Google ReCaptcha

os.environ["RECAPTCHA_PUBLIC_KEY"] = "Your recaptcha Key"
os.environ["RECAPTCHA_PRIVATE_KEY"] = "Your recaptcha Secret"

# # PayPal Live
os.environ['PAYPAL_CLIENT_ID'] = 'Your PayPal live business Account Client ID'
os.environ['PAYPAL_SECRET_KEY'] = 'Your PayPal live business Account Secret Key'

# PayPal Sendbox
os.environ['PAYPAL_CLIENT_ID'] = 'Your PayPal sendbox business Account Client ID'
os.environ['PAYPAL_SECRET_KEY'] = 'Your PayPal sendbox business Account Secret Key'


# Email Settings

os.environ["ADMIN_EMAIL"] = "Admin Email Address"
os.environ["EMAIL_BACKEND"] = "django.core.mail.backends.smtp.EmailBackend"
os.environ["EMAIL_HOST"] = "Your Email SMTP Host"
os.environ["EMAIL_PORT"] = str(587) 
os.environ["EMAIL_USE_TLS"] = "False"
os.environ["EMAIL_HOST_USER"] = "Your Email"
os.environ["EMAIL_HOST_PASSWORD"] = "Your Email Password"


