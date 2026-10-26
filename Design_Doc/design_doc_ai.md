# Section 1: Overview
The software system requested by the Bend Bike Shop will enable customers to rent and reserve bikes for a requested period of time through an online website or in strore kiosk. Employees will be able to confirm rentals, process returns, and manage the details of the store's inventory. The system handles the complete rental cycle from reservation to return.

# Section 2: Actors
* Customer: Use the online website or store kiosk to browse and filter the store's bike inventory and reserve bikes for available dates. They provide identification details, contact information, and a payment card for pre-authorization. 
* Payment Processor (external): An external third-party service that securely pre-authorizes funds, processes credit/debit card transactions, and manages card data outside the core backend database to maintain compliance.
* Store Staff: Use the employee portal to check in/out bikes, manage inventory, and check reservations.
* Store Manager: A higher level of authorization that is needed to perform certain operations including managing employees, printing reports, adding/removing inventory, and general manager approvals.

# Section 3: Goals/Non-Goals

## Goals:
* Reservation & Rental Lifecycle: Customers can browse inventory, view availability, and reserve bikes up to six months in advance; staff can verify reservations, check out, and check in rentals.
* Inventory Management: Store managers can add or remove bikes, while staff can check in/out bikes and place them under maintenance.
* Authorization Controls: Store managers can manage employee accounts and grant manager approvals for certain actions (printing reports, inventory management, and credit accounts).
* Schedules: Staff can clock in/out (with time records linked to schedules).
* Reports: Managers can manually generate/print overdue bike reports by a specified date range.
* Payment Processing: The system supports secure pre-authorizations, captures funds through an integrated payment processor, handles guest reservations via secure payment association, and logs transaction outcomes.

## Non-Goals:
The following are beyond the scope of the system and are not required for the solution.
* Automated discounts or dynamic pricing for available bikes
* No outright bike sales or automated charges of unreturned bikes. This will need an employee or manager.
* Rental extensions must also go through employees
* No automated handoffs or checkouts of bikes
* Don't worry about advertisements, that is for another team to worry about.

# Section 4: Constraints
1. Customers must be able to swipe their cards, so they don't need to enter their information manually at the kiosk.
2. Customers must be able to use the reservation system as a guest, accounts are optional.
3. Bikes have a 7-day rental limit at max (extentions are handled through the store staff). Rentals are issued at 4 hour intervals, a days rental fee is equal to 12 hours.
4. Reservations should be able to go as far as 6 months out.
5. Customers must be able to filter bikes on the website.

# Section 5: Assumptions
1. The payment processor API will be up 99% of the time.
2. The website should be able to handle an average of 200 users at a time.
3. The reservation system needs an atomic reservation operation, transaction, or locking mechanism to ensure that a bike cannot be reserved for overlapping periods.
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
