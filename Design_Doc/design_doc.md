Joshua Samuel     
CS 361 

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

# Section 8: Data Model
## Entity Relationship Diagram:
``` mermaid
erDiagram
    CUSTOMER {
        string customer_id
        string name
        string email
        string phone_number
    }

    RESERVATION {
        string reservation_id
        string customer_id
        string bike_id
        datetime start_date
        datetime end_date
        string status
    }

    BIKE {
        string bike_id
        string model
        string status
        float rental_rate
    }

    PAYMENT {
        string payment_id
        string reservation_id
        float amount
        string pre_auth_status
        datetime timestamp
    }

    CUSTOMER ||--o{ RESERVATION : "places"
    BIKE ||--o{ RESERVATION : "is booked in"
    RESERVATION ||--|{ PAYMENT : "requires"
```
## Class Diagram:
``` mermaid
classDiagram
    class InventorySystem {
        - String storeId
        + addBike()
        + removeBike()
        + checkBikeDetails()
        + updateBikeStatus()
        + changeBikeRate()
    }

    class Bike {
        - String bikeId
        - String model
        - String status
        - float rentalRate
        + getDetails()
        + updateStatus()
        + updateRentalRate()
        + setMaintenanceMode()
    }

    class Employee {
        - String employeeId
        - String name
        - int authorizationLevel
        + viewInventory()
        + checkInBike()
        + checkOutBike()
        + clockIn
        +clockOut
    }

    class Manager {
        - String managerId
        - int authorizationLevel
        + approveSpecialRequest()
        + generateOverdueReport()
        + manageEmployeeAccount()
    }

    InventorySystem --> Bike : manages inventory of
    Employee --> InventorySystem : interacts with
    Manager --|> Employee : inherits from
    Manager --> InventorySystem : oversees and authorizes actions in
```


# Section 9: Interfaces

### Non-primitive types used across the system:
* BikeStatus - The current availability of a bike. Possible values could include "Available", "Reserved", "CheckedOut", "Maintenance".
* DataRange - Represents a time span between two timestamps. Possible values may include any pair of date and times between "startDate" and "endDate" where "startDate" is less than the "endDate".
* Report - an object with summary metrics, timestamps, or other information.
* CardDetails - Represents the secure information of a customer's payment method.

### Functions:
1. InventorySystem : addBike
    * Signature: addBike(model : string, initialRate : float) -> boolean
    * Purpose: Allows a manager to introduce a new bike object into the store's inventory system with a specified base rental rate.
    * Requires: initialRate must be greater than $0.0; the caller must possess manager authorization levels.
    * Outcomes: A new Bike entity is created, assigned a unique ID, given a default status of "Available", and successfully added to the long-term database inventory.
    * Guarantees: Returns true if the bike is successfully registered in the inventory; returns false if database persistence fails or authorization is insufficient.
    * Notes: Aligns with manager inventory control requirements.

2. InventorySystem : updateBikeStatus
    * Signature: updateBikeStatus(bikeId : string, newStatus : BikeStatus, notes : string) -> boolean
    * Purpose: Allows staff or managers to update the operational state or availability of a specific bike.
    * Requires: bikeId must exist in the database; newStatus must be a valid BikeStatus type.
    * Outcomes: The target bike's record is updated with the new status, and any additional notes are logged.
    * Guarantees: Returns true if the status update commits successfully; returns false if the bike ID or newStatus is invalid.
    * Notes: Essential for handling maintenance, reservations, and general inventory tracking.

3. RentalReservationService : createReservation
    * Signature: createReservation(bikeId : string, customerId : string, rentalPeriod : DateRange) -> string
    * Purpose: Allows a customer to reserve an available bike for a designated time window up to six months in advance.
    * Requires: bikeId and customerId must be valid; rentalPeriod must not overlap with an existing reservation for the target bike and cannot be beyond six months from the current date.
    * Outcomes: An atomic system locks the bike for the requested dates to prevent overlapping reservations, records the reservation, and associates it with the customer id/details.
    * Guarantees: Returns a unique reservation_id string upon success; returns an empty string or throws an exception if an overlapping reservation conflict occurs.
    * Notes: Enforces the atomic reservation locking assumption to prevent overlapping bookings.

4. Employee : checkOutBike
    * Signature: checkOutBike(reservationId : string, employeeId : string) -> boolean
    * Purpose: Allows store staff to process the physical handover of a reserved bike to a customer.
    * Requires: reservationId must be confirmed and active for the current date; employeeId must belong to a staff member.
    * Outcomes: The associated bike's status updates from "Reserved" to "CheckedOut", and the transaction is logged to the customer's and the bike's rental history.
    * Guarantees: Returns true once the check-out is successfully processed; returns false if the reservation ID is invalid.
    * Notes: Part of the workflow for managing physical rentals.

5. PaymentProcessorAdapter : preAuthorizeCard
    * Signature: preAuthorizeCard(card : CardDetails, amount : float) -> boolean
    * Purpose: Coordinates securely with the external third-party payment processor to verify funds and pre-authorize the estimated rental total prior to checkout.
    * Requires: card must contain valid payment reference data; amount must accurately reflect the calculated rental cost.
    * Outcomes: Transmits a secure pre-authorization request to the external payment processor gateway and logs the transaction outcome.
    * Guarantees: Returns true if funds are successfully pre-authorized within the required performance window; returns false if declined.
    * Notes: Keeps card data outside the core backend database to maintain security compliance.

6. Manager : generateOverdueReport
    * Signature: generateOverdueReport(range : DateRange, managerId : string) -> Report
    * Purpose: Enables a store manager to create a list of all bikes that are still checked out past their return dates within a specified date range.
    * Requires: range must specify a valid start and end date; the caller must possess manager authorization levels.
    * Outcomes: Checks the long-term database for unreturned items matching the date range and adds them into a structured Report format for manual printing.
    * Guarantees: Returns a Report object containing all matching overdue records; returns an empty report object if no overdue records were found.
    * Notes: Fulfills the manager-specific reporting requirement outlined in the design goals.

# Section 10: Invariants 
1. Rental Duration Limit: A single bike rental or reservation period shall never exceed 7 consecutive days without explicit staff or manager extension.

2. Reservation Atomicity and Uniqueness: At any given point in time, a specific bike identifier cannot be on multiple currently active reservations or future reservations with overlapping dates.

3. Role-Based Authorization Enforcement: System actions categorized under manager permissions (such as modifying employee accounts, generating overdue reports, or altering inventory pricing) require an authenticated user with a valid manager authorization level.

4. Payment Separation: Raw payment information shall never be persisted or logged within the core long-term backend database.

# Section Failure Modes

| *ID* | *Failure* | *Detection* | *Response* | *Impact* | *Notification* |
| --- | --- | --- | --- | --- | --- |
| **FM-PAYMENT-TIMEOUT** | External payment gateway fails to respond within the pre-authorization time limit | `preAuthorizeCard` returns a timeout or network error status code | Retry once after 2 seconds. If it fails again prompt the customer to retry or use an alternative payment card. | Transaction delayed; customer unable to complete rental checkout immediately | Gateway timeout log |
| **FM-KIOSK-CARD-READER-ERROR** | Customer kiosk card swipe scanner fails to read | A function receives notification that the reader failled after 3 consecutive attempts | Display an error message on the kiosk screen prompting the customer to manually enter information or seek assistance from store staff. | Kiosk transaction temporarily blocked for the user | Kiosk hardware warning logged to the employee portal dashboard |
| **FM-DB-CONNECTION-BREAK** | Database connection breaks mid-transaction during a bike check-in or reservation save | A protection layer throws a connection timeout exception | Catch the exception and queue the transaction for when connection comes back. | Temporary reservation and inventory updates postponed | Critical database disconnect alert sent to system administrators |
| **FM-INVENTORY-SYNC-MISMATCH** | Physical bike status in the store differs from the database state | Staff attempts to check out a bike that is flagged as available, but the item cannot be located on the rack | Staff uses the `updateBikeStatus` interface to manually correct the record status to `Maintenance` and files a note to look into the bikes whereabouts. | Inventory count discrepancy; minor customer delay during pickup or refund | Discrepancy logged under inventory audit notes |
