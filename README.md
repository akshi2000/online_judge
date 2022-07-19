# Online Judge

## Goal:

To develope a web application that can process submitted code against specified testcases and give the verdict. Application should be robust and
protect it's files and database against malicious codes/scripts. Asynchronous processing os submissions to keep the server up for new requests. 
Develope a DBMS solution to save submitted scripts, results, question tags, and user analysis

## Tech Stack:

Django, DRF, Celery, Redis, ReactJs, Docker, Schroot, Linux

## Steps to Setup:

- Clone the repository
- Run command: ```docker-compose up -d --build ``` to build images and setup containers
- Run command: ```docker-compose up exec celery /bin/bash ``` to access terminal of celery worker container.
- Run command: ```./server-setup.sh ``` to setup the chroot environment, users and permissions which will provide environment for processing submissions.
- Access the backend django server at <a href="http://localhost:1337/">localhost:1337</a>
- Access the frontend nginx server at <a href="http://localhost:1338/">localhost:1338</a>
- Use the frontend client to signup/login and interact with application.
- Given API endpoints can be used to fetch transactions and accounts information.

## Features:

- Supports asynchronous processing of submissions to keep the server up for new requests.
- Uses Schroot to securely compile and execute the code submitted by users.
- Can Judge for Compilation Errors, Runtime Errors, and keep track of Time Limit. (Memory Limit Check to be added soon).
- Currently Supported Langauages: "C", "C++" and "Python" ("Java" to be added soon).
- Store and persist number of submissions by their verdicts by users.
- Support for Blogs/Tutorials
- Questions, Blogs and Testcases can be added/updated by admin.

## Postman

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/769c5f04be2bf6266abb?action=collection%2Fimport)

- **Postman Collections:** [https://www.getpostman.com/collections/769c5f04be2bf6266abb](https://www.getpostman.com/collections/769c5f04be2bf6266abb)


## API Endpoints:

```http
POST /register
```

| Parameter | Type      | Description                                                   |
| :-------- | :-------- | :------------------------------------------------------------ |
| `username`    | `string` | **Required**. username |
| `email`    | `string` | **Required**. email-id |
| `password`    | `string` | **Required**. password |

---

```http
POST /login
```

| Parameter | Type      | Description                                                   |
| :-------- | :-------- | :------------------------------------------------------------ |
| `username`    | `string` | **Required**. username |
| `password`    | `string` | **Required**. password |


---

```http
POST /logout
```

| Header     | Description                                                   |
| :------------ | :------------------------------------------------------------ |
| `Authorization`        | **Required**. Auth Token |


---

```http
GET /profile
```

| Header     | Description                                                   |
| :------------ | :------------------------------------------------------------ |
| `Authorization`        | **Required**. Auth Token |


---

```http
GET /blogs-list
```

| Header     | Description                                                   |
| :------------ | :------------------------------------------------------------ |
| `Authorization`        | **Required**. Auth Token |

---

```http
GET /blog/blog_id
```

| Header     | Description                                                   |
| :------------ | :------------------------------------------------------------ |
| `Authorization`        | **Required**. Auth Token |

---

```http
GET /questions-list
```

| Header     | Description                                                   |
| :------------ | :------------------------------------------------------------ |
| `Authorization`        | **Required**. Auth Token |

---

```http
GET /questions/questions_id
```

| Header     | Description                                                   |
| :------------ | :------------------------------------------------------------ |
| `Authorization`        | **Required**. Auth Token |

---

```http
POST /submit
```

| Header     | Description                                                   |
| :------------ | :------------------------------------------------------------ |
| `Authorization`        | **Required**. Auth Token |


| Parameter | Type      | Description                                                   |
| :-------- | :-------- | :------------------------------------------------------------ |
| `ques`    | `string` | **Required**. Questions Id |
| `code`    | `string` | **Required**. Code |
| `lang`    | `string` | **Required**. Language of the code |


### Responses

```json
{
    "detail": "success",
    "submission_data": {
        "id": "90",
        "user": "akshit1",
        "ques": "Q1",
        "code": "print(input())",
        "lang": "Python",
        "verdict": "Submission Queued"
    }
}
```
