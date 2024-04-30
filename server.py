from flask import Flask, render_template, send_file, g
from markupsafe import Markup
from werkzeug.utils import secure_filename

import os
import json

"""
    A quick helper script that makes it easier to add content to the website.
"""

app = Flask(__name__)
URL = "/"

CONTENT = {
    'NAV_OUR_STORY': {'en': "Our Story", 'nl': "Ons Verhaal"},
    'NAV_TIMELINE': {'en': "Timeline", 'nl': "Tijdlijn"},
    'NAV_ACCOMMODATION': {'en': "Accommodation", 'nl': "Accomodatie"},
    'NAV_TRANSPORT': {'en': "Transport", 'nl': "Vervoer"},
    'NAV_TODO': {'en': "To-Do", 'nl': "Te-Doen"},
    'NAV_FAQ': {'en': "FAQ", 'nl': "FAQ"},
    'NAV_RSVP': {'en': "RSVP", 'nl': "RSVP"},

    'PREVIOUS': {'en': "Previous", 'nl': "Vorige"},
    'NEXT': {'en': "Next", 'nl': "volgende"},

    # Countdown Section
    'DAYS': {'en': "Days", 'nl': "Dagen"},
    'HOURS': {'en': "Hours", 'nl': "Uren"},
    'MINUTES': {'en': "Minutes", 'nl': "Minuten"},
    'SECONDS': {'en': "Seconds", 'nl': "Seconden"},

    # Our Story Section
    'OUR_STORY': {'en': "Our Story", 'nl': "Ons Verhaal"},
    'WITH_LOVE': {'en': "WITH LOVE", 'nl': "MET LIEFDE"},
    'HOW_WE_MET': {'en': "How We Met", 'nl': "Ontmoeting"},
    'HOW_WE_MET_DESC': {
        'en': """
            Ruben went shopping for lunch and decided to buy a single banana. He took a picture for a 
            friend, who passed it on to another, before reaching Olivia. Spotting a sad face in the banana's 
            marks, she digitally drew on a little face, and sent it back to her friend. This was passed back 
            to Ruben, and a group chat (as well as our journey) was started -all thanks to a single banana
        """, 
        'nl': """
            Ruben kocht voor zijn lunch een banaan en stuurde een foto naar een vriend. Die stuurde de foto 
            door naar een ander, voordat deze Olivia bereikte. Ze zag een verdrietig gezicht in de vlekken van de 
            banaan, tekende digitaal een klein gezichtje en stuurde het terug naar haar vriend. Dit werd 
            teruggestuurd naar Ruben, en een groepschat (evenals onze reis) werd gestart - allemaal dankzij een 
            enkele banaan  
        """
    },
    'HOW_WE_MET_DATE': {'en': "20 Oct. 2017", 'nl': "20 okt. 2017"},
    'STARTED_DATING': {'en': "Started Dating", 'nl': "Verkering"},
    'STARTED_DATING_DESC': {
        'en': """
            Ruben flew over to England and joined Olivia and her family on a trip to Cornwall. One
            morning they decided to wake up early to watch the sunrise. Ruben then asked Olivia to
            be his girlfriend on the roof of the house, overlooking the sea. After Olivia said yes, 
            Ruben then got attacked by a massive fly 
            <span class="fw-light">(it hit me right in the back of the head!)</span> and we quickly 
            ran inside.
        """, 
        'nl': """
            Ruben vloog naar Engeland en vergezelde Olivia en haar familie op een reis naar Cornwall. 
            Op een ochtend besloten ze vroeg op te staan om naar de zonsopgang te kijken. Ruben vroeg 
            Olivia toen om zijn vriendin te worden op het dak van het huis, met uitzicht op de zee. 
            Nadat Olivia ja had gezegd, werd Ruben aangevallen door een enorme vlieg 
            <span class="fw-light">(hij raakte me recht op mijn achterhoofd!)</span> en we renden snel naar binnen.
        """
    },
    'STARTED_DATING_DATE': {'en': "26 Jun. 2018", 'nl': "26 jun. 2018"},
    'FINALLY_TOGETHER': {'en': "Finally Together", 'nl': "Eindelijk Samen"},
    'FINALLY_TOGETHER_DESC': {
        'en': """
            Ruben came over in March 2020 to visit Olivia for the weekend, as he did every month. 
            Before he could fly back home, the UK went into lockdown due to Covid and his diabetic 
            team back in the Netherlands advised him to stay there and not to fly due to the virus, 
            until they knew more. Since then, Ruben hasn't left and we moved in together in April 2022
        """, 
        'nl': """
            Ruben kwam in maart 2020 een weekend naar Olivia, zoals hij elke maand deed. Voordat hij 
            terug naar huis kon vliegen, werd het Verenigd Koninkrijk afgesloten vanwege Covid en zijn 
            diabetesteam in Nederland adviseerde hem om daar te blijven en niet te vliegen vanwege het 
            virus, totdat ze meer wisten. Sindsdien is Ruben niet meer weggegaan en in april 2022 kochten 
            we onze eerste woning.
        """
    },
    'FINALLY_TOGETHER_DATE': {'en': "13 Mar. 2020", 'nl': "13 mrt. 2020"},
    'HE_PROPOSED': {'en': "He Proposed", 'nl': "Het Aanzoek"},
    'HE_PROPOSED_DESC': {
        'en': """
            Ruben and Olivia went to Southport with her family to celebrate her parents' anniversary. During a 
            walk on the beach during sunset one evening, they discussed their relationship, with all of its 
            many highs. Ruben got down on one knee and asked Olivia to marry him. Olivia, overwhelmed with joy, 
            said yes, and they've been happily planning the wedding ever since!
        """, 
        'nl': """
            Ruben en Olivia gingen met haar familie naar Southport om het jubileum van haar ouders te vieren. 
            Tijdens een wandeling op het strand tijdens zonsondergang op een avond, bespraken ze hun relatie, 
            met al zijn vele hoogtepunten. Ruben ging op één knie zitten en vroeg Olivia ten huwelijk. Olivia 
            was helemaal in de wolken en zei natuurlijk ja! Sindsdien zijn ze opgetogen bezig met het plannen 
            van de bruiloft!
        """
    },
    'HE_PROPOSED_DATE': {'en': "29 Aug. 2021", 'nl': "29 aug. 2021"},
    'OUR_WEDDING_DAY': {'en': "Our Wedding Day", 'nl': "Onze Trouwdag"},
    'OUR_WEDDING_DAY_DESC': {
        'en': """
            Olivia and Ruben have booked their wedding for Friday the 13th of September, 2024 at the Foxtail 
            Barns, Consall, England. This is only the start of our journey, and we can't wait to find out what 
            wonders life has in store for us. It would be wonderful to share this beautiful moment with you; 
            we hope to see you there! 
        """, 
        'nl': """
            Olivia en Ruben hebben hun bruiloft geboekt voor vrijdag 13 september 2024 in de Foxtail Barns in 
            Consall, Engeland. Dit is nog maar het begin van onze reis en we kunnen niet wachten om te ontdekken 
            welke wonderen het leven voor ons in petto heeft. Het zou geweldig zijn om dit mooie moment met 
            jullie te delen; we hopen jullie daar te zien!
        """
    },
    'OUR_WEDDING_DAY_DATE': {'en': "13 Sep. 2024", 'nl': "13 sep. 2024"},

    # Timeline section
    'WHEN_AND_WHAT': {'en': "WHEN AND WHAT ", 'nl': "WANNEER EN WAT"},
    'TIMELINE': {'en': "Timeline", 'nl': "Tijdlijn"},
    'timeline_items': [
        {
            'time': "13:30",
            'description': {
                'en': "Guests arrive at the venue and are seated",
                'nl': "Gasten arriveren op de locatie en nemen plaats"
            }
        },
        {
            'time': "14:00",
            'description': {
                'en': "The wedding ceremony begins and the magic happens",
                'nl': "De huwelijksceremonie begint en de magie kan beginnen"
            }
        },
        {
            'time': "14:30",
            'description': {
                'en': "Drinks reception starts and the photographer takes aim",
                'nl': "De borrel begint en de fotograaf gaat op pad"
            }
        },
        {
            'time': "16:15",
            'description': {
                'en': "Have a seat, and enjoy the wedding breakfast",
                'nl': "Neem plaats en geniet van het bruiloftsontbijt"
            }
        },
        {
            'time': "18:15",
            'description': {
                'en': "Start of the speeches and tears will flow",
                'nl': "Begin van de toespraken en het vloeien van tranen"
            }
        },
        {
            'time': "19:00",
            'description': {
                'en': "Evening guests arrive and the party gets started",
                'nl': "De avondgasten arriveren en het feest kan beginnen"
            }
        },
        {
            'time': "20:00",
            'description': {
                'en': "First dance followed by evening refreshments",
                'nl': "Eerste dans gevolgd door verfrissingen"
            }
        },
        {
            'time': "00:00",
            'description': {
                'en': "Bar closes, music stops, and guests depart",
                'nl': "De bar sluit, de muziek stopt en de gasten vertrekken"
            }
        }
    ],

    # Accommodation section
    'WHERE_TO_STAY': {'en': "WHERE TO STAY", 'nl': "WAAR TE VERBLIJVEN"},
    'ACCOMMODATION': {'en': "Accommodation", 'nl': "Accomodatie"},
    'accommodations': [     
        {
            'name': "Woodland Pods",
            'img_url': f"{URL}img/Foxtail-Barns-pods.jpg",
            'description': {
                'en': """
                    These nature inspired Pods are located at our wedding venue, and are nestled in the 
                    woodland of the fabulous estate. They come in different sizes and configurations with 
                    varying check in times, and the price starts at £110 for a double room, and £150 for a 
                    family room.<br>

                    <b>Please keep in mind that these pods are very limited, can only be booked through us,
                    and are for one night only!</b> If you're interested in hiring one, please contact Ruben
                    or Olivia
                """,
                'nl': """
                    Deze natuur geïnspireerde Pods bevinden zich op het terrein en zijn gelegen in de bossen 
                    van het fantastische landgoed. Ze zijn in verschillende maten en configuraties met verschillende 
                    inchecktijden beshikbaar. De prijs begint bij £110 voor een tweepersoonskamer en £150 voor 
                    een familiekamer.<br>
                    <b>Houd er rekening mee dat deze pods zeer beperkt zijn, alleen via ons te boeken zijn, 
                    en dat maximaal voor één nacht is!</b> Heb je interesse om er één te huren, neem dan 
                    contact op met Ruben of Olivia
                """,
            },
            'costs': "£££",
            'phone': "+44 (0)7984 133024",
            'url': "https://foxtailbarns-venue.co.uk/accommodation/book-a-lodge/",
            'display_url': "foxtailbarns-venue.co.uk"
        },
        {
            'name': "The Tawny",
            'img_url': f"{URL}img/The Tawny.jpg",
            'description': {
                'en': """
                   The Tawny is the accommodation next to the venue. It has a selection of unique accommodation 
                   options with stunning surroundings. All rooms feature an outdoor spa on your private decking. 
                   Even though this is next door to the venue, these are very expensive. They are to be seen as 
                   somewhere you stay for a special treat or a special occasion rather than an average hotel. 
                   Prices range from £250 up to £605 per night
                """,
                'nl': """
                    The Tawny is de accommodatie naast de trouwlocatie. Het heeft een selectie van unieke 
                    accommodatiemogelijkheden in een prachtige omgeving. Alle kamers beschikken over een buitenspa 
                    op eigen terras. Ook al is dit naast de locatie, ze zijn erg duur. Dit moet worden gezien als 
                    een plek waar je verblijft voor een speciale traktatie of een speciale gelegenheid, in plaats 
                    van als een gemiddeld hotel. Prijzen variëren van £250 tot £605 per nacht
                """,
            },
            'costs': "£££££",
            'phone': "+44 (0)1538 787664",
            'url': "https://thetawny.co.uk/",
            'display_url': "thetawny.co.uk"
        }, 
        {
            'name': "Premier Inn - Leek",
            'img_url': f"{URL}img/Premier Inn - Leek.jpg",
            'description': {
                'en': """
                    15 minutes from Foxtail Barns. Call 'Leek Link Taxis' on 
                    <a href="tel:++441538399999">+44 (0)1538 399999</a> for the best taxi rates back to 
                    the Leek Premier Inn at the end of the night. Chargeable on-site parking is available 
                    at this hotel at £5 per night
                """,
                'nl': """
                    15 minuten van Foxtail Barns. Bel 'Leek Link Taxis' op 
                    <a href="tel:++441538399999">+44 (0)1538 399999</a> voor de beste taxitarieven terug 
                    naar de Leek Premier Inn aan het eind van de nacht. Bij dit hotel is tegen een toeslag 
                    privéparkeergelegenheid beschikbaar voor £5 per nacht
                """,
            },
            'costs': "££",
            'phone': "+44 (0)333 321 9252",
            'url': "https://www.premierinn.com/gb/en/hotels/england/staffordshire/leek/leek-town-centre.html",
            'display_url': "www.premierinn.com"
        },   
        {
            'name': "Premier Inn - Hanley",
            'img_url': f"{URL}img/Premier Inn - Hanley.jpg",
            'description': {
                'en': """
                    9 miles from Foxtail Barns, with free parking. Just a ten-minute walk to the shops and cafés
                    of Hanley town centre plus the cute pottery outlets. There are two types of rooms, standard and
                    plus. Theres also two types of room rates, flexible (where you can pay cancel up to 13:00
                    on the same day and you can pay on arrival), and advanced (where you pay now and get free
                    cancellation up to 28 days before). Either king or twin rooms
                """,
                'nl': """
                    15 km van Foxtail Barns, met gratis parkeergelegenheid. Slechts tien minuten lopen naar de winkels
                    en cafés in het stadscentrum van Hanley, plus de schattige aardewerkwinkels. Er zijn twee soorten kamers, 
                    standaard en plus. Er zijn ook twee soorten kamertarieven: "flexible" (waarbij je tot 13.00 uur op 
                    dezelfde dag kan annuleren en bij aankomst kan betalen) en "advanced" (waarbij je nu betaalt en tot 28 
                    dagen van tevoren gratis kan annuleren). Zowel kamers met kingsize bed of tweepersoonskamers met 2 aparte 
                    bedden
                """,
            },
            'costs': "££",
            'phone': "+44 (0) 333 321 9337",
            'url': "https://www.premierinn.com/gb/en/hotels/england/staffordshire/stoke-on-trent/stoke-on-trent-hanley.html",
            'display_url': "www.premierinn.com"
        }, 
        {
            'name': "Hilton Garden Inn - Hanley",
            'img_url': f"{URL}img/Hilton Garden Inn - Hanley.jpg",
            'description': {
                'en': """
                    9 miles from Foxtail Barns. Within half a mile of the cultural quarter, near to the
                    Regent Theatre, Potteries Museum, Art Gallery and Potteries Shopping Centre. Multiple
                    rooms from twin rooms, king rooms and family rooms
                """,
                'nl': """
                    15 km van Foxtail Barns. Binnen 800 meter de culturele wijk, vlakbij het Regent Theatre, 
                    Potteries Museum, Art Gallery, en de Potteries Shopping Centre. Meerdere kamers, van 
                    tweepersoonskamers, kingsize kamers en familiekamers
                """,
            },
            'costs': "££££",
            'phone': "+44 (0)1782 486960",
            'url': "https://www.hilton.com/en/hotels/manstgi-hilton-garden-inn-stoke-on-trent/",
            'display_url': "www.hilton.com"
        }, 
        {
            'name': "DoubleTree by Hilton - Etruria",
            'img_url': f"{URL}img/DoubleTree by Hilton - Etruria.jpg",
            'description': {
                'en': """
                    25 minutes' drive away from Foxtail Barns. Can do group bookings for more than 10 rooms.
                    They offer multiple types of rooms, from twins, to king, to suites. Located on Festival 
                    Retail park, near the Stoke Ski Centre and Waterworld. The hotel has a full-service spa, 
                    pool, and restaurants
                """,
                'nl': """
                    25 minuten rijden van Foxtail Barns. Bieden groepsreserveringen voor meer dan 10 kamers. 
                    Meerdere soorten kamers beschikbaar, van tweelingen, tot koning, tot suites. Gelegen op 
                    Festival Retail Park, vlakbij het Stoke Ski Centre en Waterworld. Het hotel beschikt over 
                    een volledig uitgeruste spa, een zwembad en restaurants
                """,
            },
            'costs': "£££",
            'phone': "+44 (0)1782 609988",
            'url': "https://www.hilton.com/en/hotels/mandidi-doubletree-stoke-on-trent/",
            'display_url': "www.hilton.com"
        }, 
        {
            'name': "Peak Weavers - Leek",
            'img_url': f"{URL}img/Peak Weavers - Leek.jpg",
            'description': {
                'en': """
                    The house has 3 bedrooms and sleeps 6 plus cot(s). All bedrooms feature handmade,
                    wrought iron beds. Two of these rooms is king size and the third is a twin room with two singles. 
                    Self catering, and the weekly price is £595. Also have B&B 6 non-smoking bedrooms for £72. Well
                    equipped kitchen. Two pubs within 10 minute walk, one by the canal
                """,
                'nl': """
                    Het huis heeft 3 slaapkamers en is geschikt voor 6 personen plus kinderbedje(s). Alle slaapkamers 
                    zijn voorzien van handgemaakte, smeedijzeren bedden. Twee van deze kamers zijn kingsize en de 
                    derde is een tweepersoonskamer met twee eenpersoonsbedden. Zelfcatering, en de wekelijkse prijs is 
                    £595. Heeft ook 6 B&B rookvrije slaapkamers voor £72. Goed uitgeruste keuken. Twee pubs binnen 10 
                    minuten lopen, één aan de gracht
                """,
            },
            'costs': "£",
            'phone': "+44 (0)1538 383729",
            'url': "https://www.peakweavers.co.uk/self-catering-property/",
            'display_url': "www.peakweavers.co.uk"
        },   
        {
            'name': "White Hart Tea Room",
            'img_url': f"{URL}img/White Hart Tea Room.jpg",
            'description': {
                'en': """
                    15 minutes' drive from Foxtail Barns. Accommodation features eight individual en-suite
                    bedrooms. Due to the historic building, all rooms are accessed via stairs. In the heart
                    of leek, the Grace II listed building is opposite the historic Market Place. As well as
                    a B&B it's also a traditional tea room and sandwich bar
                """,
                'nl': """
                    15 minuten rijden van Foxtail Barns. De accommodatie beschikt over acht individuele slaapkamers 
                    met eigen badkamer. Omdat het historische gebouw is zijn alle kamers alleen bereikbaar via de trap. 
                    Het monumentale Grace II-gebouw ligt in het hart van Leek, tegenover de historische Grote Markt. 
                    Naast een B&B is het ook een traditionele theesalon en een broodjesbar
                """,
            },
            'costs': "£",
            'phone': "+44 (0)1538 372122",
            'url': "https://whiteharttearoom.co.uk/accommodation",
            'display_url': "whiteharttearoom.co.uk"
        },   
        {
            'name': "Middle Cottage",
            'img_url': f"{URL}img/Middle Cottage.jpg",
            'description': {
                'en': """
                    7 miles from Foxtail Barns, 1 double Bedroom property. Built in the 1700s, and situated
                    in the picturesque village of Endon. Two village pubs are only a few minutes' walk. Fully 
                    fitted kitchen included. Option of a guest bed and travel cot if required. Unsure of 
                    price, please enquire
                """,
                'nl': """
                    11 km van Foxtail Barns, 1 slaapkamer met tweepersoonsbed. Gebouwd in de 18e eeuw en 
                    gelegen in het pittoreske dorpje Endon. Twee pubs liggen op slechts een paar minuten lopen. 
                    Volledig ingerichte keuken inbegrepen. Optie voor een logeerbed en reiswieg indien nodig. 
                    Onzeker over de prijs
                """,
            },
            'costs': "?",
            'phone': "+44 (0)1782 505089",
            'url': "https://www.middlecottageholidays.co.uk/",
            'display_url': "www.middlecottageholidays.co.uk"
        },   
        {
            'name': "Allmore Cottage - Gratton Village",
            'img_url': f"{URL}img/Allmore Cottage - Gratton Village.jpg",
            'description': {
                'en': """
                    8 miles from Foxtail Barns. Allmore Cottage is a 1 king size bedroom property for 2
                    people. Prices range from £460 - £600 per week. Was originally a neglected farm building
                    turned into a cottage. Fully fitted kitchen and a conservatory at the rear of the cottage,
                    ideal for relaxing and enjoying the views of the surrounding countryside
                """,
                'nl': """
                    13 km van Foxtail Barns. Allmore Cottage is een accommodatie met 1 kingsize slaapkamer voor 
                    2 personen. Prijzen variëren van £460 to £600 per week. Oorspronkelijk was het een verwaarloosde
                    boerderij, omgebouwd tot een huis. Volledig ingerichte keuken en een serre aan de achterzijde 
                    van het huis, ideaal om te ontspannen en te genieten van het uitzicht op het omliggende platteland
                """,
            },
            'costs': "£££",
            'phone': "+44 (0)1782 505535",
            'url': "http://www.allmorecottageholidays.co.uk",
            'display_url': "www.allmorecottageholidays.co.uk"
        },   
        {
            'name': "Rose Cottages - Endon",
            'img_url': f"{URL}img/Rose Cottages - Endon.jpg",
            'description': {
                'en': """
                    7 miles from Foxtail Barns. Two Cottages with 3 Bedrooms each, can sleep up to 8 Adult
                    guests with excellent parking and gardens. Hot Tub hire available.
                    Prices from £325 per night (2 night stay) or £1075 per week (for up to 6 guests). Each
                    property features a fully equipped kitchen, comfortable living room with log burner,
                    dining area for 6-8 people and fully enclosed rear garden
                """,
                'nl': """
                    11 km van Foxtail Barns. Twee huisjes met elk 3 slaapkamers, geschikt voor maximaal 8 
                    volwassenen, elk met uitstekende parkeergelegenheid en tuinen. Hot Tub-verhuur beschikbaar. 
                    Prijzen vanaf £325 per nacht (2 nachten) of £1075 per week (voor maximaal 6 personen). 
                    Elke woning beschikt over een volledig uitgeruste keuken, een comfortabele woonkamer met 
                    houtkachel, een eetruimte voor 6-8 personen en een volledig omheinde achtertuin
                """,
            },
            'costs': "£££",
            'phone': "+44 (0)1782 645177",
            'url': "https://rosecottagesendon.co.uk/",
            'display_url': "rosecottagesendon.co.uk"
        },   
        {
            'name': "Spring Cottage",
            'img_url': f"{URL}img/Spring Cottage.jpg",
            'description': {
                'en': """
                    17 minutes from Foxtail Barns. Sleeps six. Three bedrooms, one king size, one double,
                    and one with twin beds. The kitchen has been recently renovated making this a lovely
                    space to prepare delightful meals. The grounds outside Spring Cottage offer guests a
                    place to relax and do some alfresco dining in the warmer months. Two living rooms fitted
                    with log burners. Unsure of price, please enquire
                """,
                'nl': """
                    17 minuten van Foxtail Barns. Biedt plaats voor zes personen in drie slaapkamers: één 
                    kingsize bed, één tweepersoonsbed en één met twee eenpersoonsbedden. De keuken is nieuw 
                    ingericht, waardoor dit een heerlijke ruimte is om heerlijke maaltijden te bereiden. 
                    Het terrein buiten Spring Cottage biedt gasten een plek om te ontspannen en in de 
                    warmere maanden buiten te dineren. Twee woonkamers voorzien van houtkachels. Onzeker 
                    over de prijs
                """,
            },
            'costs': "?",
            'phone': "+44 (0)7817914020",
            'url': "https://springcottageholidaylet.co.uk/",
            'display_url': "springcottageholidaylet.co.uk"
        }
    ],

    # Transport section
    'HOW_TO_GET_THERE': {'en': "HOW TO GET THERE", 'nl': "HOE DAAR TE KOMEN"},
    'TRANSPORT': {'en': "Transport", 'nl': "Vervoer"},
    'FLIGHTS': {'en': "Flights", 'nl': "Vluchten"},
    'FLIGHTS_DESC': {
        'en': """
            The best airport to land in is Manchester which is a 40-50 minute drive
            to Stoke-On-Trent. If you're flying from the Netherlands the best airlines we can recommend are
            Easyjet (<a href="https://www.easyjet.com/">www.easyjet.com</a>) and KLM 
            (<a href="https://www.klm.com/">www.klm.com</a>). Easyjet is usually the cheapest option and 
            usually reliable, whereas KLM is more luxurious and offers a snack halfway through the flight. 
            The flight is usually around 50 minutes long, and remember that you need to be at the airport two 
            hours before your flight time! We do not recommend Ryanair;  we have had negative experiences of 
            them randomly cancelling flights 
        """, 
        'nl': """
            De beste luchthaven optie is Manchester, op 40-50 minuten rijden van Stoke-On-Trent. Als je vanuit 
            Nederland vliegt, zijn de beste luchtvaartmaatschappijen die we kunnen aanbevelen Easyjet 
            (<a href="https://www.easyjet.com/">www.easyjet.com</a>) en KLM 
            (<a href="https://www.klm.com/">/www.klm.com</a>). Easyjet is doorgaans de goedkoopste optie en 
            erg betrouwbaar, terwijl KLM luxer is en halverwege de vlucht een snack aanbiedt. De vlucht duurt 
            meestal ongeveer 50 minuten. Onthoud dat je twee uur vóór de vluchttijd op de luchthaven moet zijn! 
            Wij raden Ryanair niet aan, wij hebben negatieve ervaringen met willekeurig geannuleerde vluchten
        """
    },
    'PUBLIC_TRANSPORT': {'en': "Public Transport", 'nl': "Openbaar Vervoer"},
    'PUBLIC_TRANSPORT_DESC': {
        'en': """
            There are two modes of public transport in the UK. These are train and
            bus. If you're getting a train from the airport to Stoke-On-Trent, or if you want to explore the 
            major cities of the UK, using the train will be vital. Unlike in The Netherlands and other European 
            countries, you need to buy train tickets per journey. You can do this at the train station or more 
            reliable by using the Trainline website/app (<a href="https://www.thetrainline.com/">www.thetrainline.com</a>). 
            If you're planning on travelling we recommend downloading the app. All you need to do it put your current 
            location and where you're travelling to, and it will tell you the different times and prices (we do            
            advise you to avoid peak times). If you're looking at travelling by bus around Stoke-On-Trent, the 
            most reliable bus service is the First bus (<a href="https://www.firstbus.co.uk/">www.firstbus.co.uk</a>), 
            on their website you can plan your journey or see when the next bus will be!
        """, 
        'nl': """
            Er zijn twee vormen van openbaar vervoer in Groot-Brittannië; de trein en bus. Als je vanaf het vliegveld 
            de trein naar Stoke-On-Trent neemt, of als je de grote steden van Groot-Brittannië wilt verkennen, is het 
            gebruik van de trein van cruciaal belang. Anders dan in Nederland en andere Europese landen moet je 
            treinkaartjes per reis kopen. Je kunt dit doen op het treinstation of op een betrouwbaardere manier door 
            de website/app van Trainline te gebruiken (<a href="https://www.thetrainline.com/">www.thetrainline.com</a>). 
            Als je van plan bent te reizen, raden wij u aan de app te downloaden. Het enige dat je hoeft te doen, is je 
            huidige locatie en waar je naartoe reist in te voeren. Je krijgt dan de verschillende tijden en prijzen te zien 
            (we adviseren piektijden te vermijden). Als je met de bus rond Stoke-On-Trent wilt reizen, is de meest betrouwbare 
            busdienst de First bus (<a href="https://www.firstbus.co.uk/">www.firstbus.co .uk</a>), op hun website kun je
            een reis plannen of zien wanneer de volgende bus vertrekt!
        """
    },
    'HIRED_TRANSPORT': {'en': "Hired Transport", 'nl': "Gehuurd Vervoer"},
    'HIRED_TRANSPORT_DESC': {
        'en': """
            There are lots of local taxi and mini-bus services. If there is a large
            group of travellers on the same flight and you are looking at hiring a mini-bus to 
            travel towards Stoke-on-Trent, then we are happy to help accommodate this and pass along some
            mini-bus numbers. There are a lot of taxi services in Stoke-on-Trent, these
            include Intercity (<a href="tel:+441782855855">+44 (0)1782 855855</a>), those staying in
            Leek can use Leek Link Taxis' (<a href="tel:+441538399999">+44 (0)1538 399999</a>),
            Lucky Seven (<a href="tel:+441782333333">+44 (0)1782 333333</a>), City Cabs (<a
            href="tel:+441782888888">+44 (0)1782 888888</a>), Magnum Private Hire (<a
            href="tel:+441782819819">+44 (0)1782 819819</a>). Alternatively, you can use an app
            called "Take me", which is an app that allows you to book a vehicle in seconds, you can
            view your driver and track his progress or you can use Uber, whichever is easiest for
            you!
        """, 
        'nl': """
            Er zijn veel lokale taxi- en minibusdiensten. Als er een grote groep reizigers op dezelfde vlucht 
            zitten en je overweegt een minibus te huren om richting Stoke-on-Trent te reizen, dan helpen wij 
            je graag hierbij en geven we minibusnummers door. Er zijn veel taxidiensten in Stoke-on-Trent, 
            waaronder Intercity (<a href="tel:+441782855855">+44 (0)1782 855855</a>), degenen die in Leek 
            verblijven kunnen Leek Link gebruiken Taxi's' (<a href="tel:+441538399999">+44 (0)1538 399999</a>), 
            Lucky Seven (<a href="tel:+441782333333">+44 (0)1782 333333</ a>), stadscabines 
            (<a href="tel:+441782888888">+44 (0)1782 888888</a>), Magnum Private Hire 
            (<a href="tel:+441782819819">+44 (0)1782 819819</a>). Als alternatief kan je een app genaamd 
            "Take me" gebruiken, een app waarmee je binnen enkele seconden een voertuig kan boeken, de chauffeur kan 
            bekijken en zijn voortgang kan volgen, of je kan Uber gebruiken, afhankelijk van wat het 
            gemakkelijkst voor je is!
        """
    },
    
    # Activities Section
    'WHAT_TO_DO': {'en': "WHAT TO DO", 'nl': "WAT TE DOEN"},
    'THINGS_TO_DO': {'en': "Things to do in Staffordshire", 'nl': "Dingen om te doen in Staffordshire"},

   'activities': [     
        {
            'name': "Alton Towers",
            'img_url': f"{URL}img/Alton Towers.jpg",
            'description': {
                'en': """
                    Alton Towers Resort is a theme park and resort complex in Staffordshire, England, 
                    near the village of Alton. Alton Towers Resort is home to over 40 rides and attractions, 
                    for guests of all ages. The 10 main rollercoasters are the stars of the show, each with 
                    record-breaking elements designed to thrill and delight anyone brave enough to ride. With 
                    20 attractions aimed at young children and families, Alton Towers is the only place in the 
                    UK where you can meet some of CBeebies best loved characters
                """,
                'nl': """
                    Alton Towers Resort is een themapark en resortcomplex in Staffordshire, Engeland, vlakbij het 
                    dorp Alton. Alton Towers Resort heeft meer dan 40 attracties voor gasten van alle leeftijden. 
                    De 10 belangrijkste achtbanen zijn de sterren van de show, elk met recordbrekende elementen 
                    ontworpen om iedereen die dapper genoeg is om te rijden te laten huiveren en genieten. Met 
                    20 attracties gericht op jonge kinderen en gezinnen is Alton Towers een van de leukste plekken
                    in de UK
                """,
            },
            'costs': "3+ £39",
            'address': "Farley Ln, Alton, Stoke-on-Trent ST10 4DB",
            'url': "https://www.altontowers.com",
            'display_url': "www.altontowers.com"
        },
        {
            'name': "Trentham Monkey Forest",
            'img_url': f"{URL}img/Trentham Monkey Forest.jpg",
            'description': {
                'en': """
                    If you are looking for a fun day out with a difference, look no further. Trentham Monkey 
                    Forest is a sanctuary for endangered Barbary monkeys. The natural behaviours of the monkeys 
                    can be seen right in front of your very eyes, making it one of the most fascinating and special 
                    attractions in the UK. Guests walk along the 3/4 of a mile pathway, amongst the monkeys, and see 
                    exactly how they live and behave in the wild
                """,
                'nl': """
                    Als je op zoek bent naar een leuk dagje uit, zoek dan niet verder. Trentham Monkey Forest is een 
                    toevluchtsoord voor bedreigde berberapen. Het natuurlijke gedrag van de apen is recht voor je ogen 
                    te zien, waardoor dit een van de meest fascinerende en bijzondere attracties in de UK is. Gasten lopen 
                    over een pad van 1.2 km tussen de apen door en zien precies hoe ze in het wild leven en zich gedragen
                """,
            },
            'costs': "Adult: £12.00 Children: £9.50",
            'address': "Stone Road Trentham Estate, Stoke-on-Trent ST4 8AY England",
            'url': "https://monkey-forest.com",
            'display_url': "monkey-forest.com"
        },
        {
            'name': "Trentham Gardens",
            'img_url': f"{URL}img/Trentham Gardens.jpg",
            'description': {
                'en': """
                    The Trentham Estate is home to the award-winning Trentham Gardens featuring The Italian Garden 
                    by Tom Stuart-Smith, and the Floral Labyrinth and Rivers of Grass by Piet Oudolf and vast 
                    wildflower and woodland meadow plantings by Nigel Dunnett. A fascinating wire fairy sculpture 
                    trail, fab children's adventure playground with the UK's first barefoot walk, a family-friendly maze, 
                    mile-long Capability Brown lake with seasonal boat and train trips. Trentham Monkey Forest, Trentham 
                    Treetop Adventure and Trentham Shopping Village with 50 shops and 14 cafes and restaurants can also 
                    be found at The Trentham Estate. You'll find something for everyone here
                """,
                'nl': """
                    Het Trentham Estate is de thuisbasis van de bekroonde Trentham Gardens met The Italian Garden van 
                    Tom Stuart-Smith, het Floral Labyrinth en Rivers of Grass van Piet Oudolf en uitgestrekte wilde bloemen- 
                    en bosweidebeplantingen van Nigel Dunnett. Een fascinerend sprookjesachtig sculpturenpad, een fantastische 
                    kinderspeeltuin met de eerste blotevoetenwandeling in het Verenigd Koninkrijk, een gezinsvriendelijk doolhof,
                    een kilometerslang Capability Brown-meer met seizoensgebonden boot- en treinuitstapjes. Trentham Monkey Forest,
                     Trentham Treetop Adventure en Trentham Shopping Village met 50 winkels en 14 cafés en restaurants zijn ook te 
                     vinden op The Trentham Estate. Hier vind je voor elk wat wils
                """,
            },
            'costs': "£13 Children: £9.50",
            'address': "Trentham Gardens Stone Road Trentham Estate, Trentham, Stoke-on-Trent ST4 8JG England",
            'url': "https://trentham.co.uk",
            'display_url': "trentham.co.uk"
        },
        {
            'name': "Waterworld",
            'img_url': f"{URL}img/Waterworld.jpg",
            'description': {
                'en': """
                    The UK's No.1 tropical indoor aqua park is located at the Waterworld Leisure Resort, in the heart of 
                    the Midlands, Stoke-on-Trent! Open all year round, Waterworld Aqua Park is an epic adventure for the 
                    whole family to enjoy, with over 30 different rides and attractions including Thunderbolt, the UK's 
                    first trap door drop waterslide! There's also the outdoor pool for those looking to enjoy some sunshine 
                    in the summer months! The Waterworld Leisure Resort is also home to Adventure Mini Golf with two 18-hole, 
                    tiki-themed mini golf courses, and the new M Club Spa and Fitness facility, so there has never been more 
                    choice for the best leisure experiences in Staffordshire!            
                """,
                'nl': """
                    Het nummer 1 tropische overdekte aquapark in de UK ligt in het Waterworld Leisure Resort, in het hart 
                    van de Midlands, Stoke-on-Trent! Waterworld Aqua Park is het hele jaar door geopend en is een episch 
                    avontuur voor het hele gezin, met meer dan 30 verschillende attracties waaronder Thunderbolt, de eerste 
                    valdeurwaterglijbaan in de UK. Er is ook een buitenzwembad voor wie in de zomermaanden van de zon wil 
                    genieten! Het Waterworld Leisure Resort is ook de thuisbasis van Adventure Mini Golf met twee 18-holes 
                    minigolfbanen met een tiki-thema, en de nieuwe M Club Spa en fitnessruimte, dus er is nog nooit zoveel 
                    keuze geweest voor de beste vrijetijdsbelevenissen in Staffordshire!
                """,
            },
            'costs': "Adult: £22 Children: £20",
            'address': "Waterworld Festival Way Hanley, Stoke-on-Trent ST1 5PU England",
            'url': "https://www.waterworld.co.uk",
            'display_url': "www.waterworld.co.uk"
        },
        {
            'name': "Stoke Ski Resort",
            'img_url': f"{URL}img/Stoke Ski Resort.jpg",
            'description': {
                'en': """
                    Stoke Ski Centre is one of the UK's leading dry slopes offering a wide variety of activities to suit all 
                    ages. From top-quality ski and board coaching and lessons, amazing tubing party packages for children aged 
                    2 years and above, an all new terrain park with a big kicker and quarter pipe combination as well as a 140m 
                    main race slope.<br>
                    Their facility is specifically designed to imitate the mountains and help you train or just to have fun. 
                    With constant work going into improving their slope surface, they are proud to claim it as one of the best in 
                    the country
                """,
                'nl': """
                    Stoke Ski Centre is een van de beste droge pistes in het Verenigd Koninkrijk en biedt een breed scala aan 
                    activiteiten voor alle leeftijden. Van ski- en boardcoaching en lessen van topkwaliteit, geweldige 
                    tubingpartypakketten voor kinderen vanaf 2 jaar, een gloednieuw terreinpark met een combinatie van een big 
                    kicker en een quarterpipe, tot een 140 meter lange wedstrijdpiste.<br>
                    Hun faciliteit is speciaal ontworpen om de bergen na te bootsen en je te helpen trainen of gewoon om plezier
                    te hebben. Er wordt constant gewerkt aan het verbeteren van het oppervlak van de piste en ze zijn er trots op
                    dat ze kunnen zeggen dat het een van de beste in het land is
                """,
            },
            'costs': "Adult £32 Children: £22",
            'address': "Festival Park Festival Way, Stoke-on-Trent ST1 5PU England",
            'url': "https://stokeskicentre.com",
            'display_url': "stokeskicentre.com"
        },
        {
            'name': "World of Wedgwood",
            'img_url': f"{URL}img/World of Wedgwood.jpg",
            'description': {
                'en': """
                    The home of the pottery industry in England, Stoke-on-Trent is also known as The Potteries. There's no better
                    place to experience this than at the World of Wedgwood, nestled in acres of stunning Staffordshire countryside.
                    Here, you can visit the Wedgwood Factory, the only place in the world where jasper is still made today.  
                    You can unwind at the potter's wheel or explore the galleries of the V&A Wedgwood Collection, but make sure you 
                    save time for the signature Wedgwood Afternoon Tea. So come for the plates and stay for the cake, take walks 
                    through their 240 acre estate
                """,
                'nl': """ 
                    Stoke-on-Trent, de thuisbasis van de aardewerkindustrie in Engeland, staat ook bekend als The Potteries. Er is 
                    geen betere plek om dit te ervaren dan in de World of Wedgwood, gelegen in het prachtige landschap van Staffordshire. 
                    Hier kun je de Wedgwood Factory bezoeken, de enige plek ter wereld waar jaspis nog steeds wordt gemaakt. Je kan 
                    ontspannen aan de pottenbakkersschijf of de galerijen van de V&A Wedgwood Collection verkennen, maar zorg ervoor dat 
                    je tijd vrijmaakt voor de kenmerkende Wedgwood Afternoon Tea. Dus kom voor de borden en blijf voor de taart, maak 
                    wandelingen door het 240 hectare grote landgoed
                """,
            },
            'costs': "Free to enter",
            'address': "Wedgwood Drive, Stoke-on-Trent ST12 9ER England",
            'url': " https://www.worldofwedgwood.com/",
            'display_url': "www.worldofwedgwood.com"
        },
        {
            'name': "Biddulph Grange Garden",
            'img_url': f"{URL}img/Biddulph Grange Garden.jpg",
            'description': {
                'en': """
                    This amazing Victorian garden was created by James Bateman for his collection of plants from 
                    around the world. A visit takes you on a global journey from Italy to the pyramids of Egypt, 
                    a Victorian vision of China and a re-creation of a Himalayan glen. The garden features 
                    collections of rhododendrons, summer bedding displays, a stunning Dahlia Walk and the oldest 
                    surviving golden larch in Britain, brought from China in the 1850s. The Geological Gallery 
                    shows how Bateman's interests went beyond botany. Opened in 1862 the unique hallway is a 
                    Victorian attempt to reconcile geology and theology. There are narrow gravel paths and over 
                    400 steps throughout the garden   
                """,
                'nl': """ 
                    Deze prachtige Victoriaanse tuin is aangelegd door James Bateman voor zijn verzameling planten
                    van over de hele wereld. Een bezoek neemt je mee op een mondiale reis van Italië naar de 
                    piramides van Egypte, een Victoriaanse visie op China en een herschepping van een Himalaya-dal. 
                    De tuin beschikt over collecties rododendrons, displays voor zomerbeddengoed, een prachtige 
                    Dahlia Walk en de oudste nog bestaande gouden lariks in Engeland, die in de jaren 1850 uit 
                    China werd meegenomen. De Geological Gallery laat zien hoe Bateman's interesses verder reikten 
                    dan alleen plantkunde. De unieke gang, geopend in 1862, is een Victoriaanse poging om geologie 
                    en theologie met elkaar te combineren. Er zijn smalle grindpaden en meer dan 400 treden door de 
                    tuin
                """,
            },
            'costs': "Adult: £12 Child: £6 ",
            'address': "Grange Road, Biddulph, Staffordshire, ST8 7SD ",
            'url': " https://www.nationaltrust.org.uk/visit/shropshire-staffordshire/biddulph-grange-garden",
            'display_url': "www.nationaltrust.org.uk/visit/shropshire-staffordshire/biddulph-grange-garden"
        },
        {
            'name': "Regent Theatre",
            'img_url': f"{URL}img/Regent Theatre.jpg",
            'description': {
                'en': """
                    The Regent Theatre is a theatre in Stoke-on-Trent, England. Constructed in 1929 as a cinema, it is one of several  
                    theatres in the city centre and one of two operated by the Ambassador Theatre Group on behalf of Stoke-on-Trent 
                    City Council. The Regent Theatre is a number one touring venue. Since re-opening, following a 
                    £23 million development of the city centre, it has played host to War Horse, Mamma Mia! and Jersey Boys      
                """,
                'nl': """ 
                    Het Regent Theatre is een theater in Stoke-on-Trent, Engeland. Het werd in 1929 gebouwd als bioscoop en is een van 
                    de vele theaters in het stadscentrum en een van de twee die worden uitgebaat door de Ambassador Theatre Group namens 
                    de gemeenteraad van Stoke-on-Trent. Het Regent Theatre is een van de meest populaire theaters.
                    Sinds de heropening, na een ontwikkeling van het stadscentrum van £23 miljoen, heeft het onderdak geboden aan War Horse, 
                    Mamma Mia! en Jersey Boys
                """,
            },
            'costs': "Price depends on the show",
            'address': "Piccadilly, Stoke-on-Trent, Staffordshire, ST1 1AP",
            'url': " https://www.atgtickets.com/venues/regent-theatre/",
            'display_url': "www.atgtickets.com/venues/regent-theatre/"
        },
    ],

    # FAQ Section
    'EVERYTHING_TO_KNOW': {'en': "EVERYTHING YOU WANT TO KNOW", 'nl': "ALLES WAT JE WIL WETEN"},
    'FAQ_LONG': {'en': "Frequently Asked Questions", 'nl': "Veel Gestelde Vragen"},
    'rsvp_questions': [     
        {
            'name': {'en': "How Do I RSVP?", 'nl': "Hoe laat ik weten dat ik kom?"},
            'description': {
                'en': """
                    We invite you to RSVP at the bottom of this page or by posting us the filled out RSVP card sent with the invitation
                """,
                'nl': """
                    Gelieve de RSVP op de bodem van deze webpagina te gebruiken, of door de RSVP-kaart in te sturen die bij de uitnodiging is toegevoegd
                """,
            }
        },
        {
            'name': {'en': "What date should I RSVP by?", 'nl': "Voor wanneer moet ik RSVP'en?"},
            'description': {
                'en': """
                    Please RSVP by the 29th of June
                """,
                'nl': """
                    RSVP a.u.b. vóór 29 juni
                """,
            }
        },
                {
            'name': {'en': "Can I come to the evening reception too?", 'nl': "Mag ik ook naar de avondreceptie komen?"},
            'description': {
                'en': """
                    If you are invited to the ceremony then you are invited to both the ceremony and the evening reception
                """,
                'nl': """
                    Als je bent uitgenodigd voor de ceremonie, dan ben je uitgenodigd voor zowel de ceremonie als de avondreceptie
                """,
            }
        },
        {
            'name': {'en': "What is the dress code?", 'nl': "Wat is de dresscode?"},
            'description': {
                'en': """
                    The dress code for our wedding is semi-formal/cocktail attire. Think cocktail dresses or a suit and tie
                """,
                'nl': """
                    De dresscode voor onze bruiloft is semi-formeel/cocktailkleding. Denk aan cocktailjurken of een pak en stropdas
                """,
            }
        },
        {
            'name': {'en': "What is the addresses for the wedding ceremony and reception venue?", 'nl': "Wat zijn de adressen van de trouwceremonie en receptielocatie?"},
            'description': {
                'en': """
                    Foxtail Barns Wedding Venue<br>
                    Consall Hall Gardens Estate<br>
                    Consall<br>
                    Staffordshire<br>
                    ST9 0AG
                """,
                'nl': """
                    Foxtail Barns Wedding Venue<br>
                    Consall Hall Gardens Estate<br>
                    Consall<br>
                    Staffordshire<br>
                    ST9 0AG<br>
                    Engeland
                """,
            }
        },
        {
            'name': {'en': "What time should I arrive?", 'nl': "Hoe laat word ik verwacht?"},
            'description': {
                'en': """
                    Help us get the party started as scheduled! We recommend that you arrive at 13:30, which is an 
                    hour before the start of the ceremony, to make sure everyone is seated on time""",
                'nl': """
                    Help ons het feest op tijd in gang te krijgen! We raden je aan om 13.30 uur aanwezig te zijn, 
                    wat een uur voor aanvang van de ceremonie is, om er zeker van te zijn dat iedereen op tijd zit
                """,
            }
        },
        {
            'name': {'en': "Is there available parking?", 'nl': "Is er parkeergelegenheid?"},
            'description': {
                'en': """
                    Yes, free parking is available at the venue
                """,
                'nl': """
                    Ja, er is gratis parkeergelegenheid bij de locatie
                """,
            }
        },
        {
            'name': {'en': "What should I do if I have dietary requirements?", 'nl': "Wat moet ik doen als ik dieetwensen of -beperkingen heb?"},
            'description': {
                'en': """
                    Please let us know of any dietary requirements on your RSVP
                """,
                'nl': """
                    Geef eventuele dieetwensen of -beperkingen aan ons door via de RSVP, a.u.b.
                """,
            }
        },
        {
            'name': {'en': "Where are you going on your honeymoon?", 'nl': "Waar gaan jullie heen op huwelijksreis?"},
            'description': {
                'en': """
                    We will be spending two weeks exploring Tokyo, Japan!
                """,
                'nl': """
                    We gaan twee weken lang Tokio, Japan verkennen!
                """,
            }
        },
        {
            'name': {'en': "What can we bring you as a gift?", 'nl': "Wat kunnen we jullie cadeau doen?"},
            'description': {
                'en': """
                    Your presence at our wedding is the greatest gift of all. However, if you wish to honour us with a gift, 
                    a cash gift for our honeymoon would be very welcome. Preferably in GBP(£) or Japanese Yen(¥)
                """,
                'nl': """
                    Jouw aanwezigheid op onze bruiloft is het grootste geschenk van allemaal. Maar, mocht je alsnog een 
                    cadeau willen geven, dan wordt een envelopje met contant geld voor onze huwelijksreis erg op prijs gesteld. 
                    Bij voorkeur in Engelse Ponden (£) of Japanse Yen(¥)
                """,
            }
        },
        {
            'name': {'en': "Can we take photos at the ceremony?", 'nl': "Kunnen we foto's maken tijdens de ceremonie?"},
            'description': {
                'en': """
                    We've hired a photographer and we'd love to have photos with no phones or devices in them. 
                    Please put away your cameras and phones during our wedding ceremony! Please feel free to take as many 
                    photos afterwards to remember our special day!

                """,
                'nl': """
                    We hebben een fotograaf ingehuurd en we willen graag foto's hebben zonder telefoons of camera's in beeld. 
                    Berg uw camera's en telefoons op tijdens onze huwelijksceremonie! Maak gerust achteraf een foto om onze speciale dag te herinneren!
                """,
            }
        },
        {
            'name': {'en': "Can I bring a plus one?", 'nl': "Mag ik iemand meenemen?"},
            'description': {
                'en': """
                    Due to the size of our guest list, we cannot accommodate extra people at the wedding. 
                    We only have spaces for the guests listed on your invitation
                """,
                'nl': """
                    Vanwege de omvang van onze gastenlijst kunnen wij geen extra personen op de bruiloft ontvangen. 
                    Wij hebben alleen plekken voor de gasten die op de uitnodiging staan vermeld
                """,
            }
        },
        {
            'name': {'en': "Are children allowed?", 'nl': "Zijn kinderen welkom?"},
            'description': {
                'en': """
                    Yes, however, due to venue limitations, only people listed on the invitation can attend our wedding
                """,
                'nl': """
                    Ja, maar vanwege locatiebeperkingen kunnen alleen de mensen die op de uitnodiging staan vermeld onze bruiloft bijwonen
                """,
            }
        },
        {
            'name': {'en': "We want to stay for a few days, will you be there?", 'nl': "Wij willen een paar dagen blijven, zijn jullie beschikbaar?"},
            'description': {
                'en': """
                    That's great! Due to many guests travelling afar, we've decided to wait for a week before going on honeymoon. 
                    Even though we have to work, we're available for any support, or to meet up (when available)
                """,
                'nl': """
                    Wat leuk! Omdat sommige gasten ver reizen hebben we besloten om een week te wachten voordat we op onze huwelijksreis gaan.
                    Hoewel we moeten werken zijn we beschikbaar voor steun/advies, en om af te spreken (zolang we beschikbaar zijn)
                """,
            }
        },
                {
            'name': {'en': "How does the bar operate?", 'nl': "Hoe werkt de bar?"},
            'description': {
                'en': """
                    As per traditional British weddings, the bar will open after the wedding breakfast. Guests can purchase any drinks 
                    they would like! It is recommended to bring a payment card, as we can not guarantee cash will be accepted. 
                    The bar opens at 18:45, and closes at 00:00.
                """,
                'nl': """
                    Net als bij traditionele Britse bruiloften gaat de bar na het huwelijksontbijt open. Gasten kunnen hier drankjes kopen!
                    We raden aan om een betaalkaart mee te nemen, omdat we niet kunnen garanderen dat contant geld wordt geaccepteerd. De bar 
                    gaat open om 18:45 en sluit om 00:00.
                """,
            }
        },
        {
            'name': {'en': "Can I do a speech?", 'nl': "Kan ik een toespraak houden?"},
            'description': {
                'en': """
                    Only the Father of the bride, the Groom, and the Bestman will be doing a speech. We'd appreciate if anyone else wants to say a few 
                    words on our special day, to share them with us privately after the wedding breakfast, for a more intimate conversation
                """,
                'nl': """
                   Alleen de vader van de bruid, de bruidegom, en de "best man" zullen een toespraak houden. We zouden het op prijs stellen als iemand 
                   anders een paar woorden wil delen op onze speciale dag, om deze na het huwelijksontbijt privé met ons te delen, voor een intiemer gesprek
                """,
            }
        }
    ],

    # RSVP Section
    'PLEASE_LET_US_KNOW': {'en': "PLEASE LET US KNOW", 'nl': "LAAT HET ONS WETEN"},
    'R.S.V.P.': {'en': "R.S.V.P.", 'nl': "R.S.V.P."},
    'FIRST_NAME': {'en': "First Name", 'nl': "Voornaam"},
    'LAST_NAME': {'en': "Last Name", 'nl': "Achternaam"},
    'EMAIL': {'en': "Email", 'nl': "Email"},
    'PHONE_NUMBER': {'en': "Phone Number", 'nl': "Telefoonnummer"},
    'PLEASE_SELECT': {'en': "Please select", 'nl': "Maak een keuze"},
    'NONE': {'en': "None", 'nl': "Geen"},
    'ONE': {'en': "One", 'nl': "Een"},
    'TWO': {'en': "Two", 'nl': "Twee"},
    'THREE': {'en': "Three", 'nl': "Drie"},
    'FOUR': {'en': "Four", 'nl': "Vier"},
    'FIVE': {'en': "Five", 'nl': "Vijf"},
    'HOW_MANY_INVITE': {'en': "How many people are on your invite?", 'nl': "Hoeveel personen staan op je uitnodiging?"},
    'HOW_MANY_ATTEND': {'en': "How many people of these will attend?", 'nl': "Hoeveel van deze personen komen?"},
    'PROVIDE_NAMES': {'en': "Please provide their names below", 'nl': "Vul hier a.u.b. hun namen in"},
    'DIETARY_REQUIREMENTS': {'en': "Does anyone have any dietary requirements?", 'nl': "Heeft iemand dieetwensen of -beperkingen?"},
    'SUBMIT_RSVP': {'en': "Submit RSVP", 'nl': "Verstuur RSVP"},
}

@app.template_filter('translate')
def translate_filter(translation_key):
    val = CONTENT.get(translation_key, {})
    return Markup(f"""<span lang="en">{val.get('en', "Unknown")}</span><span class="hidden" lang="nl">{val.get('nl', "Unknown")}</span>""")

@app.template_filter('translate_val')
def translate_val_filter(val):
    return Markup(f"""<span lang="en">{val.get('en', "Unknown")}</span><span class="hidden" lang="nl">{val.get('nl', "Unknown")}</span>""")

@app.template_filter('translate_select')
def translate_select_filter(translation_key, options):
    val = CONTENT.get(translation_key, {})
    return Markup(f"""
    <option {options} lang="en">{val.get('en', "Unknown")}</option>
    <option {options} lang="nl" class="hidden">{val.get('nl', "Unknown")}</option>
    """)

@app.after_request
def save_index_page(response):
    if hasattr(g, 'template'):
        with open("index.html", "w") as f:
            f.write(response.data.decode())
    return response

@app.route('/', methods=['GET', 'POST'])
def index_page():
    g.template = True
    return render_template("index.html", content=CONTENT, url=URL)

@app.route('/<path:filename>')
def send_media(filename):
    return send_file(filename)

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')