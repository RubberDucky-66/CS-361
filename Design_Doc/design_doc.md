Joshua Samuel     
CS 361 

# Section 1: Overview
The software system requested by the Bend Bike Shop will enable customers to rent and reserve bikes for a requested period of time. Employees will be able to confirm rentals, process returns, and manage the details of the store's inventory.

# Section 2: Actors
* Customer: Use the online website or store kiosk to browse the store's bike inventory and reserve bikes for available dates. Entering information such as name, email, and a card on file.
* Payment Processor (external): Verifies credit cards and handles bank card transactions.
* Store Staff: Use the employee portal to check in/out bikes, manage inventory, manage employees, check reservations, and print reports.

# Section 3: Goals/Non-Goals

## Goals:
* Staff can check bikes in and out
* Mangers can add employees and give employees manager numbers
* Managers can add or remove bikes to the inventory
* Managers can print the overdue bikes list
* Customers can view and filter the bike inventory 
* Customers can reserve bikes at an available date
* Staff can clock in and out
* Staff can view the reservations list
* Staff can mark a bike as out for maintenance

## Non-Goals:
The following are beyond the scope of the system and are not required for the solution.
* Automated discounts or dynamic pricing for available bikes
* No outright bike sales or automated charges of unreturned bikes. This will need an employee or manager.
* Rental extensions must also go through employees
* No automated handoffs or checkouts of bikes
* Don't worry about advertisements, that is for another team to worry about.

# Section 4: Constraints
1. Customers must be able to swipe their cards, so they don't need to enter their information manually.
2. Customers must be able to use the reservation system as a guest, accounts are optional.
3. Bikes have a 7-day rental limit at max (extentions are handled through the store staff). Rentals are issued at 4 hour intervals, a days rental fee is equal to 12 hours.
4. Reservations should be able to go as far as 6 months out.
5. Customers must be able to filter bikes on the website.

# Section 5: Assumptions
1. The payment processor API will be up 99% of the time.
2. The website should be able to handle an average of 200 users at a time.
3. The reservation system is first come first serve. If multiple users request the same day and same bike (if only 1 is available that day) the first request to reach the server gets approved and the other will have to make a new request. 
4. A manager will always be present for all system actions requiring manager numbers.
5. Reports will be manually printed, with a requested date range.

# Section 6: Non-Functional Requirements
1. The payment processor will have a response in 1.5 seconds 95% of the time.
2. Website reservation requests will be processed within 6 seconds.
3. Customer/Bike history lookup is loaded within 5 seconds.
4. Staff will be logged out of the portal after 1 minute of inactivity.
5. The customer kiosk will reset to the home screen if left inactive for 1 minute.

# Section 7: Component Diagram and Description

``` mermaid
flowchart TB
    subgraph Client ["Customer Interface"]
        WebKiosk[Website & Kiosk UI]
    end

    subgraph Employee ["Staff Portal"]
        Portal[Employee Portal Dashboard & UI]
    end

    subgraph Server ["Backend Server"]

        WebServer[Web Server]
        Rental[Rental & Reservation Service]
        Inventory[Inventory]
        Roles[Employee Authorization Levels]
        Reports[Reports]
        DB[(Long Term Database)]
    end

    subgraph External ["External Third-Party"]
        PaymentProcessor[Payment Processor]
    end

    WebKiosk <--> WebServer
    Portal <--> WebServer

    WebServer -->|Check Staff Roles| Roles
    WebServer -->|Browse / Reserve Bikes| Rental
    WebServer -->|Check In/Out| Inventory
    WebServer -->|Generate Overdue Lists| Reports

    Rental -->|Pre-authorize| PaymentProcessor
    Inventory -->|Charge| PaymentProcessor
    
    Rental -->|Save Reservations| DB
    Inventory -->|Update Status / Add / Remove Bikes| DB
    Reports -->|Check Records| DB
```

| Component | Responsibility |
|---|---|
| **Website & Kiosk UI** | The interface for customers that handles, browsing, inventory filtering, and reservation placement. |
| **Employee Portal Dashboard & UI** | The store staff interface that allows access to bike check in/out, inventory management, reports, and reservation schedules. |
| **Web Server** | The gateway between the user interfaces and the internal backend handling the data. |
| **Rental & Reservation Service** | Manages bike reservations, availability checks, reservation lookups, and coordinates pre-authorization with the payment processor. |
| **Inventory** | Handles bike statuses such as check in/out, maintenance notes, and the addition/removal of bikes. |
| **Employee Authorization Levels** | Controls permission levels of normal employees and management. |
| **Reports** | Creates and manages operation reports such as the overdue bikes list. |
| **Long Term Database** | Stores longterm information for customer accounts and inventory. |
| **Payment Processor** | The secure external third-party responsible for card pre-authorization and charges. |
