# recruit

A Django recruitment application for Employers, Candidates and Recruiters. This project is a work in progress.

### Environment
Environment variables are used in `settings.py` for [AWS S3](https://aws.amazon.com/s3/) and [SendGrid email](http://sendgrid.com/) configuration. These variables may be hard-coded in `settings.py` or configured in your environment. 
1. `SECRET_KEY`
2. `AWS_STORAGE_BUCKET_NAME`
3. `AWS_BUCKET_URL`
4. `AWS_ACCESS_KEY_ID`
5. `AWS_SECRET_ACCESS_KEY`
6. `SENDGRID_USER` (optional)
7. `SENDGRID_PASSWORD` (optional)

### Preparation
1. Install dependencies `pip install -r requirements.txt`
2. Create database tables `python manage.py migrate`
3. Create admin account `python manage.py createsuperuser`
4. Visit `http://localhost:8000` in your browser
5. Visit the admin panel `http://localhost:8000/admin` to easily manipulate data

### Notes
1. Email notifications are not completely integrated. Upon creating an admin/superuser visit `http://localhost:8000/admin/account/emailaddress/` and check the box `Verified` so you may login to the application at `http://localhost:8000`