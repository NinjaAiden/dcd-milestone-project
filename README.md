# Data Centric Development milestone project

## Online cookbook

This website is a data driven web application in the form of an online cookbook,
which allows users to view, add, edit, delete and search for recipes based on a 
number of criteria.

[Click here to access web page](https://dcd-milestone-project.herokuapp.com)

## Instructions

- The site will begin on a page with a list of recipes
- Clicking on a recipe title loads a web page with the full details of that recipe
- Useres who are signed in are able to modify or delete their own recipes, but not any others
- login and registration links are at the top of the page, there is also a link to
    registration from the login page
- To add a recipe, follow the 'Add a recipe' link at the top of the page
- If the user is logged in, the recipe will be signed as created by that user
- Users who are not logged in, will have their recipes signed as 'guest'
- Guests are unable to modify or delete recipes, only add or view them

## Technologies

This data driven web application uses the following technologies:

- MongoDB / NoSQL for the database
- PyMongo was used to facilitate communication between MongoDB and the application
- Python was used for the majority of this application, using the flask framework
    for the backend code
- Bootstrap 4.0 was used for CSS styling, with a custom CSS overlay, which can 
    be found under the static directory
- Some HTML was used for visual purposes and creating forms to feed information 
    into the back end

## Deployment

This application was deployed on heroku and linked to the master branch of the Github
repository for automatic synchronisation of commits