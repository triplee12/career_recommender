# Career Recommendation System

A career recommendation system is a technology-enabled tool designed to assist individuals in making informed decisions about their career path.

## APIs and Methods

1. GET ``/courses``
   - Description: Fetches a list of all available courses in the system.
   - Response: Returns an array of course objects containing course details like `course_id`, `title`, `description`, `instructor`, etc.

2. GET ``/courses/{course_id}``
   - Description: Retrieves details of a specific course.
   - Parameters: ``course_id`` (path parameter) - The unique identifier of the course.
   - Response: Returns a course object with detailed information about the requested course.

3. GET ``/users/{user_id}/recommendations``
   - Description: Retrieves course recommendations for a specific user.
   - Parameters: ``user_id`` (path parameter) - The unique identifier of the user.
   - Response: Returns an array of recommended course objects tailored to the user's preferences and history.

4. POST ``/users/{user_id}/preferences``
   - Description: Updates the user's preferences.
   - Parameters: ``user_id`` (path parameter) - The unique identifier of the user.
   - Request Body: Contains the updated user preferences in JSON format.
   - Response: Returns a success message indicating that the preferences have been updated.

5. POST ``/courses/{course_id}/enrollments``
   - Description: Enrolls the user in a specific course.
   - Parameters: ``course_id`` (path parameter) - The unique identifier of the course.
   - Request Body: Contains any additional enrollment details if required.
   - Response: Returns a success message indicating that the user has been enrolled in the course.

6. GET ``/users/{user_id}/courses``
   - Description: Retrieves the list of courses that the user has already enrolled in.
   - Parameters: ``user_id`` (path parameter) - The unique identifier of the user.
   - Response: Returns an array of course objects representing the enrolled courses for the user.

7. POST ``/courses/{course_id}/ratings``
   - Description: Allows the user to rate a specific course.
   - Parameters: ``course_id`` (path parameter) - The unique identifier of the course.
   - Request Body: Contains the user's rating for the course.
   - Response: Returns a success message indicating that the rating has been recorded.

## User Stories

As a user, I want to be able to create a profile on the website so that I can access the features of the platform.
As a user, I want to be able to search for job listings based on different criteria so that I can find job opportunities that match my skills and interests.
As a user, I want to be able to apply for job listings on the platform so that I can be considered for employment.
As a user, I want to be able to receive notifications when new job listings are posted that match my search criteria so that I don't miss out on potential opportunities.
As a user, I want to be able to track the status of my job applications so that I can know if I am being considered for employment.

User Story 1: As a user, I want to be able to create a profile on the website so that I can access the features of the platform.

## Acceptance Criteria

The user can create a profile by providing their name, email address, and password.
The user must verify their email address before they can log in to the platform.
The user can edit their profile information at any time.

User Story 2: As a user, I want to be able to search for job listings based on different criteria so that I can find job opportunities that match my skills and interests.
Acceptance Criteria:
The user can search for job listings based on keywords, location, and job type.
The user can filter job listings by salary range, job level, and industry.
The user can view job listings in a list or grid format.

User Story 3: As a user, I want to be able to apply for job listings on the platform so that I can be considered for employment.
Acceptance Criteria:
The user can apply for a job listing by submitting a resume and cover letter.
The user can preview their application before submitting it.
The user will receive a confirmation email after submitting their application.

User Story 4: As a user, I want to be able to receive notifications when new job listings are posted that match my search criteria so that I don't miss out on potential opportunities.
Acceptance Criteria:
The user can set up job alerts based on their search criteria.
The user will receive an email notification when new job listings are posted that match their search criteria.
The user can manage their job alerts and turn them on or off at any time.

User Story 5: As a user, I want to be able to track the status of my job applications so that I can know if I am being considered for employment.
Acceptance Criteria:
The user can view the status of their job applications on their profile.

## Schemas

### User

``UserBase(BaseModel)``:

- ``name: str``
- ``username``
- ``email: EmailStr``

``UserCreate(UserBase)``:

- ``password: str``

``UserUpdate(UserBase)``:

- ``pass``

``User(UserBase)``:

- ``id: str``
- ``created_at: datetime``

    ``class Config``:
      -  ``orm_mode = True``

### Course

``CourseBase(BaseModel)``:

- ``title: str``
- ``description: str``

``CourseCreate(CourseBase)``:

- ``pass``

``CourseUpdate(CourseBase)``:

- ``pass``

``Course(CourseBase)``:

- ``id: int``
- ``created_at: datetime``

    ``class Config``:
      -  ``orm_mode = True``

### Career

``CareerBase(BaseModel)``:

- ``title: str``
- ``description: str``

``CareerCreate(CareerBase)``:

- ``pass``

``CareerUpdate(CareerBase)``:

- ``pass``

``Career(CareerBase)``:

- ``id: int``

    ``class Config``:
      -  ``orm_mode = True``

``CareerWithSkills(Career)``:

- ``skills: List[str]``

``CareerRecommendation(BaseModel)``:

- ``recommended_career: Career``
- ``recommended_courses: List[str]``

### Career Recommendation

``ExperienceLevel``:

- ``ENTRY_LEVEL = "Entry Level"``
- ``JUNIOR = "Junior"``
- ``MID_LEVEL = "Mid Level"``
- ``SENIOR = "Senior"``

``Skill``:

- ``title: str``
- ``proficiency: int``  Rating from 1 to 5

``CareerRecommendationRequest``:

- ``name: str``
- ``email: EmailStr``
- ``experience_level: ExperienceLevel``
- ``skills: List[Skill]``

``CareerRecommendationResponse``:

- ``recommended_career: str``
- ``recommended_courses: List[str]``
