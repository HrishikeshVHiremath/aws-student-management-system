# AWS Student Management System

A cloud-hosted Student Management System built using **AWS, Python Flask, and MySQL**. The application supports student record management and profile image uploads using AWS services.

## Project Overview

This project demonstrates how to deploy a Python web application on AWS, connect it to a managed relational database, and securely store student profile images in Amazon S3.

## Architecture

**User → Nginx → Flask Application (Amazon EC2) → Amazon RDS for MySQL**

The application also uses Amazon S3 for image storage and an IAM role to grant the EC2 instance permission to access S3.

## AWS Architecture Diagram

![Student Management System AWS Architecture](Student%20Management%20System%20AWS%20Architecture.png)

### AWS Services Used

- **Amazon EC2:** Hosts the Flask web application.
- **Amazon RDS for MySQL:** Stores student records.
- **Amazon S3:** Stores student profile images in a private bucket.
- **AWS IAM Role:** Provides permissions for the application to access S3 without hardcoding AWS access keys.
- **Amazon VPC and Security Groups:** Control network access between the application server and database.
- **Nginx:** Acts as a reverse proxy for the Flask application.

## Technologies

- Python
- Flask
- PyMySQL
- Boto3
- MySQL
- HTML, CSS, and JavaScript
- Linux (Amazon Linux 2023)
- Git and GitHub
- Nginx

## Features

- Add new student records.
- View student details.
- Edit existing student records.
- Delete student records.
- Upload student profile images to Amazon S3.
- Generate temporary presigned URLs to display images from a private S3 bucket.
- Connect the Flask application to Amazon RDS for MySQL.
- Use IAM role-based permissions for AWS service access.
- Display a responsive dashboard with student information and search functionality.

## Security Practices

- Keep the S3 bucket private and block public access.
- Use an EC2 IAM role instead of storing AWS access keys in application code.
- Restrict database access using security groups.
- Store sensitive configuration in environment variables.
- Exclude `.env` files and private credentials from Git.

## Project Structure

```text
aws-student-management-system/
├── app.py
├── requirements.txt
├── .gitignore
└── templates/
    ├── index.html
    └── edit.html
```

## Setup and Deployment

### Prerequisites

- An AWS account
- An Amazon EC2 Linux instance
- An Amazon RDS for MySQL database
- An Amazon S3 bucket
- An IAM role with the required S3 permissions
- Python and pip

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/HrishikeshVHiremath/aws-student-management-system.git
   cd aws-student-management-system
   ```

2. Install the Python dependencies:

   ```bash
   python3 -m pip install -r requirements.txt
   ```

3. Configure the database connection and AWS settings using environment variables. Do not commit your actual credentials.

4. Configure the EC2 IAM role with the minimum required S3 permissions.

5. Configure the RDS security group to allow MySQL traffic from the EC2 security group.

6. Run the application:

   ```bash
   python3 app.py
   ```

7. Configure Nginx as a reverse proxy and use the appropriate security group rules to allow web traffic.

*Note: Exact environment variable names and configuration steps depend on the current application code.*

## Learning Outcomes

Through this project, I gained practical experience with:

- Deploying a Python web application on Amazon EC2.
- Connecting an application to Amazon RDS for MySQL.
- Integrating Amazon S3 for private image storage.
- Configuring IAM roles and security group rules.
- Generating presigned URLs for temporary image access.
- Using Linux commands, Git, GitHub, and Nginx.
- Understanding how AWS services work together in a cloud-hosted application.

## Future Improvements

- Configure automatic application startup using `systemd`.
- Add HTTPS using a domain name and TLS certificate.
- Implement stronger authentication and authorization.
- Add automated deployment using a CI/CD pipeline.
- Configure monitoring, logging, and backups.

## Author

**Hrishikesh V Hiremath**

GitHub: [HrishikeshVHiremath](https://github.com/HrishikeshVHiremath)

---

*This project was developed as a hands-on learning project to build practical AWS cloud computing skills.*
