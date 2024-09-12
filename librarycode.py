from datetime import date
from enum import Enum
from typing import List

# Enum for Book Status
class BookStatus(Enum):
    AVAILABLE = "Available"
    ON_LOAN = "On_loan"
    RESERVED = "Reserved"
    DAMAGED = "Damaged"
    LOST = "Lost"

# Base classes
class User:
    def __init__(self, user_id: str, name: str, contact_info: str, address: str, password: str):
        self.user_id = user_id
        self.name = name
        self.contact_info = contact_info
        self.address = address
        self.password = password
        self.is_authenticated = False

    def login(self, password: str) -> bool:
        self.is_authenticated = (self.password == password)
        return self.is_authenticated

    def update_contact_info(self, new_info: str):
        self.contact_info = new_info

    def change_password(self, new_password: str):
        self.password = new_password


class Member(User):
    def __init__(self, user_id: str, name: str, contact_info: str, address: str, password: str, resident_status: bool):
        super().__init__(user_id, name, contact_info, address, password)
        self.reservations: List['BookReservation'] = []
        self.loans: List['BookLoan'] = []
        self.resident_status = resident_status

    def loan_book(self, book: 'PhysicalBook') -> bool:
        if book.status == BookStatus.AVAILABLE:
            loan = BookLoan(id="L001", member=self, book=book, due_date=date.today())
            self.loans.append(loan)
            book.update_status(BookStatus.ON_LOAN)
            return True
        return False

    def return_book(self, book: 'PhysicalBook') -> bool:
        for loan in self.loans:
            if loan.book == book:
                book.update_status(BookStatus.AVAILABLE)
                self.loans.remove(loan)
                return True
        return False

    def reserve_book(self, isbn: 'BookISBN') -> bool:
        reservation = BookReservation(id="R001", member=self, ISBN=isbn, reservation_date=date.today(), book_status=BookStatus.RESERVED)
        self.reservations.append(reservation)
        return True

    def view_account_info(self):
        return {
            "name": self.name,
            "address": self.address,
            "loans": len(self.loans),
            "reservations": len(self.reservations)
        }

    def update_contact_details(self, contact_info: str):
        self.contact_info = contact_info


class Staff(User):
    def __init__(self, user_id: str, name: str, contact_info: str, address: str, password: str, admin_privileges: bool):
        super().__init__(user_id, name, contact_info, address, password)
        self.admin_privileges = admin_privileges

    def add_book(self, new_book: 'PhysicalBook'):
        Library.books.append(new_book)

    def update_book_details(self, book_id: str, new_details: dict):
        for book in Library.books:
            if book.book_id == book_id:
                book.title = new_details.get("title", book.title)
                book.author = new_details.get("author", book.author)
                book.genre = new_details.get("genre", book.genre)

    def generate_report(self, report_type: str) -> 'Report':
        report = Report(id="R001", generated_by=self, report_type=report_type, date_generated=date.today(), data="")
        # Logic to gather data based on the report type
        return report


# Additional entities
class Report:
    def __init__(self, id: str, generated_by: Staff, report_type: str, date_generated: date, data: str):
        self.id = id
        self.generated_by = generated_by
        self.report_type = report_type
        self.date_generated = date_generated
        self.data = data

    def generate_book_loan_report(self) -> 'Report':
        # Logic for book loan report
        pass

    def generate_user_report(self) -> 'Report':
        # Logic for user report
        pass

    def generate_reservation_report(self) -> 'Report':
        # Logic for reservation report
        pass

    def generate_author_report(self) -> 'Report':
        # Logic for author report
        pass


class PhysicalBook:
    def __init__(self, book_id: str, title: str, author: str, genre: str, isbn: str, status: BookStatus = BookStatus.AVAILABLE):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.isbn = isbn
        self.status = status

    def get_details(self):
        return {
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "isbn": self.isbn,
            "status": self.status
        }

    def update_status(self, status: BookStatus):
        self.status = status


class BookLoan:
    def __init__(self, id: str, member: Member, book: PhysicalBook, due_date: date):
        self.id = id
        self.member = member
        self.book = book
        self.due_date = due_date

    def loan_book(self, member: Member, book: PhysicalBook) -> 'BookLoan':
        return BookLoan(id="L001", member=member, book=book, due_date=date.today())


class BookReservation:
    def __init__(self, id: str, member: Member, ISBN: 'BookISBN', reservation_date: date, book_status: BookStatus):
        self.id = id
        self.member = member
        self.ISBN = ISBN
        self.reservation_date = reservation_date
        self.book_status = book_status

    def create_reservation(self, member: Member, ISBN: 'BookISBN') -> 'BookReservation':
        return BookReservation(id="R001", member=member, ISBN=ISBN, reservation_date=date.today(), book_status=BookStatus.RESERVED)

    def cancel_reservation(self, reservation_id: str):
        # Logic to cancel a reservation
        pass


class BookISBN:
    def __init__(self, id: str, ISBN: str):
        self.id = id
        self.ISBN = ISBN


class Library:
    def __init__(self, name: str, location: str):
        self.name = name
        self.location = location
        self.members: List[Member] = []
        self.books: List[PhysicalBook] = []
        self.users: List[User] = []
        self.reports: List[Report] = []

    def register_member(self, name: str, contact_info: str) -> Member:
        member = Member(user_id="M001", name=name, contact_info=contact_info, address="", password="", resident_status=True)
        self.members.append(member)
        return member

    def add_book(self, book: PhysicalBook):
        self.books.append(book)

    def generate_report(self) -> Report:
        report = Report(id="R002", generated_by=None, report_type="General", date_generated=date.today(), data="")
        return report

    def search_books(self, query: str) -> List[PhysicalBook]:
        return [book for book in self.books if query in book.title or query in book.author]


# Usage example
library = Library("City Library", "123 Library St.")
staff = Staff(user_id="S001", name="Alice", contact_info="alice@example.com", address="123 St.", password="pass123", admin_privileges=True)
book1 = PhysicalBook(book_id="B001", title="The Great Gatsby", author="F. Scott Fitzgerald", genre="Fiction", isbn="123456789")
staff.add_book(book1)
member = library.register_member(name="John Doe", contact_info="john@example.com")
member.loan_book(book1)
