# JobMate
A Django-based job management system for property maintenance. Built with Django, PostgreSQL, HTML, and Bootstrap. Includes user registration, engineer job tracking, shopping cart and full CRUD functionality for managing bookings and job records in a clean, responsive interface.

## What This Project Is

This application lets property managers and engineers:
- **Book maintenance jobs** such as boiler servicing, repairs, and inspections  
- **View and manage job history** with status updates and filtering  
- **Track job statuses** (Pending, In Progress, Completed) via a dashboard  
- **Assign engineers** to individual jobs 
- **Invoice jobs** add jobs to shopping cart
- **Update cart** update the actual hours worked per job 
- **Pay for completed jobs** using Stripe payment gateway

---

## Property Manager User Story

As a **Property Manager**, I want to:

- **Log in securely** to access my dashboard and manage job-related data.
- **Create, view, edit, and delete jobs** by filling out forms with details like:
  - Job title
  - Description
  - Assigned engineer
- **Assign engineers to jobs** so the right person is notified and responsible.
- **Manage engineers**:
  - View a list of engineers
  - Edit engineer details
  - Delete engineers when no longer needed
- **Manage payments**:
  - Use stripe gateway to pay engineers for completed jobs
  - Track submitted jobs via a list or dashboard to monitor status and progress
- **Update my user profile and password** to maintain account security and accuracy.

As a **Engineer**, I want to:
- **Log in securely** to access my dashboard and manage job-related data.
- View my **own jobs**  
- Update job status (e.g., mark completed)  
- **Add jobs for payment** Once the job has been completed add it to the cart.
- **Adjust jobs costs** Update the actual hours or other incured costs worked on the job.
- **Maintain my own** profile and security settings.

---

## Tech Stack

- Django (Python Web Framework)  
- PostgreSQL (Relational Database)  
- HTML5 + Bootstrap 5 (Frontend UI)  
- Django Templating Engine (Jinja-like)  
- Django Admin (for quick management)  

---

## Figma Files

<p align="center">
  <strong>Colour Pallette</strong><br>
  <img src="documentation/figma/hi-fi/colour-pallette.png" alt="Colour Pallette" width="300" />
</p>

<h1 align="left">
   <strong>Wireframe</strong><br>
</h1>

<p align="center">
  <strong>Welcome</strong><br>
  <img src="documentation/figma/wireframe/welcome.png" alt="Welcome" width="300" />
</p>

<p align="center">
  <strong>Create Account</strong><br>
  <img src="documentation/figma/wireframe/create-account.png" alt="Create Account" width="300" />
</p>

<p align="center">
  <strong>Login</strong><br>
  <img src="documentation/figma/wireframe/login.png" alt="Login" width="300" />
</p>

<p align="center">
  <strong>Logged Out</strong><br>
  <img src="documentation/figma/wireframe/logout.png" alt="Logged Out" width="300" />
</p>

<p align="center">
  <strong>Reset Password</strong><br>
  <img src="documentation/figma/wireframe/reset-password.png" alt="Reset Password" width="300" />
</p>

<p align="center">
  <strong>Profile Settings</strong><br>
  <img src="documentation/figma/wireframe/profile-settings.png" alt="Profile Settings" width="300" />
</p>

<p align="center">
  <strong>Admin Dashboard</strong><br>
  <img src="documentation/figma/wireframe/admin-dashboard.png" alt="Admin Dashboard" width="300" />
</p>

<p align="center">
  <strong>Create a Job</strong><br>
  <img src="documentation/figma/wireframe/create-job.png" alt="Creat a Job" width="300" />
</p>

<p align="center">
  <strong>Edit a Job</strong><br>
  <img src="documentation/figma/wireframe/edit-job.png" alt="Edit a Job" width="300" />
</p>

<p align="center">
  <strong>Delete a Job</strong><br>
  <img src="documentation/figma/wireframe/delete-job.png" alt="Delete a Job" width="300" />
</p>

<p align="center">
  <strong>Job Details</strong><br>
  <img src="documentation/figma/wireframe/job-details.png" alt="Job Details" width="300" />
</p>

<p align="center">
  <strong>Engineer Dashboard</strong><br>
  <img src="documentation/figma/wireframe/engineer-dashboard.png" alt="Engineer Dashboard" width="300" />
</p>

<p align="center">
  <strong>Engineers List</strong><br>
  <img src="documentation/figma/wireframe/engineers-list.png" alt="Engineers List" width="300" />
</p>

<p align="center">
  <strong>Engineer Payments Summary</strong><br>
  <img src="documentation/figma/wireframe/engineer-payments-summary.png" alt="Engineer Payments Summary" width="300" />
</p>

<p align="center">
  <strong>Admin Payments Summary</strong><br>
  <img src="documentation/figma/wireframe/admin-payments-summary.png" alt="Admin Payments Summary" width="300" />
</p>

<p align="center">
  <strong>Cart</strong><br>
  <img src="documentation/figma/wireframe/cart.png" alt="Cart" width="300" />
</p>

<p align="center">
  <strong>Pricing Adjustment</strong><br>
  <img src="documentation/figma/wireframe/pricing-adjustment.png" alt="Pricing Adjustment" width="300" />
</p>

<h1 align="left">
   <strong>Hi-Fi</strong><br>
</h1>

<p align="center">
  <strong>Welcome</strong><br>
  <img src="documentation/figma/hi-fi/welcome-hifi.png" alt="Welcome" width="300" />
</p>

<p align="center">
  <strong>Create Account</strong><br>
  <img src="documentation/figma/hi-fi/create-account-hifi.png" alt="Create Account" width="300" />
</p>

<p align="center">
  <strong>Login</strong><br>
  <img src="documentation/figma/hi-fi/login-hifi.png" alt="Login" width="300" />
</p>

<p align="center">
  <strong>Logged Out</strong><br>
  <img src="documentation/figma/hi-fi/logout-hifi.png" alt="Logged Out" width="300" />
</p>

<p align="center">
  <strong>Reset Password</strong><br>
  <img src="documentation/figma/hi-fi/reset-password-hifi.png" alt="Reset Password" width="300" />
</p>

<p align="center">
  <strong>Profile Settings</strong><br>
  <img src="documentation/figma/hi-fi/profile-settings-hifi.png" alt="Profile Settings" width="300" />
</p>

<p align="center">
  <strong>Admin Dashboard</strong><br>
  <img src="documentation/figma/hi-fi/admin-dashboard-hifi.png" alt="Admin Dashboard" width="300" />
</p>

<p align="center">
  <strong>Create a Job</strong><br>
  <img src="documentation/figma/hi-fi/create-job-hifi.png" alt="Creat a Job" width="300" />
</p>

<p align="center">
  <strong>Edit a Job</strong><br>
  <img src="documentation/figma/hi-fi/edit-job-hifi.png" alt="Edit a Job" width="300" />
</p>

<p align="center">
  <strong>Delete a Job</strong><br>
  <img src="documentation/figma/hi-fi/delete-job-hifi.png" alt="Delete a Job" width="300" />
</p>

<p align="center">
  <strong>Job Details</strong><br>
  <img src="documentation/figma/hi-fi/job-details-hifi.png" alt="Job Details" width="300" />
</p>

<p align="center">
  <strong>Engineer Dashboard</strong><br>
  <img src="documentation/figma/hi-fi/engineer-dashboard-hifi.png" alt="Engineer Dashboard" width="300" />
</p>

<p align="center">
  <strong>Engineers List</strong><br>
  <img src="documentation/figma/hi-fi/engineers-list-hifi.png" alt="Engineers List" width="300" />
</p>

<p align="center">
  <strong>Engineer Payments Summary</strong><br>
  <img src="documentation/figma/hi-fi/engineer-payments-summary-hifi.png" alt="Engineer Payments Summary" width="300" />
</p>

<p align="center">
  <strong>Admin Payments Summary</strong><br>
  <img src="documentation/figma/hi-fi/admin-dashboard-hifi.png" alt="Admin Payments Summary" width="300" />
</p>

<p align="center">
  <strong>Cart</strong><br>
  <img src="documentation/figma/hi-fi/cart-hifi.png" alt="Cart" width="300" />
</p>

<p align="center">
  <strong>Pricing Adjustment</strong><br>
  <img src="documentation/figma/hi-fi/pricing-adjutsment-hifi.png" alt="Pricing Adjustment" width="300" />
</p>

<h1 align="left">
   <strong>Mobile Hi-fi</strong><br>
</h1>

<p align="center">
  <strong>Welcome</strong><br>
  <img src="documentation/figma/mobile/welcome-mobile.png" alt="Welcome" width="300" />
</p>

<p align="center">
  <strong>Create Account</strong><br>
  <img src="documentation/figma/mobile/create-account-mobile.png" alt="Create Account" width="300" />
</p>

<p align="center">
  <strong>Login</strong><br>
  <img src="documentation/figma/mobile/login-mobile.png" alt="Login" width="300" />
</p>

<p align="center">
  <strong>Logged Out</strong><br>
  <img src="documentation/figma/hi-fi/logout-hifi.png" alt="Logged Out" width="300" />
</p>

<p align="center">
  <strong>Reset Password</strong><br>
  <img src="documentation/figma/mobile/reset-password-mobile.png" alt="Reset Password" width="300" />
</p>

<p align="center">
  <strong>Profile Settings</strong><br>
  <img src="documentation/figma/mobile/profile-settings-mobile.png" alt="Profile Settings" width="300" />
</p>

<p align="center">
  <strong>Admin Dashboard</strong><br>
  <img src="documentation/figma/mobile/admin-dashboard-mobile.png" alt="Admin Dashboard" width="300" />
</p>

<p align="center">
  <strong>Create a Job</strong><br>
  <img src="documentation/figma/mobile/create-job-mobile.png" alt="Creat a Job" width="300" />
</p>

<p align="center">
  <strong>Delete a Job</strong><br>
  <img src="documentation/figma/mobile/delete-job-mobile.png" alt="Delete a Job" width="300" />
</p>

<p align="center">
  <strong>Job Details</strong><br>
  <img src="documentation/figma/mobile/job-details-mobile.png" alt="Job Details" width="300" />
</p>