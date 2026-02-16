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
   * [Admin Page](#admin-page)
   * [CRUD Operations](#crud-operations)
   * [Database Schema](#database-schema)
   * [Skeleton](#skeleton)
   * [Surface](#surface)

* [Features](#features)
* [Future Features](#future-features)
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
 - Owner profile creation and editing with photo upload.
 - Dog profile creation and editing with photo upload.
 - Browse and discover dogs page.
 - Toggle between dog and owner profile to view their profiles while browsing.
 - View other users complete profiles (dog + owner details).
 - Like and dislike actions to find matches.
 - Automatic bidirectional matching system.
 - "It's a match!" modal popup with dogs photos.
 - Match list management (view and delete individual matches).
 - Reset all matches, dislikes, and messages to restart (available when no more dogs to browse).
 - Messaging between matched users.
 - Delete entire conversation threads.
 - Account deletion (removes all associated data).
 - Password reset via email verification form (validates account email without sending email).

#### Out of scope Features:
 - Real-time chat or live notifications.
 - Profile verification badges
 - Block/report user functionality
 - Multiple dogs per user account
 - Photo galleries (multiple photos per profile)
 - Advanced search and filters.
 - Advanced matching algorithm (based on breed compatibility, location, etc.)
 - In-app event creation (dog park meetups, playdates)
 - Social media sharing
 - Read receipts for messages
 - Payment or subscription plans.
 - Premium/paid features
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
 - Custom CSS and JavaScript for UI enhancements.
 - Environment-based config via `python-dotenv` and `env.py`.

### Admin Page

The Django admin interface provides full management capabilities for all models:

**User Management:**
- View all registered users
- Edit user details (username, first name, last name, email)
- Change user password via dedicated form
- Set user permissions (Active, Staff status, Superuser status)
- Assign users to groups
- Delete user accounts

**Owner Profiles:**
- View all owner profiles with their details
- Edit profile information (name, age, city, occupation, interests, about_me)
- Update profile photos
- Delete owner profiles

**Dog Profiles:**
- View all dog profiles
- Edit dog information (name, age, breed, size, gender, energy_level, about_me)
- Update dog photos
- Delete dog profiles

**Connections (Matches):**
- View all connections between all dogs in the database
- See from_dog and to_dog relationships for every match
- Delete connections to unmatch dogs

**Messages:**
- View all messages sent between matched dogs
- See sender, receiver, message content, and timestamp
- Search messages by dog name
- Filter messages by date
- Delete message records

### CRUD Operations

**Pawfect-Match** implements full CRUD (Create, Read, Update, Delete) functionality across all core features:

#### **User Accounts**
- **Create**: Users can register a new account with email and password
- **Read**: Users can sign in to access their account
- **Delete**: Users can permanently delete their entire account (removes user, profiles, dog, connections, and messages)

#### **Owner Profiles**
- **Create**: During registration, users create their owner profile with name, age, city, occupation, interests, and photo
- **Read**: Users can view their complete profile and other users' profiles when browsing dogs
- **Update**: Users can edit their owner profile information and update their photo at any time
- **Delete**: Owner profile is deleted as part of account deletion

#### **Dog Profiles**
- **Create**: After creating an owner profile, users add their dog's profile with photo, name, age, breed, size, gender, energy level, and about section
- **Read**: Users can view their dog's profile and browse other dogs' profiles on the discovery page
- **Update**: Users can edit their dog's profile information and update photos
- **Delete**: Dog profile is deleted as part of account deletion

#### **Connections (Matches)**
- **Create**: Users can like dogs to create automatic bidirectional matches (no swipe-right/left waiting—instant connection)
- **Create**: Users can dislike dogs to remove them from their discovery feed
- **Read**: Users can view all their matches in a dedicated matches list showing matched dogs and owner information
- **Delete**: Users can unmatch individual connections from their matches list
- **Delete**: When no more dogs are available to browse, users can reset all matches, dislikes, and messages to restart their discovery experience

#### **Messages**
- **Create**: Users can send messages to matched dogs through conversation threads
- **Read**: Users can view their inbox showing all conversations and read full message threads with each match
- **Delete**: Users can delete entire conversation threads from their inbox

#### **User Feedback**
- "It's a match!" modal popup with photos when matches occur
- Form validation error messages displayed on forms

### Database Schema
The system uses the Django ORM with a PostgreSQL database in production (via `DATABASE_URL`). The core data model is focused on owners, dogs, matches, and messaging.

**Models**
- User (Django auth)
   - Standard authentication user model used for login and ownership.
- OwnerProfile
   - user (OneToOne -> User)
   - profile_photo (CloudinaryField)
   - name, age, city, occupation
   - interests (comma-separated string)
   - about_me, created_at
- Dog
   - owner (OneToOne -> OwnerProfile)
   - profile_photo (CloudinaryField)
   - name, age, breed
   - size, gender, energy_level (choices)
   - about_me, created_at
- Connection
   - from_dog (ForeignKey -> Dog)
   - to_dog (ForeignKey -> Dog)
   - created_at
- Dislike
   - from_dog (ForeignKey -> Dog)
   - to_dog (ForeignKey -> Dog)
   - created_at
- Message
   - sender_dog (ForeignKey -> Dog)
   - receiver_dog (ForeignKey -> Dog)
   - content, created_at

**Schema characteristics**
- One-to-one: User -> OwnerProfile, OwnerProfile -> Dog.
- One-to-many: Dog -> Connection/Dislike/Message.
- Match logic uses bidirectional Connection entries.

### Skeleton

### Wireframes
   Made in figma

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

### Universal Features Across the Site

#### **Responsiveness**
- Fully responsive design adapting seamlessly from mobile to desktop
- Mobile-first approach using Bootstrap 5 grid system and custom media queries
- Collapsible navigation menu on smaller screens with hamburger toggle
- Flexible layouts that reflow content based on viewport size
- Optimized images with responsive sizing for faster load times

#### **Accessibility**
- ARIA labels on all interactive elements (buttons, links, modals, form inputs)
- Descriptive alt text on all images describing visual content
- Focus states visible on all interactive components for keyboard navigation

#### **Navigation**
- **Public Users**: Simplified navbar with:
  - Home: Hero section and value propositions
  - How it works: Step-by-step guide
  - Why Pawfect Match: Benefits overview

- **Authenticated Users**: Persistent navigation bar with links to:
  - Discover: Browse dog profiles
  - Matches: View matched connections
  - Messages: Access inbox and conversations
  - Profile: View and edit personal profiles
  - Log out: End session

- Auto-collapse on mobile when navigation link is clicked
- Consistent navbar styling across all authenticated pages

#### **Footer**
- Social media links (Twitter, Instagram, Facebook) opening in new tabs
- Copyright information (2026 Pawfect Match)
- Use of Font Awesome icons for social platforms
- Consistent placement on all pages
- Accessible with proper ARIA labels on social links (screen reader announces "Twitter", "Instagram", "Facebook")

#### **Input Fields & Forms**
- Custom form styling with CSS for consistent appearance across all forms
- Django form validation with server-side error display (errors shown after form submission)
- Required field indicators with asterisk (*) labels
- Password visibility toggle with eye icon on password inputs
- Image upload preview before form submission
- Drag-and-drop support for photo uploads
- Placeholder text for guidance

#### **Base Templates**
- **base.html**: Core layout with header, main, footer structure
- **base_auth.html**: Extended layout for authenticated user pages
- Meta tags for SEO (description, viewport)
- Favicon integration
- Centralized loading of Bootstrap 5, Font Awesome, and custom assets
- Django template blocks for flexible page-specific content

### Error Pages

#### **404 - Page Not Found**
- Custom-designed error page matching site branding
- Playful "Page isn't a match" messaging aligned with dating theme
- Sad dog illustration for emotional connection
- Clear navigation options:
  - "Back to Home" button for all users
  - "Browse Dogs" button for authenticated users, "Get Started" button for guests
- Maintains site header/footer for consistent user experience
- Prevents user frustration with friendly, helpful design

### Features Specific to Pages

#### **Homepage (Public)**
- **Hero Section**:
  - Eye-catching image of couple with dog
  - Clear value proposition: "Find Love Through Your Pet"
  - Dual CTA buttons: "Get Started" (register) and "Sign In"
  - Mobile-optimized layout with stacked content
  
- **How It Works Steps**:
  - Step 1: Find love with other pet lovers
  - Step 2: Your furry friend is the icebreaker
  - Step 3: Preview owners before liking
  - Step 4: Match and start chatting
  - Visual illustrations supporting each step
  - Scroll-friendly full-screen sections
  
- **Why Pawfect Match**:
  - Section header with tagline
  - Grid of 4 feature cards (Pet-First Approach, Authentic Connections, Safe & Friendly, Easy Communication)
  - Concise descriptions for each card

#### **Authentication Pages**

**Register**
- Email-based registration (email used as username)
- Password confirmation field for accuracy
- Password validation (minimum length, complexity)
- Link to Sign In page for existing users
- Auto-redirect to owner profile creation after successful registration
- Session-based data persistence: profile details (name, age, city, etc.) stored in session during onboarding, allowing users to return and edit before completion (images only stored after final submission)
- Form validation with Django messages

**Sign In**
- Email and password authentication
- "Forgot Password" link
- Next URL parameter support for protected pages
- Auto-redirect to browse dogs after successful login
- Error messages for invalid credentials

**Forgot Password / Change Password**
- Email verification form (checks if account exists)
- No email sent (demo/prototype mode)
- Direct password reset after email validation
- Password confirmation field
- Success page with "Go to Sign In" button
- Validation prevents password resets for non-existent accounts

#### **Profile Creation & Editing**

**Create Owner Profile**
- Multi-step onboarding flow (Owner → Dog → Browse)
- Fields: Name, Age, City, Occupation, Interests (multi-select pills), About Me, Photo
- Image upload with preview (Cloudinary integration)
- Drag-and-drop photo support
- Interests (select up to 3 as pill-style options)
- Session-based data persistence during onboarding
- Auto-redirect to Create Dog Profile after completion

**Create Dog Profile**
- Final onboarding step before accessing main app
- Fields: Name, Age, Breed, Size, Gender, Energy Level, About Me, Photo
- Dropdown selections for size (Small, Medium, Large), gender (Male, Female), energy level (Low, Medium, High)
- Image preview before upload
- One-to-one relationship with owner profile
- Auto-redirect to Browse Dogs after creation
- User login happens automatically after dog creation

**Edit Owner Profile**
- Access from Profile page
- Pre-populated form with existing data
- Update photo with new upload or keep existing
- Same fields as creation form
- Redirect back to profile view

**Edit Dog Profile**
- Access from Profile page
- Pre-populated form with current dog information
- Photo update functionality
- Same validation as creation
- Redirect back to profile view

#### **View Profile**
- **Profile Toggle**: Switch between viewing your dog profile and owner profile
- **Dog View**:
  - Dog photo, name, age, breed
  - About me section
  - Energy level and size badges
  - Edit button linking to edit form
  
- **Owner View**:
  - Owner photo, name, age, city, occupation
  - Interests displayed as pills/tags
  - About me section
  - Edit button linking to edit form
  
- **Delete Account Modal**:
  - Confirmation modal with warning message
  - Explains data deletion: user profile, dog profile, all matches, and all conversations
  - "Cancel" and "Delete Account" buttons
  - JavaScript confirmation prompt
  - Cascade delete handled by Django (removes all user data)

#### **Discover / Browse Dogs**
- **Profile Cards**:
  - Large photo display with overlay (name, age, breed, city, gender)
  - Toggle between Dog and Owner views with active state indicator
  - Smooth transitions between views
  - About me section
  - Dog metadata: Energy level and size tags
  - Owner metadata: Age, occupation, interests pills
  
- **Action Buttons**:
  - Dislike (X icon): Skip dog and remove from future results
  - Like (Heart icon): Create bidirectional match and trigger modal
  
- **Match Logic**:
  - Instant bidirectional matching (both connection entries created)
  - No waiting for mutual likes - immediate match confirmation
  - "It's a Match!" modal popup with both dog photos
  - "Send Message" and "View Matches" buttons in modal linking to chat thread and matches
  
- **Empty State**:
  - Message: "No more dogs to discover"
  - "Reset Matches" button to clear all connections, dislikes, messages
  - Returns discovery pool to full state
  
- **Filtering**:
  - Excludes own dog
  - Excludes already liked dogs
  - Excludes disliked dogs

#### **Matches List**
- Grid layout of all matched dog profiles
- Each card shows:
  - Dog photo
  - Dog name and age
  - Owner name
  - "Message" button linking to conversation
  - Red X button in top-right corner to delete match with confirmation modal
- Empty state message when no matches
- Delete match removes both bidirectional connection entries

#### **Messages / Inbox**
- List of all active conversations
- Each conversation shows:
  - Matched dog photo
  - Last message preview
  - Timestamp of last message
- Empty state: "No messages yet"
- Click conversation to open thread
- Delete conversation button (trash icon) with confirmation modal

**Message Thread**
- Full conversation history with matched dog
- Messages displayed chronologically (oldest to newest)
- Timestamps on each message
- Send message form at bottom:
  - Text area input
  - Send button
- Header shows matched dog name, breed and photo

#### **Modals**

**"It's a Match!" Modal**
- Triggered on successful like that creates a match
- Displays side-by-side photos of both matched dogs
- Congratulations message
- "Send Message" button to start conversation
- "View Matches" button to view all matches
- "×" close button (gray) to dismiss modal and continue browsing
- Overlay backdrop with click-outside-to-close

**Delete Account Modal**
- Confirmation dialog for account deletion
- Warning text explaining permanent action with warning icon
- Lists what will be deleted: User profile, dog profile, all matches, all conversations
- "Cancel" button (closes modal, no action)
- "Yes, Delete" button (red/danger styling, executes deletion)
- Triggered from Profile page

**Delete Match Confirmation**
- Appears when user clicks on red X button (×) on the top right of the match card
- Modal with confirmation message: "Are you sure you want to delete this match?"
- "Cancel" button (closes modal, no action)
- "Delete" button (red/danger styling, removes both connection entries)

**Delete Conversation Confirmation**
- Triggered from trash icon button in inbox conversation list
- Modal with confirmation message and dog name
- Warning that messages will be permanently lost
- "Cancel" button (closes modal, no action)
- "Delete" button (removes all messages from conversation)

#### **Admin Panel**
- Django admin interface at `/admin`
- Full CRUD on OwnerProfile, Dog, Connection, and Message models
- **MessageAdmin Customization**:
  - Displays: sender dog name, receiver dog name, creation date
  - Search by dog name (searches both sender and receiver dog names)
  - Filter messages by creation date
  - Read-only timestamp field to prevent accidental modification
- Delete records for moderation (default Django delete functionality)
- Default Django User management (permissions, groups, password management) available through admin

### Future Features

The following features are planned for future releases to enhance user experience and expand platform capabilities:

#### **Real-Time Communication**
- **Live Chat**: WebSocket-based instant messaging replacing current page-reload messaging
- **Push Notifications**: Browser notifications for new matches, messages, and likes
- **Online Status Indicators**: Show when matched users are currently active
- **Typing Indicators**: Real-time "..." display when other user is typing
- **Read Receipts**: Blue checkmarks showing when messages are seen

#### **Advanced Matching & Discovery**
- **Distance Filters**: Set maximum radius for potential matches (5km, 10km, 25km, etc.)
- **Advanced Search Filters**:
  - Breed preferences
  - Dog size compatibility (small, medium, large)
  - Energy level matching (low, medium, high)
  - Owner age range
  - Interests matching
- **Smart Matching Algorithm**: Score-based compatibility considering:
  - Dog size and breed compatibility
  - Owner interests overlap
  - Geographic proximity
  - Energy level compatibility
  - User preferences and behavior

#### **Enhanced Profiles**
- **Photo Galleries**: Multiple images per dog and owner (up to 6 photos)
- **Profile Verification**: Blue checkmark badge after ID/photo verification
- **Multiple Dogs Per Account**: Add and manage profiles for multiple pets
- **Extended Profile Fields**:
  - Dog vaccination status
  - Behavioral traits (friendly with kids, other dogs, etc.)
  - Favorite activities
  - Training level

#### **Safety & Moderation**
- **Block/Report User**: Report inappropriate behavior or block users
- **Safety Center**: In-app dating safety tips and resources
- **Emergency Contact Sharing**: Optional feature to share location during first meetings

#### **Social Features**
- **Events & Meetups**: Create and join local dog park meetups or playdates
- **Social Media Integration**:
  - Share profile to Instagram/Facebook
  - Login with Facebook/Google

#### **Communication Enhancements**
- **Voice Messages**: Send audio clips in conversations
- **Photo Sharing in Chat**: Send pictures directly within message threads
- **GIFs & Stickers**: Express emotions with animated images
- **Emoji Reactions**: React to messages with emojis

#### **Premium/Paid Features**
- **Subscription Plans**:
  - **Free**: Basic matching and messaging with ads
  - **Premium ($9.99/month)**: Unlimited likes, see who liked you first, priority profile visibility, ad-free experience
  - **Premium Plus ($19.99/month)**: All Premium features + profile boost, advanced filters, read receipts
  
- **In-App Purchases**:
  - Super likes (show extra interest)
  - Undo last dislike

#### **Accessibility Improvements**
- **Multiple Language Support**: Translate interface to French, Spanish, German, etc.
- **Dark Mode**: Eye-friendly dark theme option

## Technologies Used

__Languages Used__

* [HTML5](https://en.wikipedia.org/wiki/HTML5)
* [CSS](https://en.wikipedia.org/wiki/CSS)
* [JavaScript](https://en.wikipedia.org/wiki/JavaScript)
* [Python](https://en.wikipedia.org/wiki/Python_(programming_language)
  
__Frameworks, Libraries & Programs Used__

* [Bootstrap 5](https://getbootstrap.com/docs/5.3/getting-started/introduction/): was used for responsive layout, button styling, and utility classes
* [Google Fonts](https://fonts.google.com/): was used to import the 'Baloo 2', 'Quicksand', and 'Poppins' fonts into the style.css 
* [Font Awesome](https://fontawesome.com/): was used to add icons for aesthetic and UX purposes.
* [GitHub](https://github.com/): is used as the repository for the project's code after being pushed from Git.
* [Heroku]():
* [Photoshop](https://www.adobe.com/uk/products/photoshop.html): was used for early design to help get a better idea of which colors and images would suit the website. It was also used to resize and edit pictures, as well as create the menus and color palette
* [Visual Studio Git Source Control](https://learn.microsoft.com/en-us/visualstudio/version-control/git-with-visual-studio?view=vs-2022): was used to commit and push or pull changes to GitHub 
* [Figma](): was used to create the wireframes during the design process.
* [ChatGPT](https://openai.com/chatgpt): was used to assist with grammar correction, code structure improvements, and README documentation organization
* [Copilot in VS Code](https://code.visualstudio.com/docs/copilot/overview): was used to help with code completion, debugging, and suggesting best practices for JavaScript implementation
* [WAVE](https://wave.webaim.org/) & [Lighthouse](https://developer.chrome.com/docs/lighthouse): Used for accessibility testing to ensure that all content is readable and accessible to every user.
* [HTML Validator](https://validator.w3.org/#validate_by_input): Confirmed the HTML code is valid, with no errors detected.
* [CSS Validator](https://jigsaw.w3.org/css-validator/#validate_by_input): Verified the CSS code, with no errors detected.
* [JS-Beautify](https://beautifier.io/): Checked the formatting and structure of the HTML and CSS for consistency and readability.

## Testing 

### Validator Testing

[**HTML Validator**]()

[**CSS Validator**]()

#### CSS Warnings

## CSS Validation Warnings — Summary and Explanation

[**JavaScript Validator**]()

## Functionality Testing

### Performance

#### Desktop Performance

#### Mobile Performance

### Testing User Stories

## Deployment

(with Heroku)

## Credits

HERO
-https://www.freepik.com/free-photo/couple-love-looks-lying-sleeping-labrador-husband-wife-relax-cozy-atmosphere_12432327.htm#from_element=cross_selling__photo

-https://www.freepik.com/free-photo/couple-looking-road-with-their-dog_980601.htm#fromView=search&page=7&position=12&uuid=28e7f528-3d67-48ea-ba60-11e02a142fcb&query=Couple+with+dogs

-https://www.freepik.com/free-photo/joyful-girl-tourist-looks-mobile-phone-texts-message-smartphone-social-media-application-walks_38794425.htm#fromView=search&page=2&position=47&uuid=39f84724-60b2-45b5-ad1b-9b13e319a27c&query=woman+browsing+on+phone

-https://www.freepik.com/free-photo/lifestyle-portrait-handsome-young-man-sitting-cafe-checking-his-phone-drinking-coffee_157867299.htm#fromView=search&page=1&position=3&uuid=b68dfbe1-a3de-4d8a-9b96-073d5d5fba3b&query=man+browsing+phone


-Artiste/ https://unsplash.com/@maeva_vgr
-Image/ https://unsplash.com/photos/a-couple-of-dogs-standing-on-top-of-a-leaf-covered-field-uJf5PtyI6Lg

-Artiste/ https://unsplash.com/@wellgraf
-Image/ https://unsplash.com/photos/man-standing-near-golden-labrador-retriever-viewing-bridge-and-high-rise-buildings-Kr29K3_c28A

-Artiste/ https://unsplash.com/@alexandermassph
-Image/ https://unsplash.com/photos/a-woman-holding-a-dog-in-her-arms-3Tuy8tU2rEE

-Artiste/ https://unsplash.com/@nate_dumlao
-Image/ https://unsplash.com/photos/person-carrying-dog-yCKKd37OsgI

-Artiste/ https://unsplash.com/@alexandermassph
-Image/ https://unsplash.com/photos/a-woman-holding-a-dog-in-a-field-Zt8scxJbUd8

-Artiste/ https://unsplash.com/@barcstamaas
-Image/ https://unsplash.com/@alexandermassph

-Artiste/ https://unsplash.com/@alvannee
-Image/ https://unsplash.com/photos/corgi-dog-wearing-a-blue-shirt-in-a-garden-ogNx3sqEa6M


DOGS

-Artiste/ https://unsplash.com/@brookecagle
-Image/ https://unsplash.com/photos/long-coated-brown-dog-Ntm4C2lCWxQ

-Artiste/ https://unsplash.com/@kierancwhite
-Image/ https://unsplash.com/photos/close-up-photo-of-black-and-white-siberian-husky-dog-NKN25UfGfkQ

-Artiste/ https://unsplash.com/@alanking
-Image/ https://unsplash.com/photos/long-coated-brown-dog-KZv7w34tluA

-Artiste/ https://unsplash.com/@whoisperi
-Image/ https://unsplash.com/photos/white-long-coat-small-dog-5Vr_RVPfbMI

-Artiste/ https://unsplash.com/@justnjames
-Image/ https://unsplash.com/photos/adult-dog-sitting-on-white-sand-near-seashore-KFJuCzJiQYU

-Artiste/ https://unsplash.com/@dinetackimanni
-Image/ https://unsplash.com/photos/brown-and-white-long-coated-dog-8mxSINYFoSw

-Artiste/ https://unsplash.com/@baptiststandaert
-Image/ https://unsplash.com/photos/long-coated-black-and-white-dog-during-daytime-mx0DEnfYxic

-Artiste/ https://unsplash.com/@victor_vector
-Image/ https://unsplash.com/photos/black-smooth-coated-dog-2pbnDRhXc6Q

-Artiste/ https://unsplash.com/@rpnickson
-Image/ https://unsplash.com/photos/brown-puppy-on-bed-gRHEt2kF3NU

-Artiste/ https://unsplash.com/@gxldy
-Image/ https://unsplash.com/photos/black-and-white-husky-v0_MCllHY9M

PERSONE

-Artiste/ https://unsplash.com/@xoutcastx
-Image/ https://unsplash.com/photos/man-standing-in-front-of-window-8Vt2haq8NSQ

-Artiste/ https://unsplash.com/@jonasjaekenmedia
-Image/ https://unsplash.com/photos/woman-in-gray-hoodie-sitting-on-black-bench-5g7tSrQSJEo

-Artiste/ https://unsplash.com/@lancereis
-Image/ https://unsplash.com/photos/a-man-with-a-beard-pp76Y6Fq6xw

-Artiste/ https://unsplash.com/@xoutcastx
-Image/ https://unsplash.com/photos/mens-white-crew-neck-shirt-bdYJWXg4pK4

-Artiste/ https://unsplash.com/@sxth
-Image/ https://unsplash.com/photos/man-sitting-near-hibiscus-flowers-during-daytime-IMYvZjlX3jE

-Artiste/ https://unsplash.com/@courtneymcook
-Image/ https://unsplash.com/photos/woman-smiling-wearing-denim-jacket-TSZo17r3m0s

-Artiste/ https://unsplash.com/@cikstefan
-Image/ https://unsplash.com/photos/smiling-woman-wearing-white-and-black-pinstriped-collared-top-QXevDflbl8A

-Artiste/ https://unsplash.com/@haletat
-Image/ https://unsplash.com/photos/a-woman-sitting-on-a-white-chair-next-to-a-table-5b_RXCDykto

-Artiste/ https://unsplash.com/@armedshutter
-Image/ https://unsplash.com/photos/woman-looking-sideways-leaning-on-white-wall-6W4F62sN_yI

-Artiste/ https://unsplash.com/@zabegina
-Image/ https://unsplash.com/photos/woman-in-black-tank-top-and-blue-denim-shorts-5c-B5MGiv2c


### Visual Design References

WEBSITE INSPO
-https://fetchadate.com/
-https://www.frolly.com/
-https://puppilovers.com/

APP INSPO
-Bumbule
-Tinder
-Hinge

### Code References






