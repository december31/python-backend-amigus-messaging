from django.core.management import BaseCommand

from message.models import Message
from user.models import User
from utils.model_utils import get_object_or_none


class Command(BaseCommand):
    test_users_data = [
        {
            "display_name": "Sarah Smith",
            "email": "adam90@simpson.net",
            "phone_number": "+61 404 061 561",
        },
        {
            "display_name": "Anthony Nguyen",
            "email": "anthony@gmail.com",
        },
        {
            "display_name": "Gina Reed",
            "email": "zbaker@outlook.com",
            "phone_number": "152 505 7831",
        },
        {
            "display_name": "Lauren Roberts",
            "email": "belljustin@hopkins-white.net",
            "phone_number": "(415)561-2462",
        },
        {
            "display_name": "Kristen Clark",
            "email": "mezalinda@maddox.info",
            "phone_number": "01164960665",
        },
        {
            "display_name": "William Phillips",
            "email": "jamesrose@gmail.com",
            "phone_number": "707-771-1083x442",
        },
        {
            "display_name": "Gemma Roberts",
            "email": "lisaevans@carter-boyd.info",
            "phone_number": "945-727-0451",
        },
        {
            "display_name": "Heather Beasley",
            "email": "hilarypatel@outlook.com",
            "phone_number": "140 131 6965",
        },
        {
            "display_name": "Yolanda Ramos",
            "email": "josephmorales@holder-jones.com",
            "phone_number": "01134960332",
        },
        {
            "display_name": "Andrea Patel",
            "email": "whussain@outlook.com",
            "phone_number": "778.460.9797x8217",
        },
        {
            "display_name": "Caleb Flores",
            "email": "lisacampbell@holmes.com",
            "phone_number": "974.768.2374x672",
        },
        {
            "display_name": "Russell Ward-Ellis",
            "email": "kathryntaylor@patel.com",
            "phone_number": "1 (804) 133-6925",
        },
        {
            "display_name": "Lauren Rodgers",
            "email": "reesricky@bailey-smith.com",
            "phone_number": "+61.8.1325.0455",
        },
        {
            "display_name": "Katherine Dale",
            "email": "travismoore@yahoo.com",
            "phone_number": "1-180-329-5309",
        },
        {
            "display_name": "Mr Tom Wright",
            "email": "gsanchez@gmail.com",
            "phone_number": "(028) 9018832",
        },
        {
            "display_name": "Adam Graham",
            "email": "cjoyce@garcia.com",
            "phone_number": "+44(0)1632960677",
        },
        {
            "display_name": "Karen Johnson",
            "email": "mackenzierichmond@wade.com",
            "phone_number": "+44(0)141 496 0518",
        },
        {
            "display_name": "Nicholas Villanueva",
            "email": "rnicholls@gardiner.com",
            "phone_number": "5399.7078",
        },
        {
            "display_name": "Jeffrey Sloan",
            "email": "dawnryan@hotmail.com",
            "phone_number": "891.994.3427x83923",
        },
        {
            "display_name": "Michelle Christensen",
            "email": "barnesbobby@richmond.com",
            "phone_number": "+44161 4960815",
        },
        {
            "display_name": "Jorge Miller",
            "email": "oarmstrong@taylor.com",
            "phone_number": "345.576.7690",
        },
        {
            "display_name": "Gina Myers",
            "email": "douglastom@gmail.com",
            "phone_number": "855.785.8407",
        },
        {
            "display_name": "Christie Ward",
            "email": "junehooper@kemp.com",
            "phone_number": "+61.400.127.522",
        },
        {
            "display_name": "Brittany Johnson",
            "email": "jasonclay@wiggins.edu.au",
            "phone_number": "(0118) 4960753",
        },
        {
            "display_name": "Mr Gerard Smith",
            "email": "lorraine63@hotmail.co.uk",
            "phone_number": "+61 463 006 615",
        },
        {
            "display_name": "Cathy Elliott",
            "email": "ashley41@yahoo.com",
            "phone_number": "912-842-4534",
        },
        {
            "display_name": "Edward Ford",
            "email": "frederick24@turner.com",
            "phone_number": "(873) 187-9210 x305",
        },
        {
            "display_name": "Mrs Tracy Berry",
            "email": "smithsusan@williams-sutton.com",
            "phone_number": "001-035-142-2454x440",
        },
        {
            "display_name": "Paul Thomas",
            "email": "jennaliu@sanchez.net",
            "phone_number": "020 7946 0183",
        },
        {
            "display_name": "Lori Rodriguez",
            "email": "bmiles@hotmail.com",
            "phone_number": "880.446.0311",
        },
        {
            "display_name": "Elizabeth Bauer",
            "email": "johnsonantonio@hotmail.com",
            "phone_number": "+44909 879 0772",
        },
        {
            "display_name": "Austin Holmes",
            "email": "qpearson@outlook.com",
            "phone_number": "(0115)4960209",
        },
        {
            "display_name": "Heather Harrison",
            "email": "rebeccabibi@davies-humphreys.com",
            "phone_number": "+44115 4960134",
        },
        {
            "display_name": "David Ray",
            "email": "wardirene@hotmail.com",
            "phone_number": "(0141) 496 0576",
        },
        {
            "display_name": "Bryan Crawford",
            "email": "gallagherronald@thomas.com",
            "phone_number": "(747)201-8934",
        },
        {
            "display_name": "Mandy Roberts",
            "email": "karlvalencia@bailey-kennedy.com",
            "phone_number": "708 700 9284",
        },
        {
            "display_name": "Mark Trujillo",
            "email": "nguyenmike@winters.com",
            "phone_number": "(0808) 157 0178",
        },
        {
            "display_name": "Eric Blake",
            "email": "pfleming@gmail.com",
            "phone_number": "1-599-311-2124",
        },
        {
            "display_name": "Samantha Wong",
            "email": "chavezjulie@hotmail.com",
            "phone_number": "1-949-099-6082",
        },
        {
            "display_name": "Erin Haynes",
            "email": "annette36@hotmail.com",
            "phone_number": "08.0058.2623",
        },
        {
            "display_name": "Michael Hernandez",
            "email": "bonnie25@davis.org",
            "phone_number": "(804)842-6864",
        },
        {
            "display_name": "Michelle Glass",
            "email": "davissheri@garcia.net",
            "phone_number": "817-750-5429x9479",
        },
        {
            "display_name": "Scott Bennett",
            "email": "simmonsjay@bowen.com",
            "phone_number": "1-474-152-2319",
        },
        {
            "display_name": "James Soto",
            "email": "theresaphillips@moore.com",
            "phone_number": "+44(0)113 4960473",
        },
        {
            "display_name": "Ben Evans-Rogers",
            "email": "ureynolds@moore.com",
            "phone_number": "(07).1340.0916",
        },
        {
            "display_name": "Dr June Jones",
            "email": "ellisiain@yahoo.com",
            "phone_number": "088.096.2812x9277",
        },
        {
            "display_name": "Amber Hendricks",
            "email": "joelatkins@yahoo.co.uk",
            "phone_number": "(696)388-6698x8951",
        },
        {
            "display_name": "Mr Russell Long",
            "email": "mariamiller@randall.com",
            "phone_number": "+61 414 089 225",
        },
        {
            "display_name": "David Rogers",
            "email": "hernandezmitchell@bell-kirk.com",
            "phone_number": "331.808.0250",
        },
        {
            "display_name": "Dr Frances Robertson",
            "email": "victoria12@hotmail.com",
            "phone_number": "(07) 4836 5658",
        },
        {
            "display_name": "Kevin Gilbert",
            "email": "pattersonjames@sanders.biz",
            "phone_number": "692-604-7792",
        },
        {
            "display_name": "Mrs Emma Palmer",
            "email": "amandabrown@hotmail.co.uk",
            "phone_number": "716-563-8050 x255",
        },
        {
            "display_name": "Mr Jay Howard",
            "email": "ugoodwin@hotmail.com",
            "phone_number": "+44131 496 0496",
        },
        {
            "display_name": "Ronald Williams",
            "email": "cavila@hotmail.com",
            "phone_number": "406.967.7104x622",
        },
        {
            "display_name": "Alejandro Knight",
            "email": "gordonjessica@gmail.com",
            "phone_number": "(681) 595-2770 x013",
        },
        {
            "display_name": "Amber Wilson",
            "email": "gchapman@yahoo.com",
            "phone_number": "770.334.7539",
        },
        {
            "display_name": "Derek Stephenson",
            "email": "grace37@yahoo.co.uk",
            "phone_number": "578.095.2058",
        },
        {
            "display_name": "Sheri Dean",
            "email": "rachaelbailey@clarke.com",
            "phone_number": "7930.4257",
        },
        {
            "display_name": "Kevin Collins",
            "email": "bguerrero@garcia.com",
            "phone_number": "811-231-4133 x860",
        },
        {
            "display_name": "Gina Martin",
            "email": "michael99@hotmail.com",
            "phone_number": "(08).2197.7129",
        },
        {
            "display_name": "Yolanda Mcclure",
            "email": "kristina83@yahoo.com",
            "phone_number": "(874)429-1047x554",
        },
        {
            "display_name": "Alexandra Clark",
            "email": "barry98@hotmail.com",
            "phone_number": "384 262 9776",
        },
        {
            "display_name": "Paul Murphy",
            "email": "ortizerica@gmail.com",
            "phone_number": "2963775550",
        },
        {
            "display_name": "Erica Cox",
            "email": "uwebb@godfrey.info",
            "phone_number": "894.965.3183",
        },
        {
            "display_name": "Anna Green",
            "email": "pattonsteven@hotmail.com",
            "phone_number": "(109)388-4675x332",
        },
        {
            "display_name": "Mr. James Morgan",
            "email": "aguilartommy@thomas.org",
            "phone_number": "102.673.7256x356",
        },
        {
            "display_name": "Troy Anderson",
            "email": "wendymills@williamson.com",
            "phone_number": "+61-3-8319-8630",
        },
        {
            "display_name": "Tony Wong",
            "email": "joshuapatterson@yahoo.com",
            "phone_number": "+61868527786",
        },
        {
            "display_name": "Susan Lynn",
            "email": "sally63@ward-jones.com",
            "phone_number": "0141 496 0388",
        },
        {
            "display_name": "Kristen Vargas",
            "email": "wparker@nunez.com",
            "phone_number": "(905) 382-0611",
        },
        {
            "display_name": "Jody Peters",
            "email": "bradleyangela@harrell.info",
            "phone_number": "0141 4960783",
        },
        {
            "display_name": "Jean Taylor",
            "email": "mandy90@gmail.com",
            "phone_number": "(03)52648841",
        },
        {
            "display_name": "Allan Phillips",
            "email": "thomashawkins@hotmail.com",
            "phone_number": "(0808)1570891",
        },
        {
            "display_name": "Edward Burns",
            "email": "david00@gmail.com",
            "phone_number": "02.4598.2605",
        },
        {
            "display_name": "Andrew Krueger",
            "email": "deannajackson@baldwin.com.au",
            "phone_number": "715.628.1151",
        },
        {
            "display_name": "Monica Logan",
            "email": "micheal17@hotmail.com",
            "phone_number": "1-342-197-7838",
        },
        {
            "display_name": "Cody Nguyen",
            "email": "kirsty03@francis.com",
            "phone_number": "6527111198",
        },
        {
            "display_name": "Joshua Wood",
            "email": "grahamkristin@yahoo.com",
            "phone_number": "+4428 9018207",
        },
        {
            "display_name": "Maurice Andrews",
            "email": "djones@yahoo.com",
            "phone_number": "+61-7-0345-1141",
        },
        {
            "display_name": "Brittany Smith",
            "email": "ogray@gmail.com",
            "phone_number": "1-796-804-1310",
        },
        {
            "display_name": "Mrs Chloe Hill",
            "email": "vhughes@davison.co.uk",
            "phone_number": "45300104",
        },
        {
            "display_name": "Dr Graeme Tomlinson",
            "email": "leahsmith@hotmail.co.uk",
            "phone_number": "+1-032-559-9534x137",
        },
        {
            "display_name": "Stephanie Anderson",
            "email": "nancy51@walker.com.au",
            "phone_number": "(483)744-0073",
        },
        {
            "display_name": "Michael Burns",
            "email": "andreaharris@yahoo.com",
            "phone_number": "145.959.4212x4768",
        },
        {
            "display_name": "Megan Warren",
            "email": "edward53@hotmail.com",
            "phone_number": "171-522-3912",
        },
        {
            "display_name": "Heidi Harris",
            "email": "steven99@hotmail.com.au",
            "phone_number": "+44(0)115 4960990",
        },
        {
            "display_name": "David Lewis",
            "email": "bernardjeffrey@yahoo.com",
            "phone_number": "+61 8 2155 7843",
        },
        {
            "display_name": "Brianna Stevens",
            "email": "whiteemily@cox.info",
            "phone_number": "(020)74960672",
        },
        {
            "display_name": "Natalie Stokes-Richards",
            "email": "andersonthomas@hotmail.com",
            "phone_number": "+1-706-005-3397x9384",
        },
        {
            "display_name": "Craig Gomez",
            "email": "crawfordtheresa@lee.com",
            "phone_number": "+61.427.960.057",
        },
        {
            "display_name": "Anna Jones",
            "email": "allendavid@yahoo.com",
            "phone_number": "(333) 180-9533 x364",
        },
        {
            "display_name": "Victoria Daniels",
            "email": "thomas50@yahoo.com",
            "phone_number": "(566) 584-5158",
        },
        {
            "display_name": "Scott Mccormick",
            "email": "khowell@long.biz",
            "phone_number": "7984.9459",
        },
        {
            "display_name": "Amanda Reynolds",
            "email": "opennington@garcia.com",
            "phone_number": "+61.471.911.931",
        },
        {
            "display_name": "Bernard Holmes",
            "email": "danaanderson@andrews.com",
            "phone_number": "+61-3-0349-8029",
        },
        {
            "display_name": "Carolyn Mullins",
            "email": "willisconnor@hall-green.biz",
            "phone_number": "029 2018 0152",
        },
        {
            "display_name": "Michelle Pugh",
            "email": "sblevins@ryan.com",
            "phone_number": "+44306 9990914",
        },
        {
            "display_name": "Beth Barnes",
            "email": "murphychad@fields.net",
            "phone_number": "1-733-619-4009",
        },
        {
            "display_name": "Miss Vanessa Walker",
            "email": "jsoto@yahoo.com",
            "phone_number": "1-708-100-3827",
        },
        {
            "display_name": "Brian Wood MD",
            "email": "normanlaw@gordon.biz",
            "phone_number": "+44(0)131 4960012",
        },
        {
            "display_name": "Sarah Choi",
            "email": "hugh90@hotmail.com",
            "phone_number": "0306 9990215",
        },
    ]

    def handle(self, *args, **options):
        def build_user(user_data):
            email = user_data.get("email")
            display_name = user_data.get("display_name")
            phone_number = user_data.get("phone_number")

            user = get_object_or_none(User.objects, email=email)

            if user is None:
                print(f"building user {email}")
                user = User(
                    username=email,
                    email=email,
                    display_name=display_name,
                    phone=phone_number,
                    is_initialized=True,
                    is_active=True,
                )

                user.set_password("anthony123")
                return user
            else:
                return None

        print("start initiating users")

        users = [build_user(user_data) for user_data in self.test_users_data]
        users = [user for user in users if user is not None]
        
        [print(user) for user in users]
        
        User.objects.bulk_create(users)

        print(f"successful created {len(users)} users")