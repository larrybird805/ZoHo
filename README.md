# ZoHo
All things ZoHo. See the functions folder for code as of July 18, 2024.
This is currently all code pulled from the contractors. Please use the standard naming convention when we go over and rewrite everything. Camel case preferred. 
Webhooks trigger via webhook: ${webhookTrigger.payload} and most Flows follow the format:
> Webhook -> Function (on error)-> Send Email 

## Flows
1) Course feex section schedule create, update, or delete
> Webbook > managecoursefees()

2) Course Section Create or Update
> Webhook > managecourses()

3) Course section fee create or update
> Webhook > managecoursefees()

4) Grade changes to final approval for a student section grading sheet
> Webhook > processFinalApproval()

5) New Student
> Webhook > ManageStudents()
   
6) Student enrolls or drops a certificate; or certificate status changes
> Webhook > managecertificates()

7) Transaction - enrollments
> Webhook > manageenrollments2()

8) Update Student Fix #2
> Webhook > getstudentnumber() > Fetch module entry > ManageStudents()

## Functions:
- [managecoursefees](/functions/managecoursefees) -referenced twice see 1) and 3)
- [managecourses](/functions/managecourses)
- [processFinalApproval](/functions/processFinalApproval) 
- [ManageStudents](/functions/ManageStudents) -referenced in 5) and 8) 
- [managecertificates](/functions/managecertificates)
- [manageenrollments2](/functions/manageenrollments2)
- [getstudentnumber](/functions/getstudentnumber)
