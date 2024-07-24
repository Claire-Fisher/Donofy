# Testing Donofy
This project was tested continuously during development. Post build, the site has been manually tested by myself and third party testers. It has also passed on html, CSS, JS, and accessibility validators. The python has pass linting checks and is compliant with PEP8 industry standards.

[return to README.md](./README.md)

**PLEASE NOTE: This documentation contains many images which can be viewed via a dropdown toggle.**
## Table of Contents
* [**During Development Testing**](#during-development-testing)
    * [*Testing*](#testing)
    * [*Bugs and Fixes*](#bugs-and-fixes)
* [**Post Development Testing**](#post-development-testing)
  * [**Manual Testing**](#manual-testing)
    * [Home Page Manual Testing](#home-page-manual-testing)
    * [Charities Page Manual Testing](#charities-page-manual-testing)
  * [**User Story Testing**](#user-story-testing)
  * [**Validators**](#validators)
    * [Donofy Base App](#donofy-base-app)
    * [Index Page](#index-page)
* [**Future Bug Fixes**](#future-bug-fixes)


## **During Development Testing**
This project has been developed partially with a TTD approach. 
During the development process, I also manually tested continuously in the following ways:-

1. Manually tested each element for appearance and responsiveness via a simulated live server by running app.py in PORT 8000.

2. Checked functionality as I built. Dealing with bugs and error messages during development. (See bugs and fixes)

3. Sought feedback from my mentor and student peers at key intervals during development. 

## Testing:

### Browser Compatibility
During testing, I used three different browsers to ensure cross-compatibility. The desktop browsers used by myself were:

  1. Chrome
  2. Firefox  
  3. Edge

I have manually tested on Chrome.
Shaun Russell - Site tester - Tested on Firefox, and Edge.
Tom Harris - Site tester - Tested the project on Safari.

### Screen Sizes

The site has been tested at screen sizes 320px to 2560px in width.

INSERT IMAGE MOBILE
INSERT IMAGE DESKTOP

### Function Testing
The functions are built using a TDD approach, and also thoroughly manually tested via their output displayed in the terminal with print statements, the browser display, or both. (All print statements have been removed in the final version of the project).

[**Back to top**](#testing-donofy)
## ***Bugs and Fixes:***

Below is a list of bugs I discovered and fixed using TDD and manual testing :-

1. **Testing charities view - IntegrityError1** - 
    * ***Issue Found:*** 
        * IntegrityError thrown when testing charities.views.all_charities view
        <details><summary>Integrity Error</summary>
        <img src="documents/testing-images/charities-test-integrityError1.png">
        </details>
        <details><summary>Test code</summary>
        <img src="documents/testing-images/charities-test-integrityError-code1.png">
        </details>
    * ***Solution Used:*** 
        * Added all remaining fields that will not accept null according to the Charity Model, to the test setup.
        <details><summary>Integrity Error code fix</summary>
        <img src="documents/testing-images/charities-test-integrityError-code1-fix.png">
        </details>
        <details><summary>Test pass</summary>
        <img src="documents/testing-images/charities-test-integrityError1-fixed.png">
        </details>
2. **Testing charities category sort**
    * ***Issue Found:***
        <details><summary>Initial test failing</summary>
        <img src="documents/testing-images/charities-test-cate-sort-fail.png">
        </details>
        <details><summary>Value Error</summary>
        <img src="documents/testing-images/charities-test-cate-sort-valueError.png">
        </details>
        <details><summary>Assertion Error</summary>
        <img src="documents/testing-images/charities-test-cate-sort-AssertionError.png">
        </details>
    * ***Solution Used:*** 
        * Value Error: required importing Charity model, and fixing some syntax.
        * Assertion Error: filters category by ID instead of name
        <details><summary>Test Pass</summary>
        <img src="documents/testing-images/charities-test-cate-sort-pass.png">
        </details>
3. **Testing charities ASC / DESC order sort**
    * ***Issue Found:***
        <details><summary>Initial test failing</summary>
        <img src="documents/testing-images/charities-test-asc-desc-sort-fail.png">
        </details>
        <details><summary>Name Error: Lower is not defined</summary>
        <img src="documents/testing-images/charities-test-asc-desc-sort-NameError-lower.png">
        </details>
        <details><summary>Assertion Error</summary>
        <img src="documents/testing-images/charities-test-asc-desc-sort-AssertionError.png">
        </details>
        <details><summary>Assertion Error ASC only</summary>
        <img src="documents/testing-images/charities-test-asc-sort-2.png">
        </details>
    * ***Solution Used:*** 
        * Name Error: added from django.db.models.functions import Lower
        * Assertion Error: had to abandon ascend/descend feature. Category sorts will automatically sort by ascending instead.
        * Assertion Error ASC only: removed the charity with active=False as that was creating the mis-ording and causing the test to fail
        <details><summary>Test Pass</summary>
        <img src="documents/testing-images/charities-test-asc-sort-pass.png">
        </details>
4. **UserProfileAdmin errors**
    * ***Issue Found:***
        * The following errors were thrown for UserProfileAdmin during a makemigration --dry-run
        * 1 x admin.E033 error
        * 4 x admin.E108 errors
        <details><summary>UserProfileAdmin Migration Errors</summary>
        <img src="documents/testing-images/model-UserProfileAdmin-errors.png">
        </details>
    * ***Solution Used:***
        * E108: changed ordering by non-existent 'date', to last_name instead
        * E108: removed the referred to fields as they will now be stored in new donations data.
        <details><summary>UserProfileAdmin Migration Fixed</summary>
        <img src="documents/testing-images/model-UserProfileAdmin-fixed.png">
        </details>
5. **Testing profiles**
    * ***Issue Found:***
        <details><summary>First Test fail</summary>
        <img src="documents/testing-images/testing-profiles-first-test-fail.png">
        </details>
    * ***Solution Used:***
      * Imported User from models & added a 'testuser' to provide log in details for the test.
        <details><summary>First Test pass</summary>
        <img src="documents/testing-images/testing-profiles-first-test-pass.png">
        </details>
6. **Update_subscription functionality**
    * ***Issue Found:***
        <details><summary>Attribute Error on save</summary>
        <img src="documents/testing-images/update_subscription-attr-error.png">
        </details>
    * ***Solution Used:***
      * Imported the Charity model and fetched the full charity details from the list of charity IDs.
      * Changed the dict to show keys of charity_names (instead of ID ints), and int donation values. To make it easier for admin to understand the sub_breakdown by reading the dict. 
        <details><summary>sub_breakdown dict saving as expected</summary>
        <img src="documents/testing-images/update_subscription-attr-fixed.png">
        </details>
7. **Update_subscription Invalid Literal for Int error**
    * ***Issue Found:***
        * If value for charity donation left blank on save, Value error thrown.
        <details><summary>Value Error on save</summary>
        <img src="documents/testing-images/update_subscription-value-error-invalid-literal-for-int.png">
        </details>
    * ***Solution Used:***
      * Added a default_if_none:0 condition to the input value logic. So 0 will always be displayed instead of blank.
        <details><summary>Zero default fix</summary>
        <img src="documents/testing-images/update_subscription-value-error-invalid-literal-for-int-fixed.png">
        </details>

[**Back to top**](#testing-donofy)  
## **Post Development Testing**

Post development, I manually tested in the following ways:-

1. Manually tested each element for appearance and responsiveness via a simulated live server.

2. The code passed through HTML, CSS, JavaScript(ES6), pep8 validators to check for errors. As well as an Accessibility evaluation.

3. Published the page via GitHub pages and shared with fellow students and friends to test and receive feedback.

## **Manual Testing**

My manual testing logs are as follows:
### Home Page Manual Testing
***
**Home Page: Main Nav bar**
* Expected:
  * All nav links to redirect to their correct page template. (Including links only present when a user/superuser is logged in).
  * All nav elements, including site logo (home link), to respond with colour change, and/or hover animation on mouse hover to indicate they are interactive.
  * Nav links turn to a burger menu on screens <768px wide.
  * Dropdown nav menus, and sub menus to stay ontop of content on all screens sizes.
  * Drop down menu toggles dropdown list of nav elements and changes dynamically based on user logged in:
    - **Guest User** = Only Register and Login present in dropdown.
    - **User logged in** = 
      - Register / Login not present.
      - My Donofy / My Details / My History / Donate / Logout, present.
    - **SuperUser logged in** = 
      - Register / Login, not present.
      - Admin / My Donofy / My Details / My History / Donate / Logout, present.
* Testing:
  * Clicked each nav link in turn to check for broken links or incorrect pages rendered.
  * Hovered my mouse over each element to check for interactive indicators.
  * Used Chrome Dev tools to check screen widths 767px and 768px wide.
  * Toggled dropdown menus on screen sizes 320px / 576px / 992px wide.
  * Inspected nav bar as a Guest User / User / Superuser
* Result:
  * All nav links routing behaved as expected.
  * All nav links changed colour and hovered on mouse hover. Donofy navbar did nothing.
  * Nav links switched to burger menu at 767px screen width.
  * Dropdowns stayed ontop of content.
  * Correct nav links show in dropdown menu according to user type.
* Action: 
  * Added custom hover class to Donofy main logo.
***
**Home Page: "How Does Donofy Work?" Nav Card Links**
* Expected:
  * The cards to respond with colour change on mouse hover, to indicate they are interactive elements.
  * The cards to go to redirect to their correct page templates, according to user:
    - Guest User:
      - **Find Your Charities** goes to Charities page.
      - **Set a Donation amount** goes to sign in page.
      - **Make an Impact** goes to sign in page.
    - Registered User:
      - **Find Your Charities** goes to Charities page.
      - **Set a Donation amount** goes to Mange My Donofy tab on profile page.
      - **Make an Impact** goes to My Payment History tab on profile page.
* Testing:
  * Hovered over each nav card
  * Clicked each card in turn to check for broken links or incorrect pages rendered.
* Result:
  * Colour changed as expected.
  * All Guest user cards redirected as expected. First two User cards behaved as expected. "Make an Impact" card incorrectly directed to Manage My Donofy tab.
* Action: 
  * Added a shadow to make it more obvious they're interactive before the user hovers over them.
  * Corrected href on "Make an Impact" card to redirect to My Payment History tab.
***
**Home Page: Footer**
* Expected:
  * All link elements Contact Us / Github / Linkedin, to indicate they are interactive.
  * Footer link elements to redirect to their correct targets
    - Contact us redirects to Contact Us page
    - Github icon opens a new tab to my Donofy repo on Github
    - Linkedin icon opens a new tab to my Linkedin page.
* Testing:
  * Hovered my mouse over each element.
  * Clicked each element.
* Result:
  * Contact Us behaved as expected. Github & Linkedin Icons did nothing.
  * All links redirected as expected. 
* Action: 
  * Corrected colour change and hover classes for Icon links
***
**Home Page: Additional Sign up buttons**
* Expected:
  * Guest users see additional Sign Up call-to-action buttons at the top and bottom of the home page.
* Testing:
  * Logged out and inspected the page.
* Result:
  * Sign up buttons appeared as expected.
* Action: 
  * Added additional sign up info the bottom sign up button so it matches the top version.
***
**Home Page: Responsiveness**
* Expected:
  * All page content to shrink, grow and rearrange according to screen width.
  * Hero text ontop of hero image to disappear on screen width <992px and reappear below instead.
  * Hero image to switch to a different version with a shorter aspect ratio. 
* Testing:
  * Used Chrome Dev Tools to inspect the home page at screen widths 320px / 576px / 768px / 992px / 1200px / 2560px.
* Result:
  * All content behaved as expected.
* Action: 
  * None
***
### Charities Page Manual Testing
***
**Charities Page: Available for all users including guests**
* Expected:
  * Charities page to be available to all users.
* Testing:
  * Navigated to Charities page as a guest / user / superuser
* Result:
  * Page behaved as expected
* Action: 
  * None
***
**Charities Page: Search Bar**
* Expected:
  * Charities to filter by keyword in the search bar.
  * Number of charities shown to indicate how many charities have been found.
* Testing:
  * Searched for "dog".
  * Searched for "donkey".
  * Searched for "child".
* Result:
  * Searches behaved as expected. Relevant charities displayed, and all others hidden. Charities found number updated correctly.
* Action: 
  * None
***
**Charities Page: Categories dropdown**
* Expected:
  * Charities to filter according to their category group.
* Testing:
  * Searched by each of the categories via the dropdown.
* Result:
  * Category filtering behaved as expected. Relevant charities displayed, and all others hidden. Charities found number updated correctly.
* Action: 
  * None
***
**Charities Page: Charity cards**
* Expected:
  * All charity cards to respond with colour change, and/or hover animation on mouse hover to indicate they are interactive.
  * Clicking the info button, or the image of the card, will direct the user to the correct charity detail page.
* Testing:
  * Hovered my mouse over each element to check for interactive indicators.
  * Clicked multiple cards in turn. Clicked multiple card Info buttons in turn.
* Result:
  * Interactive indicators present and behaving as expected.
  * Cards behaved as expected and directed to the correct charity detail page.
* Action: 
  * None
***
**Charities Page: Charity cards - Favourite Button**
* Expected:
  * Favourite button to redirect GUEST USERS to sign in page.
  * Favourite button as a LOGGED IN USER:
    - On click of Favourite, button should change to pink "Unfavourite" button.
    - On click of Favourite, message should display telling the user that charity was Successfully added to their list.
    - On click of pink Unfavourite, button should change back to white "Favourite" button.
    - On click of pint Unfavourite, message should display telling the user that charity was Successfully removed from their list.
  * Favourite's list on profiles/my Donofy should mirror the favourited charities on the charity page. 
  * Charities removed from favourites in the profiles/My Donofy, should display the correct white "Favourite" button on the charities page.
* Testing:
  * Logged out. Clicked a favourite button on a charity card.
  * Whilst logged in:
    - Clicked various favourite buttons on different charity cards.
    - Clicked various Unfavourite buttons on different charity cards.
    - Checked the My Donofy page mirrored the corrected Favourited/Unfavourited charities on the charities page.
    - Checked removing a Favourite from the user's My Donofy page, was also mirrored in the charities page.
* Result:
  * Guest User Favourite button behaved as expected and directed to the Donofy Sigin In page.
  * Logged in user: all actions behaved as expected.
* Action: 
  * Changed the message type for Unfavouriting to blue info to make it clearer to the user.
***
**TEST NAME**
* Expected:
  * 
* Testing:
  * 
* Result:
  * 
* Action: 
  * 
***

[**Back to top**](#testing-donofy)

### User Stories Testing


[**Back to top**](#testing-donofy)
## **Validators**

I've thoroughly validated Donofy with the following validators:
  - **HTML** https://validator.w3.org/
  - **CSS** https://jigsaw.w3.org/css-validator/
  - **JS** https://jshint.com/
  - **CI Python Linter** https://pep8ci.herokuapp.com/
  - **Accessibility** https://wave.webaim.org/

Here are my reports on validation tests by page.

### Donofy Base App
<hr>
View current donofy app PEP8 Linter results here:
<details><summary>PEP8 linter for settings.py</summary>
<img src="documents/testing-images/donofy-settings-py.png">
</details>
<details><summary>PEP8 linter for donofy/urls.py</summary>
<img src="documents/testing-images/donofy-urls-py.png">
</details> 

### Index Page
<hr>
View Current Home Page validator results here:

- [HTML results](https://validator.w3.org/nu/?doc=https%3A%2F%2Fdonofy-de544b6e546f.herokuapp.com%2F)
- [CSS results](https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Fdonofy-de544b6e546f.herokuapp.com%2F&profile=css3svg&usermedium=all&warning=1&vextwarning=&lang=en)
- <details><summary>Current JS results</summary>
  <img src="documents/testing-images/home-current-js.png">
  </details> 
- <details><summary>PEP8 linter for home/views.py</summary>
  <img src="documents/testing-images/home-initial-py-views.png">
  </details> 
- <details><summary>PEP8 linter for home/urls.py</summary>
  <img src="documents/testing-images/home-initial-py-urls.png">
  </details> 
- [ACCESSIBILITY results](https://wave.webaim.org/report#/https://donofy-de544b6e546f.herokuapp.com/)
<hr>

### Index HTML Validator
<details><summary>HTML validator inital results</summary>
<img src="documents/testing-images/home-initial-html.png">
</details>

* ***Errors Found:***
    * 6 Attribute Errors.
    * 2 Type Attribute Warnings.
* ***Action Taken:***
    * Removed unecessary attributes.
    * Gave the hero images blank alt tags, as they're decorative and offer no additional info to the user.
<hr>

### Index CSS Validator
<details><summary>CSS validator inital results</summary>
<img src="documents/testing-images/home-initial-css.png">
</details>

* ***Errors Found:***
    * Value Error on .footer-box
* ***Action Taken:***
    * Removed display: absolute;
<hr>

### Index JavaScript Validator - [View initial results here]()

<details><summary>Initial JS results for Home</summary>
<img src="documents/testing-images/home-initial-js.png">
</details> 

JSHint validator was configured to recognise New JavaScript Features (ES6), and jQuery.
* ***Errors Found:***
    * Trailing comma
* ***Action Taken:***
    * Removed comma
<hr>

### Index Python CI Linter (PEP8 check)

* ***Errors Found:***
    * None.
* ***Action Taken:***
    * None.

### Index Accessibility Evaluation
<details><summary>Wave inital results</summary>
<img src="documents/testing-images/home-initial-wave.png">
</details>

* ***Errors Found:***
    * Missing alt tags
    * 3x contrast errors on hero text
* ***Action Taken:***
    * Add alt tags to hero images
    * Darkened background on all hero text to increase contrast.
<hr>

### Index Lighthouse Scores
### Test conditions
* All lighthouse tests were run from heroku and in incognito mode to avoid interference. 
* Both mobile and desktop performance are tested.
* The drop in performance is mainly due to Heroku, Stripe, and a large amount of layout behaviours to keep my site responsive. 
* All testers reported good load and response times on both desktop and mobile devices, so no adjustments will be made at this time. 

- Actions taken:
    - Hero images PNGs were replaced with webp files to try to increase performance. Small improvement recorded.
<details><summary>Desktop Results Inital</summary>
<img src="documents/testing-images/home-lighthouse-initial.png">
</details>
<details><summary>Desktop Results Current</summary>
<img src="documents/testing-images/home-lighthouse-current.png">
</details> 
<details><summary>Mobile Results Current</summary>
<img src="documents/testing-images/home-lighthouse-current-mobile.png">
</details> 
<br/>

### Charities Page
<hr>
View Current Charities Page validator results here:

- [HTML results](#)
- [CSS results](#)
- No JS for charities page
- <details><summary>PEP8 linter for charities/views.py</summary>
  <img src="#">
  </details> 
- <details><summary>PEP8 linter for charities/urls.py</summary>
  <img src="#">
  </details> 
- [ACCESSIBILITY results](#)
<hr>



## **Future Bug Fixes** 
Due to deadline constraints, some bugs remain in this version of Donofy. Whilst they are not project breaking, these are some bugs I'm aware are left unsolved. I would address these going forward before expanding to additional future features.

**Most site images nested inside the project Static folder**
  - During development MEDIA links to images inside the correct root Media folder would not display. To get around this I relocated them to static instead so the site displays as intended.

**USA Stripe Element**
 - The current stripe element input for card payments asks for a zipcode. Zip codes are not applicable for UK users. I would change the Stripe element to it's UK version. Better still, I would have it change dynamically based on a user's input in the Country field (if the site were to go global).



<hr>


## Thank you to my product testers
- Richard Wells
- Shaun Russell
- Tom Harris

[**Back to top**](#testing-donofy)

[return to README.md](./README.md)