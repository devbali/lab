## Reverse Engineering Lab

### Problem 1: Introduction
While there are many tools you can use to successfully do this lab, we would recommend using Python scripts, using the requests module, especially for Problem 3.

Make sure to check out the [requests module](https://docs.python-requests.org/en/latest/) in python!
To start the lab, go to the URL *TODO: insert URL here*
Here you see a generic web app's landing page. Go to the login page, and click forgot password to get a password for your SID.
Now log in with your SID, and inspect element to see the Network requests. What requests are being sent?
You should be directed to a page with Generic Data. Look at how this data is being fetched from the server. Pay attention to the headers, there is a particular header which is how the application knows who you are.
Try making this same request using the requests module on python.
Now think about how you can extract data for the 100th index from this API. Enter this on the Submission Form.

### Problem 2: Snackpass
- This is based on real events
Imagine this application now is Snackpass, and you checkout with coupon code "JULY420" for a July 4th sale that gets you 20% off your total.
Your total was $20.00, and upon inspecting requests you see a POST request that has this body:
```json
{
  "TODO":
}
```
To URL: TODO
Now try checking out with a $1 total. You will get a receipt id in the response if you do this successfully. Enter the receipt id in the Submission Form.

### Problem 3: BeReal
- This is based on real events
Imagine this application is now BeReal. This is a social media platform similar to Facebook or Instagram, but meant to be for more closer knit groups with more of a privacy focus.
When you go to a specific page on this application, you see these requests being made:

Empty body request to URL `/api/bereal/myid`
TODO

You know a particular person has a user id of `TODO`. Now reverse engineer and figure out how you can find the user id's of all of this user's friends. Enter this as a comma separated list on the Form Submission.
