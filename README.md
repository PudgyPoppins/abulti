# Abulti Apparel

This is the code for the *massively* popular Abulti Apparel website

## TODO:

* After the actual store item model is in, I'll add a "quickshop" button to both the homepage and store pages, with a modal so that users can buy stuff quicker.

* Add certain automatic tags (that don't use the tag model), where if an item's date is within a week of today, then add "Just arrived". If an item is the most popular for its clothing_type (most purchases), then add "best selling"

* Filling in content, like about page, mission statement, metadata descriptions, etc
* Privacy policy (can be created by me, more of a "here's the data we collect" than a legal document)
* Terms of service (should not be created by me, more of a "download a boilerplate from the internet and use that" kind of thing)
	* Get as close to plagarising another company's ToS as possible

* Later down the line, if this is even something we want to pursue, a blog page with announcements
	* Would have a blog post object in the blog models.py, would be pushed by admin
	* Shouldn't be difficult to implement

* A lot of help pages to go with
	* Inform customers about shipping, returns, contacting us, etc


## Questions to answer for moving forward (website related and bussiness related):

* Should our customers be able to sign into abulti?
	* I put a custom user object in already, we'd just have to update that to contain other information like shipping and credit card numbers.
	* Should we save credit card information for customers? That's possible. Do other sites do this? Is it a security thing?

* Under what circumstances would we offer somebody a return?

* What does it mean to be alive?

* How do we ensure that our packages arrive at their destinations?

* Do we have multiple shirt sizing available? Would weird sizes be available upon request? idk