# Donation Email Testing and SMTP Workflow Documentation

## 1. Introduction

This document outlines the testing, investigation, and implementation process for the donation confirmation email feature in the WMAA Charity Website. The goal of this feature is to automatically send a confirmation email to users after they successfully submit a donation.

This work builds on prior exploration conducted in Issues #19 and #26 and documents the final testing approach and outcomes.

---

## 2. Objective

The main objectives of this testing were:

- To verify that an email is triggered after a successful donation
- To identify limitations in the current hosting environment
- To implement and test a reliable email delivery mechanism
- To ensure the system can support automated donor communication

---

## 3. System Setup

### 3.1 Platform
- WordPress-based website
- GiveWP donation plugin used for handling donations

### 3.2 Hosting Environment
- InfinityFree hosting service

### 3.3 Email System
- Default WordPress PHP mail function (initial attempt)
- SMTP-based email system (final solution)

---

## 4. Testing Process

### 4.1 Initial Email Trigger Testing

- A test donation was submitted through the donation form
- Expected behaviour: confirmation email sent to donor
- Observed behaviour: no email received

This confirmed that the default email system was not functioning.

---

### 4.2 Issue Identification

Through testing and investigation:

- InfinityFree hosting does not support PHP mail functionality
- WordPress default mail system depends on server mail support
- As a result, email delivery failed despite correct trigger logic

---

### 4.3 SMTP-Based Solution

To resolve this issue:

- Installed and configured an SMTP plugin (WP Mail SMTP)
- Connected the system to an external email service
- Configured SMTP settings such as:
  - SMTP host
  - Port number
  - Encryption type
  - Authentication credentials

---

### 4.4 Email Delivery Testing

After SMTP configuration:

- Submitted another test donation
- Verified that:
  - Email trigger was activated
  - Email was successfully delivered to recipient inbox

This confirmed that SMTP resolved the delivery issue.

---

## 5. Results

| Test Case | Description                              | Result |
|-----------|------------------------------------------|--------|
| TC01      | Donation submission triggers email       | Passed |
| TC02      | Default email system (PHP mail)          | Failed |
| TC03      | SMTP configuration                       | Passed |
| TC04      | Email delivery after SMTP setup          | Passed |

---

## 6. Key Findings

- The donation email feature was functioning correctly at the application level
- The failure was due to hosting limitations, not code issues
- SMTP integration is essential for reliable email delivery
- External email services provide a stable and scalable solution

---

## 7. Challenges Faced

- Hosting environment restrictions (InfinityFree)
- Lack of native email support
- Need to research and configure third-party SMTP services

---

## 8. Conclusion

The donation confirmation email feature was successfully tested and validated using an SMTP-based approach. While the default email system failed due to hosting limitations, the integration of SMTP ensured reliable email delivery.

This confirms that the system is capable of supporting automated donation confirmation emails when properly configured.

---

## 9. Future Improvements

- Add email templates for better user experience
- Implement logging for email delivery tracking

---

## 10. References

- Issue #19: Initial investigation of email trigger system
- Issue #26: SMTP-based email workflow implementation
- WP Mail SMTP Plugin Documentation
