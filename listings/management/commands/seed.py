from django.core.management.base import BaseCommand
from listings.models import Listing
from realtors.models import Realtor
import random

# python manage.py seed --mode=refresh

""" Clear all data and creates addresses """
MODE_REFRESH = "refresh"

""" Clear all data and do not create any object """
MODE_CLEAR = "clear"


class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument("--mode", type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write("seeding data...")
        run_seed(self, options["mode"])
        self.stdout.write("done.")


def clear_data():
    """Deletes all the table data"""
    # logger.info("Delete Address instances")
    Listing.objects.all().delete()


def create_listing():
    """Creates an address object combining different elements from the list"""
    # logger.info("Creating address")
    street_number = ["221", "101", "550", "420", "13"]
    street_localities = [
        "Bakers Street",
        "Rajori Gardens",
        "Park Street",
        "MG Road",
        "Indiranagar",
    ]
    zipcodes = ["101234", "101232", "101231", "101236", "101239"]
    city = ["Chicago", "New York", "New Hampshire", "Boston"]
    state = ["WY", "AR", "NY", "CA"]
    description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    listing = Listing(
        realtor=random.choice(Realtor.objects.all()),
        title=random.choice(street_number)
        + " "
        + random.choice(street_localities),
        address=random.choice(street_number)
        + " "
        + random.choice(street_localities),
        city=random.choice(city),
        state=random.choice(state),
        zipcode=random.choice(zipcodes),
        description=description,
        price=random.randint(20, 60) * 10000,
        bedrooms=(random.randint(1, 4)),
        bathrooms=random.randint(1, 5),
        garage=random.randint(0, 3),
        sqft=random.randint(2000, 5000),
        lot_size=random.randint(2, 5),
    )
    listing.save()
    # logger.info("{} address created.".format(address))
    return listing


def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear
    :return:
    """
    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return

    # Creating 15 addresses
    for _ in range(20):
        create_listing()
