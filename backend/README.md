# SPRK Backend Coding Challenge

Dear [Candidate name],

Thank you for taking the time to complete our coding challenge. We value your time and efforts, so we've designed this challenge to resemble the actual day-to-day work at SPRK as much as possible.

## Background

SPRK needs to know what food is available at the location of a partner. That's why we've built an application that allows the people in warehouses (called "Pickers") to report products in a structured way. They can also create new products. Packaged products have a barcode. External information databases host relevant product data like weight or ingredients data. Most packaged products have the best before date printed on their packaging. Sales teams need this information since a product's value decreases as it approaches its best before date. Most fruit and vegetable products don't have the best before date. Here it's rather a qualitative description of the quality state.

## The Scenario

Let's assume that one of our pickers is scanning a multitude of products with our mobile app and submits the session to our Backend service. Your task is to create a backend API that interacts with a frontend application to allow the picker to scan, modify, and submit product data. The backend API should have the following endpoints:

1. Products are identified using the field `code` in combination with the field `type`.
2. The `code` field should not contain any leading zeros once it is stored in our database.
3. The `code` may be a mix of both, ones with leading zeros and without them.
4. There may be unicode characters which need to be parsed before storing in our database.
5. The field `trade_item_unit_descriptor` may also be present as `trade_item_descriptor` but should be transformed to the first before being stored in the DB.

## Your Task

Your task is to build an API in Python which can:

1. Receive the product feed, normalize it, and store it in a PostgreSQL database.
2. Return the stored product info individually (by code) or the entire range as an array if no argument is passed.

## Requirements

MUST:
- Be dockerized and runnable with a single command.
- Have endpoints to accept and return product data.

SHOULD:
- Be covered with tests.
- Be documented.

NICE TO HAVE:
- A small evidence of the applicant's frontend capabilities.

## Submission

Please submit your solution as a Git repository (you can use GitHub, GitLab, or Bitbucket) and share the repository link with us. Make sure the repository is public or accessible by the reviewers.

Good luck and have fun!

The SPRK Team

## Hints

1. Refer to the [docker docs](https://docs.docker.com/language/python/) for support with dockerizing a Python application.
