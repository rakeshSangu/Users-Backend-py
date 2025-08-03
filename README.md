# CHANGES.md

## ✅ Major Issues Identified

1. **SQL Injection Vulnerabilities**  
   User inputs were directly embedded in SQL queries, making the application highly vulnerable to SQL injection attacks.

2. **No Input Validation**  
   The API accepted all input without any checks (e.g., missing required fields, empty strings, invalid email formats).

3. **Passwords Stored in Plain Text**  
   User passwords were being stored as plain text in the database — a major security flaw.

4. **Poor Error Handling**  
   There were no `try/except` blocks to handle runtime or database errors. Any failure would cause a server crash.

5. **Inconsistent API Responses**  
   API returned raw Python objects like `str(user)` or default responses instead of structured and meaningful JSON.

6. **Missing HTTP Status Codes**  
   All API responses returned `200 OK` even when an error occurred, making it difficult for clients to understand the response status.

---

## 🔧 Changes Made and Why

| Area | Change | Reason |
|------|--------|--------|
| **Security** | Parameterized queries | Prevented SQL injection by avoiding raw input in SQL. |
| **Validation** | Added checks for missing fields, email format, and non-empty values | Improved data integrity and user experience. |
| **Password Handling** | Passwords now hashed using `bcrypt` before storing in DB | Ensures sensitive user data is never stored in plain text. |
| **Error Handling** | Introduced `try/except` blocks with clear error messages | Prevents crashes and returns informative client responses. |
| **API Response Structure** | All responses now follow a consistent JSON structure with `status`, `message`, and `data` fields | Makes the API predictable and easy to integrate. |
| **HTTP Status Codes** | Implemented appropriate status codes (200, 201, 400, 404, 500) | Enables client-side apps to reliably interpret responses. |

---

## 🧠 Assumptions and Trade-offs

- Assumed email should be unique during user registration.
- Used `bcrypt` with a fixed salt rounds (default 12) for simplicity.
- Did not implement JWT/session authentication due to time constraints.
- Allowed case-insensitive user name search for flexibility.
- Focused on fixing functionality, not optimizing performance for large datasets.

---


✅ *All changes aim to improve the API’s security, stability, and usability — ensuring it’s closer to production-grade standards.*
