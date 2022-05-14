# FashionKilla

## Organization
To execute our code for FashionKilla, you must first download the .zip file to your Github repository. 
\
\
In Codespace, you must have the ```FashionKilla``` folder which contains the ```static``` folder with a photos repository, the ```styles.css``` file, and the unique designated favicon for the header. A ```templates``` folder must also be included within the ```FashionKilla``` folder that will hold all the HTML files for the website. All the Python code that links to the HTML will be included in a file called ```app.py``` outside the templates folder, and will be supplemented by the ```helpers.py``` file. Finally, you must have a ```fashion.db``` file that links to a PHP database you create.
\
\
In your PHP database you must have tables labeled ```clothing```, ```outfits``` and ```users```; your ```clothing``` table must contain the 6 specified attributes that a user inputs: ```userid```, ```type```, ```photo```, ```color```, ```name```, and ```itemid```; your outfits table must have the 3 specified attributes: ```userid```, ```name```, and ```photo```; and your user table must include ```userid```, ```hash```, and ```name```. 
\
All attributes should be specified as ```not NULL``` and ```text```, except for ```userid``` which must be an ```integer```. None of the attributes should be a primary key except for itemid within the clothing table, which allows the user to delete items of clothing. 


## Testing
To test the code, you must execute ```cd fashionkilla``` within Codespace and subsequently execute ```flask run```. This command will open the website with the automatically-compiled code. 

# Usage
To use the project, first register an account with a username and a password. Then upload to your closet clothing items with your choice of name, photo, type and color. Try deleting items and organizing them by type and color using the designated buttons. Once you have uploaded multiple items to your closet, try using the randomizer function by navigating to the “Outfits” page and selecting the “New Random Outfit” button. Finally, try the social Explore function. This function should be tested in two ways. First, try uploading an outfit to the Explore page by adding an image and name. Then, use the logout function to sign out of your individual account and register a new account. Check the Explore page to see if you can see your previously uploaded outfit even though you are signed into a different account. 

# Demonstration
https://youtu.be/tdN6UKLQ-9s
