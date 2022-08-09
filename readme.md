# Job App APIs

Set up by running these commands:

1. pip3 install -r requirements.txt (Installing dependencies)
2. python -m venv venv (make .venv folder)
3. source .venv/bin/activate (activate virtual env, normally done automatically by IDE)
4. python manage.py migrate
5. python manage.py createsuperuser (set superuser)

Allow both companies and jobseekers to set up their account
- Companies create and Post jobs
- Job seekers can view the available jobs
- Job seekers upload their resume and apply for the Job
- Companies can view list of users applied for the job
- Companies can view the uploaded resume of the job seeker
- Companies can either reject/accept candidate
- The Job seeker can see the status of their application (Applied/Selected/Rejected)

Tech-Stack used ⚙
 - Django Rest Framework
 - SQLlite3
 - React
 - Tailwind CSS

