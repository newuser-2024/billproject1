# C$50 BillBuddy
### Video Demo:  <URL https://youtu.be/1myEwXo5G0Y?si=qzHOrfAQFvN3iyq2>
### Description:
C$50 BillBuddy is designed to simplify the process of splitting expenses among groups of people, such as friends, roommates, or travelers. Its primary goal is to make it easy to share costs fairly and transparently, reducing the stress and complexity often associated with dividing bills.


### Key Features of BillBuddy:
(1) Expense Splitting: Allows users to input expenses and then divides them among group members equally.

(2) Group Creation: Users can create groups, like for a household, a trip, or a dinner outing. This feature is especially useful for tracking shared expenses over time with a consistent group of people.

(3) Debt Simplification: The app simplifies debts among a group. For example, if person A owes B $10, B owes C $5 and A owes C $10, BillBuddy will simply show that A owes B $5 and A owes C $15, making it easier to understand and settle debts.

(4) Expense Tracking and History: Users can view their expense history, track who they owe money to, and see who owes them money. This includes detailed information on each expense.


### Implementation

#### /static directory:
(1) styles.css - used to style all the webpages of this website.

(2) money3.png - background image of the website.

#### /templates directory:
(1) apology.html - used to display error messages like username already taken or password is incorrect, etc.

(2) layout.html - serves as the blueprint of every webpage of this webapp.

(3) login.html - already existing users can login through this page.

(4) register.html - new users can register through this page.

(5) index.html - serves as default webpage which contains the introduction of this webapp.

(6) create.html - used to display the form through which users can create new groups.

(7) join.html - used to display the form through which users can join already existing group.

(8) group.html - it is displayed once the user joins the group. This webpage contains the form through which users can add their expenses and also view the expenses of other group members.

(9) summary.html - once every users have entered their individual expenses, it shows the list of transactions required to settle the


#### app.py:
it is the webapp code written in python using flask framework

#### helpers.py:
it contains helping functions required for this webapp.

#### billbuddy.db:
it's the database of the webapp which contains following tables:

Table: **users**
This table stores information about the users of your application.

**user_id**: This is the primary key for the table. It uniquely identifies each user. It's an integer and is auto-incremented, meaning it automatically gets a unique value when a new record is inserted.

**username**: This field stores the username of each user. It's a text field and is marked as not nullable, meaning every user must have a username.

**hash**: This field likely stores a hashed version of the user's password. It's a text field and not nullable.




Table: **sqlite_sequence**
This is a special table used by SQLite. It's used to keep track of the AUTOINCREMENT sequences for other tables. Generally, you don't need to interact with this table directly.

**name**: The name of the table for which the sequence number is maintained.

**seq**: The current sequence number for that table.


**Index: username**
This is a unique index created on the users table, specifically on the username column. This ensures that each username in the users table is unique.


Table: **groups**
This table holds information about different groups in your application.

**group_id**: The primary key for the table, uniquely identifying each group. It's an integer and auto-increments.

**group_name**: Stores the name of each group. It's a text field and not nullable.

**hash**: This field's purpose is not clear from the context. It could be used for some form of group identification or security, but this would depend on the specific implementation.


Table: **group_users**
This table creates a relationship between users and groups, allowing you to map which users are in which groups.

**group_id**: An integer field linking to the group_id in the groups table.

**user_id**: An integer field linking to the user_id in the users table.

The two FOREIGN KEY constraints ensure that group_id references a valid group_id in the groups table, and user_id references a valid user_id in the users table.


Table: **expenses**
This table is used to store information about expenses.

**expense_id**: The primary key for the table, uniquely identifying each expense. It's an integer and auto-increments.

**description**: A text field to store a description of the expense.

**amount**: A real (floating-point) number representing the amount of the expense. It's marked as not nullable.

**user_id**: An integer linking to the user who added the expense, referencing user_id in the users table.

**group_id**: An integer linking the expense to a specific group, referencing group_id in the groups table.

Two FOREIGN KEY constraints ensure that user_id and group_id reference valid entries in their respective tables.


These tables together form the backbone of a database for an application that manages user groups, their expenses, and the associations between them.
