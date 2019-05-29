# Data Centric Development milestone project

## Online cookbook

This website is a data driven web application in the form of an online cookbook,
which allows users to view, add, edit, delete and search for recipes based on a 
number of criteria.

[Click here to access web page](https://dcd-milestone-project.herokuapp.com)

## Instructions

- The site will begin on a page with a list of recipes
- Clicking on a recipe title loads a web page with the full details of that recipe
- Users who are signed in are able to modify or delete their own recipes, but not any others
- login and registration links are at the top of the page, there is also a link to
    registration from the login page
- To add a recipe, follow the 'Add a recipe' link at the top of the page
- If the user is logged in, the recipe will be signed as created by that user
- Users who are not logged in, will have their recipes signed as 'guest'
- Clicking on the up arrow in the full recipe view will allow an upvote of the recipe
- Users cannot upvote their own recipes
- Guests are unable to modify, upvote or delete recipes, only add or view them
- There is a search page where users are able to search for recipes based on:
1. Amount of time to cook
2. Cuisine origin
3. Ingredients
4. Allergens
- All search criteria are optional, but inputting nothing prompts a message asking for the user to try again

## UX

- In the 'Add a recipe' page, pushing the 'Add ingredient' or 'Add method' button, creates a new editable field to allow for editing before submission.
- Input fields clear after submission to make it easier to input the next item.
- Buttons in the 'View recipe' pages are colour coded to avoid accidental deletion.
- The recipe overview displays whether a recipe is vegetarian or vegan, colour 
    coded to differentiate them.
- A confirmation is required to delete recipes to avoid accidental deletions
- A message is displayed after clicking on the upvote button to advise user of whether an upvote was successful

The database schema can be found [here.](https://github.com/NinjaAiden/dcd-milestone-project/blob/master/docs/database_schema.png)

## Technologies

This data driven web application uses the following technologies:

- Python was used for the majority of this application, using the flask framework for the backend code
- MongoDB / NoSQL for the database
- PyMongo was used to facilitate communication between MongoDB and the application
- Bootstrap 4.0 was used for CSS styling, with a custom CSS overlay, which can be found under the static directory
- HTML was used for visual purposes and creating forms to feed information into the back end
- Javascript was used in some places to add or update elements of the user interface
- Font awesome links were used for button icons

## Deployment

This application is hosted on Heroku at: https://dcd-milestone-project.herokuapp.com/ In order to deploy this app to heroku, I needed to add a Procfile which tells heroku which language the app was written in and the name of the file that needs to be run - in this case this was app.py, I then set up a requirements.txt file which holds the dependencies that this app requires in order to run. Both the Procfile and requirements.txt file are committed to the repository and pushed to Heroku.

I then had to set some environment variables in Heroku in order for the live URL to run.
The following are configured under the hidden Config Vars:

- IP: 0.0.0.0
- PORT: 5000
- SECRET_KEY: SECRET_KEY

The application was then linked to the master branch of the Github repository for automatic synchronisation of commits