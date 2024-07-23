# Donofy
![Custom Logo Image](static/media/donofy-full-logo.svg)

### This site is designed as a Charities donation site. 

![A mock-up image of the Donofy project](documents/readme-images/donofy-responsive.png)

## [Click here to deploy this project live](https://donofy-de544b6e546f.herokuapp.com/)

**PLEASE NOTE: This documentation contains many images which can be viewed via a dropdown toggle.**

## Table of Contents
* [**Planning and Development**](#planning-and-development)
    * [***Target Users***](#target-users)
    * [***User Stories***](#user-stories)
    * [***Site Objectives***](#site-objectives)
    * [***Approach***](#approach)
    * [***Research***](#research)
    * [***Data Schema***](#data-schema)
    * [***Wireframes***](#wireframes)
    * [***Colour Scheme***](#colour-scheme)
    * [***Typography***](#typography)
* [**Features**](#features)
* [**Future Features**](#future-features)
* [**Testing**](#testing)
  * [Go to TESTING.md](TESTING.md)
* [**Deployment**](#deployment)
  * [Click here to deploy this project live](https://donofy-de544b6e546f.herokuapp.com/)
* [**Admin Access**](#admin-access)
* [**Languages**](#languages)
* [**Frameworks and Tools**](#frameworks-and-tools)
* [**Software**](#software)
* [**Imported Code**](#imported-code)
* [**Credits**](#credits)
* [**Thanks**](#thanks)

[**Back to top**](#donofy)

## Planning and Development
### Target Users
- Users of all age groups, but primary audience are working age.
- Users who want fast and easily accessible information on a range of charities.
- Users who want to give to multiple charities but consolidate their charity contributions into one payment.
- Users who want full control over a charity amount they can afford. 

### User Stories
1. **As a new/guest user, I want to:**
  - A: quickly understand the purpose of the site.
  - B: find the navigation intuituve, with information easy and quick to find. 
  - C: understand the value of registering for an account.
2. **As a registered user, I want to:**
  - A: log in and manage my account details so they're current.
  - B: quickly find charities that interest me, and add them to my own "Favourites" list.
  - C: feel positive feedback from even the smallest donation I make. 
  - D: understand my impact over a longer period of time / see my payment history. 
  - E: have full control over how my donation amount is split between multiple causes.
  - F: be able to adjust my donations as my preferences change.
  - G: see a summary of my donation breakdown before I set/adjust my subscription.
  - H: receive a thank you email, every time a donation payment from me is processed. 
  - I: easily contact the site admins for any reason, including account deletion. 

4. **As any user, I want to**
  - A: view and use the platform on any device.
  - B: have the site be accessible.
  - C: easily direct to a charity's main website for more information.

### Site Objectives
1. To provide a positive user experience.
2. To create an intuitive UI that provides good site flow.
3. To build a family-friendly product.
4. To deliver a site that is responsive on a large variety of screen sizes and mobile devices.
5. To create a fast, reliable site that can fetch a lot of information quickly and display it clearly.
6. To allow users to create their own profiles, with log in functionality that is secure.
7. To give users the functionality to update their own profile.
8. To allow users full CRUD functionality on their Favourited Charties list.
9. To provide a secure payment system, that's user friendly.

### Approach
- Mobile first design.
- The site functionality will be provided to the user logically and intuitively.
- The site will be created following the principles of user experience design.
- The content of the site will be inoffensive and accessible to all.
- Clean, professional design, with consistent colour-scheme, style and layouts throughout.

### Research
The following sites were examined as part of my project research:
...
...
...

Common themes found:
  - Responsive design.
  - ...
  - ...

My adjustments to suit my project aims:
  - Reduce info on the main library page to what's essential.
  - Give full page space to a single game when the user wants more info.
  - ...

[**Back to top**](#donofy)
### Data Schema


### Wireframes

Balsamiq was used to create initial layouts and wireframes.
Some features and pages have been edited or removed entirely to meet project deadlines.


Please toggle the following dropdowns to view the wireframe images.

This planning and development work is uploaded to Figma. The design page on Figma is a useful tool to layout all my early project documents in one space, and share online with others for additional input. It allowed my mentor to quickly view and understand my project themes and objectives. 

Using Figma's wireframes capabilities, I was able to play with initial layouts and plan intuitive flow around my site. This has given me a good understanding of how an MVP might be presented to me by a frontend designer.

### Colour Scheme
![Image of colour palette]()


### Typography
The highly legible and readable googlefont, League Spartan, has been selected. With Arial, Helvetica and a standard sans-serif as back up. There can be a lot of data displayed, especially on large screens, so the typography needs to be as clear and clean as possible. As a googlefont, League Spartan is less likely to have compatibility issues with different browsers.

[**Back to top**](#donofy)
## Features

This project includes many features, these include:

### Fully Responsive 
![Site mockup image showing different screen sizes]()
- This site adapts to all devices and screen sizes ranging between 320px to 2560px wide (Tested).
- Responsive break points tested on screen widths: 320px / 576px / 768px / 992px / 1200px / 1400px / 2560px. 

### Intuitive Navigation


### Clear typography
- League Spartan is a highly readable font, with Arial, Helvetica and standard sans-serif as backups. 

### Custom Logo
![Custom Logo Image](donofy/media/donofy-full-logo.svg)
- Custom designed Logo in keeping with project brand aesthetics: both in colour and typography.
- SVG format for optimum resolution quality at all screen sizes.
- With thanks to Shaun Russell for the logo design.

### Images

### Search filters functionality
- Users can filter the charities library to view only the causes that interest them. 
- Searches are instantaneous

### High performance / fast loading times. 


### User profile creation and editing
- Users are allowed to create and edit their own profile account. 

### Large Font and Buttons
- With the exception of some form/button help text, all main site text remains a minimum of 1rem (16pt) font size for readability and accessibility. 
- All buttons maintain a minimum size of 48px x 48px. These are the WCAG 2.1 recommended guidelines for touchscreen buttons.
- Large buttons also improves accessibility for people with physical disabilities who have dexterity needs.

### Theme appropriate colour scheme
- A dark pink has been selected as the main brand colour. A compassionate shade, without being too light and feminine. It has the urgency of red, without the alarm or aggression. The mid range shade of pink gives good contrast for reading text on both dark and light backgrounds. 
- Eye comfort. There is no black on white (or visa versa). This is with all user's comfort in mind, but also for those with high visual needs.  

### High Standards of Accessibility 
[According to accessguide.io](https://www.accessguide.io/)

![Lighthouse Scores Image](documents/readme-images/lighthouse-scores.png)
- .#.#.#. Rating for accessibility on Lighthouse scores.
- Definite status messages - 404 page included.
- Responsive design.
- High colour contrast.
- No colours convey information - colour blind users
- No flashing lights.
- No background audio or autoplay audio.
- Aria-labels on all interactive elements.
- Alt descriptions on all images.
- Semantic elements to assist screen reader users to navigate and access information.
- Consistent navigation.
- Minimum font size of 16px throughout the site and on all screen sizes.  

### Family Friendly
- This site is free from offensive language and imagery, and is suitable for users of all ages. As no content can be created by users, this standard is easily maintained. Users will have the ability to contact site admins via a contact form, should any content issues arise. 

### The Footer
The footer provides copyright information and name of the site creator. Plus clickable links to my github and linkedin pages. (Icons intentionally large for better accessibility - easier to press)

[**Back to top**](#donofy)
## Future Features

* **Automated subscription payment methods.** Users can set regular monthly payments to be taken on a set day every month. Users would be able to edit their subscription details (selected charities, and amounts etc) in between payments. Users could cancel or pause their subscriptions between payments.

* **Single payments for guest users** who do not want to create an account.

* **Authorised admin access for Charity representatives**, to give access to update their own charity page information.

* **Badges or 'achievement' awards/icons** users can earn and 'collect' on their profile. Adding to positive UX, giving a greater sense of making an impact, and gamifying the UX to encourage more donations. 'Achievements' examples such as: 1st donation made, 3 doantions, 10 donations etc, subcription created, 6 months of consecutive donations etc. Achievements would be focused on actions rather than amounts donated to keep in line with the site ethos: every donation counts, even the smallest. 


[**Back to top**](#donofy)
## Testing
- Please see full documentation for testing and bug reports [here](./TESTING.md)

## Deployment
[Click here to deploy this project live](https://donofy-de544b6e546f.herokuapp.com/)

## Admin Access

A general superuser has been created for this project to view backend features and access some project functions and permissions that need to be secure. A handy Admin nav link will appear in the "My Account" dropdown on the main navbar. This takes an authorised user directly to the site admin backend panels to view/edit/delete data. (To preserve data, users and charities can be toggled to Inactive, instead of deleted.).
Superusers can directly toggle a charity to inactive on the frontend, by navigating to that charity's details page. A deactivate button appears at the bottom of the details page. 

To log in as a superuser and access the admin features. Please log in with the following details:

  - username = superuser1
  - password = Auth0risedAdmin0nly123

### **Languages**
- HTML
- CSS
- Javascript
- Python

### **Frameworks and Tools**
- Git
- GitHub
- Bootstrap 4.6
- JQuery
- Django
- django-allauth
- Stripe
- Amazon Web Services (S3)
- Visual Studio Code
- Font Awesome
- GoogleFonts - League Spartan
- Figma
- Favicon.io
- Tinypng.com
- Lighthouse
- W3C Markup validation service
- W3C Jigsaw CSS validation service
- WAVE WebAIM web accessibility evaluation tool

### **Software**
- SQLite3
- Stripe
- Heroku - Deployment
- Visual Studio Code to create, load and push my code to Github.
- Git and Github as my version control system for the site.
- Figma to create design-boards, wireframes and prototypes.

[**Back to top**](#donofy)
## **Imported Code**
Template code blocks taken from [Bootstrap 4.6 Library](https://getbootstrap.com/docs/4.6/components/alerts/). Heavily modified to suit my project requirements.

<details><summary>Bootstrap 4.6 Navbar</summary>
<img src="documents/readme-images/bootstrap4-navbar.png">
</details>
<details><summary>Bootstrap 4.6 Nav-tabs</summary>
<img src="documents/readme-images/bootstrap4-nav-tabs.png">
</details>
<details><summary>Bootstrap 4.6 Image-card</summary>
<img src="documents/readme-images/bootstrap4-img-card.png">
</details>


## **Tutorials** ##

Very Academy - Tutorial Video [Django Custom User Model, Extend User Fields](https://www.google.com/search?q=django+4+extending+user+model+tutorial&sca_esv=bb6fb22019ea88f6&sca_upv=1&rlz=1C1GCEU_enGB1105GB1105&ei=VeuDZrvwHYSghbIPzIqKuAg&oq=django+4+extending+user+model+tuto&gs_lp=Egxnd3Mtd2l6LXNlcnAiImRqYW5nbyA0IGV4dGVuZGluZyB1c2VyIG1vZGVsIHR1dG8qAggAMgcQIRigARgKMgcQIRigARgKMgcQIRigARgKSLQUUJ4EWN8IcAF4AZABAJgBfKAB2gOqAQM0LjG4AQHIAQD4AQGYAgagAuUDwgIKEAAYsAMY1gQYR8ICBhAAGBYYHsICCxAAGIAEGIYDGIoFwgIIEAAYgAQYogTCAgUQIRigAcICBBAhGBWYAwCIBgGQBgiSBwM1LjGgB6wW&sclient=gws-wiz-serp#fpstate=ive&vld=cid:662df13b,vid:NLHmadrP8Y4,st:0)

Loading Overlay animation / css / js - taken from Code Institute's Boutique Ado walkthrough project. Colour modified to align with my project's colour scheme.
[View Boutique Ado Project here](https://github.com/Code-Institute-Solutions/boutique_ado_v1/tree/4f4a39d898c2c347e0d0a0201e4c0d2d6ef1c500)



## **Credits**
- Shaun Russell: site logo.
- Favicon.io for icon converter & instructions [View here](https://favicon.io/)
- Tinypng.com for image compression [View here](https://tinypng.com/)
- Accessguide.io an excellent accessibility guide [View here](https://www.accessguide.io/)

## Site Testers
- Shaun Russell - Senior UI/UX designer


## **Thanks**
- Richard Wells: Senior Developer, site tester, and my Code Institute Mentor. Thank you for going above and beyond with your support and patience! I massively appreciate the time and expertise you've given me.

- Tom Harris: Site tester, and my biggest cheerleader.

- Shaun Russell: Senior UX/UI/Product Designer. My site tester, my partner, and my provider while I study. Building my new development career change would have been infinitely harder without you. Thank you.

[**Back to top**](#donofy)