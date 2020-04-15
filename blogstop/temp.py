from gensim import corpora, models, similarities
import jieba
import numpy as np

def gettag(argument): 
    switcher = { 
        1: "Travel", 
        2: "Fitness", 
        3: "Sports", 
		4: "Political",
		5: "Finance",
		6: "Food",
		7: "Finance"
    } 
    return switcher.get(argument, "nothing") 


texts = [
	"The two main places that are within easy reach of the city are Matka Canyon and Vodno Mountain. Whilst Matka Canyon is no doubt the prettiest. The bus to Vodno Mountain ran more frequently, so I plumped for there. Getting a ticket for the bus appeared to be a bit of a ballache as you cannot buy tickets on the bus and have to buy and pre-load a card with credit. They can only be bought from special green booths which are scattered around the city. The transport company really needs to update their English webpage to make it easier for tourists to figure out how to buy tickets without having to rely on others for help. Luckily, the hostel I was staying at had cards available, but didn't know how much credit was on them. Since I was staying near the bus terminal, which is home to intercity and international buses, and also next to it is the terminal for the red London style Routemaster city buses."
	,"It’s hard to deny the aesthetic appeal of a good six-pack, but building a strong core is about more than countless crunches and the visual progress of rippling abs. That’s where rotational moves come into play. To target those all-important muscles, you’ve got to think (and train) in all three planes of motion. Pushups, pullups, biceps curls, and crunches occur in the forward-and-back sagittal plane. Others, like side lunges or chest flies, occur in the side-to-side frontal plane.If you’re not training your body for that, you’ll lose strength and stability and be more prone to injuries."
	,"India though can be proud of the fact that they are yet unbeaten in this World Cup with one game being washed out. West Indies will be tough opponents who will pose a threat as the two time world champions are all but knocked out. India need to play good cricket and avoid slip-ups.All hard teams done now, mostly and here comes a slightly lesser team. Afghanistan are the next opponents and shouldn’t be taken lightly. Two points are all but a guarantee from this game for India and hopefully the weather will help. Batsmen are in good touch and Bowling and Fielding will also be on the agenda for a complete performance."
	,"Politics is the set of activities that are associated with the governance of a country, state or area. It involves making decisions that apply to groups of members and achieving and exercising positions of governance—organized control over a human community. The academic study of politics is referred to as political science.In modern nation states, people often form political parties to represent their ideas. Members of a party often agree to take the same position on many issues and agree to support the same changes to law and the same leaders.An election is usually a competition between different parties. Some examples of political parties worldwide are: the Democratic Party (D) in the United States, the Conservative Party in the United Kingdom and the Indian National Congress in India, which has the highest number of political parties in the world "
	,"Market investments are most likely to lose significant value which can cause you to panic and liquidate in an attempt to recover as much of your money as possible. Be calm and seek professional help to assess your portfolio especially if your investments are in affected sectors, before taking any investment decisions.While its essential to have a health insurance in place for yourself and your family, it’s also important to know what all it covers. Check with your insurance company or TPA, the extent of coverage of medical expenses related to the pandemic. This can help you be prepared with spare funds to meet uncovered medical costs."
	,"When I think of comfort food, I inevitably think of chicken. chicken rice, chicken congee, chicken, chicken noodle soup, chicken with mashed potatoes is just good. give me ALL the chicken, carbs and I am one happy comforted ball of joy. I can forever come up with chicken and carb combinations and lately, lemony pepper chicken with cous cous is the one that has been bringing me joy.Juicy lemon slices turn jammy and extra sweet in the oven, mixing with savory chicken juices to create the most delicious sauce. It’s perfect for spooning over cous cous. Those fluffy little kernels just soak it up turning into tiny little bits of pure flavor"
	,"Ask a table full of women what they think about maxi dresses and you’ll get a firing squad of opinions. They’re frumpy or they’re fabulous. They travel well, but they eat your feet. They’re hot as hell or they’re as comfortable as can be. Love them or hate them, there’s one thing we can all agree on: maxi dresses are here to stay. Luckily, there are hundreds of options to choose from, no matter what you’re looking for. Here, we’ve rounded up the best of the best for the lovers, the haters and everyone in between.That’s right, some of our favorite fashion brands are allowing customers to stock their closets while giving back. From luxury fashion houses to indie labels, the selection is pretty stellar. We’re talking statement earrings, stylish jumpsuits, cool sandals and even a celebrity-favorite clutch."
]

keyword = 'Blogilates creator Cassey Ho is a certified fitness instructor with more than 10 years of experience in motivating people to move. Her infectiously inspiring approach to fitness makes this blog a place of encouragement and motivation. You’ll find workout videos, fitness challenges, nutrition guides, a calendar for consistency, and interesting posts designed to bust fitness myths and help you change bad habits, plus much more.'



texts = [jieba.lcut(text) for text in texts]
dictionary = corpora.Dictionary(texts)
feature_cnt = len(dictionary.token2id)
corpus = [dictionary.doc2bow(text) for text in texts]
tfidf = models.TfidfModel(corpus) 
kw_vector = dictionary.doc2bow(jieba.lcut(keyword))
index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features = feature_cnt)
sim = index[tfidf[kw_vector]]

sim = list(sim)

for i in range(len(sim)):
	sim[i] = round(sim[i],2)
print(sim)
max1 = max(sim)
maxpos1 = sim.index(max1)
sim[maxpos1] = 0
max1 = max(sim)
maxpos2 = sim.index(max1)
print(maxpos1,maxpos2)


mystr = gettag(maxpos1+1)+";"+gettag(maxpos2)
print(mystr)