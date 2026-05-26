# API Endpoint Contract Specification

Use this template to document the physical contract of any new or modified API route in the application before writing implementation logic.

---

## 1. Route Summary

*   **Path:** `/api/v1/resource`
*   **Method:** `GET` / `POST` / `PUT` / `DELETE`
*   **Authentication Required:** Yes / No (Role: `user` / `admin`)
*   **Version:** `v1`

---

## 2. Request Contract

### 2.1 URL Parameters (if any)
| Parameter | Type | Required | Description |
|---|---|---|---|
| `id` | UUID / Integer | Yes | Unique identifier of the target resource |

### 2.2 Query Parameters (if any)
| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `page` | Integer | No | `1` | Pagination offset index |
| `limit` | Integer | No | `20` | Max entries to return |

### 2.3 Body Payload (JSON format)
```json
{
  "name": "Required string field",
  "category": "Optional string matching allowed enum values",
  "tags": ["Array of string labels"]
}
```

---

## 3. Response Contract

### 3.1 Success Response (`200 OK` or `201 Created`)
```json
{
  "success": true,
  "data": {
    "id": "uuid-string",
    "name": "Resource Name",
    "category": "default",
    "tags": [],
    "created_at": "YYYY-MM-DDTHH:MM:SSZ"
  }
}
```

### 3.2 Error Responses
*   `400 Bad Request` — Validation failed:
    ```json
    {
      "success": false,
      "error": "validation_error",
      "message": "Field 'name' is required."
    }
    ```
*   `401 Unauthorized` — Expired or invalid token.
*   `404 Not Found` — Resource ID does not exist.
