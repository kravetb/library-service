# library-service

## Overview
Library Service is a Django project designed to manage various aspects of a library, book and borrowings.

## Contents
1. [Pages](#pages)
   	- [Book API](#book-api)
	- [Borrowing API](#borrowing-api)
    	- [User API](#user-api)
2. [Instructions for Local Setup](#instructions-for-local-setup)
3. [Environment Configuration](#environment-configuration)

## Pages

### Book API
- URL: `/api/book-service/`
- Description: Endpoint for managing book.

### Borrowing API
- URL: `/api/borrowing-service/`
- Description: Endpoint for managing borrowing - book, user.


### User API
- URL: `/api/user/`
- Description: Endpoint for user-related functionalities like registration and token management.

## Instructions for Local Setup
1. Clone the repository: `git clone https://github.com/kravetb/library-service/tree/make_test/library_service`
2. Install necessary dependencies: `pip install -r requirements.txt`
3. Start the server: `python manage.py runserver`

## Environment Configuration
- Create a `.env` file based on `env.sample` and enter your secret keys and other settings.
