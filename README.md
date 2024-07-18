# ZoHo
Most of these Flows follow the format:
Webhook -> Function (on error)-> Send Email 


## Flows
1) Course feex section schedule create, update, or delete
  -> Webbook > managecoursefees
2) Course Section Create or Update
  -> Webhook > managecourses
3) Course section fee create or update
  -> Webhook > managecoursefees
5) Grade changes to final approval for a student section grading sheet
  -> Webhook > processFinalApproval
6) New Student
  -> Webhook > ManageStudents
7) Student enrolls or drops a certificate; or certificate status changes
  -> Webhook > managecertificates
8) Transaction - enrollments
  -> Webhook > manageenrollments2
9) Transaction - enrollments
  -> Webhook > manageenrollments2
10) Update Student Fix #2
  -> Webhook > getstudentnumber > Fetch module entry > ManageStudents



## Functions:
- managecoursefees
- managecourses
