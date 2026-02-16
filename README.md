# Pawfect-Match

<p align="center">

</p>

[Link to Live Website]

## About 

**Pawfect-Match** is a web application inspired by Tinder, Bumble, and Hinge, designed to help dog owners find a companion for their dog (and maybe love for themselves too). The platform targets dog owners, whether single or not, and provides a fun, social way to connect through their pets. Users can create an account, like or dislike dogs and owners, and chat once there is a match.

## Index – Table of Contents
* [User Experience (UX)](#user-experience-ux)
   * [Strategy](#strategy)
   * [Scope](#scope)
   * [Structure](#structure)
   * [Skeleton](#skeleton)
   * [Surface](#surface)

* [Features](#features)
* [Technologies Used](#technologies-used)
* [Testing](#testing)
* [Deployment](#deployment)
* [Credits](#credits)

## User Experience (UX)

### Strategy

With **Pawfect-Match** I wanted to give dog owners a fun and safe way to connect with other dog owners. By blending the best ideas from modern dating apps into one web experience, the platform helps dogs find playmates and gives humans a chance to find love through their pets.

#### Business goals of the website
- Provide a friendly platform for dog owners to discover compatible companions.
- Encourage sign-ups and profile completion to improve matching quality.
- Build engagement through likes, matches, and messaging.

#### Customer goals of the website
- Quickly understand how the platform works.
- Create profiles for themselves and their dog with minimal friction.
- Discover and connect with other dog owners.
- Chat safely once a match is made.

#### User stories

**New User**
- I want to understand what the site is about.
- I want to see if the platform is for me without registering.
- I want to register easily.
- I want to add my dog's details.

**Existing User**
- I want to sign in and out easily.
- I want to create and edit my owner profile.
- I want to create and edit my dog profile.
- I want to like or dislike dogs to find matches.
- I want to see my matches and remove a match if I change my mind.
- I want to reset my password.

**All Users**
- I want clear feedback when I take actions on the site.
- I want to message other profiles after matching.
- I want to edit or delete my own information and images.

#### Reasons for the website
- Playmate finding
- Walk arranging
- Promoting interactions between owners
- Potential breeding
- Dating opportunities for owners through their dogs
  
### Scope

#### In scope Features:
 - Account registration and sign in.
 - Owner profile creation and editing.
 - Dog profile creation and editing.
 - Like and dislike actions to find matches.
 - Match list management.
 - Messaging between matched users.
 - Password reset without email (demo mode).

#### Out of scope Features:
 - Real-time chat or live notifications.
 - Advanced search and filters.
 - Payment or subscription plans.
 - Location-based matching.

### Structure

The home page explains the concept first with a clear hero CTA, then guides users into sign up. It also includes a navbar that links to the "How it works" and "Why Pawfect Match" sections. After that, the site follows a simple, linear flow so users always know what to do next. Navigation stays consistent with a top navbar linking to Discover, Matches, Messages, Profile and Log out.

Pawfect-Match uses a multi-page application (MPA) structure with server-side rendering (SSR) via Django, so each route loads a dedicated page instead of switching views inside a single SPA.

The page structure follows 2026 web design principles: clear primary CTAs, short task-focused screens, strong visual hierarchy, and a mobile-first layout that keeps the main actions within easy reach.

Key sections and navigation flow:
- Home: hero CTA, how it works, and value propositions.
- Auth: register, sign in, and password reset.
- Onboarding: create owner profile first, then create dog profile.
- Discover: browse profiles with dog/owner toggle and like/dislike actions.
- Matches: view matched profiles, delete a match, and message from a match.
- Messages: inbox list and message threads.
- Profile: view owner/dog profiles, edit profiles, and delete account.

#### Technical Implementation
 - Django 4.2 with a multi-app architecture.
 - Database configured via `DATABASE_URL` (PostgreSQL in production).
 - Server-rendered templates with Bootstrap 5 utilities.
 - Cloudinary for media storage and image delivery.
 - WhiteNoise for static file serving.
 - Crispy Forms + Bootstrap 5 for clean form rendering.
 - Environment-based config via `python-dotenv` and `env.py`.
 - Custom CSS and JavaScript for UI enhancements.

### Skeleton

### Wireframes
 - Wireframes created during planning for the main flows:
    - Home and onboarding: hero CTA, "How it works" steps, and value props.
    - Authentication: sign up, sign in, and password reset entry.
    - Create owner profile: photo, name, age, city, occupation, interests, and bio.
    - Create dog profile: photo, name, age, breed, size, gender, energy, and bio.
    - Discover: dog/owner toggle card with like/dislike actions and match modal.
    - Matches: grid of matched profiles, delete match action, and empty state.
    - Messaging: inbox list, message thread view, and empty thread state.
    - Profile: view owner and dog cards, edit profile flows, and delete profile modal.

### Surface

#### Visual Style

**Design:**
Warm, friendly, and playful UI with rounded elements and soft shadows.

**Typography:**
Roboto Flex with bold, readable headings for clarity.

#### Colors 
Orange brand palette for energy and warmth, balanced with light backgrounds.

## Features

#### **Responsive Design**

#### **User Experience Enhancements**

### Future Features

## Technologies Used

__Languages Used__

* [HTML5](https://en.wikipedia.org/wiki/HTML5)
* [CSS](https://en.wikipedia.org/wiki/CSS)
* [JavaScript](https://en.wikipedia.org/wiki/JavaScript)
  
__Frameworks, Libraries & Programs Used__

* [Bootstrap 5](https://getbootstrap.com/docs/5.3/getting-started/introduction/): was used for responsive layout, button styling, and utility classes
* [Google Fonts](https://fonts.google.com/): was used to import the 'Baloo 2', 'Quicksand', and 'Poppins' fonts into the style.css 
* [Font Awesome](https://fontawesome.com/): was used to add icons for aesthetic and UX purposes.
* [GitHub](https://github.com/): is used as the repository for the project's code after being pushed from Git.
* [Photoshop](https://www.adobe.com/uk/products/photoshop.html): was used for early design to help get a better idea of which colors and images would suit the website. It was also used to resize and edit pictures, as well as create the menus and color palette
* [Visual Studio Git Source Control](https://learn.microsoft.com/en-us/visualstudio/version-control/git-with-visual-studio?view=vs-2022): was used to commit and push or pull changes to GitHub 
* [Balsamiq](https://balsamiq.com/): was used to create the wireframes during the design process.
* [ChatGPT](https://openai.com/chatgpt): was used to assist with grammar correction, code structure improvements, and README documentation organization
* [Copilot in VS Code](https://code.visualstudio.com/docs/copilot/overview): was used to help with code completion, debugging, and suggesting best practices for JavaScript implementation
* [WAVE](https://wave.webaim.org/) & [Lighthouse](https://developer.chrome.com/docs/lighthouse): Used for accessibility testing to ensure that all content is readable and accessible to every user.
* [HTML Validator](https://validator.w3.org/#validate_by_input): Confirmed the HTML code is valid, with no errors detected.
* [CSS Validator](https://jigsaw.w3.org/css-validator/#validate_by_input): Verified the CSS code, with no errors detected.
* [JS-Beautify](https://beautifier.io/): Checked the formatting and structure of the HTML and CSS for consistency and readability.

## Testing 

### Validator Testing

[**HTML Validator**](https://validator.w3.org/)

[**CSS Validator**](https://jigsaw.w3.org/css-validator/)

#### CSS Warnings

## CSS Validation Warnings — Summary and Explanation

[**JavaScript Validator**](https://jshint.com/)

## Functionality Testing

### Performance

#### Desktop Performance

#### Mobile Performance

### Testing User Stories

## Deployment

(with Heroku)

## Credits

### Visual Design References

### Code References






