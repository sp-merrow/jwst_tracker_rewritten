A rewrite of my JWST tracker application. Runs much faster because:

	It uses a local .json to calculate distance & speed on the fly

	Instead of scraping with Selenium, it makes a lightweight API call

Furthermore, this script requires the NumPy module to function. To install it, run the following command:

	pip install numpy
