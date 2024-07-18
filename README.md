# ZoHo
All things ZoHo. See functions folder for code as of July 18, 2024


## Flows
Most of these Flows follow the format:
Webhook -> Function (on error)-> Send Email 

1) Course feex section schedule create, update, or delete
> Webbook > managecoursefees()

2) Course Section Create or Update
  -> Webhook > managecourses()

3) Course section fee create or update
  -> Webhook > managecoursefees()

4) Grade changes to final approval for a student section grading sheet
  -> Webhook > processFinalApproval()

5) New Student
  -> Webhook > ManageStudents()
   
6) Student enrolls or drops a certificate; or certificate status changes
  -> Webhook > managecertificates()

7) Transaction - enrollments
  -> Webhook > manageenrollments2()

8) Transaction - enrollments
  -> Webhook > manageenrollments2()

9) Update Student Fix #2
  -> Webhook > getstudentnumber() > Fetch module entry > ManageStudents()

## Functions:
- managecoursefees (referenced twice see 1) and 3)
- managecourses
- processFinalApproval 
- ManageStudents (referenced in 6) and 10) 
- managecertificates
- manageenrollments2 (referenced twice see 8) and 9) 
- getstudentnumber
