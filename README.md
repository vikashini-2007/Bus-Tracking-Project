# Real-Time Public Transport Tracking for Small Cities

## Project Description

This project is a web-based Public Transport Tracking System developed using Flask, MySQL, HTML, CSS and JavaScript.

The system helps users view available buses, driver details, routes and live bus locations. It also provides REST APIs for managing bus information.

## Technologies Used

- Python
- Flask
- MySQL
- HTML
- CSS
- JavaScript
- Leaflet.js
- OpenStreetMap
- Postman

## Main Modules

### 1. User Registration
Users can create an account using their name, email and password.

### 2. User Login
Registered users can log in to access the dashboard.

### 3. Route Management
Admin can add source and destination details for bus routes.

### 4. Bus Management
Admin can:
- Add a bus
- View buses
- Edit bus details
- Delete a bus

### 5. Location Management
The current latitude and longitude of a bus can be updated.

### 6. Bus Search
Users can search for a particular bus using the bus number.

### 7. Live Map
Bus locations are displayed on an interactive map using Leaflet.js and OpenStreetMap.

## REST API

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/buses` | Create a new bus |
| GET | `/api/buses` | Get all buses |
| GET | `/api/buses/<bus_number>` | Get one bus |
| PUT | `/api/buses/<bus_number>` | Update bus |
| DELETE | `/api/buses/<bus_number>` | Delete bus |

## Database

Database Name:

`bus_tracking`

Main tables:

- users
- buses
- routes

## Validation

The application validates required API fields and returns appropriate HTTP status codes.

Examples:

- `201` - Bus created successfully
- `400` - Invalid request
- `404` - Bus not found

## Testing

REST APIs were tested using Postman.

The following operations were tested:

- Create Bus
- Get All Buses
- Get One Bus
- Update Bus
- Delete Bus
- Validation Error
- Not Found Error

## Project Workflow

User → Frontend → Flask Backend → MySQL Database

For REST API:

Postman → Flask REST API → MySQL Database → JSON Response

## Future Enhancements

- Real-time GPS tracking
- ETA calculation
- Crowd level monitoring
- Push notifications
- Secure password hashing
- Admin authentication
- Mobile application

## Conclusion

The Real-Time Public Transport Tracking System provides a simple and efficient solution for managing and tracking public transportation in small cities.