import argparse
import shlex
from datetime import date, time, datetime
from importlib.resources import files
from pathlib import Path

from app.model.calendar import Calendar
from app.services.persistence import PersistenceService


class ConsoleView:
    def __init__(self, calendar: Calendar = None):
        file_path = str(files("app").joinpath(Path("data/calendar.data")))
        self.persistence_service: PersistenceService = PersistenceService(file_path)
        if not calendar:
            self.calendar: Calendar = self.persistence_service.load()
        else:
            self.calendar: Calendar = calendar

    @staticmethod
    def show_welcome_msg():
        print(f"{'=' * 30}")
        print("WELCOME TO THE CALENDAR APP")
        print(f"{'=' * 30}")
        print("To view the list of commands, type 'help'")

    @staticmethod
    def show_help(command: str | None = None):
        if not command:
            print("\nCOMMANDS:")
            print("help - view the list of commands. Use help <command> to view the help message for a "
                  "specific command")
            print("add_event - add a new event")
            print("update_event - update an event")
            print("delete_event - delete an event")
            print("find_events - find events in a specific date range")
            print("add_reminder - add a reminder to an event")
            print("delete_reminder - delete a reminder from an event")
            print("list_reminders - list all reminders")
            print("available_slots - list all available slots in a specific date range")
            print("exit - close the application")
        else:
            match command:
                case "help":
                    print("help <command> - view the help message for a specific command")
                case "add_event":
                    print("Add a new event to the calendar")
                    print("Usage: add_event <title> <description> <date> <start_at> <end_at>")
                    print("Example: add_event 'Meeting' 'Discuss project details' 2021-10-15 09:00 10:00")
                case "update_event":
                    print("Update an existing event in the calendar")
                    print("Usage: update_event <event_id> <title> <description> <date> <start_at> <end_at>")
                    print("Example: update_event abc12 'Nice Meeting' 'Discuss project details' 2021-10-15 09:00 10:00")
                case "delete_event":
                    print("Delete an event from the calendar")
                    print("Usage: delete_event <event_id>")
                    print("Example: delete_event abc12")
                case "find_events":
                    print("List all events in a specific date range")
                    print("Usage: find_events <start_at> <end_at>")
                    print("Example: find_events 2021-10-15 2021-10-16")
                case "add_reminder":
                    print("Add a reminder to an event of type 'system' or 'email'")
                    print("Usage: add_reminder <event_id> <date_time> <type>")
                    print("Example: add_reminder abc12 '2021-10-15 09:00' email")
                case "delete_reminder":
                    print("Delete a reminder from an event")
                    print("Usage: delete_reminder <event_id> <reminder_index>")
                    print("Example: delete_reminder abc12 1")
                case "list_reminders":
                    print("List all reminders of an event")
                    print("Usage: list_reminders <event_id>")
                    print("Example: list_reminders abc12")
                case "available_slots":
                    print("List all available slots in a specific date")
                    print("Usage: available_slots <date>")
                    print("Example: available_slots 2021-10-15 2021-10-16")
                case _:
                    print(f">>> ERROR: command {command} not supported. Type 'help' to view the list of commands")

    def add_event(self, args):
        try:
            event_id = self.calendar.add_event(args.title,
                                               args.description,
                                               datetime.strptime(args.date, '%Y-%m-%d').date(),
                                               datetime.strptime(args.start_at, '%H:%M').time(),
                                               datetime.strptime(args.end_at, '%H:%M').time())
        except ValueError as e:
            print(f">>> ERROR: {e}")
        else:
            print(f"Event added successfully with id {event_id}")

    def update_event(self, args):
        try:
            self.calendar.update_event(args.event_id,
                                       args.title,
                                       args.description,
                                       datetime.strptime(args.date, '%Y-%m-%d').date(),
                                       datetime.strptime(args.start_at, '%H:%M').time(),
                                       datetime.strptime(args.end_at, '%H:%M').time())
        except ValueError as e:
            print(f">>> ERROR: {e}")
        else:
            print("Event updated successfully")

    def delete_event(self, args):
        try:
            self.calendar.delete_event(args.event_id)
        except ValueError as e:
            print(f">>> ERROR: {e}")
        else:
            print("Event deleted successfully")

    def find_events(self, args):
        events = self.calendar.find_events(datetime.strptime(args.start_at, '%Y-%m-%d').date(),
                                           datetime.strptime(args.end_at, '%Y-%m-%d').date())
        if events:
            for date_, events_ in events.items():
                print(f"Events on {date_}:")
                for event in events_:
                    print(event)
                    print()
                print()
        else:
            print("No events found")

    def add_reminder(self, args):
        try:
            self.calendar.add_reminder(args.event_id,
                                       datetime.strptime(args.date_time, '%Y-%m-%d %H:%M'),
                                       args.type)
        except ValueError as e:
            print(f">>> ERROR: {e}")
        else:
            print("Reminder added successfully")

    def delete_reminder(self, args):
        try:
            self.calendar.delete_reminder(args.event_id, args.reminder_index - 1)
        except ValueError as e:
            print(f">>> ERROR: {e}")
        else:
            print("Reminder deleted successfully")

    def list_reminders(self, args):
        reminders = self.calendar.list_reminders(args.event_id)
        if reminders:
            for i, reminder in enumerate(reminders, start=1):
                print(f"{i}. {reminder}")
        else:
            print("No reminders found")

    def find_available_slots(self, args):
        available_slots = self.calendar.find_available_slots(
                                            datetime.strptime(args.date, '%Y-%m-%d').date())

        if available_slots:
            print(f"Available slots on {args.date}:")
            for slot in available_slots:
                print(f"- {slot}")
        else:
            print("No available slots found")

    def save_calendar(self):
        self.persistence_service.save(self.calendar)

    def process_user_command(self, user_input: str) -> bool:
        line = shlex.split(user_input)
        command = line[0]
        params = line[1:]
        parser = argparse.ArgumentParser()
        match command:
            case "help":
                if params:
                    parser.add_argument("command", type=str, help="Command to view help message for")
                    args = parser.parse_args(params)
                    self.show_help(args.command)
                else:
                    self.show_help()
            case "add_event":
                parser.add_argument("title", type=str, help="Event title")
                parser.add_argument("description", type=str, help="Event description")
                parser.add_argument("date", type=str, help="Event date")
                parser.add_argument("start_at", type=str, help="Event start time")
                parser.add_argument("end_at", type=str, help="Event end time")
                args = parser.parse_args(params)
                self.add_event(args)
            case "update_event":
                parser.add_argument("event_id", type=str, help="Event id")
                parser.add_argument("title", type=str, help="Event title")
                parser.add_argument("description", type=str, help="Event description")
                parser.add_argument("date", type=str, help="Event date")
                parser.add_argument("start_at", type=str, help="Event start time")
                parser.add_argument("end_at", type=str, help="Event end time")
                args = parser.parse_args(params)
                self.update_event(args)
            case "delete_event":
                parser.add_argument("event_id", type=str, help="Event id")
                args = parser.parse_args(params)
                self.delete_event(args)
            case "find_events":
                parser.add_argument("start_at", type=str, help="Start date")
                parser.add_argument("end_at", type=str, help="End date")
                args = parser.parse_args(params)
                self.find_events(args)
            case "add_reminder":
                parser.add_argument("event_id", type=str, help="Event id")
                parser.add_argument("date_time", type=str, help="Reminder date and time")
                parser.add_argument("type", type=str, help="Reminder type: email or system")
                args = parser.parse_args(params)
                self.add_reminder(args)
            case "delete_reminder":
                parser.add_argument("event_id", type=str, help="Event id")
                parser.add_argument("reminder_index", type=int, help="Reminder index")
                args = parser.parse_args(params)
                self.delete_reminder(args)
            case "list_reminders":
                parser.add_argument("event_id", type=str, help="Event id")
                args = parser.parse_args(params)
                self.list_reminders(args)
            case "available_slots":
                parser.add_argument("date", type=str, help="Date to check")
                args = parser.parse_args(params)
                self.find_available_slots(args)
            case "exit":
                self.save_calendar()
                return True
            case _:
                print(">>> ERROR: Invalid command. Type 'help' to view the list of commands")

    def app_loop(self):
        ConsoleView.show_welcome_msg()
        end_app: bool = False
        while not end_app:
            user_input: str = input("\nCalendarApp > ")
            end_app = self.process_user_command(user_input)