# Abulti Apparel

This is the code for the *massively* popular Abulti Apparel website

## TODO:

* After the actual store item model is in, I'll add a "quickshop" button to both the homepage and store pages, with a modal so that users can buy stuff quicker.

* Filling in content, like about page, mission statement, metadata descriptions, etc
* Privacy policy (can be created by me, more of a "here's the data we collect" than a legal document)
* Terms of service (should not be created by me, more of a "download a boilerplate from the internet and use that" kind of thing)
	* Get as close to plagarising another company's ToS as possible

* Later down the line, if this is even something we want to pursue, a blog page with announcements
	* Would have a blog post object in the blog models.py, would be pushed by admin
	* Shouldn't be difficult to implement

* A lot of help pages to go with
	* Inform customers about shipping, returns, contacting us, etc

* Add some kind of lightbox / image switcher for the item display view when multiple images are present

* Before deployment:
	* Change DEBUG.text to False
	* Change robots.txt to allow site indexing
	* Create a .xml sitemap for google to index the site in the first place

* Payment-processing needs:
	* Users can add - without signing in - items to a cart. DONE
		* Without signing in is probably done by sessions
		* Users can specify what sizes for relevant items they want DONE
	* Users can review their cart at any time, and delete any items from their cart. DONE
		* Users can see the total price, change quantities of the items they are buying, etc DONE

	* When a user wishes to "check out", they can review their cart, then enter their credit card information DONE
	* A payment is made (via Stripe), so that we get money and they lose money DONE
	* The purchase count of the items purchased is increased DONE
	* A model object is created, an order, that tells us what items they purchased and what sizes. It also tells us their address and email. DONE
		* The order object is saved to the database (we can see it on the admin site), and a copy is emailed to us. DONE
		* We email them automatically that their order has been processed, and a copy of the order. KIND OF DONE
		* We email them manually that we have shipped their items to them. OK

	* The user, still without signing in, can see what stage their order is in: processed, delivering, delivered DONE

	* The user can request a refund, with a reason, and we could maybe grant it COVERED IN THE EMAIL SENT TO THEM


## Questions to answer for moving forward (website related and bussiness related):

* Should our customers be able to sign into abulti?
	* I put a custom user object in already, we'd just have to update that to contain other information like shipping and credit card numbers.
	* Should we save credit card information for customers? That's possible. Do other sites do this? Is it a security thing?

* Under what circumstances would we offer somebody a return?

* How do we ensure that our packages arrive at their destinations?

* Do we have multiple shirt sizing available? Would weird sizes be available upon request? idk