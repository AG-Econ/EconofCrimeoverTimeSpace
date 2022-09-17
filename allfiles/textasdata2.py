import re
import os
import nltk
import pandas as pd
import spacy

nltk.download('maxent_ne_chunker')
nltk.download('punkt')
nltk.download('stopwords')

NER = spacy.load("en_core_web_sm")

dat_dir = 'YOUR DIRECTORY'
dat_link = dat_dir + 'raw_data_2.csv'
scraped_data = pd.read_csv(dat_link)

'''To bring out all the named entities - interesting to understand why 
we cannot use the built-in commands (check commented out examples below)'''


def all_ents(v):
    return [(ent.text, ent.label_) for ent in NER(v).ents]


scraped_data['Entities'] = scraped_data['Raw_Text'].apply(lambda v: all_ents(v))

scraped_data.head()

'''EXAMPLE START'''
'''#Example! why date and time!
text = "William Henry Marney, known as Bill, was shot dead outside his home in Crayford, Bexley, just before 10pm on 23 June 2005"
text1 = NER(text)
for word in text1.ents:
    print(word.text, word.label_)
#Example! Age gets put in Date entity, Locations stored as ORG as well (same with FAC)
text = "Benjamin Onwuka, 24, was shot in the head in Maxilla Walk, Harlesden, on 2 January 2005. He died a short time later in hospital"
text1 = NER(text)
for word in text1.ents:
    print(word.text, word.label_)
#Example! Location is recognised as person.
text = "Stuart Christopher McMahon, 45, was found shot dead at his home at 8 Magdalen Road, Earlsfield, on 30 September 2006"
text1 = NER(text)
for word in text1.ents:
print(word.text, word.label_)'''
'''EXAMPLE END'''

''' Let's find the dates of incidents - can do entity recognition or regex (prefer regex as dates can only be stored in 
some specific formats in our data. Adjust approach if needed in other data'''

'''Regex: I like https://regex101.com/ to build/test my regex etc'''
'''Why 3 stages below? Because I want to pick up the most common (standard) way stored dates first'''
'''This set: 2(3) January 2005 or January 23, 2005 or 23 January, 2005'''
dpattern = r'\d{1,2}\s(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s\d{4}|\s(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s\d{1,2}\,\s\d{4}|\s\d{1,2}\s(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\,\s\d{4}'

results = []
for i in scraped_data.Raw_Text:
    num = re.search(dpattern, i)
    if num:
        results.append(num.group(0))
    else:
        results.append("")

scraped_data['Date1'] = results

'''This set: 2(3) January '''

dpattern2 = r'\s\d{1,2}\s(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)'
results2 = []
for i in scraped_data.Raw_Text:
    num = re.search(dpattern2, i)
    if num:
        results2.append(num.group(0))
    else:
        results2.append("")

scraped_data['Date2'] = results2

'''This set: 2(3)rd January 2005'''
dpattern3 = r'\s\d{1,2}\w+\s(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s\d{4}'
results3 = []
for i in scraped_data.Raw_Text:
    num = re.search(dpattern3, i)
    if num:
        results3.append(num.group(0))
    else:
        results3.append("")

scraped_data['Date3'] = results3

scraped_data["Date"] = scraped_data["Date1"]

scraped_data.loc[scraped_data["Date"] == '', 'Date'] = scraped_data["Date2"]
scraped_data.loc[scraped_data["Date"] == '', 'Date'] = scraped_data["Date3"]
scraped_data.drop(['Date1', 'Date2', 'Date3'], axis=1, inplace=True)

'''Fives cases - like no specific date, just a month, of Valentines day/New years eve/Boxing day as date descriptions won't be 
picked up. NER can pick some of these up - but might miss some others.'''

scraped_data["Date"].head()

'''Let's try to find the locations'''
scraped_data.dtypes


# write a function to display basic entity info:
def show_ents(text):
    if text.ents:
        for e in text.ents:
            print(e.text + '-' + str(e.start_char) + '-' + str(e.end_char) + '-' + str(spacy.explain(e.label_)))
        else:
            print('No other named entities found.')


doc = NER(
    u'Dean Tully, 37, was shot dead in Fraser House on the Haverfield Estate off Green Dragon Lane, Brentford, at around 9.15pm on 25 January 2007. Police said two men burst into a two-bedroom flat and sprayed bullets from a Czech-made CZ25 sub-machine gun.')
show_ents(doc)

LABEL = "FINLOC"

TRAIN_DATA = [(
    "Bjorn Brown, a 23-year-old mechanic, was stabbed in Thornton Heath at around 8.33pm on 29 March 2017. He died in hospital five days later. CCTV footage showed Bjorn having a short conversation with two men at the junction of in Kelling Gardens and Bensham Lane. They then walk into Kelling Gardens, out of view of the camera.",
    {"entities": [(52, 66, "FINLOC")]}),
    (
        "Antonio Rodney-Cole, 22, was stabbed to death in Stoke Newington at around 11.30am on 2 December 2013. Detectives believe he was attacked during a robbery of the mobile phone he used to deal drugs to customers in the area.",
        {"entities": [(49, 64, "FINLOC")]}),
    (
        "Geoffrey Bacon, a 90-year-old WWII veteran, was killed for his travel pass and ¬£40 in cash on 26 April 2010. At around 10.45am, as he entered his flat on the second floor of the Peabody Estate in Camberwell Green, south London, he was bundled to the floor and punched in the face. The robber, described as a light-skinned black man aged 30-40, took Mr Bacon‚Äôs wallet before searching the bedroom. He then fled the scene, shutting the front door behind him, leaving Mr Bacon on the floor of his hallway with a broken hip until a neighbour heard his cries for help. Mr Bacon spent 11 weeks in hospital recovering but never moved back to his flat and died on Thursday 5 August 2010 at a care home in Westgate-on-Sea, Kent.",
        {"entities": [(175, 213, "FINLOC")]}),
    (
        "Fifteen year-old Adam Regis, the nephew of Olympic sprinter John Regis, was stabbed to death in an unprovoked attack in east London on 17 March 2007. He was on the phone to his girlfriend when he was targeted by up to four men as he walked home along Kingsland Road, Plaistow, at around 9.30pm.",
        {"entities": [(251, 275, "FINLOC")]}),
    (
        "Eighty-one year-old Molly Morgan died after being mugged in the street on January 15, 2009. Molly was on her way to Kenton Library to hear a lecture on ‚ÄòBuildings of London‚Äô when she was attacked in Streatfield Road, Harrow, at 7.40pm.",
        {"entities": [(203, 227, "FINLOC")]}),
    (
        "Ade Pukeliene, 57, died after being robbed by two masked men on a scooter as she walked home from work. The Lithuanian grandmother fell to the ground and fractured her skull after the muggers snatched her bag in Emerald Close in Beckton at around 6.45am on 28 February 2008. ",
        {"entities": [(229, 236, "FINLOC")]}),
    (
        "A 78-year-old man was found unresponsive at an address in Jamaica Road, Bermondsey, Southwark, at around 11.55am on 12 May.",
        {"entities": [(72, 93, "FINLOC")]}),
    (
        "Benjamin Onwuka, 24, was shot in the head in Maxilla Walk, Harlesden, on 2 January 2005. He died a short time later in hospital. Four men were arrested and a ¬£10,000 reward for information was offered but nobody has ever been charged.",
        {"entities": [(45, 68, "FINLOC")]}),
    (
        "Philip Sylvester, 62, was last seen alive visiting a local convenience store in Whetstone Road, Kidbrooke, south London on December 2, 2009. He was found dead on December 13 after police officers forced their way into his home in Kellaway Road at 5.50pm.",
        {"entities": [(230, 243, "FINLOC")]}),
    (
        "Xiong Zhang, 33, was attacked on a towpath near the River Roding in Barking on 19 July 2007. Two police officers found him lying injured as they walked in the area near Hertford Road.",
        {"entities": [(169, 182, "FINLOC")]}),
    (
        "Philip Poru, 18, was shot dead in a suspected gang war on Sunday 14 October 2007. The student was sitting with his friends in a car in Long Walk, Plumstead, south London, at around 10pm when they were approached by two men.",
        {"entities": [(135, 155, "FINLOC")]}),
    (
        "Detectives investigating the case of Joanna Borucka, who was found dead in a suitcase in Southall, west London, on 18 December, are yet to reveal a specific cause of death but have appealed for help tracing Lithuanian Petras Zalynas, 50, who is believed to have left the UK and headed to Germany.",
        {"entities": [(89, 110, "FINLOC")]}),
    (
        "Redwan El-Ghaidouni, 38, was shot dead in a suspected ‚Äòhit‚Äô outside his home in Vine, Lane Uxbridge on 3 February 2015.",
        {"entities": [(84, 103, "FINLOC")]}),
    (
        "Malachi Brooks, 21, was stabbed to death in the street in a revenge gang attack on 28 March 2017. He was walking home along Surrey lane in Battersea when a car pulled up and three masked men got out and attacked him shortly after 1am.",
        {"entities": [(124, 148, "FINLOC")]}),
    (
        "Nathan Williams, 24, was shot dead in New Cross at 1.30am on July 28, 2009. The father-of-one was sitting in a black VW Golf in Ludwick Mews when he was blasted with a shotgun and a handgun.",
        {"entities": [(38, 47, "FINLOC")]}),
    (
        "Stuart Christopher McMahon, 45, was found shot dead at his home at 8 Magdalen Road, Earlsfield, on 30 September 2006. The victim was described in media reports as a millionaire father-of-two who ran his own building firm. He had been living at the five-bedroom house after splitting up with his wife six months earlier but had recently sold the property for ¬£850,000.",
        {"entities": [(67, 94, "FINLOC")]}),
    (
        "Jerome Vassell, 19, was shot dead in Hornsey, north London, on 28 October 2006. He suffered a bullet wound to the head in the car park of the West Indian Cultural Centre in Clarendon Road shortly before 1am.",
        {"entities": [(37, 58, "FINLOC")]}),
    (
        "Martine Vik Magnussen, 23, was last seen alive leaving a nightclub in London‚Äôs West End with the son of one of the wealthiest businessmen in Yemen at around 2am on 14 March 2008. She was found dead in a basement at 222 Great Portland Street two days later. Police have named Farouk Abdulhak as the prime suspect but he is believed to be in hiding in Yemen. Read more.",
        {"entities": [(217, 242, "FINLOC")]}),
    (
        "Edvin Johnson, 19, was stabbed to death in the stairwell of a block of flats in Camberwell on Sunday 16 September 2007. The teenager was a few days away from starting a course in business studies at Southampton University when he was attacked at Barnet House on the Crawford Estate at around 9pm.",
        {"entities": [(80, 90, "FINLOC")]}),
    (
        "Taofeek Lamidi, 20, was stabbed in the heart in the street in Memorial Avenue, West Ham, at around 7.37pm on New Years Eve 2017. Call the incident room on 020 8721 4005.",
        {"entities": [(62, 87, "FINLOC")]}),
    (
        "Kamil Malysz, a 34 year-old Polish national, was found stabbed to death at a flat in Alfred Road, Acton, at 10.15am on 27 January. Police are appealing for information about suspect Patryk Makuch, also a 34 year-old Polish national, who is believed to have travelled to Europe.",
        {"entities": [(85, 103, "FINLOC")]}),
    (
        "Drekwon Patterson, 16, was found stabbed near Preston Road station in Wembley at around 11.30pm on 18 February. He died in hospital at 9am the next morning.",
        {"entities": [(46, 58, "FINLOC")]}),
    (
        "Peter Oduwole, 37, was shot dead in the street in Hackney, east London, on 23 April 2006. He was handing out flyers at venues in Hackney Road when he was attacked at around 8.30pm.",
        {"entities": [(50, 70, "FINLOC")]}),
    (
        "The remains of Alexandre Madeira Marques, a 61-year-old waiter, were discovered near Woodside Road, Luton, Bedfordshire, on 2 January 2006. He had last been seen alive at his flat in Clanricarde Gardens, Notting Hill, west London, at around 11am on 16 October 2006.",
        {"entities": [(85, 105, "FINLOC")]}),
    (
        "Moses Mayele was stabbed to death on his 23rd birthday. He was attacked in Manford Way, Hainault, at around 10.20pm on 12 October 2018 and was pronounced dead at the scene. A black VW Golf car, which was used by the suspects on the night of the murder, was later found burnt out in Park View Gardens. Three suspects were seen walking in the area carrying a petrol can. A 19-year-old man was charged with murder but the case was dropped by the Crown Prosecution Service in January 2019. Call police on 020 8345 1570.",
        {"entities": [(75, 96, "FINLOC")]}),
    (
        "Latwaan Griffiths, 18, was fatally stabbed on 25 July 2018. He was found injured after falling off the back of a moped in Denmark Road, Camberwell, at around 6.55pm. The moped driver rode off and Latwaan was taken to hospital, where he died at 12.22am on 26 July 2018. Evidence heard in another court case suggested Latwaan was a member of the Harlem Spartans gang based in Kennington, which was involved in a feud with a rival ‚Äò150‚Äô gang in Lambeth. Contact police on 0208 721 4205.",
        {"entities": [(122, 146, "FINLOC")]}),
    (
        "Cafer Aslam, a 54-year-old cafe owner of Turkish origin, was found shot dead at the junction of Westminster Road and Bounces Road in Enfield at around 9.10pm on 23 August 2017. The suspect used a stolen Grey Audi Q5 which had been parked in Huxley Road, Edmonton, in the two days before the murder.",
        {"entities": [(96, 140, "FINLOC")]}),
    (
        "Dipo Seweje, 20, was shot dead on the Aylesbury Estate in Walworth on Boxing Day 2007. His body was found in a communal garden near Chartridge House the following day, more than 24 hours later.",
        {"entities": [(38, 66, "FINLOC")]}),
    (
        "Harjit Singh Dulai, 44, was stabbed to death after meeting a drug dealer in Rosedale Park off Albion Road in Hayes at around 6.40pm on 27 January 2016. A 16 year-old boy was acquitted of murder in July 2016 but police continue to appeal for information.",
        {"entities": [(76, 105, "FINLOC")]}),
    (
        "Lorry driver Andrew Cunningham was stabbed to death in a sadistic attack on 10 December 2008. The 52 year-old‚Äôs body was found in his caravan at the Business Centre on Riverside Road, Earlsfield, south London, shortly after 7.30am.",
        {"entities": [(170, 196, "FINLOC")]}),
    (
        "The body of Damian Chlywka, aged around 30, was found in a well in the garden of 11a Audley Drive, Warlingham, Croydon, on 15 November 2013. He had last been seen alive in March 2011.",
        {"entities": [(85, 109, "FINLOC")]}),
    (
        "Amaan Shakoor, 16, was shot in the head outside Walthamstow Leisure Centre in Markhouse Road at around 10pm on 2 April 2018. He was taken to hospital and died the following day.",
        {"entities": [(78, 92, "FINLOC")]}),
    (
        "Abdirashid Mohamoud, 17, was chased and stabbed to death near flats in Union Lane, Isleworth, at around 10.35pm on 22 March. He died at the scene a short time later. Five men were arrested on suspicion of murder but nobody has been charged.",
        {"entities": [(71, 92, "FINLOC")]}),
    (
        "Mohammed Hassan, 35, was stabbed to death on the Winstanley Estate in Battersea at around 6.06pm on 3 August 2016. Two other men, aged 33 and 35, also suffered stab injuries. Police described it as ‚Äúa violent attack in broad daylight.‚Äù Call the incident room on 020 8721 4005.",
        {"entities": [(49, 79, "FINLOC")]}),
    (
        "On Thursday 4th June 2009 Anthony Otton was gunned down on a balcony in Fulham, southwest London. The 28 year-old was shot in the heart outside 262 Fulham Court at around 6.50pm and died at the scene.",
        {"entities": [(72, 96, "FINLOC")]}),
    (
        "Edward Simpson, 25, was shot at Exeter House on Water Mill Way, Feltham, at around 11.08pm on 21 June. ",
        {"entities": [(48, 71, "FINLOC")]}),
    (
        "Matthew Kitandwe, 18, was stabbed to death outside his home in Wayford Street, Battersea on 21 June 2016. He was a student at South Thames College who had played football for the Ugandan youth team. Call the incident room on 020 8721 4054.",
        {"entities": [(63, 88, "FINLOC")]}),
    (
        "Dean Tully, 37, was shot dead in Fraser House on the Haverfield Estate off Green Dragon Lane, Brentford, at around 9.15pm on 25 January 2007. Police said two men burst into a two-bedroom flat and sprayed bullets from a Czech-made CZ25 sub-machine gun.",
        {"entities": [(75, 103, "FINLOC")]})
]

# Load pre-existing spacy model
from spacy.training import Example

nlp = spacy.load('en_core_web_sm')

# Getting the pipeline component
ner = nlp.get_pipe("ner")
# Adding labels to the `ner`
# Disable pipeline components we dont need to change
pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
unaffected_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

# Add the new label to ner
ner.add_label(LABEL)

# Resume training
optimizer = nlp.resume_training()
move_names = list(ner.move_names)

# List of pipes we want to train
pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]

# List of pipes which should remain unaffected in training
other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
# Importing requirements
from spacy.util import minibatch, compounding
import random

# Begin training by disabling other pipeline components
with nlp.disable_pipes(*other_pipes):
    sizes = compounding(1.0, 4.0, 1.001)
    # Training for 30 iterations
    for itn in range(30):
        # shuffle examples before training
        random.shuffle(TRAIN_DATA)
        # batch up the examples using spaCy's minibatch
        batches = minibatch(TRAIN_DATA, size=sizes)
        # Dictionary to store losses
        losses = {}
        for batch in batches:
            texts, annotations = zip(*batch)
            example = []
            for i in range(len(texts)):
                doc = nlp.make_doc(texts[i])
                example.append(Example.from_dict(doc, annotations[i]))
                nlp.update(example, sgd=optimizer, drop=0.35, losses=losses)
                print("Losses", losses)

# Testing the NER
test_text = "Seventeen year-old James Andre Smartt-Ford, known as Dre, was shot dead at Streatham ice rink in Streatham High Road, south London on 3 February 2007. He had been one of 300 guests at a disco when he was was approached by a black youth wearing dark clothing at the bottom of the stairs leading to the rink at around 11pm."
doc = nlp(test_text)
print("Entities in '%s'" % test_text)
for ent in doc.ents:
    print(ent.text, ent.label_)


# Testing the NER in dataframe
def loc_ents(v):
    return [ent.text for ent in nlp(v).ents]


scraped_data['Locations'] = scraped_data['Raw_Text'].apply(lambda v: loc_ents(v))

'''Because we might get an issue of some locations not getting recognised - let's try to be greedy and use NER in-built GPE or LOC
(mainly for the cases where training failed)'''

'''Let's check a case'''
doc = NER(
    u'David Adegbite, 18, was shot in the head in St Ann‚Äôs, Barking, at around 7.09pm on 19 March 2017. The former college student was attacked as he cycled through the housing estate while visiting friends.')
show_ents(doc)

loc_label = ['GPE', 'LOC']


def extract_locs(texts):
    doc = NER(texts)
    results = [ent.text for ent in doc.ents if ent.label_ in loc_label]
    return results


scraped_data['Locations2'] = scraped_data['Raw_Text'].apply(extract_locs)

loc_label2 = ['FAC', 'ORG']


def extract_locs2(texts):
    doc2 = NER(texts)
    res = [ent.text for ent in doc2.ents if ent.label_ in loc_label2]
    return res


scraped_data['Locations3'] = scraped_data['Raw_Text'].apply(extract_locs2)

'''It will highly depend on the training session for the 1st loc - training- the straight from the box solution of location 
with NER will give things like 'detectives', 'BMW' with fac, org but also locations like Edmonton.'''
'''Let us map these locations - Where are the unsolved murders??'''
'''read in the london_places.csv'''
len(scraped_data.index)
dat2_link = dat_dir + 'london_places.csv'
london_places = pd.read_csv(dat2_link)
print(london_places.head())
london_places.dtypes
london_places['Location'] = pd.Series(london_places['Location'], dtype="string")
len(london_places.index)

'''We drop the duplicates like Grove Park in Hounslow or Lewisham : does not matter much for this session - for 
research data this can be adjusted accordingly'''
london_places = london_places.drop_duplicates(subset=['Location'])
len(london_places.index)

'''Map postcode districts to our data from london_places'''
mapper = london_places.set_index('Location')['Postcodedistrict'].to_dict()

def get_postcode(l):
    for x in l:
        if x in mapper:
            return mapper[x]

    return None


scraped_data['PC1'] = scraped_data['Locations'].apply(get_postcode)
scraped_data['PC2'] = scraped_data['Locations2'].apply(get_postcode)
scraped_data['PC3'] = scraped_data['Locations3'].apply(get_postcode)

scraped_data["PCode_final"] = scraped_data["PC1"]

scraped_data["PCode_final"] = scraped_data["PCode_final"].fillna(scraped_data["PC2"])
scraped_data["PCode_final"] = scraped_data["PCode_final"].fillna(scraped_data["PC3"])

scraped_data.drop(['PC1', 'PC2', 'PC3'], axis=1, inplace=True)

scraped_data.dtypes
len(scraped_data.index)
scraped_data['Location_check'] = scraped_data['Locations'].astype(str).str.replace("[']", "", regex=True)
scraped_data['Location_check'] = scraped_data['Location_check'].astype(str).str.strip('[|]')
scraped_data['Location_check'] = pd.Series(scraped_data['Location_check'], dtype="string")
print(scraped_data['Location_check'].head())

scraped_data = scraped_data.join(
    scraped_data.pop('Location_check').str.split(', ', expand=True).add_prefix('locparts'))

scraped_data.dtypes
len(scraped_data.index)

'''greedy merging the postcode district for the cases we did not get before'''
# create a mapping series
s = london_places.set_index('Location')['Postcodedistrict']

# Substitute values in similar columns
for c in scraped_data.filter(like='locpart'):
    scraped_data[c.replace('locpart', 'Postcodedistrict')] = scraped_data[c].map(s)

'''filling in the missing values where we find it'''
for c in scraped_data.filter(like='Postcodedistrict'):
    scraped_data["PCode_final"] = scraped_data["PCode_final"].fillna(scraped_data[c])

'''dropping some variables'''
for c in scraped_data.filter(like='Postcodedistrict'):
    scraped_data.drop(c, axis=1, inplace=True)

'''create a subset'''
loc_date = scraped_data[["ID", "PCode_final", "Date"]]
print(loc_date.head())
len(loc_date.index)

'''drop obs where couldn't get a match of postcode district'''
loc_date.dropna(subset=['PCode_final'], inplace=True)
len(loc_date.index)


'''Mapping the locations'''
from geopy.geocoders import Nominatim
import folium

dat3_link = dat_dir + 'postcode_outcodes.csv'
latlong = pd.read_csv(dat3_link)
print(latlong)

'''merge the latitude and longitude of all postcode districts'''

loc_date = pd.merge(loc_date, latlong[['postcode', 'latitude', 'longitude']], left_on='PCode_final',
                        right_on='postcode',
                        how='left', validate='m:1')
print(loc_date)

df_loc = loc_date.copy()
df_loc.head(5)
len(loc_date.index)
len(df_loc.index)
'''drop if null values in coordinates'''
df_loc['latitude'].isnull().values.any()
df_loc.dropna(inplace=True)

'''Actual mapping'''
address = 'London, United Kingdom'
geolocator = Nominatim(user_agent="chrome")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('The geographical coordinate of London are {}, {}.'.format(latitude, longitude))

map_london = folium.Map(location=[latitude, longitude], zoom_start=12)
'''Let's save our initial map'''
m_name = "londonmap.html"
m_na = os.path.join(dat_dir, m_name)
map_london.save(m_na)

'''I don't collapse the data or make cluster etc - can be extended/modified in many many ways'''
# Adding markers to map
for lat, lng, pcode in zip(df_loc['latitude'],
                        df_loc['longitude'],
                        df_loc['PCode_final']):
    label = '{}'.format(pcode)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7).add_to(map_london)

'''Let's save our final map'''
map_name = "unsolvedmurdersinLondon.html"
mName = os.path.join(dat_dir, map_name)

map_london.save(mName)
