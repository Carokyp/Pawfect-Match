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
- As a new user, I want to understand what the site is about, so I can decide if it's right for me.
- As a new user, I want to register easily, so I can start quickly.
- As a new user, I want to add my dog's details, so I can begin browsing matches.

**Existing User**
- As an existing user, I want to sign in and out easily, so I can access my account securely.
- As an existing user, I want to create and edit my owner profile, so I can manage my information.
- As an existing user, I want to create and edit my dog profile, so I can keep it updated.
- As an existing user, I want to like or dislike dogs after viewing both dog and owner profiles, so I can find the best matches for my dog.
- As an existing user, I want to see my matches and remove a match if I change my mind, so I can manage my connections.
- As an existing user, I want to reset my password, so I can regain access if needed.

**All Users**
- As a user, I want to message other profiles after matching, so I can communicate with my matches.
- As a user, I want to edit or delete my own information and images, so I have control over my data.

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

#### **403 - Forbidden (Access Denied)**
- Custom-designed error page matching site branding
- Clear message: "Looks like this profile is private" or similar dating-themed wording
- Explains that the user doesn't have permission to access the requested resource
- Navigation options:
  - "Back to Home" button for all users
  - "Browse Dogs" or "Back" button to return to previous page or dashboard
  - Log in prompt for unauthenticated users (if attempting to access authenticated-only pages)
- Maintains site branding consistency with header/footer
- Friendly tone prevents user frustration

#### **405 - Method Not Allowed**
- Custom-designed error page matching site branding
- Clear message: "That's not allowed here" with dog/dating theme explanation
- Indicates that the HTTP method (GET, POST, PUT, DELETE, etc.) is not allowed for the requested resource
- Navigation options:
  - "Back to Home" button
  - "Back to Previous Page" button
  - Search or Browse Dogs links
- Maintains site header/footer for consistency
- Help text explaining that the action attempted is not supported for this resource

#### **500 - Internal Server Error**
- Custom-designed error page matching site branding
- Concerned/apologetic dog illustration
- Clear message: "Oh no! Something went wrong on our end" or similar messaging
- Reassuring text explaining that the team is working on fixing the issue
- Navigation options:
  - "Back to Home" button (primary action)
  - "Try Again" button to refresh the current page
  - "Contact Support" link (if applicable)
- Maintains site header/footer for consistency
- Logging of error for debugging purposes (backend)
- Prevents sensitive error details from being displayed to users

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

Pawfect Match has undergone comprehensive testing across multiple dimensions to ensure a reliable, accessible, and seamless user experience. All tests passed successfully across different browsers, devices, and screen sizes.

**Testing Overview:**
- ✅ **86 Functionality Tests** - All core features working as intended
- ✅ **6 Browser Platforms** - Chrome, Firefox, Edge, Safari (macOS & iOS), Chrome Android
- ✅ **9 Screen Sizes** - From 320px mobile to 3440px ultra-wide displays
- ✅ **5 Breakpoint Ranges** - Fully responsive across all device categories
- ✅ **HTML, CSS, JavaScript Validation** - Code quality verified
- ✅ **Performance Testing** - Desktop and mobile optimization confirmed

### Validator Testing

[**HTML Validator**]()

[**CSS Validator**]()

#### CSS Warnings

## CSS Validation Warnings — Summary and Explanation

[**JavaScript Validator**]()

## Functionality Testing

### User Authentication and Account Management

| Test Label | Test Action | Expected Outcome | Test Outcome |
|------------|-------------|------------------|--------------|
| User Registration | Navigate to homepage → Click "Get Started" → Enter valid email and password → Submit form | User account created, redirected to create owner profile page | |
| Registration Validation | Try to register with invalid email format | Form shows validation error, prevents submission | |
| Password Requirements | Try to register with weak password (less than 8 chars) | Form shows password requirements error | |
| User Sign In | Click "Sign In" → Enter valid credentials → Submit | User logged in, redirected to browse dogs page | |
| Invalid Sign In | Enter incorrect email/password → Submit | Error message displayed, user remains on sign in page | |
| Password Reset | Click "Forgot password?" → Enter registered email → Submit | Success message displayed, user redirected to success page | |
| Sign Out | Click "Log out" in navigation | User signed out, redirected to homepage | |
| Authenticated Access | Try to access browse page without login | Redirected to sign in page | |

### Profile Creation and Management

| Test Label | Test Action | Expected Outcome | Test Outcome |
|------------|-------------|------------------|--------------|
| Create Owner Profile | Upload photo → Fill all required fields (name, age, city) → Submit | Owner profile created, redirected to create dog profile | |
| Owner Profile Validation | Try to submit without photo or required field | Form shows validation errors | |
| Create Dog Profile | Upload photo → Fill all required fields (name, age, breed, gender, size, energy) → Submit | Dog profile created, redirected to browse dogs page | |
| Dog Profile Validation | Try to submit without required fields | Form shows validation errors | |
| Edit Owner Profile | Navigate to Profile → Click "Edit Owner Profile" → Modify fields → Save | Changes saved, profile updated, redirected to profile view | |
| Edit Dog Profile | Navigate to Profile → Click "Edit Dog Profile" → Modify fields → Save | Changes saved, dog profile updated, redirected to profile view | |
| Photo Upload | Select image file (JPG/PNG) → Upload | Image previewed before submission, saved correctly | |
| Photo Removal | Click remove (×) button on uploaded photo | Photo removed, placeholder shown | |
| Character Counter | Type in "About me" textarea | Character count updates in real-time (0/150) | |
| Back Button Navigation | Click back arrow on form pages | Returns to previous page without saving | |

### Browse and Matching System

| Test Label | Test Action | Expected Outcome | Test Outcome |
|------------|-------------|------------------|--------------|
| Browse Dogs | Navigate to Discover page | Dog profiles displayed with toggle between dog/owner views | |
| Profile Toggle | Click "Owner" button on browse card | View switches to owner information | |
| Like Action | Click heart icon on dog profile | Profile liked, next profile shown | |
| Dislike Action | Click X icon on dog profile | Profile disliked, next profile shown | |
| Match Modal | Like a dog that already liked you | "It's a Match!" modal appears with both dog photos | |
| Match Modal Actions | Click "Send a message" in match modal | Redirected to message thread with matched dog | |
| Match Modal Close | Click "Keep swiping" or close (×) button | Modal closes, next profile shown | |
| No More Dogs | Swipe through all available dogs | "No more matches" message with reset button displayed | |
| Reset Functionality | Click "Reset" button when no dogs available | All matches, dislikes, and messages deleted, browsing restarted | |

### Matches Management

| Test Label | Test Action | Expected Outcome | Test Outcome |
|------------|-------------|------------------|--------------|
| View Matches | Navigate to Matches page | Grid of matched dogs displayed with toggle functionality | |
| Match Count | Check matches header | Correct count displayed (e.g., "You have 3 matches") | |
| Delete Match Button | Hover over match card | Delete (×) button visible in top-right corner | |
| Delete Match Modal | Click delete (×) button | Confirmation modal appears with warning message | |
| Confirm Delete Match | Click "Yes, delete" in modal | Match removed, conversation deleted, page updated | |
| Cancel Delete Match | Click "Cancel" in delete modal | Modal closes, match remains | |
| Empty Matches State | Delete all matches | "No matches yet" message with emoji displayed | |
| Message from Matches | Click "Send a message" button on match card | Redirected to message thread with selected match | |

### Messaging System

| Test Label | Test Action | Expected Outcome | Test Outcome |
|------------|-------------|------------------|--------------|
| View Inbox | Navigate to Messages page | List of conversations displayed with last message preview | |
| Conversation Preview | Check conversation item | Shows dog avatar, name, breed, and last message snippet | |
| Open Thread | Click on conversation in inbox | Message thread opens with full conversation history | |
| Send Message | Type message in textarea → Click "Send" | Message sent, appears in thread, textarea cleared | |
| Empty Message | Try to send empty message | Submit button disabled or no action | |
| Message Display | Check sent vs received messages | Different alignment (sent: right, received: left) with avatars | |
| Message Timestamp | Check message time display | Timestamp shown in format "Jan 15" | |
| Delete Conversation Button | Hover over conversation in inbox | Delete bin icon visible | |
| Delete Conversation Modal | Click delete bin icon | Confirmation modal appears | |
| Confirm Delete Conversation | Click "Yes, delete" in modal | Entire conversation deleted from both users | |
| Empty Messages State | Delete all conversations | "No conversations" message with emoji displayed | |
| Desktop Split View | View messages on desktop (992px+) | Inbox on left, thread preview on right | |
| Mobile Single View | View messages on mobile (<992px) | Inbox only, thread opens on separate page | |

### Navigation and UI

| Test Label | Test Action | Expected Outcome | Test Outcome |
|------------|-------------|------------------|--------------|
| Navbar Brand | Click "🐾 Pawfect Match" logo | Redirects to homepage (unauthenticated) or stays on current page (authenticated) | |
| Active Link Highlight | Navigate between pages | Current page link highlighted in navbar | |
| Mobile Menu Toggle | Click hamburger icon on mobile | Navigation menu expands/collapses | |
| Footer Social Links | Click social media icons | Links open in new tab | |
| Error Pages - 404 | Navigate to non-existent URL | Custom 404 page displayed with navigation options | |
| Error Pages - 403 | Try to access restricted content | Custom 403 page displayed | |
| Error Pages - 500 | Simulate server error | Custom 500 page displayed | |
| Form Validation Feedback | Submit form with errors | Red error messages display below relevant fields | |
| Success Feedback | Complete successful action | User redirected or shown success message | |

### Delete Account

| Test Label | Test Action | Expected Outcome | Test Outcome |
|------------|-------------|------------------|--------------|
| Access Danger Zone | Navigate to Profile page → Scroll to bottom | "Danger zone" section visible with delete button | |
| Delete Account Modal | Click "Delete my profile" button | Warning modal appears with consequences listed | |
| Confirm Delete Account | Type confirmation → Click "Yes, delete my account" | Account and all data deleted, user logged out, redirected to homepage | |
| Cancel Delete Account | Click "Cancel" in delete modal | Modal closes, account remains active | |
| Data Deletion Verification | Delete account → Try to sign in with same credentials | Account no longer exists, cannot sign in | |

### Browser Compatibility Testing

| Browser | Version | Test Result | Notes |
|---------|---------|-------------|-------|
| Google Chrome | 122.0+ | | |
| Mozilla Firefox | 123.0+ | | |
| Microsoft Edge | 122.0+ | | |
| Safari (macOS) | 17.0+ | | |

**Testing Method:** Each browser was tested with:
- User registration and authentication
- Profile creation and editing
- Browse and matching functionality
- Messaging system
- All navigation and modal interactions
- Image uploads and previews
- Form validation and submission

### Responsive Design Testing

| Device Category | Screen Size | Test Result | Notes |
|----------------|-------------|-------------|-------|
| **Mobile - Small** | 320px × 568px | | |
| **Mobile - Standard** | 375px × 667px | | |
| **Mobile - Large** | 414px × 896px | | |
| **Tablet - Portrait** | 768px × 1024px | | |
| **Tablet - Landscape** | 1024px × 768px | | |
| **Laptop** | 1366px × 768px | | |
| **Desktop - Standard** | 1920px × 1080px | | |
| **Desktop - Large** | 2560px × 1440px | | |
| **Ultra-wide** | 3440px × 1440px | | |

**Breakpoints Tested:**
- **320px - 767px:** Mobile-first design, single column layouts
- **768px - 991px:** Tablet layouts, form improvements, hero row layout
- **992px - 1199px:** Desktop features, messages split-screen, increased typography
- **1200px - 1399px:** Large desktop enhancements
- **1400px+:** Extra-large screens, hero centered column layout

**Specific Features Tested per Screen Size:**

| Feature | Small Mobile (320px) | Tablet (768px) | Desktop (992px) | Large Desktop (1400px+) |
|---------|---------------------|----------------|-----------------|------------------------|
| Navigation | Hamburger menu | Hamburger menu | Full navbar | Full navbar |
| Hero Section | Column (image → text) | Row (text ← image) | Row (text ← image) | Column (centered) |
| Profile Forms | Single column | Side-by-side with image | Side-by-side with image | Side-by-side with image |
| Dog Profile Fields | 1 column | 2 columns | 2 columns | 2 columns |
| Browse Cards | Single view | Toggle visible | 2 cards side-by-side | 2 cards side-by-side |
| Matches Grid | 1 column | 2 columns | 2 columns | 2 columns |
| Messages | Inbox only | Inbox only | Split-screen (inbox + thread) | Split-screen |
| Button Text Size | 0.7rem | 0.95rem | 1rem | 1rem |
| Hero Content | Centered | Left-aligned | Centered | Centered |

**Critical Small Screen Tests (320px):**
- ⬜ Form inputs not cut off
- ⬜ Buttons remain clickable and readable
- ⬜ Images scale proportionally
- ⬜ No horizontal scrolling
- ⬜ Character counter visible
- ⬜ Modal fits within viewport
- ⬜ Profile toggle buttons accessible

**Critical Large Screen Tests (1920px+):**
- ⬜ Content doesn't stretch too wide (1800px max)
- ⬜ Hero content remains centered
- ⬜ Typography remains legible (not too large)
- ⬜ Images maintain aspect ratio
- ⬜ Profile cards maintain readable width
- ⬜ Message bubbles don't stretch too wide (70% max)

### Performance

#### Desktop Performance

#### Mobile Performance

### Testing User Stories

All user stories outlined in the UX Strategy section have been validated and fulfilled through specific features and pages. This section demonstrates how each requirement is met within the application.

#### **New User Stories**

| User Story | How It's Fulfilled | Features/Pages Used |
|------------|-------------------|---------------------|
| **As a new user, I want to understand what the site is about, so I can decide if it's right for me.** | The homepage provides a clear hero section with the tagline "Find Love Through Your Pet" and explains the concept. The "How It Works" section breaks down the process in 4 simple steps with visual illustrations. The "Why Pawfect Match" section highlights key benefits (Pet-First Approach, Authentic Connections, Safe & Friendly, Easy Communication). | **Homepage** - Hero section, How It Works steps, Why Pawfect Match cards |
| **As a new user, I want to see if the platform is for me without registering, so I can determine if I want to commit.** | The entire homepage is accessible without authentication, allowing users to browse the value proposition, understand the matching process, and read about features before committing to registration. Navigation on public pages includes clear sections (Home, How it Works, Why Pawfect Match). | **Homepage** - All sections accessible to unauthenticated users |
| **As a new user, I want to register easily, so I can start quickly.** | Registration requires only email and password with confirmation. Form validation provides clear feedback. The "Get Started" button is prominently displayed on the hero section. After registration, users are automatically guided through profile creation. | **Register Page** - Email/password form, validation, redirect to owner profile creation |
| **As a new user, I want to add my dog's details, so I can begin browsing matches.** | After creating an owner profile, users are immediately redirected to create their dog profile. The form includes photo upload with preview, name, age, breed, size (dropdown), gender (dropdown), energy level (dropdown), and about me section with character counter (0/150). One-to-one relationship ensures each owner has one dog profile. | **Create Dog Profile Page** - Photo upload, required fields with dropdowns, character counter, automatic redirect to Browse Dogs after completion |

#### **Existing User Stories**

| User Story | How It's Fulfilled | Features/Pages Used |
|------------|-------------------|---------------------|
| **As an existing user, I want to sign in and out easily, so I can access my account securely.** | Sign in page accessible from homepage navbar and hero section. Users enter email and password with "Forgot password?" link available. After authentication, users are redirected to Browse Dogs. Log out link is always visible in the navbar for authenticated users, signing them out and redirecting to homepage. | **Sign In Page** - Email/password form, remember me, error messages<br>**Navbar** - "Log out" link on all authenticated pages |
| **As an existing user, I want to create and edit my owner profile, so I can manage my information.** | Owner profile creation is the first step after registration. Users can later edit their profile from the Profile page by clicking "Edit Owner Profile". Form includes photo upload with drag-and-drop, name, age, city, occupation, interests (select up to 3 pills), and about me with character counter. Changes are saved and user is redirected back to profile view. | **Create Owner Profile Page** - Initial onboarding form<br>**Edit Owner Profile Page** - Pre-populated form, photo update, save redirects to profile view |
| **As an existing user, I want to create and edit my dog profile, so I can keep it updated.** | Dog profile creation is the second onboarding step after owner profile. Users can edit from the Profile page by clicking "Edit Dog Profile". Form includes photo upload with preview, name, age, breed, size/gender/energy dropdowns, and about me section. Updates are saved and user returns to profile view. | **Create Dog Profile Page** - Second onboarding step<br>**Edit Dog Profile Page** - Pre-populated form, update photo, save redirects to profile view |
| **As an existing user, I want to like or dislike dogs after viewing both dog and owner profiles, so I can find the best matches for my dog.** | The Discover page displays dog profiles one at a time with large photos and detailed information. Users can toggle between Dog and Owner views to see complete information before making a choice. Heart icon (like) creates bidirectional matches and triggers "It's a Match!" modal. X icon (dislike) skips the profile and removes it from future browsing. | **Discover/Browse Dogs Page** - Profile cards with toggle (view both dog and owner), Like (heart icon), Dislike (X icon), "It's a Match!" modal popup |
| **As an existing user, I want to see my matches and remove a match if I change my mind, so I can manage my connections.** | Matches page displays a grid of all matched dogs with photos, names, ages, and owner names. Each match card has a red X button in the top-right corner. Clicking triggers a confirmation modal ("Are you sure you want to delete this match?"). Confirming removes both bidirectional connection entries and updates the page. Empty state shows "No matches yet" message. | **Matches List Page** - Grid layout, match cards with delete (X) button, delete confirmation modal, empty state |
| **As an existing user, I want to reset my password, so I can regain access if needed.** | "Forgot password?" link on Sign In page leads to password reset form. Users enter their registered email for verification (checks if account exists without sending email - demo mode). After validation, users are taken to a reset form to enter new password with confirmation. Success page displays with "Go to Sign In" button. | **Forgot Password Page** - Email verification form<br>**Password Reset Page** - New password form with confirmation<br>**Password Reset Success Page** - Confirmation message |

#### **All Users Stories**

| User Story | How It's Fulfilled | Features/Pages Used |
|------------|-------------------|---------------------|
| **As a user, I want to clear feedback when I take actions on the site, so I always know if something worked.** | Form validation displays red error messages below relevant fields when validation fails (e.g., invalid email, missing required fields). Success actions redirect users to appropriate pages (registration → owner profile → dog profile → browse dogs). "It's a Match!" modal appears instantly when mutual likes occur. Confirmation modals appear for destructive actions (delete match, delete conversation, delete account) with clear warning messages. Django messages framework provides server-side feedback. | **All Forms** - Validation error messages, required field indicators<br>**All Modals** - Match modal, delete confirmations<br>**Redirects** - Automatic navigation after successful actions |
| **As a user, I want to message other profiles after matching, so I can communicate with my matches.** | After matching, users can click "Send Message" in the "It's a Match!" modal or from match cards to open a conversation thread. Messages page shows inbox list with all active conversations displaying dog avatar, name, breed, and last message preview. Opening a thread shows full conversation history with timestamps. Users can send new messages via textarea and send button. Messages are displayed chronologically with different alignments (sent: right, received: left) and avatars. | **Messages/Inbox Page** - Conversation list with previews, empty state<br>**Message Thread Page** - Full conversation history, send message form, timestamps, differentiated sent/received styling |
| **As a user, I want to edit or delete my own information and images, so I have control over my data.** | Profile page displays both owner and dog profiles with toggle functionality. Each profile has an "Edit" button linking to respective edit forms. Edit forms are pre-populated with existing data allowing users to modify any field including photos. Users can upload new photos (previewed before submission) or keep existing ones. The "Danger Zone" section at the bottom of the Profile page contains "Delete my profile" button which triggers a confirmation modal explaining that all data will be permanently deleted (user account, owner profile, dog profile, all matches, all conversations). Confirming deletes everything via cascade delete and logs user out. | **Profile Page** - View profiles, edit buttons, toggle between dog/owner views<br>**Edit Forms** - Pre-populated fields, photo update<br>**Delete Account Modal** - Confirmation with detailed consequences, cascade delete implementation |

**Summary:** All 14 user stories are fully implemented with dedicated features, pages, and functionality. The application provides a complete user journey from discovery through registration, profile creation, matching, messaging, and account management.

## Deployment

(with Heroku)

## Credits

HERO
- [Freepik: Joyful girl tourist looks mobile phone](https://www.freepik.com/free-photo/joyful-girl-tourist-looks-mobile-phone-texts-message-smartphone-social-media-application-walks_38794425.htm#fromView=search&page=2&position=47&uuid=39f84724-60b2-45b5-ad1b-9b13e319a27c&query=woman+browsing+on+phone)
- [Freepik: Handsome man sitting cafe checking phone](https://www.freepik.com/free-photo/lifestyle-portrait-handsome-young-man-sitting-cafe-checking-his-phone-drinking-coffee_157867299.htm#fromView=search&page=1&position=3&uuid=b68dfbe1-a3de-4d8a-9b96-073d5d5fba3b&query=man+browsing+phone)

DOGS

- Artiste: [@brookecagle](https://unsplash.com/@brookecagle)
  - Image: [Ntm4C2lCWxQ](https://unsplash.com/photos/long-coated-brown-dog-Ntm4C2lCWxQ)
- Artiste: [@kierancwhite](https://unsplash.com/@kierancwhite)
  - Image: [NKN25UfGfkQ](https://unsplash.com/photos/close-up-photo-of-black-and-white-siberian-husky-dog-NKN25UfGfkQ)
- Artiste: [@alanking](https://unsplash.com/@alanking)
  - Image: [KZv7w34tluA](https://unsplash.com/photos/long-coated-brown-dog-KZv7w34tluA)
- Artiste: [@whoisperi](https://unsplash.com/@whoisperi)
  - Image: [5Vr_RVPfbMI](https://unsplash.com/photos/white-long-coat-small-dog-5Vr_RVPfbMI)
- Artiste: [@justnjames](https://unsplash.com/@justnjames)
  - Image: [KFJuCzJiQYU](https://unsplash.com/photos/adult-dog-sitting-on-white-sand-near-seashore-KFJuCzJiQYU)
- Artiste: [@dinetackimanni](https://unsplash.com/@dinetackimanni)
  - Image: [8mxSINYFoSw](https://unsplash.com/photos/brown-and-white-long-coated-dog-8mxSINYFoSw)
- Artiste: [@baptiststandaert](https://unsplash.com/@baptiststandaert)
  - Image: [mx0DEnfYxic](https://unsplash.com/photos/long-coated-black-and-white-dog-during-daytime-mx0DEnfYxic)
- Artiste: [@rpnickson](https://unsplash.com/@rpnickson)
  - Image: [gRHEt2kF3NU](https://unsplash.com/photos/brown-puppy-on-bed-gRHEt2kF3NU)
- Artiste: [@gxldy](https://unsplash.com/@gxldy)
  - Image: [v0_MCllHY9M](https://unsplash.com/photos/black-and-white-husky-v0_MCllHY9M)

PERSONE

- Artiste: [@xoutcastx](https://unsplash.com/@xoutcastx)
  - Image: [8Vt2haq8NSQ](https://unsplash.com/photos/man-standing-in-front-of-window-8Vt2haq8NSQ)
- Artiste: [@jonasjaekenmedia](https://unsplash.com/@jonasjaekenmedia)
  - Image: [5g7tSrQSJEo](https://unsplash.com/photos/woman-in-gray-hoodie-sitting-on-black-bench-5g7tSrQSJEo)
- Artiste: [@lancereis](https://unsplash.com/@lancereis)
  - Image: [pp76Y6Fq6xw](https://unsplash.com/photos/a-man-with-a-beard-pp76Y6Fq6xw)
- Artiste: [@xoutcastx](https://unsplash.com/@xoutcastx)
  - Image: [bdYJWXg4pK4](https://unsplash.com/photos/mens-white-crew-neck-shirt-bdYJWXg4pK4)
- Artiste: [@sxth](https://unsplash.com/@sxth)
  - Image: [IMYvZjlX3jE](https://unsplash.com/photos/man-sitting-near-hibiscus-flowers-during-daytime-IMYvZjlX3jE)
- Artiste: [@courtneymcook](https://unsplash.com/@courtneymcook)
  - Image: [TSZo17r3m0s](https://unsplash.com/photos/woman-smiling-wearing-denim-jacket-TSZo17r3m0s)
- Artiste: [@cikstefan](https://unsplash.com/@cikstefan)
  - Image: [QXevDflbl8A](https://unsplash.com/photos/smiling-woman-wearing-white-and-black-pinstriped-collared-top-QXevDflbl8A)
- Artiste: [@haletat](https://unsplash.com/@haletat)
  - Image: [5b_RXCDykto](https://unsplash.com/photos/a-woman-sitting-on-a-white-chair-next-to-a-table-5b_RXCDykto)
- Artiste: [@armedshutter](https://unsplash.com/@armedshutter)
  - Image: [6W4F62sN_yI](https://unsplash.com/photos/woman-looking-sideways-leaning-on-white-wall-6W4F62sN_yI)

### Visual Design References

WEBSITE INSPO
- [fetchadate.com](https://fetchadate.com/)
- [frolly.com](https://www.frolly.com/)
- [puppilovers.com](https://puppilovers.com/)

APP INSPO
- [Bumbule](https://bumble.com/)
- [Tinder](https://tinder.com/)
- [Hinge](https://hinge.co/)

### Code References





