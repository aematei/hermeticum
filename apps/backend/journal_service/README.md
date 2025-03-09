# Journal Service API Endpoints

## Health Check
- **GET /** - Check if the service is running
- Returns a message confirming the service is running

## Journal Entries

### Create Journal Entry
- **POST /journals/**
- Creates a new journal entry
- Request body:
  - `user_id`: UUID of the user
  - `title`: Title of the journal entry
  - `content`: Content of the journal entry

### Get Journal Entry
- **GET /journals/{journal_id}**
- Retrieves a specific journal entry by ID
- Path parameters:
  - `journal_id`: UUID of the journal entry

### Update Journal Entry
- **PUT /journals/{journal_id}**
- Updates an existing journal entry
- Path parameters:
  - `journal_id`: UUID of the journal entry
- Request body:
  - `title`: New title
  - `content`: New content

### Delete Journal Entry
- **DELETE /journals/{journal_id}**
- Deletes a journal entry by ID
- Path parameters:
  - `journal_id`: UUID of the journal entry
- Returns a success message

### Get User's Journal Entries
- **GET /users/{user_id}/journals**
- Retrieves all journal entries for a specific user
- Path parameters:
  - `user_id`: UUID of the user
- Returns a list of journal entries