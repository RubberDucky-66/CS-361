Design Document Review: Bend Bike Shop Rental System
1. Logical Issues
1.1 Reservation Availability and Concurrency
The first-come, first-served reservation assumption does not define how simultaneous requests are handled. Two requests could pass an availability check before either reservation is saved, resulting in double-booking.
The system needs an atomic reservation operation, transaction, or locking mechanism to ensure that a bike cannot be reserved for overlapping periods.
The document refers to availability by day in Section 5, but rentals have four-hour intervals in Section 4. It is unclear whether availability is calculated by calendar day, time slot, or the entire requested rental period.
The system does not specify what happens when a payment pre-authorization fails after a reservation request is submitted.
1.2 Incomplete Rental Lifecycle
The document does not define the complete lifecycle of a rental, from reservation through pickup, return, inspection, and closure.
It is unclear whether reservations automatically become rentals when a customer arrives or whether staff must explicitly convert them.
There is no defined process for no-shows, cancellations, late pickups, damaged bikes, or bikes returned late.
Rental extensions are excluded from customer self-service but are not defined as a staff workflow.
The system does not specify whether a bike can be checked out without a reservation or whether walk-in rentals are supported.
1.3 Ambiguous Pricing and Time Rules
The statement that a day's rental fee equals 12 hours is ambiguous. It does not explain how four-hour intervals translate into daily charges.
The maximum rental duration of seven days is not clearly connected to the 12-hour pricing rule.
No rules define partial-day pricing, rounding, taxes, deposits, refunds, cancellation fees, or late fees.
The document does not clarify whether the rental clock begins at the scheduled reservation time, actual pickup time, or staff checkout time.
Time zones, business hours, and daylight-saving transitions are not addressed.
1.4 Incomplete Payment Handling
The system specifies pre-authorization and charges but does not define when authorization occurs, how long it remains valid, or when funds are captured or released.
It is unclear whether the system stores card details or delegates all card storage and processing to the payment processor.
The requirement for customers to swipe cards does not specify whether the website, kiosk, or both must support physical card readers.
Guest reservations require identifying information, but the document does not define how a guest's payment method and reservation are associated.
Payment failures, processor timeouts, duplicate payment requests, refunds, and reconciliation are not addressed.
1.5 Incomplete Inventory Management
Bike statuses are not fully defined. Possible states include available, reserved, checked out, overdue, under maintenance, and retired.
The document does not define valid transitions between bike statuses or prevent conflicting operations.
It is unclear whether a bike can be removed from inventory while reserved or rented.
Maintenance handling lacks rules for existing reservations when a bike becomes unavailable.
The system does not specify whether bike condition, damage, repair history, or maintenance completion must be recorded.
1.6 Incomplete Employee and Manager Authorization
The document refers to manager numbers but does not define whether they are unique identifiers, credentials, approval codes, or authorization tokens.
The assumption that a manager will always be present conflicts with the possibility of managers being unavailable during normal operations.
Employee authentication, password management, session protection, and account deactivation are unspecified.
Staff clock-in and clock-out functionality has no defined connection to employee schedules, time records, or corrections.
The document does not specify whether all staff can access customer information, process payments, or view reports.
Manager authorization for sensitive operations needs to be enforced by the backend, not only by the employee interface.
2. Structural Issues
2.1 Missing Functional Requirements

The goals list high-level capabilities but does not provide enough detail to implement or test them reliably.

Missing or underspecified requirements include:

Reservation creation, modification, cancellation, and confirmation.
Reservation confirmation and failure messages.
Customer contact information validation.
Search, sorting, and filtering behavior.
Reservation lookup and customer/bike history access.
Rental checkout and return validation.
Overdue rental calculation and report contents.
Employee account creation, modification, and deactivation.
Maintenance scheduling and completion.
Payment authorization, capture, refund, and failure recovery.
Data validation, error handling, and audit logging.
2.2 No Explicit Acceptance Criteria

The non-functional requirements specify several response times but do not consistently define how they will be measured.

For example:

"Website reservation requests will be processed within 6 seconds" does not state a percentile, workload, or whether payment processor latency is included.
"Customer/Bike history lookup is loaded within 5 seconds" does not specify a percentile or dataset size.
"Average of 200 users at a time" is an assumption rather than a measurable capacity requirement.
The document does not define a target availability percentage for the overall system.

Each requirement should have measurable acceptance criteria and a test method.

2.3 Missing Data Model

The component diagram references a long-term database but does not define the data entities or their relationships.

Likely entities include:

Bike
Reservation
Rental
Customer
Payment transaction
Employee
Employee role
Maintenance record
Time-clock record
Audit event

The document should clarify how reservations, rentals, customers, bikes, and payments are linked and which records must be retained.

2.4 Missing Error and Exception Flows

The design focuses on successful operations without defining failure behavior.

Examples include:

Payment processor unavailable.
Bike becoming unavailable during reservation.
Database or backend failure during checkout.
Duplicate requests caused by retries.
Failed staff authentication.
A bike returned in damaged condition.
A printer being unavailable during report generation.

The design should specify recovery behavior, user-facing errors, and whether an operation can be safely retried.

2.5 Incomplete Scope Definition

The non-goals section excludes several features but leaves important boundaries unclear.

For example:

Automated charges for unreturned bikes are excluded, but the manual payment workflow is not defined.
Rental extensions require staff involvement, but their effects on subsequent reservations are unspecified.
Automated checkouts are excluded, but the distinction between kiosk reservation and physical pickup is not explained.
Advertisements are excluded, but the document does not identify external dependencies or integration boundaries beyond payments.
3. Component Diagram Issues
3.1 Missing Database Relationships
The diagram shows reservations being saved to the database, but inventory changes, employee records, payment records, rental records, and time-clock records are not consistently represented.
The database is described as storing customer accounts and inventory, but guest reservations and rental history also require persistent storage.
The diagram does not show how reservations are associated with specific bikes and rental periods.
3.2 Unclear Component Responsibilities
The Rental & Reservation Service and Inventory component both appear responsible for operations that affect bike availability. This creates ambiguity about which component owns reservation conflict prevention.
The Web Server is described as a gateway, but it appears to perform authorization checks directly. A clearer distinction is needed between routing, authentication, authorization, and business logic.
The Employee Authorization Levels component appears to manage permissions, but there is no explicit employee identity or authentication component.
The Reports component is described as creating and managing reports, but the diagram only shows it reading records. Report generation, printing, and scheduling responsibilities are not fully defined.
3.3 Missing Communication Paths
There is no explicit flow for staff to view reservations.
The diagram does not show employee management or staff clock-in/clock-out operations.
There is no explicit path for maintenance status changes or maintenance completion.
Customer and bike history lookup is not represented.
Payment outcomes are not shown flowing back to the reservation or rental service.
There is no explicit notification mechanism for reservation confirmation, cancellation, overdue rentals, or payment failures.
3.4 Potential Security and Architecture Concerns
The diagram does not show TLS or other transport security between clients, the web server, and the payment processor.
No audit logging, monitoring, or centralized error handling components are shown.
The design does not establish whether card data passes through the backend or is handled directly by a payment provider's secure integration.
There is no defined boundary between public customer functionality and privileged employee functionality.
The diagram does not specify transaction boundaries for operations involving multiple components.
4. Non-Functional Requirement Issues
4.1 Session Timeout
Logging staff out after one minute of inactivity may interrupt routine operations and is unusually restrictive for an employee portal.
The requirement does not specify whether an active operation or unsaved work is interrupted.
Session expiration should include secure session invalidation and a clear reauthentication flow.
The kiosk reset should clear sensitive customer and payment information, not merely return to the home screen.
4.2 Performance and Scalability
The six-second reservation target needs to define whether it includes payment authorization and database commit time.
The system needs a defined load profile for 200 concurrent users, including the proportion browsing inventory versus submitting reservations.
No capacity or response-time requirement exists for peak loads, report generation, or inventory searches.
No database growth, retention, backup, or recovery requirements are specified.
4.3 Reliability and Availability
The payment processor's 99% availability is an assumption, not a guarantee, and implies substantial potential downtime.
The system's own availability requirement is missing.
The document does not define how the system behaves when the payment processor or database is unavailable.
Backup frequency, recovery time objective (RTO), recovery point objective (RPO), and disaster recovery procedures are absent.
4.4 Security and Privacy
No explicit requirements cover encryption at rest, encryption in transit, least-privilege access, or audit logs.
Customer personal information and payment-related data need retention, deletion, and access policies.
Guest reservations require protection against unauthorized reservation lookup or modification.
The design should clarify applicable payment-card security obligations, including PCI DSS scope.
The system does not specify protection against common web vulnerabilities, automated reservation abuse, or repeated authentication failures.
4.5 Accessibility and Usability
There are no accessibility requirements for the website, kiosk, or employee portal.
The kiosk requirements do not address accessible controls, readable text, screen-reader support where applicable, or alternative input methods.
The card-swiping constraint does not address payment methods or accessibility needs for customers unable to use the reader.
5. Contradictions and Ambiguities
Daily pricing versus rental intervals: Four-hour rental intervals and a daily fee equivalent to 12 hours are not sufficiently reconciled.
First-come, first-served versus availability: Processing order alone does not guarantee that concurrent reservations cannot double-book a bike.
Guest reservations versus customer history: The design requires customer/bike history lookups but does not define how guest identities are matched across reservations.
Manager presence assumption: Requiring a manager to always be present does not establish a reliable authorization or approval process.
Payment authorization versus charging: Pre-authorization and charging are assigned to different components without defining the payment lifecycle or recovery behavior.
Bike removal versus active rentals: Removing bikes from inventory is allowed, but the effect on current rentals and future reservations is undefined.
Overdue reporting versus rental extensions: The document excludes automated extensions but does not define how manually approved extensions affect overdue calculations.
Reservation limits versus inventory availability: A seven-day maximum rental duration and a six-month booking horizon are stated, but the rules for overlapping reservations and maintenance periods are missing.
Staff logout versus operational tasks: A one-minute inactivity timeout may interfere with checkout, return, or reporting workflows.
Customer card swiping versus website access: The required card-swiping behavior is not mapped to specific supported devices or interfaces.
6. Missing Examples and Edge Cases

The design would benefit from concrete examples covering:

A customer successfully reserving an available bike for two four-hour intervals.
Two customers attempting to reserve the same bike for overlapping periods at nearly the same time.
A reservation request failing because payment authorization is declined.
A bike being marked for maintenance after a customer has reserved it.
A rental becoming overdue and appearing on a report for a specified date range.
A staff member attempting an operation that requires manager approval.
A guest retrieving an existing reservation without creating an account.
A payment processor timing out after a reservation request has been submitted.
A customer returning a damaged bike or returning a bike after the scheduled return time.
A kiosk timing out while a customer is entering personal information.

These examples should specify the expected system behavior and resulting data changes.

7. Recommended Priorities
High Priority
Define the reservation and rental lifecycle, including cancellation, pickup, return, and extensions.
Establish precise pricing, rental interval, and overdue rules.
Define atomic reservation processing to prevent double-booking.
Specify payment authorization, capture, failure, and recovery workflows.
Define bike status transitions and their relationship to reservations.
Clarify employee authentication, manager approval, and access control.
Add measurable acceptance criteria for functional and non-functional requirements.
Medium Priority
Define the database entities, relationships, and retention policies.
Update the component diagram to show missing data flows and responsibilities.
Specify error handling, audit logging, monitoring, and reporting behavior.
Define session timeout behavior and kiosk data-clearing requirements.
Establish backup, recovery, availability, and load-testing requirements.
Lower Priority
Add accessibility and usability requirements.
Add detailed operational examples and edge-case scenarios.
Document external dependencies and integration boundaries.
Clarify report formats, print failures, and staff workflows.
Overall Assessment

The document provides a useful high-level overview of the Bend Bike Shop rental system, its main actors, broad goals, and initial component structure. However, it is not yet sufficiently detailed to serve as a complete implementation-ready design.

The most significant risks are ambiguous rental and pricing rules, concurrent reservation handling, incomplete payment workflows, unclear inventory state transitions, and underspecified employee authorization. Addressing these issues first will help prevent double-bookings, incorrect charges, inconsistent inventory records, and unauthorized operations.

The next revision should prioritize explicit functional requirements, business rules, state transitions, acceptance criteria, and failure scenarios before expanding the component diagram or selecting implementation technologies.