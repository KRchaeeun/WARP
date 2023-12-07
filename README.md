# Warp
This is the project about the movie recommendation website using Django & Vue.js.  

<br>
<br>
 
## MEMBERS 👩‍👧‍👧  
- [Hana Na](https://github.com/hana-nana)
- [Yejin Eum](https://github.com/yjeum)  
- [Chaeeun Lee](https://github.com/KRchaeeun)  

<br>
<br>
   
## OUR CODE COLLABORATION RULES 📑  
This is our code collaboration rules.
These rules are designed to establish a consistent, organized, and efficient approach to using Git, committing changes, and managing merges. They ensure that all team members contribute in a uniform manner. This consistency streamlines the code review process, reduces errors, and facilitates easier collaboration and understanding among developers.
 
<br>

<img src='./img/git1.PNG' width="250" height="200"> <img src='./img/git2.PNG' width="250" height="200">

<img src='./img/git3.PNG' width="250" height="200"> <img src='./img/git4.PNG' width="250" height="200">

<br>
 
### COMMIT: Commit Messages  
1. Purposefulness: Clearly convey the purpose and content of the changes.  
2. Format: Use the format [Type]: Description. For example, [FEAT]: Add user login functionality.  
3. Detailing: In the body of the message, explain in detail why the change was necessary or what problem it solves.  
 
<br>
 
### COMMIT: Commit Types  
1. FILE: Creation of folders and files.
2. INIT: Establishing the initial framework for a feature.
3. CREATE: Writing initial functionalities.
4. UPDATE: Adding new features.
5. FIX: Correcting bugs.
6. MERGE: Merging code branches.
7. TEST: Adding or modifying test code (e.g., console.log).
8. STYLE: Changes or additions to design.
9. DOCS: Documentation related changes (like README updates). 
 
<br>
 
### GIT: Branch Strategy  
1. main: Maintains stable, release-ready code.
2. dev: Holds code currently under development.
3. Feature-Specific Branches: For example, feature/login, feature/signup.
 
<br>
 
### MERGE: Regular Code Review and Merging  
1. Ensure to undergo a code review process and obtain team consensus before merging.  

<br>
<br>
 
## PREPARATION 💦

<br>

### Project Specification
This document defines the functional and non-functional requirements for the development of a movie recommendation website. The system offers services like recommending representative movies by year, hidden masterpieces, and includes a login system, user profile page, movie recommendation and detail pages, real-time popular movie services, and community features.
 
| Major Category            | Page                | Function                   | Detailed Function                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Additional Feature                                                                                                                 |
|-------------------|-----------------------|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|
|Header & Footer    |                       |User/Admin Header| > Click on logo to go to main page (maintain recommended year)<br> > Click on recommendation to move to movie recommendation page<br> > Click on community to move to community page<br> > Provide search bar<br> > Add movie registration button for admin (only admin can register movies)<br> > Click on profile picture to toggle detailed content (My Page, Edit Profile, Logout)                                                                                                                           |                                                                                                                          |
|                   |                       |Basic Footer            | > Frequently Asked Questions<br> > Contact Email<br> > Team Name and GitHub Address (team repository and individual GitHub)<br>                                                                                                                           |                                                                                                                          |
| Login / User Management | Registration Page       | Sign Up               | > Enter ID, Password, Password Confirmation, Email, Name, Date of Birth<br> > Check for ID duplication<br> > Verify password and password confirmation match<br> > Move to login page after completing registration<br>                                                                                                                                                                                                                                                                                                                         | > Complex registration process                                                                                                        |
|                   | Login Page         | Login                 | > Enter ID, Password<br> > Display error message "Unable to find ID or password" if ID does not exist or if ID and password do not match<br> > Move to main page upon successful login<br>                                                                                                                                                                                                                                                                                                             |                                                                                                                          |
|                   | Find ID           | Retrieve ID            | > Enter Email<br> > Send ID reset link to email<br> > Move to login page after completing ID change<br>                                                                                                                                                                                                                                                                                                                                                                                             |                                                                                                                          |
|                   | Find Password         | Reset Password          | > Enter Email<br> > Send password reset link to email<br> > Move to login page after completing password change<br>                                                                                                                                                                                                                                                                                                                                                                                         |                                                                                                                          |
| My Page        | My Page List (Main) | Logout               | > Move to main page after logout<br>                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |                                                                                                                          |
|                   |                       | 	Saved Movies       | > Display list of movies saved for later viewing (private)<br> > Display list of liked movies (public)<br> > Display list of reviews written by the user<br>                                                                                                                                                                                                                                                                                                                                                                                                            | > Pie chart of genres of liked movies                                                                              |
|                   |                       | Following, Followers       | > Display profile image<br> > Display brief self-introduction<br> > Display following count<br> > Display follower count<br> > Click on following or follower count to pop up list of following or followers<br>                                                                                                                                                                                                                                                                                                                                                                                                            | > Pie chart of genres of liked movies 
|                   |                       | Other User Profiles       | > Click on another user's ID to view their liked movies and written reviews<br>                                                                                                                                                                                                                                                                                                                                                                                                                                | > Rating feature like in Carrot Market? -> Identifies if the reviewer is reliable                                                                      |
|                   | My Page Edit       | Profile Image Upload     | > Click on profile picture to load a window for selecting an image file to upload<br> > Upload image upon file selection, display message "Profile image update completed" upon completion<br> > Update only this part<br>                                                                                                                                                                                                                                                                                               |                                                                                                                          |
|                   |                       | Edit User Information           | > Unable to change ID<br> > Can change name, email, mobile phone<br> > Update only this part<br>                                                                                                                                                                                                                                                                                                                                                                                                              |                                                                                                                          |
|                   |                       | Change Password          | > Allow information modification only if the existing password matches<br> > Verify password and password confirmation match<br> > Update only the password upon completion<br>                                                                                                                                                                                                                                                                                                                             |                                                                                                                          |
|                   |                       | Account Deletion              | > Process deletion only if the entered password before deletion matches<br> > Display confirmation message when clicking the delete button<br> > Move to logout and then to the main page after deletion<br>                                                                                                                                                                                                                                                                                                                                  |                                                                                                                          |
| Movie Recommendation          | Main Recommendation Page   | Periodical Movie Recommendations | > Select period (1960s to 2020s)<br> > First select decade, then detailed year<br> > Upon period selection, recommend 5 representative movies and 5 hidden masterpieces for that period, and provide a video of the top movie<br> > Genre selection feature<br> > Provide a function to check desired genres through a popup window, including a checkbox for selecting all genres<br> > Representative Movies<br> : List of top-rated movies for the selected year<br> : Consider weight of movies that did well in box office or received many awards<br> > Hidden Masterpieces<br> : Recommend movies with high ratings but low box office performance or screenings<br> : Discover hidden masterpieces based on user reviews and ratings<br>       |  > Adult content filter<br> > Add a 'Do Not Recommend' button<br> > Exclude 'Do Not Recommend' movies from the list and recommend the next in line<br> |
|                   | Movie Detail Page      | Main Movie Details | > Movie poster image, title, genre, detailed description, release year, runtime, average rating, movie video<br> > Write and display reviews under the movie video<br> > Provide a section for rating and writing content in the review writing window<br> > Save to 'Watch Later' and 'Like' button, save to respective databases<br> > Provide a list of reviews with author, content, and rating in recent order<br> > Click on review author to move to author's page                                                                                                                                                                                                                                                                | > Data analysis of ratings                                                                                                        |
|                   |                       | Review List            | > Rating, author, review title<br> > Show the latest 5 reviews<br> > Click on review author to move to author's profile<br>                                                                                                                                                                                                                                                                                                                                                                |                                                                                                                          |
|                   |                       | Write/Edit Rating & Review       | > Write on movie detail page<br> > Write rating and review<br> > For rating, use a colored star rating system<br>                                                                                                                                                                                                                                                                                                                                                                                                    | > Need to check if review and community features should be separated -> Yes, separate<br> -> Write reviews on movie detail page<br>                |
|                   |                       | Edit Review              | > Only the review author can edit<br> > Edit on movie detail page<br> > Update only this part<br> > Show the original review content during editing<br>                                                                                                                                                                                                                                                                                                                                        |                                                                                                                          |
|                   |                       | Delete Review              | > Only the review author and admin can delete<br> > Confirm deletion again<br> > Update only this part<br>                                                                                                                                                                                                                                                                                                                                                                                                               |                                                                                                                          |
| Search             |                      |                       | > Provide a list of movies containing the searched word in the title when a word is entered in the search bar<br> > Move to movie detail page upon clicking a movie<br>                                                                                                                                                                                                                                                                                                                                                                                                                                                 | > Display message "List of movies searched with 'keyword'"
| Community          | Main Community Page  | Post List          | > Display 20 posts<br> > Display list number + title + author + creation time + number of likes<br> > Provide two display methods (likes, most recent) in button format<br> > Post according to the number of likes<br> > Display posts in order of most recent creation                                                                                                                                                                                                                                                                                                                                                                                                                                                 | > Notice feature (only admin can write)<br>                                                    |
|                   |                       | Write Post            | > Only possible in logged-in state<br> Provide title, content, and a 'Write' button                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |                                                                                                                          |
|                   | Community Detail Page  | Post Details            | > Display title, content, like button, comments, sub-comments list<br> > Only the post author can see edit, delete buttons<br> > Admin can also delete                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |                                                                                                                          |
|                   |                     | Edit Post            | > Only the post author can edit                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |                                                                                                                          |
|                   |                       | Delete Post            | > Only the post author and admin can delete                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |                                                                                                                          |
|                   |                       | Comment List            |> Display only on the respective post page<br> > Display comment author and content<br> > Allow likes on comments<br> > Display the number of likes on comments<br>                                                                                                                                                                                                                                                                                                                                                                                                                         |                                                       |
|                   |                       | Sub-Comment List          | > Display under the parent comment<br> > Display sub-comment author and content<br>                                                                                                                                                                                                                                                                                                                                                                                                                      | > Allow likes on sub-comments<br> > Display the number of likes on sub-comments<br>                                                  |
|                   |                       | Write Comment              | > Only possible on the post detail page<br> > Only possible in logged-in state<br> > Update only this part<br>                                                                                                                                                                                                                                                                                                                                                                                                   |                                                                                                                          |
|                   |                       | Write Sub-Comment            | > Only possible under the parent comment on the post detail page<br> > Only possible in logged-in state<br> > Update only this part<br>                                                                                                                                                                                                                                                                                                                                                                                     |                                                                                                                          |
|                   |                       | Edit Comment              | > Only possible on the post detail page<br> > Only the comment author can edit<br> > Update only this part<br>                                                                                                                                                                                                                                                                                                                                                                                                         |                                                                                                                          |
|                   |                       | Edit Sub-Comment            | > Only possible under the parent comment on the post detail page<br> > Only the sub-comment author can edit<br> > Update only this part<br>                                                                                                                                                                                                                                                                                                                                                                                         |                                                                                                                          |
|                   |                       |  Comment Deletion              |  > Deletion only possible on the detailed post page<br> > Only the comment author and administrators can delete<br> > Updates only the relevant section<br> > When a comment is deleted, all its associated replies are also removed<br>                                                                                                                                                                                                                                                                                                                                              |                                                                                                                          |
|                   |                       | Reply Deletion            | > Deletion only possible under the parent comment on the detailed post page<br> > Only the reply author can delete<br> > Updates only the relevant section<br>                                                                                                                                                                                                                                                                                                                                                                                   |                                                                                                                          |
 
<br>
<br>
 
### ERD  
This document details the Entity-Relationship Diagram (ERD) designed for the movie recommendation website project. The ERD illustrates the system's database schema, showcasing how various entities such as users, movies, reviews, and community posts are interconnected.  

<br>

<img src='./img/ERD_final.png'>

<br>
<br>
 
### API Design  
This document outlines the API design for the movie recommendation website. The API serves as the backbone for communication between the website's front-end and back-end, facilitating features like user authentication, movie information retrieval, reviews handling, and community interaction.

#### Authentication-Related APIs (Using 'accounts' app / dj-rest-auth) 
 
| Function                | Method     | Endpoint                                           | Description                                       |
|-------------------------|------------|----------------------------------------------------|---------------------------------------------------|
| User Registration       | POST       | `/api/v1/accounts/signup/`                         | Registers a new user.                             |
| User Login              | POST       | `/api/v1/accounts/login/`                          | Logs in a user.                                   |
| User Logout             | POST       | `/api/v1/accounts/logout/`                         | Logs out a user.                                  |
| User Follow/Unfollow    | GET, POST  | `/api/v1/accounts/user/{username}/follow/`         | Follows or unfollows a specific user.             |
| Following List          | GET        | `/api/v1/accounts/{username}/followingslist/`      | Retrieves the following list of a specific user.  |
| Follower List           | GET        | `/api/v1/accounts/{username}/followerslist/`       | Retrieves the followers list of a specific user.  |
| Movie Like/Unlike       | POST       | `/api/v1/accounts/movies/{movie_id}/like/`         | Toggles like status for a specific movie.         |
| Movie Likes List        | GET        | `/api/v1/accounts/users/{username}/likelist/`      | Retrieves the like list for specific movies.      |
| Movie Wishlist Add/Remove | POST     | `/api/v1/accounts/movies/{movie_id}/wishlist/`     | Toggles a specific movie's inclusion in the wishlist. |
| Movie Wishlist List     | GET        | `/api/v1/accounts/users/{username}/wishlistlist/`  | Retrieves the wishlist of movies for a user.      |
| My Page                 | GET        | `/api/v1/accounts/profile/{username}/`             | Retrieves the profile page of a user.             |
| Account Deletion        | POST       | `/api/v1/accounts/delete_account/`                 | Proceeds with the account deletion for a logged-in user. |
| Movie Recommendation Info | GET      | `/api/v1/accounts/like_wishlist_recommendations/{username}/` | Retrieves info for movie recommendations based on last liked and wishlisted movies. |
| Genre for Recommendation | GET       | `/api/v1/accounts/get_genre/`                      | Returns the most prevalent genre from wishlisted movies for recommendations. |
 
#### Movie/Movie Review APIs (Using 'movies' app)  
 
| Function                | Method     | Endpoint                                      | Description                                     |
|-------------------------|------------|-----------------------------------------------|-------------------------------------------------|
| All Movies List         | GET        | `/api/v1/movies/`                             | Retrieves a list of all movies.                 |
| Movie Details           | GET        | `/api/v1/movies/{movie_id}/`                  | Retrieves detailed information about a specific movie. |
| Specific Movie Reviews View/Add | GET, POST | `/api/v1/movies/{movie_id}/reviews/`       | Views or adds reviews for a specific movie.     |
| Specific Movie Review Edit/Delete | PUT, DELETE | `/api/v1/movies/reviews/{review_id}`    | Edits or deletes a specific review and rating.  |
| Masterpiece Movie Recommendation | GET   | `/api/v1/movies/recommend/`                  | Recommends movies based on selected year and genre, ranked by rating. |
| Hidden Gem Movie Recommendation | GET    | `/api/v1/movies/recommend_hidden/`           | Recommends high-rated but less known movies based on selected year and genre. |
| Recommended Movies List | GET        | `/api/v1/movies/list/<int:movie_id>`          | Retrieves a list of recommended movies.         |
 
#### Community-Related APIs (Using 'communities' app) 
 

| Function                | Method     | Endpoint                                      | Description                                     |
|-------------------------|------------|-----------------------------------------------|-------------------------------------------------|
| Posts List View/Add     | GET, POST  | `/api/v1/community/posts/`                    | Views or adds posts in the community section.   |
| Post View/Edit/Delete   | GET, PUT, DELETE | `/api/v1/community/posts/{post_id}/`       | Manages specific community posts.               |
| Post Like/Unlike        | POST       | `/api/v1/community/posts/{post_id}/like/`     | Adds or removes a like on a specific post.      |
| Comments/Replies View/Add | GET, POST | `/api/v1/community/posts/{post_id}/comments/` | Views or adds comments and replies to a post.   |
| Comment/Reply Edit/Delete | PUT, DELETE | `/api/v1/community/comments/{comment_id}/`  | Edits or deletes a comment or reply.            |
| Comment Like/Unlike     | POST       | `/api/v1/community/comments/{comment_id}/like/` | Adds or removes a like on a specific comment.   |
   
<br>
<br>
 
### VUE COMPONENTS  
This document provides an overview of the Vue components used in the movie recommendation website. Vue.js, a progressive JavaScript framework, is utilized to create interactive and dynamic user interfaces. The components are modular and reusable, enhancing the efficiency of the development process.
 
<br>

<img src='./img/Vue.png'>
   
<br>
<br>
 
## ABOUT OUR PROJECT 👀

### Signup  
1. Display text using Typed.js.
2. Display feature descriptions and frequently asked questions.
3. Add movement on button hover.
4. Navigate to Login and Signup.
5. Do not display the navigation bar in the Intro window.
<video src="./img/signup.mp4" style="max-width: 730px;" autoplay muted></video>

<br>

### Account Deletion  
1. When proceeding with account deletion, delete the information from the database, log out, and then navigate to the INTRO PAGE.  
<video src="./img/account deletion.mp4" style="max-width: 730px;" autoplay muted></video>
 
<br>
 
### Login & Logout  
1. Access the database using the username and password when logging in.  
2. Navigate to the INTRO PAGE upon logging out.  
<video src="./img/login&logout.mp4" style="max-width: 730px;" autoplay muted></video>
 
<br>  
 
### Select Decade & Genre  
1. Set the decade.  
2. For the genre, enable both 'select all' and 'multiple selections'.  
3. Receive decade and genre data and navigate to the movie recommendation page.  
<video src="./img/preference survey.mp4" style="max-width: 730px;" autoplay muted></video>
 
<br>  
 
### Provide a List of Recommended Movies  
1. Recommend movies based on the preference survey.  
2. Provide trailer videos for the recommended movies.  
3. Recommend 10 masterpieces and 10 hidden gems separately; masterpieces are recommended based on ratings, while hidden gems are high-rated but lesser-known movies.  
<video src="./img/provide list.mp4" style="max-width: 730px;" autoplay muted></video>
 
<br>  
 
### Movie Information, Similar Movie Recommendations, Reviews, Likes, WISHLIST Storage  
1. Provide movie information including posters, trailers, etc.  
2. Use the SIMILAR API to recommend movies similar to the current one.  
3. Enable writing movie reviews, saving likes, and WISHLIST.  
<video src="./img/movie information.mp4" style="max-width: 730px;" autoplay muted></video>
 
<br>
 
### Continuous Recommendations of Similar Movies
1. Clicking on a movie recommended as similar navigates to its detailed page.
2. Writing movie reviews is possible.
<video src="./img/continuous.mp4" style="max-width: 730px;" autoplay muted></video>  
 
<br>  
 
### Ability to Write Review Content and Star Ratings  
1. When writing a review, the star rating is filled in according to mouse movement.
2. For movie reviews, only one's own reviews can be edited or deleted.
3. When editing, the original data is displayed.
<video src="./img/star rating.mp4" style="max-width: 730px;" autoplay muted></video>  
 
<br>  
 
### Search  
1. Search is conducted through a modal window.
2. Entering a word in the search bar provides a list of movies containing that word in their title.
3. Clicking on a movie navigates to its detailed page.
4. When there are multiple movies, scrolling is possible within the modal.
<video src="./img/search.mp4" style="max-width: 730px;" autoplay muted></video> 
  
<br>  
  
### Community  
1. Display the list number, title, author, time of creation, and the number of likes.
2. Provide two display formats (by likes, by recency) as buttons: Display posts in order of likes, Display posts in order of most recent creation.
<video src="./img/community1.mp4" style="max-width: 730px;" autoplay muted></video>  
 
<br>  
 
1. Writing Community Posts.
<video src="./img/community2.mp4" style="max-width: 730px;" autoplay muted></video>  
 
<br>
 
### Community Comments  
1. Write comments on community posts.
2. Ability to like posts.
3. View only the comments relevant to a specific post.
4. Only the author can edit or delete their comments.  
<video src="./img/community comments.mp4" style="max-width: 730px;" autoplay muted></video>  
 
<br>  
 
### Follow & Follower  
1. Clicking on an author's name in the community redirects to that USER's PROFILE PAGE.
2. Ability to follow or unfollow if the user is not oneself.
3. Provides a list of followings and followers.
4. WISHLIST is not displayed if the user is not oneself.  
<video src="./img/follow follower.mp4" style="max-width: 730px;" autoplay muted></video> 

<br>
<br>
 
## BRAINSTORMING IDEAS 🧠  
This is the records of discussions/meetings during the project duration.  
  
### 2023.10.24

1. Roles of Members
    - Front-End: Hana Na (Provides the overall concept and necessary feature ideas for the front-end) 
    - Back-End: Yejin Eum, Chaeun Lee (Handles the back-end, design concept, and assists with the front-end)
  
2. Tools to be used 
    - Django, Vue.js/Vanilla js, Bootstrap  
  
3. Movie Recommendation Website Ideas  
    - Recommendations based on the day of the week
    - Recommendations by time of day
    - Movie suggestions according to the weather
    - Movie suggestions related to favorite songs
    - Movies suitable for preferred genres, gender, and age groups 
    - Recommendations based on zodiac sign 
    - Recommendations according to blood type
    - Movie suggestions based on physiognomy (face reading)
    - Real-time popular movies
    - A service that reads out movies for visually impaired individuals
  
4. Website Design Ideas
    - When clicking on a number (e.g., genre), a can from a vending machine shows the recommended movie.
    - Recommended movies shown as leaves falling from a tree 

5. Features to be Implemented 
    - Real-time trending movies
    - User registration, login, logout, and profile update 
    - Community features:
      - Post and comment
      - Q & A, Inquiries, Pinned Posts (Frequently Asked Questions)
    - Articles: 
      - Professional critic reviews:
        - Lengthy review content allowed
      - Regular user reviews:
        - Short reviews with a rating system
        - Receipt reviews (Trust enhanced by verifying with ticket pictures)